"""Create a read-only, hash-verified evidence bundle.

The tool never enumerates or opens a serial device.  It copies only explicitly
named evidence files into a zip archive with a SHA-256 manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence


class SupportBundleError(ValueError):
    """The requested evidence cannot form a reproducible bundle."""


def build_support_bundle(
    output: Path,
    evidence_paths: Sequence[Path],
    *,
    tool_version: str = "1",
) -> None:
    """Write ``output`` from explicit existing files, plus ``manifest.json``."""
    if not evidence_paths:
        raise SupportBundleError("at least one explicit evidence file is required")
    output_path = output.resolve()
    resolved_paths = [path.resolve() for path in evidence_paths]
    if output_path in resolved_paths:
        raise SupportBundleError("output archive cannot also be evidence")
    if len(set(resolved_paths)) != len(resolved_paths):
        raise SupportBundleError("each evidence file may be included only once")
    names = [path.name for path in resolved_paths]
    if len(set(names)) != len(names):
        raise SupportBundleError("each evidence file must have a unique basename")

    entries: list[tuple[Path, bytes, dict[str, object]]] = []
    for path in resolved_paths:
        try:
            data = path.read_bytes()
        except OSError as error:
            raise SupportBundleError(f"could not read evidence file: {path}") from error
        entries.append((path, data, {"name": path.name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}))
    manifest = {
        "format": "apple1-support-bundle/v1",
        "created_utc": datetime.now(UTC).isoformat(),
        "tool_version": tool_version,
        "files": [entry for _, _, entry in entries],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, data, _ in entries:
            archive.writestr(f"evidence/{path.name}", data)
        archive.writestr("manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="destination .zip path")
    parser.add_argument("evidence", nargs="+", type=Path, help="explicit evidence files to copy")
    parser.add_argument("--tool-version", default="1")
    args = parser.parse_args()
    build_support_bundle(args.output, args.evidence, tool_version=args.tool_version)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
