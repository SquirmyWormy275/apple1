from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.storage_commissioning import (
    SSD_ROLE,
    build_migration_manifest,
    copy_migration,
    initialize_ssd_root,
    initialize_temporary_root,
    verify_migration,
)

with TemporaryDirectory() as d:
    root = Path(d)
    source = root / "temporary"
    destination = root / "fixture-destination"
    destination.mkdir()
    initialize_temporary_root(source)
    initialize_ssd_root(destination, volume_id="DISPOSABLE-TEXTBOOK-FIXTURE", confirmation=SSD_ROLE)
    (source / "lesson.txt").write_text("PRESERVE THESE BYTES")
    manifest = build_migration_manifest(source, destination)
    copied = copy_migration(manifest)
    verify_migration(copied)
    assert (source / "lesson.txt").read_bytes() == (destination / "lesson.txt").read_bytes()
    print("Copy verified: True")
    print("Source retained:", (source / "lesson.txt").exists())
    print("Real SSD or mount modified: False")
