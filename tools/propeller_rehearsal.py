"""File-only diagnostic rehearsal using the existing SerialOwner and fake I/O."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

from tools.serial_owner import SerialOwner, TargetIdentity
from tools.sigrok_summary import summarize, write_json

SCENARIOS = ("stable", "missing-resn", "unstable-idle", "capture-not-ready", "capture-failure", "reset-during-open")


class FakeTransport:
    """Has no route to a real serial backend. Transmission is always an error."""

    def __init__(self) -> None:
        self.opens = 0
        self.closes = 0
        self.settings: dict[str, object] = {}

    def configure(self, **settings: object) -> None:
        self.settings = settings

    def open(self) -> None:
        self.opens += 1

    def close(self) -> None:
        self.closes += 1

    def read_available(self) -> bytes:
        return b""

    def write(self, payload: bytes) -> int:
        raise RuntimeError("transmission is outside this rehearsal")


def fixture(path: Path, *, samples: int, pulse_at: int | None = None) -> None:
    """Synthetic 1 kHz data for sequence checks, never hardware evidence."""
    data = bytearray([7]) * samples
    if pulse_at is not None:
        data[pulse_at:pulse_at + 2] = b"\x03\x03"
    with ZipFile(path, "x", ZIP_DEFLATED) as archive:
        archive.writestr("version", "2")
        archive.writestr("metadata", "[global]\nsigrok version=synthetic-rehearsal\n\n[device 1]\n"
                         "capturefile=logic-1\ntotal probes=8\nsamplerate=1 kHz\ntotal analog=0\n"
                         "probe1=TX-O\nprobe2=RX-I\nprobe3=RESn\nunitsize=1\n")
        archive.writestr("logic-1-1", data[:samples // 2])
        archive.writestr("logic-1-2", data[samples // 2:])


def rehearse(root: Path, scenario: str) -> dict[str, object]:
    if scenario not in SCENARIOS:
        raise ValueError("unknown rehearsal scenario")
    # A fresh directory prevents any overwrite of preserved evidence.
    root.mkdir(parents=True, exist_ok=False)
    events = []
    elapsed = 0.0
    transport = FakeTransport()
    result = "PASS_REHEARSAL"

    def event(name: str, **details: object) -> None:
        events.append({"event": name, "simulated_seconds": elapsed, **details})

    def advance(seconds: float) -> None:
        nonlocal elapsed
        elapsed += seconds

    event("preflight", synthetic=True, physical_device_access=False)
    if scenario == "missing-resn":
        result = "STOP_MISSING_RESN"
        event("stop", reason=result)
    else:
        event("passive_capture_started")
        fixture(root / "passive-idle.sr", samples=12000, pulse_at=6000 if scenario == "unstable-idle" else None)
        advance(12)
        baseline = summarize(root / "passive-idle.sr", expected_samples=12000)
        write_json(root / "passive-summary.json", baseline)
        event("passive_capture_saved")
        if any(channel["transitions"] or channel["initial"] != 1 for channel in baseline["enabled_channels"]):
            result = "STOP_UNSTABLE_IDLE"
            event("stop", reason=result)
        elif scenario == "capture-not-ready":
            result = "STOP_CAPTURE_NOT_READY"
            event("stop", reason=result)
        else:
            event("event_capture_ready")
            advance(5)
            # Identity points only at a regular temporary file created here.
            with TemporaryDirectory(prefix="apple1-fake-owner-") as temporary:
                directory = Path(temporary)
                target = directory / "synthetic-device"
                target.touch()
                owner = SerialOwner(TargetIdentity(target, target), directory / "owner.lock", transport,
                                    root / "owner.jsonl", sleep=advance)
                event("simulated_owner_invoked")
                try:
                    owner.acquire_and_open()
                finally:
                    owner.close()
            event("simulated_owner_closed")
            if scenario == "capture-failure":
                # Retain partial data and failure record. Never retry the owner.
                fixture(root / "partial-capture.sr", samples=5200)
                result = "STOP_CAPTURE_FAILURE"
                event("partial_capture_saved")
                event("stop", reason=result)
            else:
                if scenario == "reset-during-open":
                    result = "STOP_SIMULATED_RESET"
                    event("stop", reason=result)
                    samples = 5200
                else:
                    advance(24.8)
                    samples = 30000
                fixture(root / "event-capture.sr", samples=samples,
                        pulse_at=5100 if scenario == "reset-during-open" else None)
                capture = summarize(root / "event-capture.sr", expected_samples=samples)
                write_json(root / "event-summary.json", capture)
                event("event_capture_saved")
                if scenario == "reset-during-open":
                    event("operator_recovery_required", simulated=True)
    report = {
        "scenario": scenario, "result": result, "evidence_class": "TEST_FIXTURE",
        "physical_device_access": False, "physical_serial_opened": False,
        "simulated_owner_opens": transport.opens, "simulated_owner_closes": transport.closes,
        "transmit_calls": 0, "retry_count": 0, "simulated_duration_seconds": elapsed,
        "events": events,
        "note": "SerialOwner wall-clock logs are execution timestamps, not physical capture timing. "
                "1 kHz fixtures and simulated seconds test ordering only; they do not validate USB throughput or SSH.",
    }
    write_json(root / "rehearsal.json", report)
    hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(root.iterdir()) if path.is_file()}
    write_json(root / "hashes.json", hashes)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True, help="new directory; must not already exist")
    parser.add_argument("--scenario", choices=(*SCENARIOS, "all"), default="all")
    args = parser.parse_args()
    if args.scenario == "all":
        args.out.mkdir(parents=True, exist_ok=False)
        results = [rehearse(args.out / scenario, scenario) for scenario in SCENARIOS]
    else:
        results = [rehearse(args.out, args.scenario)]
    print(json.dumps([{key: item[key] for key in ("scenario", "result", "simulated_owner_opens", "physical_device_access")}
                      for item in results], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
