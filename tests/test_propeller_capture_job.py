from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from tools.propeller_capture_job import (
    LiveBackend,
    bounded_command,
    capture_cycle,
    export_capture,
    fingerprint,
    job_lock,
    qualify,
    read_config,
    remote_command,
    run_job,
    service_command,
    validate_owner,
)
from tools.propeller_job_simulation import SCENARIOS, SIM_TIMING, SimulatedBackend
from tools.propeller_remote_owner import execute_once, source_hashes
from tools.serial_owner import TargetIdentity


def configuration(tmp_path: Path) -> dict:
    record = tmp_path / "setup.md"
    record.write_text("TEST FIXTURE: synthetic physical setup attestation, not hardware evidence.\n")
    return {"local_hostname": "strathex-P1", "analyzer_sysfs": "/sys/bus/usb/devices/1-1",
            "sigrok_cli": "/usr/bin/sigrok-cli", "ssh": "/usr/bin/ssh", "pi_ssh_host": "existing-pi",
            "pi_hostname": "intended-pi", "pi_repo": "/home/alex/Apple 1's repo", "pi_python": "/usr/bin/python3",
            "pi_output_root": "/home/alex/propeller-runs",
            "serial_by_id": "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0",
            "serial_by_path": "/dev/serial/by-path/platform-xhci-hcd.0-usbv2-0:2:1.0-port0", "setup_record": str(record)}


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_real_controller_with_synthetic_child_processes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, scenario: str) -> None:
    def forbidden(*args, **kwargs):
        pytest.fail("simulation attempted a live backend")

    monkeypatch.setattr(LiveBackend, "preflight", forbidden)
    root = tmp_path / ("simulation-" + scenario)
    started = time.monotonic()
    report = run_job(root, configuration(tmp_path), SimulatedBackend(scenario), mode="simulation", timing=SIM_TIMING)
    assert time.monotonic() - started < 5
    assert report["evidence_class"] == "TEST_FIXTURE"
    assert report["scientific_result"] == "INCONCLUSIVE_ROOT_CAUSE"
    assert report["display_result"] == "UNOBSERVED"
    assert report["retry_count"] == 0
    assert report["result"] == ("COMPLETE_DIGITAL_QUIET" if scenario == "stable" else "STOP")
    events = [json.loads(line) for line in (root / "events.jsonl").read_text().splitlines()]
    invocations = [event for event in events if event["event"] == "owner_invoked"]
    expected_open = scenario not in {"missing-analyzer", "unstable-idle", "capture-not-ready"}
    assert report["owner_attempted"] is expected_open
    assert len(invocations) == int(expected_open)
    if invocations:
        assert invocations[0]["samples_before_ssh"] >= SIM_TIMING.rate * SIM_TIMING.pre
    if scenario == "stable":
        assert report["owner_confirmed_closed"]
        assert [capture["sample_count"] for capture in report["captures"]] == [150, 1000]
        owner_receipt = next(e for e in events if e["event"] == "owner_receipt")
        capture_done = next(e for e in events if e["event"] == "capture_complete" and e["capture"] == "event")
        assert capture_done["elapsed_seconds"] - owner_receipt["elapsed_seconds"] >= SIM_TIMING.post
    if scenario == "ssh-loss-after-open":
        assert not report["owner_confirmed_closed"]
        remote = json.loads((root / "simulated-pi" / root.name / "result.json").read_text())
        assert [event["event"] for event in remote["owner_records"]] == ["opened", "startup_drained", "closed"]
    if scenario in {"reset-during-open", "partial-capture"}:
        assert 0 < (root / "event.bin").stat().st_size < 1000
    if scenario == "reset-during-open":
        assert report["captures"][-1]["enabled_channels"][2]["low_samples"] >= 1
    for name, digest in json.loads((root / "hashes.json").read_text()).items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest
    with pytest.raises(ValueError, match="attended hardware"):
        qualify(root, display_stable=True)


def test_raw_export_preserves_bit_positions_and_boundary_edges(tmp_path: Path) -> None:
    raw = tmp_path / "original.bin"
    data = b"\x07" * (1024 * 1024) + b"\x03\x07\x00"
    raw.write_bytes(data)
    result = export_capture(raw, 4_000_000)
    assert raw.read_bytes() == data
    assert result["sample_count"] == len(data)
    assert result["enabled_channels"][2]["transitions"] == 3
    assert len(result["enabled_channels"]) == 3


def test_config_and_remote_shell_quoting(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    assert read_config(path) == config
    command = remote_command(config, "session", "run-12345678")
    assert "-oBatchMode=yes" in command and "-oStrictHostKeyChecking=yes" in command
    remote = shlex.split(command[-1])
    assert remote[:4] == ["cd", "--", config["pi_repo"], "&&"]
    assert "--kill-after=2s" in remote and "5s" in remote
    assert "--transmit" not in remote
    config["pi_ssh_host"] = "-oProxyCommand=unexpected"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        read_config(path)
    config["pi_ssh_host"] = "REPLACE_ME"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError, match="placeholders"):
        read_config(path)


def test_unattended_gate_checks_before_preflight(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    backend = SimulatedBackend("missing-analyzer")
    with pytest.raises(ValueError, match="qualification receipt"):
        run_job(tmp_path / "not-started", config, backend, mode="unattended")
    receipt = tmp_path / "receipt.json"
    for changes in ({"fingerprint": "wrong"}, {"display_stable": False},
                    {"qualified_utc": (datetime.now(UTC) - timedelta(days=2)).isoformat()}):
        value = {"fingerprint": fingerprint(config), "display_stable": True, "qualified_utc": datetime.now(UTC).isoformat(), **changes}
        receipt.write_text(json.dumps(value))
        with pytest.raises(ValueError, match="qualification must match"):
            run_job(tmp_path / "not-started", config, backend, mode="unattended", qualification=receipt)
    assert not (tmp_path / "not-started").exists()


def test_qualification_binds_verified_packet_and_setup(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    root = tmp_path / "attended-fixture"
    root.mkdir()
    state = {"mode": "attended", "evidence_class": "LIVE_CAPTURE", "result": "COMPLETE_DIGITAL_QUIET",
             "owner_confirmed_closed": True, "run_id": root.name, "fingerprint": fingerprint(config),
             "environment": {"synthetic_test": True},
             "finished_utc": datetime.now(UTC).isoformat()}
    (root / "result.json").write_text(json.dumps(state))
    (root / "config.json").write_text(json.dumps(config))
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in root.iterdir()}
    (root / "hashes.json").write_text(json.dumps(hashes))
    with pytest.raises(ValueError):
        qualify(root, display_stable=False)
    receipt = qualify(root, display_stable=True)
    assert json.loads(receipt.read_text())["fingerprint"] == fingerprint(config)
    Path(config["setup_record"]).write_text("changed probe routing")
    with pytest.raises(ValueError, match="code/setup changed"):
        qualify(root, display_stable=True)


def test_existing_output_and_concurrent_lock_are_preserved(tmp_path: Path) -> None:
    root = tmp_path / "existing-job"
    root.mkdir()
    sentinel = root / "evidence"
    sentinel.write_text("keep")
    with pytest.raises(FileExistsError):
        run_job(root, configuration(tmp_path), SimulatedBackend("stable"), mode="simulation", timing=SIM_TIMING)
    assert sentinel.read_text() == "keep"
    lock = tmp_path / "job.lock"
    with job_lock(lock), pytest.raises(BlockingIOError), job_lock(lock):
        pytest.fail("concurrent lock acquired")
    with job_lock(lock):
        pass


def test_child_timeout_is_reaped(tmp_path: Path) -> None:
    pidfile = tmp_path / "pid"
    script = "import os,time; from pathlib import Path; Path(" + repr(str(pidfile)) + ").write_text(str(os.getpid())); time.sleep(20)"
    with pytest.raises(RuntimeError, match="timed out"):
        bounded_command([sys.executable, "-c", script], tmp_path / "child", seconds=0.2)
    assert not Path("/proc", pidfile.read_text()).exists()


class Transport:
    def __init__(self):
        self.opens = 0
        self.closed = False

    def configure(self, **settings):
        assert settings["dtr"] is settings["rts"] is False

    def open(self):
        self.opens += 1

    def read_available(self):
        return b""

    def close(self):
        self.closed = True

    def write(self, payload):
        pytest.fail("unexpected transmit")


def test_remote_id_survives_repeat_and_cleanup_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    device = tmp_path / "fake"
    device.touch()
    target = TargetIdentity(device, device)
    transport = Transport()
    result = execute_once(target, tmp_path / "remote", "run-12345678", transport, physical=False, settle_seconds=0)
    assert transport.opens == 1 and transport.closed
    assert validate_owner(result, "run-12345678", physical=False)
    with pytest.raises(FileExistsError):
        execute_once(target, tmp_path / "remote", "run-12345678", transport, physical=False, settle_seconds=0)
    assert transport.opens == 1

    def unplug():
        device.unlink()
        return b""

    other = Transport()
    monkeypatch.setattr(other, "read_available", unplug)
    failed = execute_once(target, tmp_path / "remote", "run-87654321", other, physical=False, settle_seconds=0)
    assert other.closed and failed["error"]
    assert not (tmp_path / "remote" / "fake-owner.lock").exists()


def test_owner_validation_rejects_extra_open_or_transmit() -> None:
    value = {"run_id": "run-12345678", "physical_device_access": False, "error": None,
             "source_hashes": source_hashes(), "retry_count": 0, "owner_records": [{"event": "transmit"}]}
    with pytest.raises(RuntimeError, match="exactly one"):
        validate_owner(value, "run-12345678", physical=False)


def test_event_finishing_before_owner_never_opens(tmp_path: Path) -> None:
    class FastBackend(SimulatedBackend):
        def capture(self, root, name, samples, seconds):
            return [sys.executable, "-c", f"import sys; sys.stdout.buffer.write(b'\\x07' * {samples})"]

        def owner(self, root, run_id):
            pytest.fail("capture had already ended")

    state = {"owner_attempted": False}
    with pytest.raises(RuntimeError, match="post-owner|too far"):
        capture_cycle(tmp_path, "event", FastBackend("stable"), SIM_TIMING, state, lambda *a, **kw: None)
    assert not state["owner_attempted"]


def test_plan_cli_never_launches_backend(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    config["ssh"] = "/not-an-executable/ssh"
    config["sigrok_cli"] = "/not-an-executable/sigrok"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config))
    result = subprocess.run([sys.executable, "-m", "tools.propeller_capture_job", "plan", "--config", str(path),  # noqa: S603 -- test fixture argv
                             "--out", str(tmp_path / "planned-job")], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout)["device_access"] is False
    assert not (tmp_path / "planned-job").exists()


def test_service_launcher_is_bounded_and_preserves_arguments(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("tools.propeller_capture_job.shutil.which", lambda name: "/usr/bin/" + name)
    monkeypatch.setenv("SSH_AUTH_SOCK", "/run/user/1000/agent.sock")
    config = tmp_path / "config with $literal.json"
    qualification = tmp_path / "receipt.json"
    command = service_command(config, tmp_path / "night-123456", "unattended", qualification)
    assert "--property=Restart=no" in command and "--property=RuntimeMaxSec=180" in command
    assert "--what=sleep" in command and "--no-ask-password" in command
    assert "--expand-environment=no" in command
    assert str(config) in command and str(qualification) in command
    assert "--setenv=SSH_AUTH_SOCK=/run/user/1000/agent.sock" in command
    with pytest.raises(ValueError, match="qualification"):
        service_command(config, tmp_path / "night-123456", "unattended", None)


def test_runtime_environment_change_stops_before_capture(tmp_path: Path) -> None:
    config = configuration(tmp_path)
    receipt = tmp_path / "qualification.json"
    receipt.write_text(json.dumps({"fingerprint": fingerprint(config), "display_stable": True,
                                   "qualified_utc": datetime.now(UTC).isoformat(), "environment": {"version": "old"}}))

    class Changed(SimulatedBackend):
        def preflight(self, root, run_id):
            return {"version": "new"}

        def capture(self, *args):
            pytest.fail("must stop before acquisition")

    state = run_job(tmp_path / "changed-runtime", config, Changed("stable"), mode="unattended", qualification=receipt)
    assert state["result"] == "STOP" and not state["owner_attempted"]
    assert "changed since qualification" in state["error"]
