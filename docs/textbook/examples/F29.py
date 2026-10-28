from pathlib import Path
from tempfile import TemporaryDirectory

from tools.export_cf_card_sources import export_sources

with TemporaryDirectory() as d:
    root = Path(d)
    repo = root / "repo"
    for name in ("approved", "candidate", "baseline"):
        (repo / name).mkdir(parents=True)
    (repo / "approved/page.txt").write_text("READY\n")
    (repo / "candidate/page.txt").write_text("CANDIDATE\n")
    (repo / "baseline/MANIFEST.md").write_text("FIXTURE BASELINE")
    manifest = {
        "baseline": {"manifest_path": "baseline/MANIFEST.md", "image_path": "baseline/absent.img", "size_bytes": 0, "sha256": "0" * 64},
        "sources": [
            {"source_path": "approved", "staging_path": "overlay", "format": "ascii-40x24", "include_in_default_export": True},
            {"source_path": "candidate", "staging_path": "candidate", "format": "mixed", "include_in_default_export": False},
        ],
    }
    export_sources(repo, manifest, root / "staged")
    print("Approved page staged:", (root / "staged/overlay/page.txt").exists())
    print("Candidate staged:", (root / "staged/candidate").exists())
    assert (root / "staged/overlay/page.txt").exists() and not (root / "staged/candidate").exists()
