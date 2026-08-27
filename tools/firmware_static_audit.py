"""Read-only structural audit of the vendor Replica 1 Plus source candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Sequence


MAIN_SOURCE = "replica 110REV03.spin"


def audit_vendor_source(root: str | Path) -> dict[str, object]:
    """Report static candidate facts without compiling or accessing a device."""
    source_path = Path(root) / MAIN_SOURCE
    source = source_path.read_text(encoding="latin-1")
    pins = {
        "rx": _constant(source, "RX_Pin"),
        "tx": _constant(source, "TX_Pin"),
        "clock": _constant(source, "CLK0"),
    }
    writers = _keyboard_bus_writers(source)
    serial_section = _pub_section(source, "serial")
    strobe = _single_integer(serial_section, r"PauseMS\((\d+)\)")
    return {
        "candidate_only": True,
        "source": str(source_path),
        "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
        "pins": pins,
        "keyboard_bus_writers": writers,
        "serial_strobe_ms": strobe,
        "device_access": False,
        "compile_performed": False,
    }


def _constant(source: str, name: str) -> int:
    match = re.search(rf"^\s*{re.escape(name)}\s*=\s*(\d+)", source, flags=re.MULTILINE)
    if match is None:
        raise ValueError(f"missing candidate constant: {name}")
    return int(match.group(1))


def _pub_section(source: str, name: str) -> str:
    match = re.search(rf"^PUB\s+{re.escape(name)}\b.*?(?=^PUB\s+|\Z)", source, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE)
    if match is None:
        raise ValueError(f"missing candidate routine: {name}")
    return match.group(0)


def _keyboard_bus_writers(source: str) -> set[str]:
    writers: set[str] = set()
    for name in ("ps2", "serial"):
        section = _pub_section(source, name)
        normalized = section.upper()
        if "OUTA[22..16]" in normalized and "OUTA[23]" in normalized:
            writers.add(name)
    return writers


def _single_integer(source: str, pattern: str) -> int:
    match = re.search(pattern, source)
    if match is None:
        raise ValueError(f"missing expected expression: {pattern}")
    return int(match.group(1))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args(argv)
    print(json.dumps(audit_vendor_source(args.source), indent=2, sort_keys=True, default=sorted))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
