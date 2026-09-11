"""Summarize saved single-device, 8-bit sigrok v2 logic files; no hardware access."""

from __future__ import annotations

import argparse
import configparser
import hashlib
import json
import re
import stat
from collections.abc import Sequence
from decimal import Decimal
from pathlib import Path
from zipfile import ZipFile


def regular_file(path: Path) -> Path:
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError(f"input must be a regular file: {path}")
    return path


def sample_rate(text: str) -> int:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([kMG]?)Hz\s*", text)
    if match is None:
        raise ValueError("unsupported samplerate; expected a positive Hz/kHz/MHz/GHz value")
    value = Decimal(match[1]) * {"": 1, "k": 1000, "M": 1000000, "G": 1000000000}[match[2]]
    if value <= 0 or value != int(value):
        raise ValueError("samplerate must be a positive whole number of Hz")
    return int(value)


def summarize(path: Path, *, expected_samples: int | None = None) -> dict[str, object]:
    """Count enabled bits only, preserving transitions across archive/read chunks.

    Intentionally supports only the format used by the retained fx2lafw files:
    sigrok v2, one digital device, unitsize=1, at most eight probes, no analog.
    Other layouts fail explicitly instead of being guessed.
    """
    regular_file(path)
    if expected_samples is not None and expected_samples <= 0:
        raise ValueError("expected_samples must be positive")
    with path.open("rb") as raw:
        digest = hashlib.file_digest(raw, "sha256").hexdigest()
    with ZipFile(path) as archive:
        names = archive.namelist()
        if len(set(names)) != len(names):
            raise ValueError("duplicate archive member")
        for name in ("version", "metadata"):
            if archive.getinfo(name).file_size > 65536:
                raise ValueError("oversized session metadata")
        if archive.read("version").strip() != b"2":
            raise ValueError("only sigrok session format v2 is supported")
        config = configparser.ConfigParser(interpolation=None)
        config.read_string(archive.read("metadata").decode("utf-8"))
        if set(config.sections()) != {"global", "device 1"}:
            raise ValueError("expected one device and a global metadata section")
        device = config["device 1"]
        total_probes = device.getint("total probes")
        if device.getint("unitsize") != 1 or not 1 <= total_probes <= 8 or device.getint("total analog", 0) != 0:
            raise ValueError("only 1-byte digital samples with 1-8 probes are supported")
        if device["capturefile"] != "logic-1":
            raise ValueError("unsupported capturefile")
        rate = sample_rate(device["samplerate"])
        channels = {}
        for key, label in device.items():
            match = re.fullmatch(r"probe(\d+)", key)
            if match:
                number = int(match[1])
                if not 1 <= number <= total_probes or not label.strip():
                    raise ValueError("invalid enabled probe metadata")
                channels[number - 1] = label
        if not channels or len(set(channels.values())) != len(channels):
            raise ValueError("enabled probes must have distinct nonempty labels")
        numbered = []
        for name in names:
            match = re.fullmatch(r"logic-1-([1-9]\d*)", name)
            if match:
                numbered.append((int(match[1]), name))
        numbered.sort()
        if "logic-1" in names:
            if numbered:
                raise ValueError("mixed legacy and chunked logic data")
            chunks = ["logic-1"]
        else:
            if not numbered or [n for n, _ in numbered] != list(range(1, len(numbered) + 1)):
                raise ValueError("missing or noncontiguous data chunks")
            chunks = [name for _, name in numbered]
        if set(names) != {"version", "metadata", *chunks}:
            raise ValueError("unexpected archive members; layout not supported")
        sizes = [archive.getinfo(name).file_size for name in chunks]
        count = sum(sizes)
        if min(sizes) <= 0 or count > 512 * 1024 * 1024:
            raise ValueError("empty chunk or capture exceeds 512 MiB analysis bound")
        if expected_samples is not None and count != expected_samples:
            raise ValueError(f"sample count mismatch: {count} != {expected_samples}")
        stats = {bit: {"bit": bit, "label": label, "high_samples": 0, "low_samples": 0,
                       "rising_edges": 0, "falling_edges": 0, "initial": None, "final": None}
                 for bit, label in sorted(channels.items())}
        tables = {bit: bytes((value >> bit) & 1 for value in range(256)) for bit in channels}
        read_count = 0
        for chunk in chunks:
            with archive.open(chunk) as stream:
                while data := stream.read(1024 * 1024):
                    read_count += len(data)
                    for bit, item in stats.items():
                        levels = data.translate(tables[bit])
                        high = levels.count(b"\x01")
                        item["high_samples"] += high
                        item["low_samples"] += len(levels) - high
                        item["rising_edges"] += levels.count(b"\x00\x01")
                        item["falling_edges"] += levels.count(b"\x01\x00")
                        if item["initial"] is None:
                            item["initial"] = levels[0]
                        elif item["final"] != levels[0]:
                            item["rising_edges" if levels[0] else "falling_edges"] += 1
                        item["final"] = levels[-1]
        if read_count != count:
            raise ValueError("decoded sample count disagrees with archive lengths")
        for item in stats.values():
            item["transitions"] = item["rising_edges"] + item["falling_edges"]
        return {
            "format": "sigrok-v2-single-device-unitsize-1", "file": path.name,
            "sha256": digest, "sample_rate_hz": rate, "sample_count": count,
            "duration_seconds": count / rate, "archive_chunks": len(chunks),
            "total_probes": total_probes, "enabled_channels": list(stats.values()),
            "device_access": False,
            "limits": ["Only enabled bits named by probeN metadata are interpreted.",
                       "Archive consistency alone does not prove absence of upstream dropped samples.",
                       "Digital levels do not measure supply amplitude or establish physical probe placement."],
        }


def write_json(path: Path, value: object) -> None:
    """Create a new regular output; never overwrite an existing file/device."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as output:
        json.dump(value, output, indent=2, sort_keys=True)
        output.write("\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture", type=Path)
    parser.add_argument("--expected-samples", type=int)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    result = summarize(args.capture, expected_samples=args.expected_samples)
    if args.out:
        write_json(args.out, result)
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
