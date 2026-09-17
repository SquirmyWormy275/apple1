"""Fail-closed Linux storage checks for the installed NEURAL1 application."""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from neural1.storage_commissioning import SSD_MARKER_NAME, SSD_ROLE


@dataclass(frozen=True)
class StorageIdentity:
    root: Path
    uuid: str
    source: str
    free_bytes: int


def _mount(path: Path) -> dict[str, Any]:
    result = subprocess.run(  # noqa: S603 - fixed executable and argument vector; no shell
        ["/usr/bin/findmnt", "--json", "--target", str(path), "--output", "TARGET,SOURCE,UUID,OPTIONS"],
        capture_output=True, text=True, check=True, timeout=10,
    )
    mounts = json.loads(result.stdout).get("filesystems", [])
    if len(mounts) != 1:
        raise ValueError(f"cannot establish unique filesystem identity for {path}")
    return dict(mounts[0])


def verify_storage(
    root: str | Path,
    expected_uuid: str,
    *,
    write_paths: Sequence[str | Path] = (),
    min_free_bytes: int = 512 * 1024 * 1024,
) -> StorageIdentity:
    """Check the actual mount, role, free space, and each resolved write path.

    Call before launching workloads and again before each bulk-write stage.
    The role marker's volume_id must be the filesystem UUID. This check never
    creates directories, so a missing SSD cannot trigger microSD fallback writes.
    """
    if not expected_uuid.strip() or min_free_bytes < 0:
        raise ValueError("expected filesystem UUID and nonnegative reserve required")
    supplied_root = Path(root).absolute()
    resolved_root = supplied_root.resolve(strict=True)
    if supplied_root != resolved_root or not resolved_root.is_dir():
        raise ValueError("SSD root must be a real directory without symlink indirection")
    mount = _mount(resolved_root)
    if Path(str(mount.get("target", ""))) != resolved_root or mount.get("uuid") != expected_uuid:
        raise ValueError("required SSD is not mounted at the configured root with its expected UUID")
    if "rw" not in str(mount.get("options", "")).split(","):
        raise ValueError("required SSD mount is not writable")
    marker = resolved_root / SSD_MARKER_NAME
    if marker.is_symlink():
        raise ValueError("SSD role marker must not be a symlink")
    role = json.loads(marker.read_text(encoding="utf-8"))
    if role.get("role") != SSD_ROLE or role.get("volume_id") != expected_uuid:
        raise ValueError("SSD role/volume marker does not match the expected filesystem UUID")
    for value in write_paths:
        path = Path(value)
        if not path.is_absolute():
            path = resolved_root / path
        resolved = path.resolve(strict=False)
        if not resolved.is_relative_to(resolved_root):
            raise ValueError(f"write path escapes SSD root: {value}")
        ancestor = resolved
        while not ancestor.exists():
            ancestor = ancestor.parent
        actual_mount = _mount(ancestor)
        if actual_mount.get("uuid") != expected_uuid or Path(str(actual_mount.get("target", ""))) != resolved_root:
            raise ValueError(f"write path uses a different filesystem or nested mount: {value}")
    free = shutil.disk_usage(resolved_root).free
    if free < min_free_bytes:
        raise ValueError("insufficient free space on required SSD")
    return StorageIdentity(root=resolved_root, uuid=expected_uuid, source=str(mount["source"]), free_bytes=free)
