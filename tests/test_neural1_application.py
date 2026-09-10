"""Synthetic software integration tests, never Pi or real-provider acceptance."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from unittest.mock import Mock

import pytest

from neural1.application import Application, ApplicationConfig, ingest, preset, worker
from neural1.core import Neural1Error
from neural1.models import FakeProvider, GenerationResult
from neural1.registry import ModelRegistry, RegisteredModel


@pytest.fixture
def configured(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[ApplicationConfig, Application]:
    ssd = tmp_path / 'synthetic-ssd'
    for name in ('logs', 'exports', 'meta'):
        (ssd / name).mkdir(parents=True)
    registry_path = tmp_path / 'registry.json'
    registry = ModelRegistry()
    registry.add(RegisteredModel('fixture', 'synthetic', 'test', 'fake', 'fake-v1', '0', 'NONE', 4096, 'fixture', 'TEST-ONLY', {}))
    registry.save(registry_path)
    config = ApplicationConfig(tmp_path / 'config.json', ssd, 'synthetic-uuid', registry_path, tmp_path, 'fixture')
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(ApplicationConfig, 'storage_check', lambda self: {'synthetic': True})
    monkeypatch.setattr(ApplicationConfig, 'check', lambda self: {'synthetic': True})
    monkeypatch.setattr('neural1.application.check_model', lambda *args: {'provider': 'synthetic'})
    monkeypatch.setattr('neural1.application.secrets.token_hex', lambda _: 'synthetic-launch-id')
    return config, Application(config)


def saved_spec(config: ApplicationConfig, seed: int = 1):
    spec = preset('4k-mind', 'fixture', seed=seed)
    root = config.output / 'campaigns' / spec.campaign_id
    spec.save(root / 'spec.json')
    return spec, root


def test_stop_resume_preserves_completed_turns_and_other_run_cancel(configured, monkeypatch):
    config, app = configured
    spec, root = saved_spec(config)
    other_spec, other_root = saved_spec(config, seed=2)
    app.cancel(other_spec.campaign_id)
    other_marker = (other_root / 'CANCEL').read_bytes()

    class StopAfterOne(FakeProvider):
        def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
            result = super().generate(prompt, agent_id=agent_id, seed=seed)
            app.cancel(spec.campaign_id)
            return result

    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.os.kill', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: StopAfterOne(default='0200: A9 2A 85 10 00\n0200R'))
    assert worker(config, spec.campaign_id, False) == 2
    transcript = next(root.glob('cells/*/transcript.jsonl'))
    first_turn = transcript.read_bytes()
    assert len(first_turn.splitlines()) == 1
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider(default='0200: A9 2A 85 10 00\n0200R'))
    assert worker(config, spec.campaign_id, True) == 0
    assert transcript.read_bytes().startswith(first_turn)
    assert len(transcript.read_bytes().splitlines()) == 3
    assert (other_root / 'CANCEL').read_bytes() == other_marker
    assert not (root / 'CANCEL').exists()
    assert app.browse()[0]['turns'] in (0, 3)


def test_start_passes_explicit_paths_and_resume_to_worker(configured, monkeypatch):
    config, app = configured
    spec, root = saved_spec(config)
    app.registry.save(root / 'effective-registry.json')
    (root / 'worker.json').write_text('{"launch_id":"synthetic-launch-id"}')
    monkeypatch.setattr(app, 'running', Mock(side_effect=[False, True]))
    process = Mock()
    process.poll.return_value = None
    popen = Mock(return_value=process)
    monkeypatch.setattr('neural1.application.subprocess.Popen', popen)
    assert app.start(spec.campaign_id) == spec.campaign_id
    argv = popen.call_args.args[0]
    assert argv[:3] == ['/usr/bin/systemd-run', '--user', '--collect']
    assert '--unit=neural1-run-' + spec.campaign_id in argv
    assert '--property=WorkingDirectory=' + str(config.checkout) in argv
    assert '--property=StandardOutput=append:' + str(config.ssd / 'logs' / f'{spec.campaign_id}.log') in argv
    assert popen.call_args.kwargs.get('shell', False) is False
    assert argv[argv.index('--launch-id') + 1] == 'synthetic-launch-id'
    assert '--resume' in argv
    assert argv[argv.index('--config') + 1] == str(config.path)
    assert argv[argv.index('--worker') + 1] == spec.campaign_id
    assert popen.call_args.kwargs['start_new_session'] is True


@pytest.mark.parametrize('identifier', ['../outside', 'N1-P-../../outside', '/N1-P-outside', 'N1-P-a/b'])
def test_invalid_campaign_paths_rejected(configured, identifier):
    _, app = configured
    with pytest.raises(Neural1Error):
        app.root(identifier)


def test_symlinked_campaign_cannot_write_outside_storage(configured, tmp_path):
    config, app = configured
    outside = tmp_path / 'outside'
    outside.mkdir()
    campaigns = config.output / 'campaigns'
    campaigns.mkdir(parents=True)
    (campaigns / 'N1-P-linked').symlink_to(outside, target_is_directory=True)
    with pytest.raises((Neural1Error, ValueError)):
        app.cancel('N1-P-linked')
    assert not (outside / 'CANCEL').exists()


def test_missing_mount_stops_start_before_any_writes(configured, monkeypatch):
    config, app = configured

    def missing(self):
        raise ValueError('required SSD is not mounted')

    monkeypatch.setattr(ApplicationConfig, 'check', missing)
    with pytest.raises(ValueError, match='not mounted'):
        app.start()
    assert not config.output.exists()
    assert list((config.ssd / 'logs').iterdir()) == []


def test_real_engine_records_ingest_query_export_reopen(configured, monkeypatch):
    config, app = configured
    spec, root = saved_spec(config)
    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider(default='0200: A9 2A 85 10 00\n0200R'))
    assert worker(config, spec.campaign_id, False) == 0
    claim_id = ingest(config, root)
    first_history = app.meta('HISTORY', claim_id)
    assert first_history
    assert ingest(config, root) == claim_id
    assert app.meta('HISTORY', claim_id) == first_history
    assert app.meta('CLAIM', claim_id)['scope']['target'] == 'VIRTUAL'
    assert app.meta('QUEUE')
    bundle = app.export(spec.campaign_id)
    reopened = app.command(f'OPEN {bundle}')
    assert reopened['verification']['valid']
    assert reopened['summary']['status'] == 'COMPLETED'
    assert reopened['meta']['claim_id'] == claim_id
    with sqlite3.connect(Path(bundle) / 'records/meta.sqlite') as database:
        assert database.execute('SELECT COUNT(*) FROM claims').fetchone()[0] >= 1
        assert database.execute('SELECT COUNT(*) FROM evidence').fetchone()[0] >= 1
        assert database.execute('SELECT COUNT(*) FROM edges').fetchone()[0] >= 1
    assert Application(config).meta('CLAIM', claim_id) == app.meta('CLAIM', claim_id)
    (Path(bundle) / 'records/summary.json').write_text('{}')
    with pytest.raises(Neural1Error, match='identity mismatch'):
        app.command(f'OPEN {bundle}')


def test_interrupted_worker_never_writes_after_storage_loss(configured, monkeypatch):
    config, _ = configured
    spec, root = saved_spec(config)
    lost = False

    def check(self):
        if lost:
            raise ValueError('required SSD is not mounted')
        return {}

    def disappear(*args, **kwargs):
        nonlocal lost
        lost = True
        raise KeyboardInterrupt

    monkeypatch.setattr(ApplicationConfig, 'check', check)
    monkeypatch.setattr(ApplicationConfig, 'storage_check', check)
    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider())
    monkeypatch.setattr('neural1.application.CampaignEngine.run', disappear)
    with pytest.raises(ValueError, match='not mounted'):
        worker(config, spec.campaign_id, False)
    assert not (root / 'CANCEL').exists()
    assert not (root / 'summary.json').exists()
    assert not config.database.exists()


def test_meta_retry_repairs_interruption_between_claim_and_evidence(configured, monkeypatch):
    config, app = configured
    _, root = saved_spec(config)
    (root / 'summary.json').write_text('{"status":"SYNTHETIC_NEGATIVE_RESULT"}')
    from neural1.meta_store import ResearchDatabase
    original = ResearchDatabase.put_evidence
    monkeypatch.setattr(ResearchDatabase, 'put_evidence', Mock(side_effect=OSError('simulated interruption')))
    with pytest.raises(OSError, match='interruption'):
        ingest(config, root)
    assert not (root / 'meta-link.json').exists()
    monkeypatch.setattr(ResearchDatabase, 'put_evidence', original)
    claim_id = ingest(config, root)
    assert (root / 'meta-link.json').is_file()
    assert len(app.meta('HISTORY', claim_id)) == 1
    assert 'SYNTHETIC_NEGATIVE_RESULT' in app.meta('CLAIM', claim_id)['statement']
    with sqlite3.connect(config.database) as database:
        assert database.execute('SELECT COUNT(*) FROM evidence').fetchone()[0] == 1
        assert database.execute('SELECT COUNT(*) FROM edges').fetchone()[0] == 1


def test_application_config_rejects_relative_deployment_paths(tmp_path):
    import json
    path = tmp_path / 'config.json'
    path.write_text(json.dumps({'ssd': 'relative', 'uuid': 'expected', 'registry': '/registry', 'checkout': '/checkout', 'default_model': 'fixture'}))
    with pytest.raises(Neural1Error, match='absolute'):
        ApplicationConfig.load(path)


def test_export_contains_verified_checkpoint_snapshot(configured, monkeypatch):
    import hashlib
    import json
    config, app = configured
    spec, _ = saved_spec(config)
    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider(default='0200: A9 2A 85 10 00\n0200R'))
    assert worker(config, spec.campaign_id, False) == 0
    bundle = Path(app.export(spec.campaign_id))
    for checkpoint_file in (bundle / 'records').glob('cells/*/checkpoint.json'):
        checkpoint = json.loads(checkpoint_file.read_text())
        snapshot = bundle / 'records' / checkpoint['snapshot_path']
        assert snapshot.is_file(), 'export omitted a checkpoint dependency'
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == checkpoint['snapshot_sha256']
    assert app.command(f'OPEN {bundle}')['verification']['valid']


def test_export_rejects_missing_checkpoint_snapshot(configured, monkeypatch):
    import json
    config, app = configured
    spec, root = saved_spec(config)
    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider(default='0200: A9 2A 85 10 00\n0200R'))
    assert worker(config, spec.campaign_id, False) == 0
    checkpoint = json.loads(next(root.glob('cells/*/checkpoint.json')).read_text())
    (config.output / checkpoint['snapshot_path']).unlink()
    with pytest.raises((Neural1Error, OSError, ValueError)):
        app.export(spec.campaign_id)


def test_console_help_launches_outside_checkout(tmp_path):
    import subprocess
    import sys
    launcher = Path(sys.executable).parent / 'neural1'
    assert launcher.is_file(), 'test requires the installed editable application entry point'
    result = subprocess.run([str(launcher), 'console', '--help'], cwd=tmp_path, capture_output=True, text=True, timeout=15)  # noqa: S603 - installed launcher and literal args
    assert result.returncode == 0, result.stderr
    assert '--config' in result.stdout and '--command' in result.stdout


def test_field_library_absolute_corpus_outside_checkout(tmp_path, monkeypatch):
    from neural1.field_library import LessonCorpus
    checkout = Path(__file__).resolve().parents[1]
    monkeypatch.chdir(tmp_path)
    context, sources = LessonCorpus(checkout / 'docs/field-library').context('M01')
    assert context.strip()
    assert sources
    assert any('M01-meet-the-monitor' in source for source in sources)


def test_installed_console_refuses_plain_directory_as_ssd(tmp_path):
    import json
    import subprocess
    import sys
    ssd = tmp_path / 'not-mounted'
    ssd.mkdir()
    config = tmp_path / 'config.json'
    config.write_text(json.dumps({'ssd': str(ssd), 'uuid': 'definitely-not-a-real-uuid', 'registry': str(tmp_path / 'registry'), 'checkout': str(tmp_path), 'default_model': 'fixture'}))
    launcher = Path(sys.executable).parent / 'neural1'
    result = subprocess.run([str(launcher), 'console', '--config', str(config), '--command', 'START'], cwd=tmp_path, capture_output=True, text=True, timeout=15)  # noqa: S603 - installed launcher and local fixture config
    assert result.returncode == 2
    assert 'not mounted' in result.stderr
    assert list(ssd.iterdir()) == []


def test_stop_interrupts_actual_slow_worker_process(configured):
    """Exercise SIGTERM/PID ownership in a subprocess; all mocks stay in test code."""
    import json
    import selectors
    import subprocess
    import sys
    import time
    config, app = configured
    spec, root = saved_spec(config)
    config.path.write_text(json.dumps({
        'ssd': str(config.ssd), 'uuid': config.uuid, 'registry': str(config.registry),
        'checkout': str(config.checkout), 'default_model': config.default_model,
    }))
    script = '''
from pathlib import Path
import sys, time
from unittest.mock import patch
from neural1.application import ApplicationConfig, worker
from neural1.models import FakeProvider
class SyntheticSlowProvider(FakeProvider):
    def generate(self, *args, **kwargs):
        print("SYNTHETIC_PROVIDER_ENTERED", flush=True)
        time.sleep(60)
        return super().generate(*args, **kwargs)
config = ApplicationConfig.load(Path(sys.argv[2]))
with patch.object(ApplicationConfig, "check", return_value={}), patch.object(ApplicationConfig, "storage_check", return_value={}), patch("neural1.application.check_model", return_value={"provider": "synthetic"}), patch("neural1.application.provider_for", return_value=SyntheticSlowProvider(default="0200: A9 2A 85 10 00")):
    raise SystemExit(worker(config, sys.argv[3], False))
'''
    process = subprocess.Popen(  # noqa: S603 - explicit test harness; no production guard changes
        [sys.executable, '-c', script, 'neural1.application', str(config.path), spec.campaign_id],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=config.checkout, start_new_session=True,
    )
    try:
        assert process.stdout is not None
        with selectors.DefaultSelector() as selector:
            selector.register(process.stdout, selectors.EVENT_READ)
            assert selector.select(timeout=10), 'worker did not enter provider within startup bound'
            assert process.stdout.readline().strip() == 'SYNTHETIC_PROVIDER_ENTERED'
        started = time.monotonic()
        assert app.cancel(spec.campaign_id)['cancellation_requested']
        assert process.wait(timeout=5) == 2
        assert time.monotonic() - started < 5
        assert json.loads((root / 'summary.json').read_text())['status'] == 'INTERRUPTED'
        assert json.loads((root / 'CANCEL').read_text()) == {'owner': 'neural1-campaign', 'campaign_id': spec.campaign_id}
    finally:
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        if process.stdout is not None:
            process.stdout.close()


@pytest.mark.parametrize('locked,marker_present', [(False, False), (False, True), (True, False)])
def test_systemd_run_success_alone_does_not_confirm_running(configured, monkeypatch, locked, marker_present):
    config, app = configured
    spec, root = saved_spec(config)
    app.registry.save(root / 'effective-registry.json')
    if marker_present:
        (root / 'worker.json').write_text('{"launch_id":"synthetic-launch-id"}')
    monkeypatch.setattr(app, 'running', Mock(side_effect=[False] + [locked] * 50))
    process = Mock()
    process.poll.return_value = 0
    monkeypatch.setattr('neural1.application.subprocess.Popen', Mock(return_value=process))
    monkeypatch.setattr('neural1.application.time.sleep', lambda _: None)
    with pytest.raises(Neural1Error, match='startup unconfirmed'):
        app.start(spec.campaign_id)


def test_start_waits_for_worker_lock_and_marker_after_service_submission(configured, monkeypatch):
    config, app = configured
    spec, root = saved_spec(config)
    app.registry.save(root / 'effective-registry.json')
    running = Mock(side_effect=[False, False, True, True])
    monkeypatch.setattr(app, 'running', running)
    process = Mock()
    process.poll.return_value = 0
    monkeypatch.setattr('neural1.application.subprocess.Popen', Mock(return_value=process))
    pauses = []

    def pause(seconds):
        pauses.append(seconds)
        if len(pauses) == 2:
            (root / 'worker.json').write_text('{"launch_id":"synthetic-launch-id"}')

    monkeypatch.setattr('neural1.application.time.sleep', pause)
    assert app.start(spec.campaign_id) == spec.campaign_id
    assert len(pauses) == 2
    assert running.call_count == 4


@pytest.mark.parametrize('active,status', [(True, 'RUNNING'), (False, 'FINISHED')])
def test_stale_launch_marker_never_confirms_new_start(configured, monkeypatch, active, status):
    import json
    config, app = configured
    spec, root = saved_spec(config)
    app.registry.save(root / 'effective-registry.json')
    (root / 'worker.json').write_text(json.dumps({'launch_id': 'old-launch', 'status': status}))
    monkeypatch.setattr(app, 'running', Mock(side_effect=[False] + [active] * 50))
    process = Mock()
    process.poll.return_value = 0
    monkeypatch.setattr('neural1.application.subprocess.Popen', Mock(return_value=process))
    monkeypatch.setattr('neural1.application.time.sleep', lambda _: None)
    with pytest.raises(Neural1Error, match='startup unconfirmed'):
        app.start(spec.campaign_id)


def test_same_launch_finished_worker_is_confirmed(configured, monkeypatch):
    config, app = configured
    spec, root = saved_spec(config)
    app.registry.save(root / 'effective-registry.json')
    (root / 'worker.json').write_text('{"launch_id":"synthetic-launch-id","status":"FINISHED"}')
    monkeypatch.setattr(app, 'running', lambda: False)
    process = Mock()
    process.poll.return_value = 0
    monkeypatch.setattr('neural1.application.subprocess.Popen', Mock(return_value=process))
    assert app.start(spec.campaign_id) == spec.campaign_id


def test_stop_is_available_when_thermal_launch_check_fails(configured, monkeypatch):
    import json
    config, app = configured
    spec, root = saved_spec(config)
    monkeypatch.setattr(ApplicationConfig, 'check', Mock(side_effect=Neural1Error('thermal stop: 80 C')))
    assert app.cancel(spec.campaign_id)['cancellation_requested']
    assert json.loads((root / 'CANCEL').read_text()) == {'owner': 'neural1-campaign', 'campaign_id': spec.campaign_id}
    with pytest.raises(Neural1Error, match='thermal stop'):
        app.start(spec.campaign_id)


def test_selfhost_console_ingest_rebuild_reopen_and_meta(configured, monkeypatch):
    """Synthetic provider bytes exercise archive persistence, never live acceptance."""
    import hashlib
    config, app = configured
    spec = preset('selfhost1', 'fixture', seed=81)
    root = config.output / 'campaigns' / spec.campaign_id
    spec.save(root / 'spec.json')
    monkeypatch.setattr('neural1.application.signal.signal', lambda *args: None)
    monkeypatch.setattr('neural1.application.provider_for', lambda *args, **kwargs: FakeProvider(default='0200: A9 41 20 EF FF 4C 1F FF\n0200R'))
    assert worker(config, spec.campaign_id, False) == 0
    imported = app.command('SELFHOST INGEST ' + spec.campaign_id)
    assert imported['result']
    artifact = imported['result'][0]
    assert artifact['origin_run_id'] == spec.campaign_id
    assert artifact['evidence_class'] == 'SYNTHETIC_OR_REPLAY'
    assert artifact['qualified']
    reopened = Application(config)
    assert reopened.command('SELFHOST') == app.command('SELFHOST LIST')
    rebuilt = reopened.command('SELFHOST REBUILD ' + artifact['artifact_id'])
    assert rebuilt['result']
    claim = app.command('META CLAIM ' + rebuilt['claim_id'])
    assert claim['scope']['target'] == 'VIRTUAL'
    assert claim['scope']['evidence_hash'] == hashlib.sha256(Path(rebuilt['receipt']).read_bytes()).hexdigest()
    assert app.command('META HISTORY ' + rebuilt['claim_id'])
    assert app.command('META QUEUE')
    exported = reopened.command('SELFHOST EXPORT ' + artifact['artifact_id'])
    bundle = Path(exported['result']['destination'])
    verified = reopened.command('SELFHOST OPEN ' + str(bundle))
    assert verified['valid']
    assert verified['records'][0]['evidence_class'] == 'SYNTHETIC_OR_REPLAY'
    image = bundle / artifact['artifact_id'] / 'image.bin'
    image.write_bytes(bytes(4096))
    with pytest.raises(Neural1Error):
        reopened.command('SELFHOST OPEN ' + str(bundle))


def test_selfhost_archive_commands_refuse_external_evidence(configured, tmp_path):
    _, app = configured
    external = tmp_path / 'outside-evidence.json'
    external.write_text('{}')
    with pytest.raises(Neural1Error, match='configured SSD'):
        app.command('SELFHOST QUALIFY ' + str(external))
    with pytest.raises(Neural1Error, match='configured SSD'):
        app.command('SELFHOST OPEN ' + str(external))


def test_selfhost_mutations_wait_for_active_campaign(configured, monkeypatch):
    _, app = configured
    monkeypatch.setattr(app, 'running', lambda: True)
    with pytest.raises(Neural1Error, match='active campaign'):
        app.command('SELFHOST INGEST N1-P-example')


def test_foreground_operation_is_stopped_on_resource_failure(configured, monkeypatch):
    import multiprocessing
    import time

    from neural1.application import monitored_call
    config, _ = configured
    baseline = {process.pid for process in multiprocessing.active_children()}
    checks = 0

    def check(self):
        nonlocal checks
        checks += 1
        if checks > 1:
            raise Neural1Error('synthetic thermal threshold')
        return {}

    monkeypatch.setattr(ApplicationConfig, 'check', check)
    started = time.monotonic()
    with pytest.raises(Neural1Error, match='thermal threshold'):
        monitored_call(config, lambda: time.sleep(30), timeout_seconds=40)
    assert time.monotonic() - started < 5
    assert {process.pid for process in multiprocessing.active_children()} == baseline


def test_foreground_operation_success_and_timeout_leave_no_child(configured):
    import multiprocessing
    import time

    from neural1.application import monitored_call
    config, _ = configured
    baseline = {process.pid for process in multiprocessing.active_children()}
    assert monitored_call(config, lambda: {'synthetic': True}, timeout_seconds=5) == {'synthetic': True}
    with pytest.raises(Neural1Error, match='time limit'):
        monitored_call(config, lambda: time.sleep(30), timeout_seconds=0.1)
    assert {process.pid for process in multiprocessing.active_children()} == baseline


def test_model_selection_persists_across_console_instances(configured, monkeypatch):
    import json
    import os
    config, app = configured
    registry = ModelRegistry.load(config.registry)
    registry.add(RegisteredModel('second', 'synthetic', 'test', 'fake', 'fake-v2', '0', 'NONE', 4096, 'fixture', 'TEST-ONLY', {}))
    registry.save(config.registry)
    app = Application(config)
    check = Mock(return_value={'model_id': 'second', 'validated': 'synthetic'})
    monkeypatch.setattr('neural1.application.check_model', check)
    assert app.command('MODEL second')['validated'] == 'synthetic'
    check.assert_called_once_with(app.registry, 'second')
    assert Application(config).model_id == 'second'
    preference = json.loads(app.preferences.read_text())
    assert preference['uid'] == os.getuid()
    assert preference['model_id'] == 'second'
    assert app.preferences.stat().st_mode & 0o777 == 0o600
    assert app.command('STATUS')['selected_model'] == 'second'


def test_failed_live_model_validation_never_changes_preference(configured, monkeypatch):
    config, app = configured
    app.command('MODEL fixture')
    before = app.preferences.read_bytes()
    monkeypatch.setattr('neural1.application.check_model', Mock(side_effect=Neural1Error('manifest mismatch')))
    with pytest.raises(Neural1Error, match='manifest mismatch'):
        app.command('MODEL missing')
    assert app.preferences.read_bytes() == before
    assert Application(config).model_id == 'fixture'


@pytest.mark.parametrize('content', ['not-json', '{"schema_version":1,"uid":-1,"model_id":"fixture"}'])
def test_corrupt_model_preference_falls_back_and_model_command_repairs(configured, content):
    config, app = configured
    app.preferences.write_text(content)
    reopened = Application(config)
    assert reopened.model_id == config.default_model
    assert reopened.preference_warning
    assert reopened.command('STATUS')['preference_warning']
    reopened.command('MODEL fixture')
    assert Application(config).preference_warning is None


def test_symlink_model_preference_is_replaced_without_touching_target(configured, tmp_path):
    config, app = configured
    protected = tmp_path / 'unrelated.json'
    protected.write_text('unrelated data')
    app.preferences.symlink_to(protected)
    reopened = Application(config)
    assert reopened.preference_warning
    reopened.command('MODEL fixture')
    assert not app.preferences.is_symlink()
    assert protected.read_text() == 'unrelated data'


def test_removed_registry_model_preference_falls_back(configured):
    import json
    import os
    config, app = configured
    app.preferences.write_text(json.dumps({'schema_version': 1, 'uid': os.getuid(), 'model_id': 'removed'}))
    reopened = Application(config)
    assert reopened.model_id == config.default_model
    assert reopened.preference_warning


def test_directory_in_preference_slot_is_preserved_and_recovered(configured):
    config, app = configured
    app.preferences.mkdir()
    (app.preferences / 'retain.txt').write_text('retain this unrelated content')
    reopened = Application(config)
    assert reopened.preference_warning
    reopened.command('MODEL fixture')
    assert Application(config).preference_warning is None
    backups = list(app.preferences.parent.glob('.neural1-invalid-preference-*/prior/retain.txt'))
    assert len(backups) == 1
    assert backups[0].read_text() == 'retain this unrelated content'
