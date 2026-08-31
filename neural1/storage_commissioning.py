"""Read-only Pi image inspection and verified NEURAL1 storage migration tools."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections.abc import Iterator, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SSD_MARKER_NAME = ".neural1-ssd.json"
TEMP_MARKER_NAME = ".neural1-temporary.json"
SSD_ROLE = "NEURAL1_DEDICATED_SSD"
TEMP_ROLE = "NEURAL1_TEMPORARY_STORAGE"
DELETE_CONFIRMATION = "DELETE_VERIFIED_TEMPORARY_NEURAL1_COPY"
MANIFEST_VERSION = 1
_HASH_CHUNK = 8 * 1024 * 1024


@dataclass(frozen=True)
class PartitionEntry:
    index: int
    bootable: bool
    type_code: int
    start_lba: int
    sectors: int
    byte_offset: int
    byte_length: int


@dataclass(frozen=True)
class ImageInspection:
    path: str
    size_bytes: int
    mbr_signature_valid: bool
    disk_signature_hex: str
    partitions: tuple[PartitionEntry, ...]
    sha256: str | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(_HASH_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_image(path: str | Path, *, include_sha256: bool = False) -> ImageInspection:
    image = Path(path)
    size = image.stat().st_size
    if size < 512:
        raise ValueError("raw image is smaller than one 512-byte sector")
    with image.open("rb") as stream:
        sector = stream.read(512)
    disk_signature = int.from_bytes(sector[440:444], "little")
    partitions: list[PartitionEntry] = []
    for index in range(4):
        offset = 446 + index * 16
        entry = sector[offset : offset + 16]
        type_code = entry[4]
        start_lba = int.from_bytes(entry[8:12], "little")
        sectors = int.from_bytes(entry[12:16], "little")
        if type_code == 0 and sectors == 0:
            continue
        partitions.append(
            PartitionEntry(
                index=index + 1,
                bootable=entry[0] == 0x80,
                type_code=type_code,
                start_lba=start_lba,
                sectors=sectors,
                byte_offset=start_lba * 512,
                byte_length=sectors * 512,
            )
        )
    return ImageInspection(
        path=str(image),
        size_bytes=size,
        mbr_signature_valid=sector[510:512] == b"\x55\xaa",
        disk_signature_hex=f"0x{disk_signature:08x}",
        partitions=tuple(partitions),
        sha256=sha256_file(image) if include_sha256 else None,
    )


def _parse_os_release(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def _noncomment_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    return [
        line
        for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines()
        if (line := raw_line.strip()) and not line.startswith("#")
    ]


def _dpkg_packages(root: Path) -> list[dict[str, str]]:
    status = root / "var/lib/dpkg/status"
    if not status.is_file():
        return []
    packages: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in status.read_text(encoding="utf-8", errors="replace").splitlines() + [""]:
        if not line:
            if current.get("Package") and current.get("Status") == "install ok installed":
                packages.append(
                    {
                        "name": current["Package"],
                        "version": current.get("Version", ""),
                        "architecture": current.get("Architecture", ""),
                    }
                )
            current = {}
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        current[key] = value.strip()
    return sorted(packages, key=lambda item: (item["name"], item["architecture"]))


def _enabled_systemd_units(root: Path) -> list[str]:
    systemd = root / "etc/systemd/system"
    if not systemd.is_dir():
        return []
    units: set[str] = set()
    for wants_dir in sorted(systemd.glob("*.wants")):
        if not wants_dir.is_dir():
            continue
        for unit in wants_dir.iterdir():
            if unit.is_symlink() or unit.is_file():
                units.add(unit.name)
    return sorted(units)


def baseline_rootfs(root: str | Path) -> dict[str, Any]:
    """Collect a read-only software/configuration baseline from a mounted rootfs."""
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError("rootfs path must be an existing directory")
    boot_candidates = (
        "boot/cmdline.txt",
        "boot/config.txt",
        "boot/firmware/cmdline.txt",
        "boot/firmware/config.txt",
    )
    boot_files: list[dict[str, Any]] = []
    for relative in boot_candidates:
        candidate = root_path / relative
        if candidate.is_file():
            boot_files.append({"path": relative, "size_bytes": candidate.stat().st_size, "sha256": sha256_file(candidate)})
    packages = _dpkg_packages(root_path)
    return {
        "root": str(root_path),
        "collection_mode": "READ_ONLY",
        "os_release": _parse_os_release(root_path / "etc/os-release"),
        "fstab": _noncomment_lines(root_path / "etc/fstab"),
        "boot_files": boot_files,
        "enabled_systemd_units": _enabled_systemd_units(root_path),
        "installed_packages": packages,
        "installed_package_count": len(packages),
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def initialize_temporary_root(root: str | Path) -> Path:
    root_path = Path(root).resolve()
    root_path.mkdir(parents=True, exist_ok=True)
    marker = root_path / TEMP_MARKER_NAME
    if marker.exists():
        payload = json.loads(marker.read_text(encoding="utf-8"))
        if payload.get("role") != TEMP_ROLE:
            raise ValueError("existing temporary marker has an unexpected role")
        return marker
    _write_json(marker, {"schema_version": MANIFEST_VERSION, "role": TEMP_ROLE})
    return marker


def initialize_ssd_root(root: str | Path, *, volume_id: str, confirmation: str) -> Path:
    if confirmation != SSD_ROLE:
        raise ValueError(f"SSD initialization requires exact confirmation token {SSD_ROLE}")
    if not volume_id.strip():
        raise ValueError("volume_id must be non-empty")
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError("SSD root must already exist; this tool never formats or partitions disks")
    marker = root_path / SSD_MARKER_NAME
    if marker.exists():
        payload = json.loads(marker.read_text(encoding="utf-8"))
        if payload.get("role") != SSD_ROLE or payload.get("volume_id") != volume_id:
            raise ValueError("existing SSD marker does not match requested dedicated volume")
    else:
        _write_json(marker, {"schema_version": MANIFEST_VERSION, "role": SSD_ROLE, "volume_id": volume_id})
    for directory in (
        "preservation/pi-images",
        "models/canonical",
        "models/candidates",
        "models/cache",
        "datasets",
        "campaigns",
        "runs",
        "checkpoints",
        "research",
        "meta",
        "exports",
        "logs",
        "manifests",
    ):
        (root_path / directory).mkdir(parents=True, exist_ok=True)
    return marker


def _load_role_marker(root: Path, marker_name: str, expected_role: str) -> dict[str, Any]:
    marker = root / marker_name
    if not marker.is_file():
        raise ValueError(f"missing required role marker: {marker}")
    payload = json.loads(marker.read_text(encoding="utf-8"))
    if payload.get("role") != expected_role:
        raise ValueError(f"unexpected storage role in {marker}")
    return payload


def _assert_disjoint_roots(source: Path, destination: Path) -> None:
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("source and destination storage roots must be disjoint")


def _safe_payload_path(root: Path, relative_text: str) -> Path:
    relative = Path(relative_text)
    if relative.is_absolute() or not relative.parts:
        raise ValueError(f"unsafe payload path: {relative_text}")
    candidate = root.joinpath(relative)
    resolved = candidate.resolve(strict=False)
    if resolved == root or root not in resolved.parents:
        raise ValueError(f"payload path escapes storage root: {relative_text}")
    current = root
    for part in relative.parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"payload path crosses symlinked directory: {relative_text}")
    return candidate


def _destination_relative(source_relative: Path) -> Path:
    """Normalize the known pre-SSD temporary layout into the canonical SSD layout."""
    if source_relative == Path("README.md"):
        return Path("manifests/temporary-storage-README.md")
    if source_relative.parts and source_relative.parts[0] == "pi-images":
        return Path("preservation/pi-images").joinpath(*source_relative.parts[1:])
    return source_relative


def _iter_payload_files(root: Path) -> Iterator[Path]:
    excluded = {TEMP_MARKER_NAME}
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink() and path.name not in excluded:
            yield path


def build_migration_manifest(source_root: str | Path, destination_root: str | Path) -> dict[str, Any]:
    source = Path(source_root).resolve()
    destination = Path(destination_root).resolve()
    _assert_disjoint_roots(source, destination)
    _load_role_marker(source, TEMP_MARKER_NAME, TEMP_ROLE)
    destination_marker = _load_role_marker(destination, SSD_MARKER_NAME, SSD_ROLE)
    items: list[dict[str, Any]] = []
    destination_paths: set[str] = set()
    for path in _iter_payload_files(source):
        source_relative = path.relative_to(source)
        destination_relative = _destination_relative(source_relative)
        destination_text = destination_relative.as_posix()
        if destination_text in destination_paths:
            raise ValueError(f"multiple source files map to one destination: {destination_text}")
        destination_paths.add(destination_text)
        items.append(
            {
                "source_path": source_relative.as_posix(),
                "destination_path": destination_text,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return {
        "schema_version": MANIFEST_VERSION,
        "state": "PLANNED",
        "source_root": str(source),
        "destination_root": str(destination),
        "destination_volume_id": destination_marker["volume_id"],
        "items": items,
    }


def _validate_manifest_roots(manifest: dict[str, Any]) -> tuple[Path, Path]:
    if manifest.get("schema_version") != MANIFEST_VERSION:
        raise ValueError("unsupported migration manifest version")
    source = Path(str(manifest["source_root"])).resolve()
    destination = Path(str(manifest["destination_root"])).resolve()
    _assert_disjoint_roots(source, destination)
    _load_role_marker(source, TEMP_MARKER_NAME, TEMP_ROLE)
    destination_marker = _load_role_marker(destination, SSD_MARKER_NAME, SSD_ROLE)
    if destination_marker.get("volume_id") != manifest.get("destination_volume_id"):
        raise ValueError("destination volume marker does not match migration manifest")
    return source, destination


def _manifest_paths(source: Path, destination: Path, item: dict[str, Any]) -> tuple[Path, Path]:
    source_text = str(item["source_path"])
    destination_text = str(item["destination_path"])
    return _safe_payload_path(source, source_text), _safe_payload_path(destination, destination_text)


def copy_migration(manifest: dict[str, Any]) -> dict[str, Any]:
    source, destination = _validate_manifest_roots(manifest)
    for item in manifest.get("items", []):
        source_path, destination_path = _manifest_paths(source, destination, item)
        if not source_path.is_file() or source_path.is_symlink():
            raise ValueError(f"source payload is missing or unsafe: {item['source_path']}")
        if source_path.stat().st_size != item["size_bytes"] or sha256_file(source_path) != item["sha256"]:
            raise ValueError(f"source payload changed after planning: {item['source_path']}")
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        if destination_path.exists():
            if destination_path.stat().st_size != item["size_bytes"] or sha256_file(destination_path) != item["sha256"]:
                raise ValueError(f"destination already exists with different content: {item['destination_path']}")
            continue
        shutil.copy2(source_path, destination_path)
    copied = dict(manifest)
    copied["state"] = "COPIED"
    return copied


def verify_migration(manifest: dict[str, Any]) -> dict[str, Any]:
    source, destination = _validate_manifest_roots(manifest)
    for item in manifest.get("items", []):
        source_path, destination_path = _manifest_paths(source, destination, item)
        if not source_path.is_file() or source_path.is_symlink():
            raise ValueError(f"source payload is missing or unsafe: {item['source_path']}")
        if not destination_path.is_file() or destination_path.is_symlink():
            raise ValueError(f"destination payload is missing or unsafe: {item['destination_path']}")
        expected_size = int(item["size_bytes"])
        expected_hash = str(item["sha256"])
        if source_path.stat().st_size != expected_size or sha256_file(source_path) != expected_hash:
            raise ValueError(f"source verification failed: {item['source_path']}")
        if destination_path.stat().st_size != expected_size or sha256_file(destination_path) != expected_hash:
            raise ValueError(f"destination verification failed: {item['destination_path']}")
    verified = dict(manifest)
    verified["state"] = "VERIFIED"
    return verified


def finalize_migration(manifest: dict[str, Any], *, confirmation: str) -> dict[str, Any]:
    if confirmation != DELETE_CONFIRMATION:
        raise ValueError(f"finalization requires exact confirmation token {DELETE_CONFIRMATION}")
    verified = verify_migration(manifest)
    source, destination = _validate_manifest_roots(verified)
    destination_record = destination / "manifests/storage-migration-verified.json"
    _write_json(destination_record, verified)
    for item in verified.get("items", []):
        source_path, _ = _manifest_paths(source, destination, item)
        source_path.unlink()
    (source / TEMP_MARKER_NAME).unlink()
    directories = sorted((path for path in source.rglob("*") if path.is_dir()), key=lambda path: len(path.parts), reverse=True)
    for directory in directories:
        if not any(directory.iterdir()):
            directory.rmdir()
    residual_paths = sorted(path.relative_to(source).as_posix() for path in source.rglob("*") if path.exists() or path.is_symlink())
    source_root_removed = False
    if not residual_paths:
        source.rmdir()
        source_root_removed = True
    completed = dict(verified)
    completed["state"] = "SOURCE_TEMPORARY_ROOT_DELETED" if source_root_removed else "SOURCE_PLANNED_COPIES_DELETED_WITH_RESIDUALS"
    completed["source_root_removed"] = source_root_removed
    completed["residual_paths"] = residual_paths
    _write_json(destination_record, completed)
    return completed


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    inspect_parser = commands.add_parser("inspect-image", help="read only the raw image and report MBR metadata")
    inspect_parser.add_argument("image", type=Path)
    inspect_parser.add_argument("--sha256", action="store_true")

    baseline_parser = commands.add_parser("baseline-rootfs", help="read a mounted rootfs and emit a software/configuration baseline")
    baseline_parser.add_argument("root", type=Path)
    baseline_parser.add_argument("--output", type=Path)

    temp_parser = commands.add_parser("init-temporary-root", help="mark an isolated NEURAL1 temporary-storage root")
    temp_parser.add_argument("root", type=Path)

    ssd_parser = commands.add_parser("init-ssd-root", help="mark an already-mounted, positively identified dedicated SSD")
    ssd_parser.add_argument("root", type=Path)
    ssd_parser.add_argument("--volume-id", required=True)
    ssd_parser.add_argument("--confirm-role", required=True)

    plan_parser = commands.add_parser("plan-migration", help="hash the temporary tree and create a migration manifest")
    plan_parser.add_argument("source", type=Path)
    plan_parser.add_argument("destination", type=Path)
    plan_parser.add_argument("--manifest", type=Path, required=True)

    copy_parser = commands.add_parser("copy-migration", help="copy planned files without deleting source data")
    copy_parser.add_argument("manifest", type=Path)

    verify_parser = commands.add_parser("verify-migration", help="rehash both source and SSD copies")
    verify_parser.add_argument("manifest", type=Path)

    finalize_parser = commands.add_parser("finalize-migration", help="delete only verified temporary source copies")
    finalize_parser.add_argument("manifest", type=Path)
    finalize_parser.add_argument("--confirm-delete", required=True)

    args = parser.parse_args(argv)
    if args.command == "inspect-image":
        print(json.dumps(asdict(inspect_image(args.image, include_sha256=args.sha256)), indent=2, sort_keys=True))
        return 0
    if args.command == "baseline-rootfs":
        payload = baseline_rootfs(args.root)
        if args.output:
            _write_json(args.output, payload)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    if args.command == "init-temporary-root":
        print(initialize_temporary_root(args.root))
        return 0
    if args.command == "init-ssd-root":
        print(initialize_ssd_root(args.root, volume_id=args.volume_id, confirmation=args.confirm_role))
        return 0
    if args.command == "plan-migration":
        payload = build_migration_manifest(args.source, args.destination)
        _write_json(args.manifest, payload)
        print(args.manifest)
        return 0
    if args.command == "copy-migration":
        payload = copy_migration(_load_manifest(args.manifest))
        _write_json(args.manifest, payload)
        return 0
    if args.command == "verify-migration":
        payload = verify_migration(_load_manifest(args.manifest))
        _write_json(args.manifest, payload)
        return 0
    payload = finalize_migration(_load_manifest(args.manifest), confirmation=args.confirm_delete)
    _write_json(args.manifest, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
