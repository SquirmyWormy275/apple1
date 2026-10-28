import json
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.support_bundle import build_support_bundle

with TemporaryDirectory() as d:
    p = Path(d)
    source = p / "observation.txt"
    source.write_text("TEXTBOOK FIXTURE")
    build_support_bundle(p / "support.zip", [source])
    with zipfile.ZipFile(p / "support.zip") as bundle:
        names = sorted(bundle.namelist())
        manifest = json.loads(bundle.read("manifest.json"))
    print("Archive members:", names)
    print("Evidence files:", len(manifest["files"]))
    assert len(manifest["files"]) == 1 and "evidence/observation.txt" in names
