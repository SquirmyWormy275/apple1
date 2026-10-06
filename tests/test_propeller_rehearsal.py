from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.propeller_rehearsal import rehearse
from tools.serial_owner import PySerialTransport


@pytest.mark.parametrize(("scenario", "opens", "result"), [
    ("stable", 1, "PASS_REHEARSAL"),
    ("missing-resn", 0, "STOP_MISSING_RESN"),
    ("unstable-idle", 0, "STOP_UNSTABLE_IDLE"),
    ("capture-not-ready", 0, "STOP_CAPTURE_NOT_READY"),
    ("capture-failure", 1, "STOP_CAPTURE_FAILURE"),
    ("reset-during-open", 1, "STOP_SIMULATED_RESET"),
])
def test_sequence_never_uses_real_transport_or_retries(tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
                                                     scenario: str, opens: int, result: str) -> None:
    def forbidden(*args: object, **kwargs: object) -> None:
        pytest.fail("rehearsal attempted real serial transport")

    monkeypatch.setattr(PySerialTransport, "__init__", forbidden)
    root = tmp_path / scenario
    report = rehearse(root, scenario)
    assert report["result"] == result
    assert report["simulated_owner_opens"] == report["simulated_owner_closes"] == opens
    assert report["physical_device_access"] is False
    assert report["retry_count"] == report["transmit_calls"] == 0
    events = report["events"]
    assert [e["simulated_seconds"] for e in events] == sorted(e["simulated_seconds"] for e in events)
    assert report["simulated_duration_seconds"] <= 42
    if opens:
        names = [e["event"] for e in events]
        ready = events[names.index("event_capture_ready")]["simulated_seconds"]
        invoked = events[names.index("simulated_owner_invoked")]["simulated_seconds"]
        assert invoked - ready >= 5
        owner = [json.loads(line) for line in (root / "owner.jsonl").read_text().splitlines()]
        assert [e["event"] for e in owner] == ["opened", "startup_drained", "closed"]
        assert owner[0]["control_policy"] == {"dtr": False, "rts": False}
        assert owner[1]["payload_hex"] == ""
    else:
        assert not (root / "owner.jsonl").exists()
    if scenario == "capture-failure":
        assert (root / "partial-capture.sr").is_file()
    if scenario == "reset-during-open":
        channel = json.loads((root / "event-summary.json").read_text())["enabled_channels"][2]
        assert channel["falling_edges"] == channel["rising_edges"] == 1
    for name, digest in json.loads((root / "hashes.json").read_text()).items():
        assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest


def test_existing_output_is_preserved(tmp_path: Path) -> None:
    root = tmp_path / "existing"
    root.mkdir()
    sentinel = root / "evidence"
    sentinel.write_text("do not overwrite")
    with pytest.raises(FileExistsError):
        rehearse(root, "stable")
    assert sentinel.read_text() == "do not overwrite"
