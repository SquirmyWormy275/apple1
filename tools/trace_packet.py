"""Validate a logic-trace evidence packet without talking to hardware."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Sequence


class TracePacketError(ValueError):
    """The packet cannot support a safe electrical conclusion."""


def validate_trace_packet(packet: Mapping[str, object]) -> None:
    required = {"result", "physical_changes", "analyzer", "channels", "raw_capture_files", "display_video", "owner_jsonl"}
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
    if not isinstance(packet["raw_capture_files"], list) or not packet["raw_capture_files"]:
        raise TracePacketError("at least one native raw capture file is required")
    if not isinstance(packet["display_video"], str) or not packet["display_video"]:
        raise TracePacketError("display_video is required")
    if not isinstance(packet["owner_jsonl"], str) or not packet["owner_jsonl"]:
        raise TracePacketError("owner_jsonl is required")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path)
    args = parser.parse_args(argv)
    validate_trace_packet(json.loads(args.packet.read_text(encoding="utf-8")))
    print("valid trace packet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
