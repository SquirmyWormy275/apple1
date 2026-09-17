import json
from pathlib import Path
from unittest.mock import patch

import pytest

from neural1.deployment import verify_storage
from neural1.storage_commissioning import (
    SSD_ROLE,
    build_migration_manifest,
    copy_migration,
    initialize_ssd_root,
    initialize_temporary_root,
    verify_migration,
)


def migration(tmp_path: Path) -> dict:
    source, destination = tmp_path / "source", tmp_path / "destination"
    initialize_temporary_root(source)
    destination.mkdir()
    initialize_ssd_root(destination, volume_id="uuid", confirmation=SSD_ROLE)
    (source / "payload").write_bytes(b"important bytes")
    return build_migration_manifest(source, destination)


def test_interrupted_copy_retries_without_corrupt_final(tmp_path: Path) -> None:
    manifest = migration(tmp_path)
    destination = Path(manifest["destination_root"]) / "payload"

    def interrupt(incoming, output, **kwargs):
        output.write(incoming.read(3))
        raise InterruptedError("interrupted write")

    with patch("neural1.storage_commissioning.shutil.copyfileobj", side_effect=interrupt), pytest.raises(InterruptedError):
        copy_migration(manifest)
    assert not destination.exists()
    assert not list(destination.parent.glob(".neural1-copy-*.partial"))
    assert verify_migration(copy_migration(manifest))["state"] == "VERIFIED"


def test_publication_race_preserves_unrelated_file(tmp_path: Path) -> None:
    manifest = migration(tmp_path)
    destination = Path(manifest["destination_root"]) / "payload"

    def raced_link(source, target):
        target.write_bytes(b"unrelated")
        raise FileExistsError

    with patch("neural1.storage_commissioning.os.link", side_effect=raced_link), pytest.raises(ValueError, match="different content"):
        copy_migration(manifest)
    assert destination.read_bytes() == b"unrelated"


def test_copy_rejects_symlink_even_matching_content(tmp_path: Path) -> None:
    manifest = migration(tmp_path)
    destination = Path(manifest["destination_root"]) / "payload"
    destination.symlink_to(Path(manifest["source_root"]) / "payload")
    with pytest.raises(ValueError):
        copy_migration(manifest)


def test_storage_checks_uuid_mount_role_and_paths(tmp_path: Path) -> None:
    initialize_ssd_root(tmp_path, volume_id="expected", confirmation=SSD_ROLE)
    mount = {"target": str(tmp_path), "source": "/dev/test", "uuid": "expected", "options": "rw,relatime"}
    with patch("neural1.deployment._mount", return_value=mount):
        assert verify_storage(tmp_path, "expected", write_paths=["runs/new"], min_free_bytes=0).uuid == "expected"
        with pytest.raises(ValueError, match="expected UUID"):
            verify_storage(tmp_path, "wrong")
        with pytest.raises(ValueError, match="escapes"):
            verify_storage(tmp_path, "expected", write_paths=["../outside"])
        (tmp_path / ".neural1-ssd.json").write_text(json.dumps({"role": "backup", "volume_id": "expected"}))
        with pytest.raises(ValueError, match="role/volume"):
            verify_storage(tmp_path, "expected")


def test_storage_rejects_directory_without_mount_and_nested_mount(tmp_path: Path) -> None:
    initialize_ssd_root(tmp_path, volume_id="expected", confirmation=SSD_ROLE)
    mounted = {"target": str(tmp_path), "source": "/dev/test", "uuid": "expected", "options": "rw"}
    with patch("neural1.deployment._mount", return_value={**mounted, "target": "/"}), pytest.raises(ValueError, match="not mounted"):
        verify_storage(tmp_path, "expected")
    (tmp_path / "nested").mkdir()
    with (
        patch("neural1.deployment._mount", side_effect=[mounted, {**mounted, "target": str(tmp_path / "nested")}]),
        pytest.raises(ValueError, match="nested mount"),
    ):
        verify_storage(tmp_path, "expected", write_paths=["nested/result"])


def test_corrupt_copy_is_never_published(tmp_path: Path) -> None:
    manifest = migration(tmp_path)

    def corrupt(incoming, output, **kwargs):
        output.write(b"invalid bytes")

    with (
        patch("neural1.storage_commissioning.shutil.copyfileobj", side_effect=corrupt),
        pytest.raises(ValueError, match="verification failed"),
    ):
        copy_migration(manifest)
    assert not (Path(manifest["destination_root"]) / "payload").exists()


def test_retry_ignores_abandoned_partial_and_reuses_complete_file(tmp_path: Path) -> None:
    manifest = migration(tmp_path)
    destination = Path(manifest["destination_root"])
    abandoned = destination / ".neural1-copy-abandoned.partial"
    abandoned.write_bytes(b"interrupted")
    copy_migration(manifest)
    inode = (destination / "payload").stat().st_ino
    copy_migration(manifest)
    assert abandoned.read_bytes() == b"interrupted"
    assert (destination / "payload").stat().st_ino == inode
