"""Validate a logic-trace evidence packet without talking to hardware."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from pathlib import Path


class TracePacketError(ValueError):
    """The packet cannot support a safe electrical conclusion."""


_SHA256 = re.compile(r"[0-9a-f]{64}")
_PLACEHOLDERS = {"unavailable", "missing", "none", "n/a", "na"}


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TracePacketError(f"{label} must be a non-empty string")
    return value.strip()


def _relative_path(value: object, label: str) -> Path:
    path = Path(_text(value, label))
    if path.is_absolute() or ".." in path.parts:
        raise TracePacketError(f"{label} must be a safe relative path")
    return path


def _local_file(packet_dir: Path | None, value: object, label: str) -> Path:
    path = _relative_path(value, label)
    if packet_dir is not None:
        resolved = (packet_dir / path).resolve()
        try:
            resolved.relative_to(packet_dir.resolve())
        except ValueError as exc:
            raise TracePacketError(f"{label} escapes the packet directory") from exc
        if not resolved.is_file() or resolved.stat().st_size == 0:
            raise TracePacketError(f"{label} does not name a non-empty local file: {path}")
        return resolved
    return path


def _valid_hash(value: object, label: str) -> str:
    digest = _text(value, label)
    if _SHA256.fullmatch(digest) is None:
        raise TracePacketError(f"{label} must be a lowercase SHA-256 digest")
    return digest


def _validate_display_evidence(evidence: object, packet_status: object, packet_dir: Path | None) -> None:
    if not isinstance(evidence, Mapping):
        raise TracePacketError("display_evidence must be an object")
    availability = evidence.get("availability")
    artifacts = evidence.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        raise TracePacketError("display_evidence.artifacts must be a non-empty list")
    if availability == "external_hash_identified":
        if packet_status != "COMPLETE_WITH_EXTERNAL_MEDIA":
            raise TracePacketError("external display evidence requires COMPLETE_WITH_EXTERNAL_MEDIA")
        _local_file(packet_dir, evidence.get("record_file"), "display_evidence.record_file")
        if "external_manifest" in evidence:
            _local_file(packet_dir, evidence.get("external_manifest"), "display_evidence.external_manifest")
        reason = _text(evidence.get("local_copy_absent_reason"), "display_evidence.local_copy_absent_reason")
        if reason.casefold() in _PLACEHOLDERS:
            raise TracePacketError("external display evidence requires a substantive local-copy reason")
        if evidence.get("codex_inspected_bytes") is not False:
            raise TracePacketError("external evidence must state that Codex did not inspect unavailable bytes")
        for index, artifact in enumerate(artifacts):
            label = f"display_evidence.artifacts[{index}]"
            if not isinstance(artifact, Mapping):
                raise TracePacketError(f"{label} must be an object")
            _text(artifact.get("filename"), f"{label}.filename")
            _valid_hash(artifact.get("sha256"), f"{label}.sha256")
            custody = artifact.get("custody")
            if not isinstance(custody, list) or not custody or not all(isinstance(item, str) and item.strip() for item in custody):
                raise TracePacketError(f"{label}.custody must identify at least one location")
            if artifact.get("local_repository_copy") is not False:
                raise TracePacketError(f"{label}.local_repository_copy must be false")
            inspection = artifact.get("inspection")
            if not isinstance(inspection, Mapping) or inspection.get("performed") is not True:
                raise TracePacketError(f"{label}.inspection must record a performed inspection")
            for field in ("inspector", "method", "summary"):
                _text(inspection.get(field), f"{label}.inspection.{field}")
    elif availability == "local":
        if packet_status != "COMPLETE_LOCAL_MEDIA":
            raise TracePacketError("local display evidence requires COMPLETE_LOCAL_MEDIA")
        for index, artifact in enumerate(artifacts):
            label = f"display_evidence.artifacts[{index}]"
            if not isinstance(artifact, Mapping):
                raise TracePacketError(f"{label} must be an object")
            media = _local_file(packet_dir, artifact.get("path"), f"{label}.path")
            expected = _valid_hash(artifact.get("sha256"), f"{label}.sha256")
            if packet_dir is not None and hashlib.sha256(media.read_bytes()).hexdigest() != expected:
                raise TracePacketError(f"{label} SHA-256 does not match the local file")
    else:
        raise TracePacketError("display_evidence.availability must be local or external_hash_identified")


def _validate_sha256sums(packet_dir: Path) -> None:
    manifest = packet_dir / "SHA256SUMS"
    if not manifest.exists():
        return
    listed: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise TracePacketError("SHA256SUMS contains a malformed line")
        digest, raw_path = parts
        _valid_hash(digest, "SHA256SUMS digest")
        relative = _relative_path(raw_path.removeprefix("*"), "SHA256SUMS path")
        listed[relative.as_posix().removeprefix("./")] = digest
    expected = {
        path.relative_to(packet_dir).as_posix()
        for path in packet_dir.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if set(listed) != expected:
        raise TracePacketError("SHA256SUMS must cover every local regular file except itself")
    for relative, digest in listed.items():
        if hashlib.sha256((packet_dir / relative).read_bytes()).hexdigest() != digest:
            raise TracePacketError(f"SHA256SUMS mismatch for {relative}")


def validate_trace_packet(packet: Mapping[str, object], *, packet_dir: Path | None = None) -> None:
    required = {"result", "physical_changes", "analyzer", "channels", "raw_capture_files", "owner_jsonl"}
    missing = required.difference(packet)
    if missing:
        raise TracePacketError(f"missing trace evidence: {', '.join(sorted(missing))}")
    if packet["result"] not in {"PASS", "STOP", "INCONCLUSIVE"}:
        raise TracePacketError("result must be PASS, STOP, or INCONCLUSIVE")
    if packet["physical_changes"] != "none":
        raise TracePacketError("this packet validator is limited to no-change characterization")
    analyzer = packet["analyzer"]
    if not isinstance(analyzer, Mapping) or not analyzer.get("model") or not analyzer.get("input_rating"):
        raise TracePacketError("analyzer must record model and input_rating")
    channels = packet["channels"]
    if not isinstance(channels, list) or not channels:
        raise TracePacketError("at least one channel record is required")
    reset_channels = [channel for channel in channels if isinstance(channel, Mapping) and channel.get("logical_name") == "RESn"]
    if reset_channels:
        if not any(channel.get("safe") and channel.get("physical_point_evidence") for channel in reset_channels):
            raise TracePacketError("a recorded RESn channel must be safe and physically evidenced")
    elif not isinstance(packet.get("resn_unavailable_reason"), str) or not packet["resn_unavailable_reason"].strip():
        raise TracePacketError("record a safe RESn channel or resn_unavailable_reason")
    raw_files = packet["raw_capture_files"]
    if not isinstance(raw_files, list) or not raw_files:
        raise TracePacketError("at least one native raw capture file is required")
    for index, raw_file in enumerate(raw_files):
        _local_file(packet_dir, raw_file, f"raw_capture_files[{index}]")
    _local_file(packet_dir, packet["owner_jsonl"], "owner_jsonl")
    if "worksheet" in packet:
        _local_file(packet_dir, packet["worksheet"], "worksheet")
    if "display_evidence" in packet:
        if packet.get("evidence_format_version") != 2:
            raise TracePacketError("structured display_evidence requires evidence_format_version 2")
        if packet.get("execution_status") not in {"COMPLETE", "NOT_EXECUTED", "ABORTED"}:
            raise TracePacketError("invalid execution_status")
        packet_status = packet.get("packet_status")
        if packet_status not in {"COMPLETE_LOCAL_MEDIA", "COMPLETE_WITH_EXTERNAL_MEDIA", "INCOMPLETE"}:
            raise TracePacketError("invalid packet_status")
        portability = packet.get("portability_status")
        if packet_status == "COMPLETE_LOCAL_MEDIA" and portability != "SELF_CONTAINED":
            raise TracePacketError("local media packets must be SELF_CONTAINED")
        if packet_status == "COMPLETE_WITH_EXTERNAL_MEDIA" and portability != "NOT_SELF_CONTAINED_MEDIA":
            raise TracePacketError("external media packets must be NOT_SELF_CONTAINED_MEDIA")
        _validate_display_evidence(packet["display_evidence"], packet_status, packet_dir)
        probe = packet.get("probe_point_evidence")
        if not isinstance(probe, Mapping):
            raise TracePacketError("probe_point_evidence is required for version 2 packets")
        _local_file(packet_dir, probe.get("record_file"), "probe_point_evidence.record_file")
    else:
        legacy = _text(packet.get("display_video"), "display_video")
        if legacy.casefold() in _PLACEHOLDERS or any(legacy.casefold().startswith(f"{item}:") for item in _PLACEHOLDERS):
            raise TracePacketError("display_video cannot be a placeholder")
        _local_file(packet_dir, legacy, "display_video")
    if packet_dir is not None:
        _validate_sha256sums(packet_dir)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args(argv)
    packet_path = args.packet.resolve()
    validate_trace_packet(json.loads(packet_path.read_text(encoding="utf-8")), packet_dir=packet_path.parent)
    print("valid trace packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
