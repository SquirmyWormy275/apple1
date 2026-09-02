from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tools.trace_packet import TracePacketError, validate_trace_packet


def _base(tmp_path: Path) -> dict[str, object]:
    for name in ("trace.sr", "owner.jsonl", "worksheet.md", "probe-point-record.md"):
        (tmp_path / name).write_bytes(b"evidence")
    return {
        "evidence_format_version": 2,
        "execution_status": "COMPLETE",
        "result": "INCONCLUSIVE",
        "packet_status": "COMPLETE_WITH_EXTERNAL_MEDIA",
        "portability_status": "NOT_SELF_CONTAINED_MEDIA",
        "physical_changes": "none",
        "analyzer": {"model": "known", "input_rating": "known"},
        "channels": [{"logical_name": "TX-O", "safe": True, "physical_point_evidence": "silkscreen"}],
        "resn_unavailable_reason": "No evidenced safe point was available.",
        "raw_capture_files": ["trace.sr"],
        "owner_jsonl": "owner.jsonl",
        "worksheet": "worksheet.md",
        "probe_point_evidence": {"record_file": "probe-point-record.md"},
    }


def _external(tmp_path: Path) -> dict[str, object]:
    packet = _base(tmp_path)
    (tmp_path / "display-video-record.md").write_bytes(b"custody record")
    packet["display_evidence"] = {
        "availability": "external_hash_identified",
        "record_file": "display-video-record.md",
        "local_copy_absent_reason": "The operator retains the media outside this repository.",
        "codex_inspected_bytes": False,
        "artifacts": [{
            "filename": "display.mov",
            "sha256": "a" * 64,
            "custody": ["operator_phone"],
            "local_repository_copy": False,
            "inspection": {"performed": True, "inspector": "prior session", "method": "frames", "summary": "Display changed."},
        }],
    }
    return packet


def test_valid_external_media_packet_passes(tmp_path: Path) -> None:
    validate_trace_packet(_external(tmp_path), packet_dir=tmp_path)


def test_valid_local_media_packet_passes(tmp_path: Path) -> None:
    packet = _base(tmp_path)
    media = tmp_path / "display.mov"
    media.write_bytes(b"video")
    packet.update(packet_status="COMPLETE_LOCAL_MEDIA", portability_status="SELF_CONTAINED")
    packet["display_evidence"] = {
        "availability": "local",
        "artifacts": [{"path": "display.mov", "sha256": hashlib.sha256(b"video").hexdigest()}],
    }
    validate_trace_packet(packet, packet_dir=tmp_path)


@pytest.mark.parametrize("placeholder", ["UNAVAILABLE", "MISSING"])
def test_legacy_placeholder_fails(placeholder: str) -> None:
    packet = {
        "result": "STOP", "physical_changes": "none",
        "analyzer": {"model": "known", "input_rating": "known"},
        "channels": [{"logical_name": "RESn", "safe": True, "physical_point_evidence": "photo"}],
        "raw_capture_files": ["trace.sr"], "display_video": placeholder, "owner_jsonl": "owner.jsonl",
    }
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet)


def test_missing_and_empty_local_media_fail(tmp_path: Path) -> None:
    packet = _base(tmp_path)
    packet.update(packet_status="COMPLETE_LOCAL_MEDIA", portability_status="SELF_CONTAINED")
    packet["display_evidence"] = {"availability": "local", "artifacts": [{"path": "absent.mov", "sha256": "a" * 64}]}
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)
    (tmp_path / "absent.mov").touch()
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


def test_local_media_hash_mismatch_fails(tmp_path: Path) -> None:
    packet = _base(tmp_path)
    (tmp_path / "display.mov").write_bytes(b"video")
    packet.update(packet_status="COMPLETE_LOCAL_MEDIA", portability_status="SELF_CONTAINED")
    packet["display_evidence"] = {"availability": "local", "artifacts": [{"path": "display.mov", "sha256": "a" * 64}]}
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


@pytest.mark.parametrize("mutation", ["missing_hash", "bad_hash", "missing_custody", "missing_summary"])
def test_external_artifact_required_fields(mutation: str, tmp_path: Path) -> None:
    packet = _external(tmp_path)
    artifact = packet["display_evidence"]["artifacts"][0]  # type: ignore[index]
    if mutation == "missing_hash":
        artifact.pop("sha256")
    elif mutation == "bad_hash":
        artifact["sha256"] = "ABC"
    elif mutation == "missing_custody":
        artifact.pop("custody")
    else:
        artifact["inspection"].pop("summary")
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


def test_external_mode_requires_local_record(tmp_path: Path) -> None:
    packet = _external(tmp_path)
    (tmp_path / "display-video-record.md").unlink()
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


def test_complete_external_mode_requires_external_artifacts(tmp_path: Path) -> None:
    packet = _external(tmp_path)
    packet["display_evidence"]["artifacts"] = []  # type: ignore[index]
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


@pytest.mark.parametrize(
    ("availability", "packet_status"),
    [("external_hash_identified", "COMPLETE_LOCAL_MEDIA"), ("local", "COMPLETE_WITH_EXTERNAL_MEDIA")],
)
def test_packet_status_must_match_availability(availability: str, packet_status: str, tmp_path: Path) -> None:
    packet = _external(tmp_path)
    packet["packet_status"] = packet_status
    packet["display_evidence"]["availability"] = availability  # type: ignore[index]
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)


def test_resn_unavailable_and_inconclusive_complete_packet_passes(tmp_path: Path) -> None:
    packet = _external(tmp_path)
    assert packet["result"] == "INCONCLUSIVE"
    validate_trace_packet(packet, packet_dir=tmp_path)


def test_path_traversal_fails(tmp_path: Path) -> None:
    packet = _external(tmp_path)
    packet["raw_capture_files"] = ["../trace.sr"]
    with pytest.raises(TracePacketError):
        validate_trace_packet(packet, packet_dir=tmp_path)
