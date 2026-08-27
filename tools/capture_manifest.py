"""Validate hardware-capture metadata before it is treated as evidence."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from pathlib import Path


class ManifestValidationError(ValueError):
    """A capture lacks the minimum information needed to reproduce it."""


REQUIRED_FIELDS = frozenset(
    {
        "target_identity",
        "timestamp_utc",
        "board_revision",
        "power_source",
        "usb_topology",
        "result",
    }
)
VALID_RESULTS = frozenset({"PASS", "STOP", "INCONCLUSIVE"})


def validate_manifest(manifest: Mapping[str, object]) -> None:
    missing = REQUIRED_FIELDS.difference(manifest)
    if missing:
        raise ManifestValidationError(f"missing required evidence: {', '.join(sorted(missing))}")

    identity = manifest["target_identity"]
    if not isinstance(identity, Mapping) or not identity.get("by_id") or not identity.get("by_path"):
        raise ManifestValidationError("target_identity must contain non-empty by_id and by_path")
    if manifest["result"] not in VALID_RESULTS:
        raise ManifestValidationError(f"result must be one of {', '.join(sorted(VALID_RESULTS))}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    validate_manifest(json.loads(args.manifest.read_text(encoding="utf-8")))
    print("valid capture manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
