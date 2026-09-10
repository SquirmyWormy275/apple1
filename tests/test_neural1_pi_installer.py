"""Pure installer preflight tests; never mutate host configuration or services."""
from pathlib import Path

import pytest

from tools.neural1_install_pi import fstab_content, require_pi


def test_installer_rejects_host_even_with_pi_model_fixture(tmp_path):
    model = tmp_path / 'model'
    model.write_bytes(b'Raspberry Pi 5 Model B Rev 1.0\0')
    with pytest.raises(ValueError, match='host installation refused'):
        require_pi(machine='x86_64', model_path=model)
    assert require_pi(machine='aarch64', model_path=model).startswith('Raspberry Pi 5')
    model.write_bytes(b'Other ARM board\0')
    with pytest.raises(ValueError, match='host installation refused'):
        require_pi(machine='aarch64', model_path=model)


@pytest.mark.parametrize('fail', [False, True])
def test_installer_code_mask_is_explicit_and_callers_mask_restored(tmp_path, monkeypatch, fail):
    import argparse
    import os
    import stat

    from tools import neural1_install_pi as installer

    def build(args):
        directory = tmp_path / 'release'
        directory.mkdir()
        payload = directory / 'code.py'
        payload.write_text('pass\n')
        assert stat.S_IMODE(directory.stat().st_mode) == 0o755
        assert stat.S_IMODE(payload.stat().st_mode) == 0o644
        if fail:
            raise RuntimeError('synthetic installation failure')
        return {'synthetic': True}

    monkeypatch.setattr(installer, '_install', build)
    original = os.umask(0o077)
    try:
        if fail:
            with pytest.raises(RuntimeError, match='synthetic'):
                installer.install(argparse.Namespace())
        else:
            assert installer.install(argparse.Namespace()) == {'synthetic': True}
        assert os.umask(0o077) == 0o077
    finally:
        os.umask(original)


def test_fstab_mount_is_uuid_based_nofail_and_idempotent():
    original = 'proc /proc proc defaults 0 0\n'
    result = fstab_content(original, 'aaaa-bbbb', Path('/mnt/neural1-ssd'))
    assert original in result
    assert 'UUID=aaaa-bbbb' in result
    assert 'nofail,x-systemd.device-timeout=10s' in result
    assert fstab_content(result, 'aaaa-bbbb', Path('/mnt/neural1-ssd')) == result


def test_fstab_existing_conflicts_are_never_replaced():
    with pytest.raises(ValueError, match='conflicting'):
        fstab_content('UUID=cccc-dddd /mnt/neural1-ssd ext4 defaults 0 2\n', 'aaaa-bbbb', Path('/mnt/neural1-ssd'))
    with pytest.raises(ValueError, match='another mountpoint'):
        fstab_content('UUID=aaaa-bbbb /backup ext4 defaults 0 2\n', 'aaaa-bbbb', Path('/mnt/neural1-ssd'))
    with pytest.raises(ValueError, match='unsupported'):
        fstab_content('', 'aaaa-bbbb', Path('/mnt/unsafe path'))


@pytest.mark.parametrize('previous', ['yes', 'no'])
def test_linger_preserves_prior_state_and_enables_only_target(tmp_path, monkeypatch, previous):
    import json

    from tools import neural1_install_pi as installer
    calls = []
    state = previous

    def fake_command(args):
        nonlocal state
        calls.append(args)
        if args[:2] == ['loginctl', 'show-user']:
            assert args[2] == 'runtime-user'
            return state
        if args[:2] == ['loginctl', 'enable-linger']:
            saved = json.loads((tmp_path / 'linger.json').read_text())
            assert saved['previous'] == previous
            assert args[2] == 'runtime-user'
            state = 'yes'
        return 'active'

    monkeypatch.setattr(installer, 'command', fake_command)
    result = installer.ensure_linger('runtime-user', 1001, tmp_path, lambda: None)
    enables = [call for call in calls if call[:2] == ['loginctl', 'enable-linger']]
    assert len(enables) == int(previous == 'no')
    assert result['changed'] == (previous == 'no')
    assert ['systemctl', 'is-active', 'user@1001.service'] in calls
