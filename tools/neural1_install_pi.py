#!/usr/bin/env python3
"""Install a pinned NEURAL1 checkout on a live Pi; never format or migrate media.

Run only after SSD commissioning/model migration. All arguments are explicit;
no network package acquisition is performed. A local py65 wheel is optional
when the existing native Python already imports py65.
"""
from __future__ import annotations

import argparse
import fcntl
import grp
import hashlib
import json
import os
import platform
import pwd
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def command(args: list[str], **kwargs: Any) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True, timeout=180, **kwargs)  # noqa: S603 - explicit argument vectors, no shell
    return str(result.stdout).strip()


def require_pi(*, machine: str | None = None, model_path: Path = Path('/proc/device-tree/model')) -> str:
    machine = machine or platform.machine()
    model = model_path.read_bytes().rstrip(b'\0').decode()
    if machine != 'aarch64' or not model.startswith('Raspberry Pi '):
        raise ValueError('installer requires the actual ARM64 Raspberry Pi; host installation refused')
    if sys.version_info < (3, 12):  # noqa: UP036 - installer preflight may run with an older system Python
        raise ValueError('native Python >=3.12 is required')
    return model


def fstab_content(previous: str, uuid: str, mount: Path) -> str:
    if not re.fullmatch(r'[0-9A-Fa-f-]+', uuid) or not re.fullmatch(r'/[A-Za-z0-9_./-]+', str(mount)):
        raise ValueError('UUID or mount path contains unsupported characters')
    expected = f'UUID={uuid}'
    lines = previous.splitlines()
    matched = False
    for index, line in enumerate(lines):
        fields = line.split()
        if not fields or fields[0].startswith('#') or len(fields) < 4:
            continue
        if fields[1] == str(mount):
            if fields[0] != expected or fields[2] != 'ext4' or matched:
                raise ValueError('conflicting existing fstab mount; inspect before deployment')
            matched = True
            options = list(dict.fromkeys([*fields[3].split(','), 'nofail', 'x-systemd.device-timeout=10s']))
            fields[3] = ','.join(options)
            lines[index] = '\t'.join(fields)
        elif fields[0] == expected:
            raise ValueError('SSD UUID already configured at another mountpoint')
    if not matched:
        lines.append(f'{expected}\t{mount}\text4\tdefaults,nofail,x-systemd.device-timeout=10s\t0\t2')
    return '\n'.join(lines) + '\n'


def ensure_linger(user: str, uid: int, backup: Path, guard: Callable[[], None]) -> dict[str, Any]:
    """Record and change only the requested account's user-service persistence."""
    previous = command(['loginctl', 'show-user', user, '--property=Linger', '--value'])
    if previous not in {'yes', 'no'}:
        raise ValueError('cannot establish prior target-account linger state')
    record = {'user': user, 'uid': uid, 'previous': previous, 'changed': previous == 'no',
              'rollback': f'loginctl disable-linger {user}' if previous == 'no' else 'No linger change to roll back.'}
    guard()
    (backup / 'linger.json').write_text(json.dumps(record, indent=2) + '\n')
    if previous == 'no':
        guard()
        command(['loginctl', 'enable-linger', user])
    command(['systemctl', 'start', f'user@{uid}.service'])
    command(['systemctl', 'is-active', f'user@{uid}.service'])
    if command(['loginctl', 'show-user', user, '--property=Linger', '--value']) != 'yes':
        raise ValueError('target-account linger was not enabled')
    return record


def install(args: argparse.Namespace) -> dict[str, Any]:
    sys.dont_write_bytecode = True
    model = require_pi()
    if os.geteuid() != 0:
        raise ValueError('run through the normal local root/sudo authorization mechanism')
    for path in (args.ssd, args.ollama_store, args.registry):
        if not re.fullmatch(r"/[A-Za-z0-9_./-]+", str(path)):
            raise ValueError("deployment paths must be absolute with no whitespace or shell metacharacters")
    try:
        import py65  # noqa: F401 - source package imports the existing emulator at import time
    except ImportError:
        if args.py65_wheel is None:
            raise ValueError("existing py65 or explicit local py65 1.2.0 wheel required for preflight") from None
        wheel = args.py65_wheel.resolve(strict=True)
        if not wheel.name.startswith("py65-1.2.0-") or not wheel.name.endswith(".whl"):
            raise ValueError("only an explicit py65 1.2.0 wheel is accepted") from None
        sys.path.insert(0, str(wheel))
    source = args.source.resolve(strict=True)
    if command(['git', '-C', str(source), 'status', '--porcelain', '--untracked-files=no']):
        raise ValueError('source checkout has tracked modifications; commit tested implementation first')
    revision = command(['git', '-C', str(source), 'rev-parse', 'HEAD'])
    if not re.fullmatch('[0-9a-f]{40}', revision):
        raise ValueError('invalid source revision')
    sys.path.insert(0, str(source))
    from neural1.deployment import verify_storage
    from neural1.registry import ModelRegistry
    account = pwd.getpwnam(args.user)
    store = args.ollama_store.resolve(strict=True)
    registry = args.registry.resolve(strict=True)
    models = ModelRegistry.load(registry)
    if models.require(args.default_model).backend != 'ollama':
        raise ValueError('default model must identify the existing native Ollama model')

    def guard() -> None:
        verify_storage(args.ssd, args.uuid, write_paths=(store, registry, args.ssd / 'runs', args.ssd / 'meta', args.ssd / 'logs', args.ssd / 'exports'), min_free_bytes=2 * 1024**3)

    guard()
    if not (store / 'blobs').is_dir() or not (store / 'manifests').is_dir():
        raise ValueError('native Ollama blobs/manifests must already be verified and migrated onto SSD')
    filesystem = command(['findmnt', '-n', '-o', 'FSTYPE', '--target', str(args.ssd)])
    if filesystem != 'ext4':
        raise ValueError('this installer supports an already commissioned ext4 SSD')
    service_user = command(['systemctl', 'show', 'ollama.service', '--property=User', '--value']) or 'root'
    command(['systemctl', 'cat', 'ollama.service'])
    service_start = command(['systemctl', 'show', 'ollama.service', '--property=ExecStart', '--value'])
    binary_match = re.search(r'path=([^ ;]+)', service_start)
    if not binary_match:
        raise ValueError('cannot identify native Ollama service executable')
    with Path(binary_match[1]).open('rb') as stream:
        elf = stream.read(20)
    if elf[:4] != b'\x7fELF' or elf[4:6] != b'\x02\x01' or int.from_bytes(elf[18:20], 'little') != 183:
        raise ValueError('existing Ollama service executable is not native ARM64 ELF')
    command(['runuser', '-u', service_user, '--', 'test', '-r', str(store / 'manifests')])
    command(['runuser', '-u', service_user, '--', 'test', '-w', str(store / 'blobs')])
    fstab = Path('/etc/fstab')
    new_fstab = fstab_content(fstab.read_text(), args.uuid, args.ssd)
    guard()
    backup = Path('/var/backups/neural1') / datetime.now(UTC).strftime('%Y%m%dT%H%M%S.%fZ')
    backup.mkdir(parents=True, mode=0o700)
    backup.chmod(0o700)
    changes: list[dict[str, Any]] = []

    def write(path: Path, data: bytes, mode: int = 0o644) -> None:
        guard()
        if path.is_symlink():
            raise ValueError(f'refusing to replace symlink: {path}')
        if path.exists() and path.read_bytes() == data:
            return
        entry: dict[str, Any] = {'path': str(path), 'existed': path.exists()}
        if path.exists():
            saved = backup / path.relative_to('/')
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
            entry['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            if hashlib.sha256(saved.read_bytes()).hexdigest() != entry['sha256']:
                raise ValueError('configuration backup verification failed')
            entry['backup'] = str(saved)
        changes.append(entry)
        (backup / 'manifest.json').write_text(json.dumps(changes, indent=2) + '\n')
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.chmod(mode)
        guard()
        os.replace(temporary, path)

    tracked_sizes = command(['git', '-C', str(source), 'ls-tree', '-r', '-l', revision])
    checkout_bytes = sum(int(line.split()[3]) for line in tracked_sizes.splitlines() if line.split()[3].isdigit())
    if shutil.disk_usage('/opt').free < 2 * checkout_bytes + 1024**3:
        raise ValueError('insufficient OS filesystem space for pinned code and native venv')
    release = Path('/opt/neural1/releases') / revision
    guard()
    release.parent.mkdir(parents=True, exist_ok=True)
    if not release.exists():
        with tempfile.TemporaryDirectory(prefix='neural1-release-', dir=release.parent) as workspace:
            temporary = Path(workspace)
            archive = temporary / 'checkout.tar'
            command(['git', '-C', str(source), 'archive', '--format=tar', '-o', str(archive), revision])
            tree = temporary / 'tree'
            tree.mkdir()
            with tarfile.open(archive) as stream:
                stream.extractall(tree, filter='data')  # noqa: S202 - Python safe data extraction filter
            files = {str(path.relative_to(tree)): hashlib.sha256(path.read_bytes()).hexdigest() for path in tree.rglob('*') if path.is_file()}
            (tree / '.neural1-files.json').write_text(json.dumps(files, sort_keys=True) + '\n')
            (tree / '.neural1-revision').write_text(revision + '\n')
            guard()
            os.rename(tree, release)
    elif (release / '.neural1-revision').read_text().strip() != revision:
        raise ValueError('existing release has no matching deployment identity')
    for relative, digest in json.loads((release / '.neural1-files.json').read_text()).items():
        path = release / relative
        if not path.resolve().is_relative_to(release) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('existing release content no longer matches its deployment manifest')
    venv = release / '.venv'
    python = venv / 'bin/python'
    if not python.exists():
        guard()
        command([sys.executable, '-m', 'venv', '--system-site-packages', str(venv)])
    try:
        command([str(python), '-c', 'import py65.devices.mpu6502'])
    except subprocess.CalledProcessError:
        if args.py65_wheel is None:
            raise ValueError('py65 missing; provide an existing local py65 1.2.0 wheel') from None
        wheel = args.py65_wheel.resolve(strict=True)
        if not wheel.name.startswith('py65-1.2.0-') or not wheel.name.endswith('.whl'):
            raise ValueError('only an explicit py65 1.2.0 wheel is accepted') from None
        guard()
        command([str(python), '-m', 'pip', 'install', '--no-index', '--no-deps', str(wheel)])
    command([str(python), '-c', 'from importlib.metadata import version; assert version("py65") == "1.2.0"'])
    for name in ('runs', 'meta', 'logs', 'exports'):
        guard()
        directory = args.ssd / name
        directory.mkdir(exist_ok=True)
        os.chown(directory, account.pw_uid, account.pw_gid)
    provider_logs = args.ssd / 'logs/provider'
    provider_log = provider_logs / 'ollama.log'
    guard()
    if provider_logs.is_symlink() or provider_log.is_symlink():
        raise ValueError('provider log paths must not be symlinks')
    provider_logs.mkdir(exist_ok=True)
    provider_account = pwd.getpwnam(service_user)
    os.chown(provider_logs, provider_account.pw_uid, provider_account.pw_gid)
    provider_logs.chmod(0o750)
    provider_log.touch(exist_ok=True)
    os.chown(provider_log, provider_account.pw_uid, provider_account.pw_gid)
    provider_log.chmod(0o640)
    config = {'ssd': str(args.ssd), 'uuid': args.uuid, 'registry': str(registry), 'checkout': str(release), 'default_model': args.default_model, 'temperature_limit': 75.0, 'minimum_free_bytes': 2 * 1024**3}
    write(Path('/etc/neural1/config.json'), (json.dumps(config, indent=2) + '\n').encode())
    session_environment = 'export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"\nexport DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=$XDG_RUNTIME_DIR/bus}"\n'
    for executable, module in (('neural1', 'neural1.cli'), ('neural1-meta', 'neural1.meta_console'), ('neural1-storage', 'neural1.storage_commissioning')):
        launcher = f'#!/bin/sh\nexport PYTHONPATH={release}\nexport PYTHONDONTWRITEBYTECODE=1\n{session_environment}exec {python} -m {module} "$@"\n'
        write(Path('/usr/local/bin') / executable, launcher.encode(), 0o755)
    guard_script = f'#!/bin/sh\nexport PYTHONPATH={release}\nexport PYTHONDONTWRITEBYTECODE=1\nexec {python} -c \'from neural1.deployment import verify_storage; verify_storage("{args.ssd}", "{args.uuid}", min_free_bytes=536870912)\'\n'
    write(Path('/usr/local/libexec/neural1-storage-check'), guard_script.encode(), 0o755)
    mount_unit = command(['systemd-escape', '--path', '--suffix=mount', str(args.ssd)])
    override = f'[Unit]\nRequires={mount_unit}\nAfter={mount_unit}\nStartLimitIntervalSec=60\nStartLimitBurst=2\n\n[Service]\nEnvironment="OLLAMA_MODELS={store}"\nEnvironment="OLLAMA_NUM_PARALLEL=1"\nEnvironment="OLLAMA_MAX_LOADED_MODELS=1"\nEnvironment="OLLAMA_MAX_QUEUE=4"\nEnvironment="OLLAMA_KEEP_ALIVE=60s"\nEnvironment="OLLAMA_NO_CLOUD=1"\nExecStartPre=/usr/local/libexec/neural1-storage-check\nRestart=on-failure\nRestartSec=10\n'
    override += f'StandardOutput=append:{provider_log}\nStandardError=append:{provider_log}\n'
    if not Path('/usr/sbin/logrotate').is_file():
        raise ValueError('native logrotate is required for durable bounded provider logs')
    provider_group = grp.getgrgid(provider_account.pw_gid).gr_name
    rotation = f'{provider_log} {{\n    daily\n    maxsize 16M\n    rotate 4\n    missingok\n    notifempty\n    compress\n    delaycompress\n    copytruncate\n    su {service_user} {provider_group}\n    prerotate\n        /usr/local/libexec/neural1-storage-check\n    endscript\n}}\n'
    write(Path('/etc/logrotate.d/neural1-ollama'), rotation.encode())
    command(['/usr/sbin/logrotate', '--debug', '/etc/logrotate.d/neural1-ollama'])
    command(['systemctl', 'is-enabled', 'logrotate.timer'])
    write(fstab, new_fstab.encode())
    write(Path('/etc/systemd/system/ollama.service.d/90-neural1-storage.conf'), override.encode())
    guard()
    command(['systemctl', 'daemon-reload'])
    environment = shlex.split(command(['systemctl', 'show', 'ollama.service', '--property=Environment', '--value']))
    required_environment = {f'OLLAMA_MODELS={store}', 'OLLAMA_NUM_PARALLEL=1', 'OLLAMA_MAX_LOADED_MODELS=1', 'OLLAMA_MAX_QUEUE=4', 'OLLAMA_KEEP_ALIVE=60s', 'OLLAMA_NO_CLOUD=1'}
    if not required_environment.issubset(environment):
        raise ValueError('another service override prevents required storage/resource/local-only settings')
    command(['systemctl', 'enable', 'ollama.service'])
    command(['systemctl', 'restart', 'ollama.service'])
    command(['systemctl', 'is-active', 'ollama.service'])
    linger = ensure_linger(args.user, account.pw_uid, backup, guard)
    command(['runuser', '-u', args.user, '--', '/usr/local/bin/neural1', 'console', '--command', 'STATUS'], cwd='/')
    for attempt in range(5):
        try:
            command(['runuser', '-u', args.user, '--', '/usr/local/bin/neural1', 'console', '--command', 'MODEL ' + shlex.quote(args.default_model)], cwd='/')
            break
        except subprocess.CalledProcessError:
            if attempt == 4:
                raise
            time.sleep(1)
    result = {'status': 'INSTALLED_NEEDS_LIVE_ACCEPTANCE', 'pi_model': model, 'revision': revision, 'launch': 'neural1', 'release': str(release), 'backup': str(backup), 'user': args.user, 'linger': linger, 'provider_log': str(provider_log)}
    guard()
    (backup / 'installation.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--ssd', type=Path, required=True)
    parser.add_argument('--uuid', required=True)
    parser.add_argument('--user', required=True)
    parser.add_argument('--ollama-store', type=Path, required=True)
    parser.add_argument('--registry', type=Path, required=True)
    parser.add_argument('--default-model', required=True)
    parser.add_argument('--py65-wheel', type=Path)
    args = parser.parse_args()
    # Verify real target before opening even the installation lock.
    require_pi()
    if os.geteuid() != 0:
        parser.error('root authorization is required on the actual Pi')
    with Path('/run/neural1-install.lock').open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        print(json.dumps(install(args), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
