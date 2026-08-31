from __future__ import annotations

import json
from pathlib import Path

import pytest

from neural1.storage import (
    DELETE_CONFIRMATION,
    SSD_ROLE,
    baseline_rootfs,
    build_migration_manifest,
    copy_migration,
    finalize_migration,
    initialize_ssd_root,
    initialize_temporary_root,
    inspect_image,
    verify_migration,
)


def test_inspect_image_reads_mbr_without_writing(tmp_path: Path) -> None:
    image = tmp_path / "pi.img"
    payload = bytearray(4096)
    payload[440:444] = (0xA329DF98).to_bytes(4, "little")
    partition = 446
    payload[partition] = 0x80
    payload[partition + 4] = 0x0C
    payload[partition + 8 : partition + 12] = (1).to_bytes(4, "little")
    payload[partition + 12 : partition + 16] = (4).to_bytes(4, "little")
    payload[510:512] = b"\x55\xaa"
    image.write_bytes(payload)

    result = inspect_image(image, include_sha256=True)

    assert result.size_bytes == 4096
    assert result.disk_signature_hex == "0xa329df98"
    assert result.mbr_signature_valid is True
    assert result.sha256 is not None
    assert result.partitions[0].type_code == 0x0C
    assert result.partitions[0].byte_offset == 512
    assert result.partitions[0].byte_length == 2048


def test_verified_migration_copy_then_delete(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="test-ssd", confirmation=SSD_ROLE)
    payload = source / "preservation/pi-images/pi.img"
    payload.parent.mkdir(parents=True)
    payload.write_bytes(b"preserved image bytes")

    manifest = build_migration_manifest(source, destination)
    copied = copy_migration(manifest)
    verified = verify_migration(copied)
    completed = finalize_migration(verified, confirmation=DELETE_CONFIRMATION)

    assert completed["state"] == "SOURCE_TEMPORARY_ROOT_DELETED"
    assert not source.exists()
    assert (destination / "preservation/pi-images/pi.img").read_bytes() == b"preserved image bytes"
    record = json.loads((destination / "manifests/storage-migration-verified.json").read_text(encoding="utf-8"))
    assert record["state"] == "SOURCE_TEMPORARY_ROOT_DELETED"


def test_migration_refuses_unmarked_destination(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "not-an-ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    (source / "payload.bin").write_bytes(b"data")

    with pytest.raises(ValueError, match="missing required role marker"):
        build_migration_manifest(source, destination)


def test_finalize_rehashes_destination_before_deletion(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="test-ssd", confirmation=SSD_ROLE)
    payload = source / "payload.bin"
    payload.write_bytes(b"original")
    manifest = verify_migration(copy_migration(build_migration_manifest(source, destination)))
    (destination / "payload.bin").write_bytes(b"corrupt")

    with pytest.raises(ValueError, match="destination verification failed"):
        finalize_migration(manifest, confirmation=DELETE_CONFIRMATION)

    assert payload.read_bytes() == b"original"


def test_finalize_requires_explicit_confirmation(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="test-ssd", confirmation=SSD_ROLE)
    payload = source / "payload.bin"
    payload.write_bytes(b"original")
    manifest = verify_migration(copy_migration(build_migration_manifest(source, destination)))

    with pytest.raises(ValueError, match="finalization requires exact confirmation token"):
        finalize_migration(manifest, confirmation="yes")

    assert payload.exists()


def test_baseline_rootfs_is_read_only_inventory(tmp_path: Path) -> None:
    root = tmp_path / "rootfs"
    (root / "etc/systemd/system/multi-user.target.wants").mkdir(parents=True)
    (root / "var/lib/dpkg").mkdir(parents=True)
    (root / "boot/firmware").mkdir(parents=True)
    (root / "etc/os-release").write_text('NAME="Test OS"\nVERSION_ID="1"\n', encoding="utf-8")
    (root / "etc/fstab").write_text('# comment\nUUID=abc / ext4 ro 0 1\n', encoding="utf-8")
    (root / "boot/firmware/config.txt").write_text("arm_64bit=1\n", encoding="utf-8")
    (root / "var/lib/dpkg/status").write_text(
        "Package: python3\nStatus: install ok installed\nVersion: 3.12\nArchitecture: arm64\n\n",
        encoding="utf-8",
    )
    service = root / "etc/systemd/system/multi-user.target.wants/neural1.service"
    service.write_text("unit", encoding="utf-8")

    result = baseline_rootfs(root)

    assert result["collection_mode"] == "READ_ONLY"
    assert result["os_release"]["NAME"] == "Test OS"
    assert result["fstab"] == ["UUID=abc / ext4 ro 0 1"]
    assert result["installed_package_count"] == 1
    assert result["installed_packages"][0]["name"] == "python3"
    assert result["enabled_systemd_units"] == ["neural1.service"]


def test_pi_preservation_record_pins_verified_artifact() -> None:
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root / "data/neural1/preservation/pi-image-2026-08-30.json").read_text(encoding="utf-8"))

    assert record["record_type"] == "PRESERVATION_RECORD"
    assert record["size_bytes"] == 127_865_454_592
    assert record["sha256"] == "58e46686e02a54fbe8c7060afdb8a2fdc5eea5e3107478366c7881c7957169da"
    assert record["disk_signature"] == "0xa329df98"
    assert record["source_read_only_after_imaging"] is True
    assert record["seagate_general_backup_touched"] is False
    assert record["physical_apple_hardware_touched"] is False
    assert record["future_ssd_migration_required"] is True


def test_manifest_path_traversal_cannot_escape_source(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="test-ssd", confirmation=SSD_ROLE)
    (source / "payload.bin").write_bytes(b"safe")
    outside = tmp_path / "outside.bin"
    outside.write_bytes(b"do not delete")
    manifest = build_migration_manifest(source, destination)
    manifest["items"][0]["path"] = "../outside.bin"

    with pytest.raises(ValueError, match="escapes storage root"):
        copy_migration(manifest)

    assert outside.read_bytes() == b"do not delete"


def test_finalize_preserves_unplanned_residual_file(tmp_path: Path) -> None:
    source = tmp_path / "temporary"
    destination = tmp_path / "ssd"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="test-ssd", confirmation=SSD_ROLE)
    planned = source / "planned.bin"
    planned.write_bytes(b"planned")
    manifest = verify_migration(copy_migration(build_migration_manifest(source, destination)))
    residual = source / "created-after-plan.txt"
    residual.write_text("preserve me", encoding="utf-8")

    completed = finalize_migration(manifest, confirmation=DELETE_CONFIRMATION)

    assert completed["state"] == "SOURCE_PLANNED_COPIES_DELETED_WITH_RESIDUALS"
    assert completed["residual_paths"] == ["created-after-plan.txt"]
    assert residual.read_text(encoding="utf-8") == "preserve me"
