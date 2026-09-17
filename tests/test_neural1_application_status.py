"""Synthetic process-table controls for truthful console liveness display."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

import neural1.application as application
from neural1.application import Application, ApplicationConfig, _verified_worker_running, preset
from neural1.registry import ModelRegistry, RegisteredModel


def fixture(tmp_path: Path, monkeypatch):
    ssd = tmp_path / 'ssd'
    registry = ModelRegistry()
    registry.add(RegisteredModel('fixture', 'synthetic', 'test', 'fake', 'fake', '0', 'NONE', 4096, 'fixture', 'TEST', {}))
    registry_path = tmp_path / 'registry.json'
    registry.save(registry_path)
    config = ApplicationConfig(tmp_path / 'config.json', ssd, 'synthetic', registry_path, tmp_path, 'fixture')
    monkeypatch.setattr(ApplicationConfig, 'storage_check', lambda self: None)
    monkeypatch.setattr(ApplicationConfig, 'check', lambda self: {'synthetic': True})
    app = Application(config)
    spec = preset('4k-mind', 'fixture', seed=17)
    root = config.output / 'campaigns' / spec.campaign_id
    spec.save(root / 'spec.json')
    proc = tmp_path / 'proc'
    pid = proc / '123'
    pid.mkdir(parents=True)
    # Field 3 begins after comm; starttime is field22.
    fields = ['S'] + ['0'] * 18 + ['456'] + ['0'] * 10
    (pid / 'stat').write_text('123 (python with spaces) ' + ' '.join(fields))
    arguments = ['/python', '-m', 'neural1.application', '--config', str(config.path), '--worker', root.name, '--launch-id', 'current-launch']
    (pid / 'cmdline').write_bytes(b'\0'.join(arg.encode() for arg in arguments) + b'\0')
    (root / 'worker.json').write_text(json.dumps({'pid': 123, 'process_start': '456', 'status': 'RUNNING', 'launch_id': 'current-launch'}))
    monkeypatch.setattr(application, '_verified_worker_running', lambda root, config: _verified_worker_running(root, config, proc_root=proc))
    return app, root, pid, proc


@pytest.mark.parametrize('prior_status', [None, 'INTERRUPTED', 'COMPLETED'])
def test_verified_worker_takes_precedence_over_stale_summary(tmp_path, monkeypatch, prior_status):
    app, root, _, _ = fixture(tmp_path, monkeypatch)
    if prior_status:
        (root / 'summary.json').write_text(json.dumps({'status': prior_status}))
    original = (root / 'summary.json').read_bytes() if prior_status else None
    row = app.browse()[0]
    assert row['status'] == 'RUNNING' and row['worker_active']
    assert row['recorded_status'] == (prior_status or 'INTERRUPTED_OR_STARTING')
    status = app.command('STATUS')
    assert status['worker_active'] and status['runs'][0]['status'] == 'RUNNING'
    # Display never overwrites previous science/lifecycle evidence.
    assert ((root / 'summary.json').read_bytes() if prior_status else None) == original


@pytest.mark.parametrize('failure', ['reused-pid', 'other-config', 'other-campaign', 'other-launch', 'other-module', 'zombie', 'finished', 'missing', 'malformed'])
def test_stale_or_unrelated_process_never_reports_running(tmp_path, monkeypatch, failure):
    app, root, pid, _ = fixture(tmp_path, monkeypatch)
    (root / 'summary.json').write_text('{"status":"INTERRUPTED"}')
    if failure == 'reused-pid':
        (pid / 'stat').write_text((pid / 'stat').read_text().replace('456', '789'))
    elif failure in ('other-config', 'other-campaign', 'other-launch', 'other-module'):
        old = {'other-config': str(app.config.path).encode(), 'other-campaign': root.name.encode(), 'other-launch': b'current-launch', 'other-module': b'neural1.application'}[failure]
        (pid / 'cmdline').write_bytes((pid / 'cmdline').read_bytes().replace(old, b'unrelated'))
    elif failure == 'zombie':
        (pid / 'stat').write_text((pid / 'stat').read_text().replace(') S ', ') Z '))
    elif failure == 'finished':
        (root / 'worker.json').write_text((root / 'worker.json').read_text().replace('RUNNING', 'FINISHED'))
    elif failure == 'missing':
        (pid / 'stat').unlink()
    else:
        (root / 'worker.json').write_text('{partial')
    # A held global lock does not identify which campaign/process is alive.
    monkeypatch.setattr(app, 'running', lambda: True)
    status = app.command('STATUS')
    assert status['worker_lock_held'] and not status['worker_active']
    assert status['runs'][0]['status'] == 'INTERRUPTED'
    assert not status['runs'][0]['worker_active']


def test_running_summary_alone_is_not_process_evidence(tmp_path, monkeypatch):
    app, root, pid, _ = fixture(tmp_path, monkeypatch)
    (root / 'summary.json').write_text('{"status":"RUNNING"}')
    (pid / 'stat').unlink()
    row = app.browse()[0]
    assert row['status'] == 'INTERRUPTED'
    assert row['recorded_status'] == 'RUNNING'
    assert not row['worker_active']
