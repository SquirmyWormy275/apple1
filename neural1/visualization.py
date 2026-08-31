"""Deterministic, printable, Apple-1-sized visual system."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Mapping


PRINTABLE = set(chr(value) for value in range(0x20, 0x7F))


def validate_frame(text: str, *, width: int = 40, height: int | None = None, uppercase: bool = True) -> list[str]:
    errors: list[str] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        if len(line) > width:
            errors.append(f"line {number}: width {len(line)} exceeds {width}")
        if any(character not in PRINTABLE for character in line):
            errors.append(f"line {number}: unsupported character")
        if uppercase and line != line.upper():
            errors.append(f"line {number}: lower-case character")
    if height is not None and len(lines) > height:
        errors.append(f"height {len(lines)} exceeds {height}")
    return errors


def paginate(text: str, *, height: int = 23) -> tuple[str, ...]:
    lines = text.splitlines()
    return tuple("\n".join(lines[index : index + height]) for index in range(0, len(lines), height)) or ("",)


def run_sigil(run_id: str, *, size: int = 7) -> str:
    """Mirror-symmetric visual fingerprint derived solely from run identity."""
    digest = hashlib.sha256(run_id.encode("ascii")).digest()
    half = (size + 1) // 2
    rows = []
    bit = 0
    glyphs = ".+#"
    for _ in range(size):
        left = []
        for _ in range(half):
            value = (digest[(bit // 4) % len(digest)] >> ((bit % 4) * 2)) & 0x03
            left.append(glyphs[value % len(glyphs)])
            bit += 1
        rows.append("".join(left + left[-2::-1] if size % 2 else left + left[::-1]))
    return "\n".join(rows)


def memory_map(payload: bytes, *, start: int = 0x0200, row_bytes: int = 256) -> str:
    lines = []
    for offset in range(0, len(payload), row_bytes):
        chunk = payload[offset : offset + row_bytes]
        cells = 16
        step = max(1, len(chunk) // cells)
        bars = "".join("#" if any(chunk[i : i + step]) else "." for i in range(0, len(chunk), step))[:cells]
        lines.append(f"{start + offset:04X} |{bars:<16}|")
    return "\n".join(lines)


def rom_genome(rom: bytes) -> str:
    if len(rom) != 256:
        raise ValueError("ROM genome requires exactly 256 bytes")
    glyphs = ".ABCJMSX"
    return "\n".join("".join(glyphs[byte >> 5] for byte in rom[row : row + 16]) for row in range(0, 256, 16))


def selfhost_tower(stages: Iterable[str], *, achieved: bool = False) -> str:
    layers = [f"|{stage[:30].center(30)}|" for stage in stages]
    title = "*** TRUE SELF-HOST QUALIFIED ***" if achieved else "SELFHOST/1 BOOTSTRAP"
    return "\n".join([title, "+------------------------------+", *layers, "+------------------------------+"])


def constellation(claim: str, supports: Iterable[str], opposes: Iterable[str]) -> str:
    lines = [f"[{claim}]", " | SUPPORT", *[f" +--[{item}]" for item in supports], " | OPPOSE", *[f" +--[{item}]" for item in opposes]]
    return "\n".join(lines)


def lint_provenance(root: str | Path) -> list[str]:
    import json
    errors: list[str] = []
    required = {"asset_id", "origin", "author", "license_status", "redistribution_status", "changes", "attribution"}
    for path in sorted(Path(root).glob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            errors.append(f"{path}: invalid JSON: {error}")
            continue
        missing = required - record.keys()
        if missing:
            errors.append(f"{path}: missing {sorted(missing)}")
        if record.get("origin") in {"external", "derivative"} and not record.get("attribution"):
            errors.append(f"{path}: external/derivative asset lacks attribution")
        if record.get("redistribution_status") == "DO_NOT_VENDOR" and record.get("published", False):
            errors.append(f"{path}: blocked asset marked published")
    return errors
