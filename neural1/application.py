"""Installed virtual NEURAL1 console and bounded, recoverable local workers."""
from __future__ import annotations

import argparse
import fcntl
import json
import os
import secrets
import shlex
import shutil
import signal
import sqlite3
import subprocess
import sys
import textwrap
import threading
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any
from urllib.request import urlopen

from .bundle import export_bundle, verify_bundle
from .campaign import CampaignEngine, CampaignSpec
from .core import Neural1Error, sha256_bytes, stable_id
from .drivers import parse_commands
from .experiments import EXPERIMENTS
from .meta import CausalStatus, Claim, Evidence
from .meta_store import ResearchDatabase
from .models import OllamaHttpProvider
from .provider_factory import provider_for
from .registry import ModelRegistry

DEFAULT_CONFIG = Path('/etc/neural1/config.json')
LABELS = ('4K MIND', '1976 MULTIVERSE', 'SELFHOST/1', '256-BYTE UNIVERSE', 'RAM REPUBLIC')


@dataclass(frozen=True)
class ApplicationConfig:
    path: Path
    ssd: Path
    uuid: str
    registry: Path
    checkout: Path
    default_model: str
    temperature_limit: float = 75.0
    minimum_free_bytes: int = 2 * 1024**3

    @classmethod
    def load(cls, path: Path) -> ApplicationConfig:
        data = json.loads(path.read_text())
        for name in ('ssd', 'registry', 'checkout'):
            if not Path(data[name]).is_absolute():
                raise Neural1Error(f'{name} must be an absolute deployment path')
        return cls(path.resolve(), Path(data['ssd']), data['uuid'], Path(data['registry']), Path(data['checkout']), data['default_model'], float(data.get('temperature_limit', 75)), int(data.get('minimum_free_bytes', 2 * 1024**3)))

    @property
    def output(self) -> Path:
        return self.ssd / 'runs' / 'console'

    @property
    def database(self) -> Path:
        return self.ssd / 'meta' / 'console.sqlite'

    def storage_check(self) -> Any:
        from .deployment import verify_storage
        try:
            return verify_storage(self.ssd, self.uuid, write_paths=(self.output, self.database, self.ssd / 'logs', self.ssd / 'exports'), min_free_bytes=0)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            raise Neural1Error(f'storage unavailable: {error}') from error

    def check(self) -> dict[str, Any]:
        identity = self.storage_check()
        if identity.free_bytes < self.minimum_free_bytes:
            raise Neural1Error("resource stop: insufficient SSD working reserve")
        temperatures = [int(path.read_text()) / 1000 for path in Path('/sys/class/thermal').glob('thermal_zone*/temp')]
        if temperatures and max(temperatures) >= self.temperature_limit:
            raise Neural1Error(f'thermal stop: {max(temperatures):.1f} C')
        memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        available = int(memory['MemAvailable'].split()[0]) * 1024
        if available < 256 * 1024**2:
            raise Neural1Error('resource stop: less than 256 MiB available RAM')
        throttling = None
        utility = Path('/usr/bin/vcgencmd')
        if utility.exists():
            response = subprocess.run([str(utility), 'get_throttled'], capture_output=True, text=True, check=True, timeout=3)  # noqa: S603 - fixed native diagnostic
            throttling = int(response.stdout.strip().split('=')[1], 16)
            if throttling & 0xF:
                raise Neural1Error(f'Pi power/clock/thermal stop: current flags {throttling & 0xF:#x}')
        return {'storage': {**asdict(identity), 'root': str(identity.root)}, 'temperatures_c': temperatures, 'available_memory_bytes': available, 'throttling_flags': throttling}


def check_model(registry: ModelRegistry, model_id: str) -> dict[str, Any]:
    model = registry.require(model_id)
    if model.backend != 'ollama':
        raise Neural1Error('installed console requires a qualified native local Ollama provider')
    endpoint = str(model.generation_defaults.get('base_url', 'http://127.0.0.1:11434'))
    OllamaHttpProvider(model.backend_name, base_url=endpoint)
    with urlopen(endpoint.rstrip('/') + '/api/tags', timeout=5) as response:  # noqa: S310 - loopback endpoint validated above
        tags = json.load(response)['models']
    matching = [tag for tag in tags if tag['name'] == model.backend_name and tag['digest'].removeprefix('sha256:') == model.digest]
    if not matching:
        raise Neural1Error('live model manifest identity differs from qualified deployment registry')
    return {'model_id': model_id, 'name': model.backend_name, 'digest': model.digest, 'quantization': model.quantization, 'endpoint': endpoint}


def preset(family: str, model_id: str, *, seed: int | None = None) -> CampaignSpec:
    if family not in EXPERIMENTS:
        raise Neural1Error('unknown experiment family')
    return CampaignSpec.create(experiments=(family,), model_ids=(model_id,), seeds=(seed if seed is not None else time.time_ns() % 2147483647,), generations=3, agents_per_cell=2 if family == 'ram-republic' else 1, ram_budget=4096, max_tokens=1024 if family == '256-byte-universe' else 512 if family == '1976-multiverse' else 192, generation_settings={'preset': 'bounded-console-v1', 'context_reset_generations': 2}, matched_control='deterministic family evaluator; controls are separate from model evidence', wall_clock_limit_seconds=600)


def ingest(config: ApplicationConfig, root: Path) -> str:
    """Index actual persisted evidence; never turn negative outcomes into success."""
    files = sorted(root.glob('cells/*/family-result.json')) + sorted(root.glob('cells/*/checkpoint.json'))
    summary = json.loads((root / 'summary.json').read_text()) if (root / 'summary.json').exists() else {'status': 'INTERRUPTED'}
    payload = {'summary': summary, 'records': {str(path.relative_to(root)): json.loads(path.read_text()) for path in files}}
    digest = sha256_bytes(json.dumps(payload, sort_keys=True).encode())
    claim_id = stable_id('N1-C', {'campaign': root.name})
    database = ResearchDatabase(config.database)
    try:
        previous = database.claim(claim_id)
        evidence_id = stable_id('N1-E', {'hash': digest})
        link = {'claim_id': claim_id, 'evidence_id': evidence_id, 'artifact_hash': digest}
        link_path = root / 'meta-link.json'
        complete = database.connection.execute("SELECT 1 FROM evidence e JOIN edges x ON x.source=e.evidence_id WHERE e.evidence_id=? AND x.target=? AND x.relation='supports'", (evidence_id, claim_id)).fetchone()
        if previous and previous.get('scope', {}).get('evidence_hash') == digest and complete and link_path.exists() and json.loads(link_path.read_text()) == link:
            return claim_id
        statement = f'Virtual campaign {root.name} recorded status {summary["status"]}; inspect domain results for scientific outcome.'
        claim = Claim(claim_id, statement, {'campaign': root.name, 'target': 'VIRTUAL', 'evidence_hash': digest}, causal_status=CausalStatus.OBSERVED)
        if not previous or previous.get("scope", {}).get("evidence_hash") != digest:
            database.put_claim(claim)
        evidence = Evidence(evidence_id, 'ACTUAL_RUN_RECORDS', digest, (root.name,), statement)
        database.put_evidence(evidence)
        database.relate(evidence.evidence_id, 'supports', claim_id)
        database.enqueue(f'Assess recorded outcome of {root.name}', uncertainty=1, novelty=0, information_gain=0.5, cross_experiment_relevance=0, normalized_compute_cost=0.1)
        (root / 'meta-link.json').write_text(json.dumps({'claim_id': claim_id, 'evidence_id': evidence.evidence_id, 'artifact_hash': digest}, indent=2) + '\n')
        return claim_id
    finally:
        database.close()


class Application:
    def __init__(self, config: ApplicationConfig):
        self.config = config
        config.storage_check()
        self.registry = ModelRegistry.load(config.registry)
        self.model_id = config.default_model
        self.family = EXPERIMENTS[0]

    def root(self, campaign_id: str) -> Path:
        if not campaign_id.startswith('N1-P-') or Path(campaign_id).name != campaign_id:
            raise Neural1Error('invalid campaign ID')
        path = self.config.output / 'campaigns' / campaign_id
        if path.is_symlink() or path.resolve().parent != (self.config.output / "campaigns").resolve():
            raise Neural1Error("campaign path escapes its storage root")
        if not path.is_dir():
            raise Neural1Error('unknown campaign')
        return path

    def running(self) -> bool:
        self.config.storage_check()
        self.config.output.mkdir(parents=True, exist_ok=True)
        with (self.config.output / 'worker.lock').open('a') as stream:
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return True
        return False

    def start(self, campaign_id: str | None = None) -> str:
        self.config.check()
        if self.running():
            raise Neural1Error('a console run is already active; cancel it first')
        if campaign_id is None:
            check_model(self.registry, self.model_id)
            spec = preset(self.family, self.model_id)
            root = self.config.output / 'campaigns' / spec.campaign_id
            spec.save(root / 'spec.json')
        else:
            root = self.root(campaign_id)
            spec = CampaignSpec.load(root / 'spec.json')
            check_model(self.registry, spec.model_ids[0])
        log = self.config.ssd / 'logs' / f'{spec.campaign_id}.log'
        launch_id = secrets.token_hex(12)
        with log.open('ab') as stream:
            process = subprocess.Popen(['/usr/bin/systemd-run', '--user', '--collect', '--unit=neural1-run-' + spec.campaign_id, '--property=WorkingDirectory=' + str(self.config.checkout), '--property=StandardOutput=append:' + str(log), '--property=StandardError=append:' + str(log), '--setenv=PYTHONPATH=' + str(self.config.checkout), '--setenv=PYTHONDONTWRITEBYTECODE=1', sys.executable, '-m', 'neural1.application', '--config', str(self.config.path), '--worker', spec.campaign_id, '--launch-id', launch_id, *(['--resume'] if campaign_id else [])], stdin=subprocess.DEVNULL, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True, cwd=self.config.checkout)  # noqa: S603 - fixed service command and pinned Python, argument array
        for _ in range(50):
            if process.poll() not in (None, 0):
                raise Neural1Error(f'worker exited with {process.returncode}; inspect {log}')
            active = self.running()
            if (root / 'worker.json').exists():
                info = json.loads((root / 'worker.json').read_text())
                if info.get('launch_id') == launch_id and (active or info.get('status') == 'FINISHED'):
                    return spec.campaign_id
            time.sleep(0.1)
        raise Neural1Error(f'worker startup unconfirmed; inspect {log}')

    def cancel(self, campaign_id: str) -> dict[str, Any]:
        self.config.storage_check()
        root = self.root(campaign_id)
        CampaignEngine(self.config.output, self.registry, {}).cancel(campaign_id)
        info_path = root / 'worker.json'
        if info_path.exists():
            info = json.loads(info_path.read_text())
            proc = Path('/proc') / str(info['pid'])
            try:
                same_start = proc.joinpath('stat').read_text().split()[21] == info['process_start']
                arguments = proc.joinpath('cmdline').read_bytes().split(b'\0')
                if same_start and b'neural1.application' in arguments and campaign_id.encode() in arguments:
                    os.kill(info['pid'], signal.SIGTERM)
            except (FileNotFoundError, ProcessLookupError):
                pass
        return {'campaign_id': campaign_id, 'cancellation_requested': True}

    def browse(self) -> list[dict[str, Any]]:
        self.config.storage_check()
        result = []
        for path in sorted((self.config.output / 'campaigns').glob('*/spec.json')):
            root = path.parent
            summary = json.loads((root / 'summary.json').read_text()) if (root / 'summary.json').exists() else {'status': 'INTERRUPTED_OR_STARTING'}
            result.append({'campaign_id': root.name, 'family': json.loads(path.read_text())['experiments'][0], 'status': summary['status'], 'turns': sum(len(p.read_text().splitlines()) for p in root.glob('cells/*/transcript.jsonl'))})
        return result

    def export(self, campaign_id: str) -> str:
        self.config.check()
        if self.running():
            raise Neural1Error('wait for or cancel the active run before exporting')
        root = self.root(campaign_id)
        ingest(self.config, root)
        for checkpoint_path in root.glob("cells/*/checkpoint.json"):
            checkpoint = json.loads(checkpoint_path.read_text())
            relative = Path(checkpoint["snapshot_path"])
            if relative.is_absolute() or ".." in relative.parts:
                raise Neural1Error("unsafe snapshot dependency")
            source = self.config.output / relative
            if self.config.output.resolve() not in source.resolve().parents or not source.is_file():
                raise Neural1Error("missing or escaped snapshot dependency")
            if sha256_bytes(source.read_bytes()) != checkpoint["snapshot_sha256"]:
                raise Neural1Error("snapshot dependency hash mismatch")
            destination = root / relative
            if destination.exists() and sha256_bytes(destination.read_bytes()) != checkpoint["snapshot_sha256"]:
                raise Neural1Error("conflicting export snapshot")
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                shutil.copyfile(source, destination)
        database = sqlite3.connect(self.config.database)
        snapshot = sqlite3.connect(root / 'meta.sqlite')
        try:
            database.backup(snapshot)
        finally:
            snapshot.close()
            database.close()
        destination = self.config.ssd / 'exports' / f'{campaign_id}-{time.time_ns()}'
        export_bundle(root, destination, reproduction_command=f'neural1 console; RESUME {campaign_id}')
        if not verify_bundle(destination).valid:
            raise Neural1Error('export verification failed')
        return str(destination)

    def meta(self, operation: str, identifier: str = '') -> Any:
        self.config.check()
        database = ResearchDatabase(self.config.database)
        try:
            if operation == 'QUEUE':
                return database.research_queue()
            if operation == 'HISTORY':
                return database.claim_history(identifier)
            if operation == 'CLAIM':
                return database.claim(identifier)
            return [json.loads(row[0]) for row in database.connection.execute('SELECT payload FROM claims ORDER BY updated_at DESC LIMIT 30')]
        finally:
            database.close()

    def command(self, line: str) -> Any:
        self.config.storage_check()
        args = shlex.split(line)
        if not args:
            return None
        op = args[0].upper()
        if op in ('1', '2', '3', '4', '5'):
            self.family = EXPERIMENTS[int(op) - 1]
            return {'selected': LABELS[int(op) - 1]}
        if op == 'MODELS':
            return [asdict(model) for model in self.registry.models.values()]
        if op == 'MODEL' and len(args) == 2:
            value = check_model(self.registry, args[1])
            self.model_id = args[1]
            return value
        if op == 'START':
            return {'started': self.start()}
        if op == 'RESUME' and len(args) == 2:
            return {'started': self.start(args[1])}
        if op == 'STOP' and len(args) == 2:
            return self.cancel(args[1])
        if op in ('RUNS', 'STATUS'):
            return {'worker_active': self.running(), 'runs': self.browse(), 'resources': self.config.check()}
        if op == 'TRANSCRIPT' and len(args) == 2:
            root = self.root(args[1])
            return {str(path.relative_to(root)): [json.loads(line) for line in path.read_text().splitlines()[-12:]] for path in root.glob('cells/*/transcript.jsonl')}
        if op == 'SHOW' and len(args) == 2:
            root = self.root(args[1])
            return {str(path.relative_to(root)): json.loads(path.read_text()) for path in sorted(root.glob('cells/*/family-result.json')) + sorted(root.glob('cells/*/checkpoint.json'))}
        if op == 'EXPORT' and len(args) == 2:
            return {'verified_export': self.export(args[1])}
        if op == 'OPEN' and len(args) == 2:
            path = Path(args[1]).resolve()
            if self.config.ssd.resolve() not in path.parents:
                raise Neural1Error('bundle must be on the configured SSD')
            verification = verify_bundle(path)
            if not verification.valid:
                raise Neural1Error(str(verification.errors))
            for checkpoint_path in (path / "records").glob("cells/*/checkpoint.json"):
                checkpoint = json.loads(checkpoint_path.read_text())
                source = (path / "records" / checkpoint["snapshot_path"]).resolve()
                if (path / "records").resolve() not in source.parents or not source.is_file() or sha256_bytes(source.read_bytes()) != checkpoint["snapshot_sha256"]:
                    raise Neural1Error("exported snapshot dependency is missing or invalid")
            return {'verification': asdict(verification), 'summary': json.loads((path / 'records/summary.json').read_text()), 'meta': json.loads((path / 'records/meta-link.json').read_text())}
        if op == 'META':
            return self.meta(args[1].upper() if len(args) > 1 else 'LIST', args[2] if len(args) > 2 else '')
        if op == 'LESSONS':
            return [path.name for path in sorted((self.config.checkout / 'docs/field-library').glob('*-*')) if (path / 'README.md').exists()]
        if op in ('ASK', 'HINT', 'EXPLAIN', 'SOURCE', 'CHECK', 'TRACE') and len(args) >= 3:
            from .field_library import FieldLibraryAssistant, LessonCorpus
            corpus = LessonCorpus(self.config.checkout / 'docs/field-library')
            context, paths = corpus.context(args[1], include_answers=op == 'CHECK')
            if op == 'SOURCE':
                return {'sources': paths, 'text': context}
            self.config.check()
            check_model(self.registry, self.model_id)
            assistant = FieldLibraryAssistant(corpus, provider_for(self.registry.require(self.model_id), record_path=self.config.ssd / 'logs/field-library.jsonl'))
            if op == 'TRACE':
                return asdict(assistant.assemble_explain(args[1], ' '.join(args[2:]).replace('\\n', '\n')))
            return asdict(assistant.answer(op, args[1], ' '.join(args[2:])))
        raise Neural1Error('unknown command or missing argument; HELP lists implemented operations')


HELP = '''[V] NEURAL1 / VIRTUAL APPLE-1
1  4K MIND
2  1976 MULTIVERSE
3  SELFHOST/1
4  256-BYTE UNIVERSE
5  RAM REPUBLIC
MODELS / MODEL model-id
START / STATUS / RUNS / SHOW run-id
TRANSCRIPT run-id
STOP run-id / RESUME run-id
EXPORT run-id / OPEN bundle-path
META / META CLAIM claim-id
META HISTORY claim-id / META QUEUE
LESSONS
ASK|HINT|EXPLAIN|CHECK lesson question
SOURCE lesson sources
TRACE lesson "assembly with \\n lines"
HELP / QUIT (active run continues)'''


def worker(config: ApplicationConfig, campaign_id: str, resume: bool, launch_id: str | None = None) -> int:
    config.check()
    config.output.mkdir(parents=True, exist_ok=True)
    with (config.output / 'worker.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise Neural1Error('another console worker owns the run lock') from None
        os.chdir(config.output)  # Pin the verified mount against ordinary unmount.
        app = Application(config)
        root = app.root(campaign_id)
        spec = CampaignSpec.load(root / 'spec.json')
        config.check()
        identity = check_model(app.registry, spec.model_ids[0])
        (root / 'worker.json').write_text(json.dumps({'pid': os.getpid(), 'process_start': Path('/proc/self/stat').read_text().split()[21], 'started_at': time.time(), 'model': identity, 'launch_id': launch_id, 'status': 'RUNNING'}, indent=2))
        stop = threading.Event()
        violations: list[str] = []

        def interrupted(signum: int, frame: Any) -> None:
            raise KeyboardInterrupt

        def watch() -> None:
            while not stop.wait(2):
                try:
                    sample = config.check()
                    CampaignEngine._append_jsonl(root / "resources.jsonl", {"time": time.time(), **sample})
                except Exception as error:
                    violations.append(str(error))
                    os.kill(os.getpid(), signal.SIGTERM)
                    return

        signal.signal(signal.SIGTERM, interrupted)
        signal.signal(signal.SIGINT, interrupted)
        threading.Thread(target=watch, daemon=True).start()
        run_registry = ModelRegistry({name: replace(app.registry.require(name), generation_defaults={**app.registry.require(name).generation_defaults, "max_tokens": spec.max_tokens}) for name in spec.model_ids})
        run_registry.save(root / "effective-registry.json")
        providers = {name: provider_for(run_registry.require(name), record_path=root / f'provider-{name}.jsonl') for name in spec.model_ids}
        engine = CampaignEngine(config.output, run_registry, providers)
        from .family_runner import family_objective

        def safety_check() -> None:
            config.check()

        try:
            execute = engine.resume if resume else engine.run
            summary = execute(spec, objective_factory=lambda cell, generation: family_objective(cell.experiment_id), command_parser=parse_commands, safety_check=safety_check)
            print(json.dumps(asdict(summary)), flush=True)
            return 0 if summary.status == 'COMPLETED' else 2
        except KeyboardInterrupt:
            config.storage_check()
            engine.cancel(campaign_id)
            CampaignEngine._atomic_json(root / 'summary.json', {'campaign_id': campaign_id, 'status': 'RESOURCE_STOP' if violations else 'INTERRUPTED', 'reasons': violations})
            return 2
        finally:
            stop.set()
            # Refuse any further SSD writes if mount identity/resource checks fail.
            try:
                config.storage_check()
                ingest(config, root)
                info = json.loads((root / "worker.json").read_text())
                info.update(status="FINISHED", finished_at=time.time())
                CampaignEngine._atomic_json(root / "worker.json", info)
            except Exception as error:
                print(f'Evidence ingestion deferred: {error}', flush=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=DEFAULT_CONFIG)
    parser.add_argument('--worker')
    parser.add_argument('--resume', action='store_true')
    parser.add_argument('--launch-id')
    parser.add_argument('--command')
    args = parser.parse_args(argv)
    try:
        config = ApplicationConfig.load(args.config)
        if args.worker:
            return worker(config, args.worker, args.resume, args.launch_id)
        app = Application(config)
        if args.command:
            print(json.dumps(app.command(args.command), indent=2, default=str))
            return 0
        print(HELP)
        while True:
            try:
                line = input(f'[V] {app.family}> ')
                if line.strip().upper() in ('QUIT', 'EXIT', '0'):
                    return 0
                if line.strip().upper() in ('HELP', '?'):
                    print(HELP)
                    continue
                value = app.command(line)
                for paragraph in json.dumps(value, indent=2, default=str).splitlines():
                    print(textwrap.fill(paragraph, width=40, replace_whitespace=False))
            except (ValueError, OSError, Neural1Error) as error:
                print(textwrap.fill(f'Cannot proceed: {error}', width=40))
            except (EOFError, KeyboardInterrupt):
                print('\nConsole closed; active worker retains state.')
                return 0
    except (ValueError, OSError, Neural1Error) as error:
        print(f'NEURAL1 unavailable: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
