from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.archive_manifest import ArchiveInput, build_archive_manifest
from tools.firmware_static_audit import audit_vendor_source
from tools.propeller_preflight import preflight_toolchain
from tools.trace_packet import TracePacketError, validate_trace_packet


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_static_audit_reports_candidate_pins_and_both_keyboard_bus_writers() -> None:
    report = audit_vendor_source(REPO_ROOT / "firmware" / "vendor" / "110REV03")

    assert report["candidate_only"] is True
    assert report["pins"] == {"rx": 31, "tx": 30, "clock": 15}
    assert report["keyboard_bus_writers"] == {"ps2", "serial"}
    assert report["serial_strobe_ms"] == 7


def test_toolchain_preflight_is_compile_only_and_reports_missing_tool() -> None:
    report = preflight_toolchain(REPO_ROOT / "firmware" / "vendor" / "110REV03")

    assert report["action"] == "compile-only-preflight"
    assert report["device_access"] is False
    assert report["tool_present"] is False
    assert report["archived_tool"] == "Propeller Tool version 1.3.2"


def test_archive_manifest_hashes_only_explicit_files(tmp_path: Path) -> None:
    manual = tmp_path / "manual.pdf"
    manual.write_bytes(b"manual")

    manifest = build_archive_manifest([ArchiveInput(category="manual", path=manual)])

    assert manifest["artifacts"][0]["category"] == "manual"
    assert manifest["artifacts"][0]["sha256"]
    with pytest.raises(ValueError):
        build_archive_manifest([ArchiveInput(category="manual", path=tmp_path / "missing.pdf")])


def test_trace_packet_requires_raw_capture_and_safety_evidence() -> None:
    valid = {
        "result": "STOP",
        "physical_changes": "none",
        "analyzer": {"model": "known", "input_rating": "known"},
        "channels": [{"logical_name": "RESn", "safe": True, "physical_point_evidence": "photo"}],
        "raw_capture_files": ["host-open.sal"],
        "display_video": "display.mp4",
        "owner_jsonl": "owner.jsonl",
    }
    validate_trace_packet(valid)
    valid.pop("raw_capture_files")

    with pytest.raises(TracePacketError):
        validate_trace_packet(valid)


def test_trace_packet_allows_an_explicit_resn_unavailable_stop() -> None:
    packet = {
        "result": "INCONCLUSIVE",
        "physical_changes": "none",
        "analyzer": {"model": "known", "input_rating": "known"},
        "channels": [{"logical_name": "DTR", "safe": True, "physical_point_evidence": "photo"}],
        "resn_unavailable_reason": "Revision-specific point is not identified safely.",
        "raw_capture_files": ["host-open.sal"],
        "display_video": "display.mp4",
        "owner_jsonl": "owner.jsonl",
    }

    validate_trace_packet(packet)
