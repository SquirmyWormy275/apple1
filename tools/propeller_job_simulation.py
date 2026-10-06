"""Synthetic subprocesses for the real capture controller; never USB or SSH."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path

from tools.propeller_capture_job import JobStop, Timing, run_job
from tools.propeller_rehearsal import FakeTransport
from tools.propeller_remote_owner import execute_once
from tools.serial_owner import TargetIdentity

SIM_TIMING = Timing(rate=1000, baseline=0.15, duration=1.0, pre=0.10, post=0.10,
                    startup=0.8, stall=0.35, owner=0.35, poll=0.005)
SCENARIOS = ("stable", "missing-analyzer", "unstable-idle", "capture-not-ready", "partial-capture",
             "reset-during-open", "owner-failure", "ssh-loss-after-open", "owner-timeout", "startup-bytes")


class SimulatedBackend:
    physical = False

    def __init__(self, scenario: str) -> None:
        if scenario not in SCENARIOS:
            raise ValueError("unknown scenario")
        self.scenario = scenario

    def preflight(self, root: Path, run_id: str) -> None:
        if self.scenario == "missing-analyzer":
            raise JobStop("simulated missing analyzer")

    def capture(self, root: Path, name: str, samples: int, seconds: float) -> list[str]:
        return [sys.executable, "-m", "tools.propeller_job_simulation", "capture", "--scenario", self.scenario,
                "--phase", name, "--samples", str(samples), "--seconds", str(seconds), "--root", str(root)]

    def owner(self, root: Path, run_id: str) -> list[str]:
        return [sys.executable, "-m", "tools.propeller_job_simulation", "owner", "--scenario", self.scenario,
                "--root", str(root), "--run-id", run_id]


def emit_capture(args) -> int:
    if args.phase == "event" and args.scenario == "capture-not-ready":
        time.sleep(10)
        return 0
    total = args.samples
    start = time.monotonic()
    sent = 0
    reset_emitted = False
    while sent < total:
        time.sleep(0.01)
        end = min(total, int((time.monotonic() - start) / args.seconds * total))
        data = bytearray([7]) * (end - sent)
        pulse = int(total * (0.5 if args.phase == "baseline" else 0.3))
        disturbed = args.phase == "baseline" and args.scenario == "unstable-idle"
        if disturbed and sent <= pulse < end:
            data[pulse - sent] = 3
        owner_log = args.root / "simulated-pi" / args.root.name / "owner.jsonl"
        if (args.phase == "event" and args.scenario == "reset-during-open" and not reset_emitted
                and data and owner_log.is_file() and '"event": "opened"' in owner_log.read_text()):
            data[0] = 3
            reset_emitted = True
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.flush()
        sent = end
        if args.phase == "event" and args.scenario == "partial-capture" and sent >= total * 0.35:
            return 1
    return 0


def emit_owner(args) -> int:
    if args.scenario == "owner-failure":
        return 1
    if args.scenario == "owner-timeout":
        time.sleep(10)
        return 1
    with tempfile.TemporaryDirectory(prefix="propeller-synthetic-") as temporary:
        target_file = Path(temporary) / "fake-device"
        target_file.touch()
        target = TargetIdentity(target_file, target_file)
        transport = FakeTransport()
        if args.scenario == "startup-bytes":
            transport.read_available = lambda: b"x"
        value = execute_once(target, args.root / "simulated-pi", args.run_id, transport,
                             physical=False, settle_seconds=0.3 if args.scenario == "reset-during-open" else 0.01)
    if args.scenario == "ssh-loss-after-open":
        return 255  # Remote evidence remains; no local receipt reaches the controller.
    print(json.dumps(value))
    return 0


def rehearse_all(root: Path) -> int:
    root.mkdir(parents=True, exist_ok=False)
    setup = root / "synthetic-setup.md"
    setup.write_text("TEST FIXTURE: no physical wiring or device access.\n")
    results = []
    for scenario in SCENARIOS:
        value = run_job(root / ("simulation-" + scenario), {"setup_record": str(setup)},
                        SimulatedBackend(scenario), mode="simulation", timing=SIM_TIMING)
        results.append({key: value[key] for key in ("run_id", "result", "owner_attempted", "owner_confirmed_closed")})
        expected = "COMPLETE_DIGITAL_QUIET" if scenario == "stable" else "STOP"
        if value["result"] != expected:
            raise RuntimeError(f"simulation failed: {scenario}: {value.get('error')}")
    (root / "simulation-results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("capture", "owner"))
    parser.add_argument("--scenario", choices=SCENARIOS, required=True)
    parser.add_argument("--phase", choices=("baseline", "event"))
    parser.add_argument("--samples", type=int)
    parser.add_argument("--seconds", type=float)
    parser.add_argument("--root", type=Path)
    parser.add_argument("--run-id")
    args = parser.parse_args()
    return emit_capture(args) if args.command == "capture" else emit_owner(args)


if __name__ == "__main__":
    raise SystemExit(main())
