from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.bundle import export_bundle, verify_bundle

with TemporaryDirectory() as d:
    root = Path(d)
    source = root / "source"
    source.mkdir()
    (source / "record.txt").write_text("OBSERVATION")
    bundle = export_bundle(source, root / "bundle", reproduction_command="textbook F06")
    print("Original bundle valid:", verify_bundle(bundle).valid)
    assert verify_bundle(bundle).valid
    (bundle / "records/record.txt").write_text("CHANGED")
    print("Changed bundle valid:", verify_bundle(bundle).valid)
    assert not verify_bundle(bundle).valid
