"""Build a hash manifest from explicitly selected collection artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class ArchiveInput:
    category: str
    path: Path


def build_archive_manifest(artifacts: Sequence[ArchiveInput]) -> dict[str, object]:
    if not artifacts:
        raise ValueError("at least one explicit artifact is required")
    entries = []
    for artifact in artifacts:
        if not artifact.category.strip():
            raise ValueError("artifact category must be non-empty")
        if not artifact.path.is_file():
            raise ValueError(f"artifact does not exist: {artifact.path}")
        content = artifact.path.read_bytes()
        entries.append(
            {
                "category": artifact.category,
                "filename": artifact.path.name,
                "bytes": len(content),
                "sha256": hashlib.sha256(content).hexdigest(),
            }
        )
    return {"format": "apple1-archive-manifest/v1", "generated_utc": datetime.now(UTC).isoformat(), "artifacts": entries}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("artifacts", nargs="+", type=Path)
    parser.add_argument("--category", required=True)
    args = parser.parse_args(argv)
    manifest = build_archive_manifest([ArchiveInput(args.category, path) for path in args.artifacts])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
