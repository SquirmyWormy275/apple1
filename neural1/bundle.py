"""Portable, hash-verifiable research release bundles."""

from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .core import Neural1Error, sha256_bytes

BUNDLE_SCHEMA = "neural1-release-bundle-0.1"


@dataclass(frozen=True)
class BundleVerification:
    valid: bool
    checked_files: int
    errors: tuple[str, ...]


def export_bundle(source: str | Path, destination: str | Path, *, reproduction_command: str) -> Path:
    source_path, destination_path = Path(source), Path(destination)
    if not source_path.is_dir() or destination_path.exists():
        raise Neural1Error("bundle source must exist and destination must not exist")
    shutil.copytree(source_path, destination_path / "records")
    files: dict[str, dict[str, Any]] = {}
    for path in sorted((destination_path / "records").rglob("*")):
        if path.is_file():
            relative = path.relative_to(destination_path).as_posix()
            payload = path.read_bytes()
            files[relative] = {"sha256": sha256_bytes(payload), "bytes": len(payload)}
    manifest = {"schema_version": BUNDLE_SCHEMA, "files": files, "reproduction_command": reproduction_command}
    (destination_path / "bundle-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return destination_path


def verify_bundle(path: str | Path) -> BundleVerification:
    root = Path(path)
    try:
        manifest = json.loads((root / "bundle-manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return BundleVerification(False, 0, (f"manifest unreadable: {error}",))
    errors: list[str] = []
    if manifest.get("schema_version") != BUNDLE_SCHEMA:
        errors.append("unsupported bundle schema")
    for relative, record in manifest.get("files", {}).items():
        candidate = (root / relative).resolve()
        if root.resolve() not in candidate.parents:
            errors.append(f"unsafe path: {relative}")
        elif not candidate.is_file():
            errors.append(f"missing file: {relative}")
        else:
            payload = candidate.read_bytes()
            if sha256_bytes(payload) != record.get("sha256") or len(payload) != record.get("bytes"):
                errors.append(f"identity mismatch: {relative}")
    expected = set(manifest.get("files", {}))
    actual = {
        item.relative_to(root).as_posix()
        for item in root.rglob("*")
        if item.is_file() and item.name != "bundle-manifest.json"
    }
    for relative in sorted(actual - expected):
        errors.append(f"unlisted file: {relative}")
    return BundleVerification(not errors, len(manifest.get("files", {})), tuple(errors))
