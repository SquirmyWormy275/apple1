from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.export_cf_card_sources import export_sources, validate_ascii_40x24


def test_ascii_40x24_validator_accepts_valid_page(tmp_path: Path) -> None:
    root = tmp_path / "card"
    root.mkdir()
    (root / "page.txt").write_text("HELLO\n" + ("X" * 40) + "\n", encoding="ascii")
    assert validate_ascii_40x24(root) == []


def test_ascii_40x24_validator_rejects_width_and_lowercase(tmp_path: Path) -> None:
    root = tmp_path / "card"
    root.mkdir()
    (root / "page.txt").write_text("lower\n" + ("X" * 41) + "\n", encoding="ascii")
    errors = validate_ascii_40x24(root)
    assert any("lowercase" in error for error in errors)
    assert any("exceeds 40" in error for error in errors)


def test_default_export_skips_candidates_and_copies_metadata(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    approved = repo / "docs" / "approved"
    candidate = repo / "docs" / "candidate"
    approved.mkdir(parents=True)
    candidate.mkdir(parents=True)
    (approved / "00.txt").write_text("READY\n", encoding="ascii")
    (candidate / "candidate.txt").write_text("CANDIDATE\n", encoding="ascii")

    baseline_dir = repo / "preservation" / "cf"
    baseline_dir.mkdir(parents=True)
    (baseline_dir / "MANIFEST.md").write_text("BASELINE\n", encoding="utf-8")

    manifest = {
        "baseline": {
            "manifest_path": "preservation/cf/MANIFEST.md",
            "image_path": "preservation/cf/original.img",
            "size_bytes": 10,
            "sha256": "0" * 64,
        },
        "sources": [
            {
                "source_path": "docs/approved",
                "staging_path": "overlay/approved",
                "format": "ascii-40x24",
                "include_in_default_export": True,
            },
            {
                "source_path": "docs/candidate",
                "staging_path": "candidate/source",
                "format": "mixed",
                "include_in_default_export": False,
            },
        ],
    }

    output = tmp_path / "out"
    export_sources(repo, manifest, output)

    assert (output / "overlay" / "approved" / "00.txt").read_text() == "READY\n"
    assert not (output / "candidate").exists()
    assert (output / "metadata" / "ORIGINAL-CF-MANIFEST.md").is_file()
    inventory = json.loads((output / "metadata/FILES.json").read_text())
    for name, entry in inventory.items():
        data = (output / name).read_bytes()
        assert entry == {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def _fixture(repo: Path) -> dict:
    repo.mkdir()
    (repo / "baseline.md").write_text("BASELINE")
    (repo / "source").mkdir()
    (repo / "source/page.txt").write_text("READY\n")
    return {"baseline": {"manifest_path": "baseline.md"}, "sources": [
        {"source_path": "source", "staging_path": "overlay/pages", "include_in_default_export": True, "format": "ascii-40x24"}
    ]}


def test_export_never_replaces_existing_output(tmp_path):
    repo = tmp_path / "repo"
    manifest = _fixture(repo)
    keep = tmp_path / "keep"
    keep.mkdir()
    (keep / "precious.txt").write_text("DO NOT DELETE")
    with pytest.raises(FileExistsError):
        export_sources(repo, manifest, keep)
    assert (keep / "precious.txt").read_text() == "DO NOT DELETE"


@pytest.mark.parametrize("field,value", [("source_path", "../elsewhere"), ("source_path", "/etc"),
    ("staging_path", "../escape"), ("staging_path", "/outside/escape"), ("staging_path", "metadata/overwrite"),
    ("staging_path", ".")])
def test_invalid_manifest_is_rejected_before_output_creation(tmp_path, field, value):
    repo = tmp_path / "repo"
    manifest = _fixture(repo)
    manifest["sources"][0][field] = value
    output = tmp_path / "new"
    with pytest.raises(ValueError):
        export_sources(repo, manifest, output)
    assert not output.exists()


def test_nested_source_symlink_is_rejected_before_output_creation(tmp_path):
    repo = tmp_path / "repo"
    manifest = _fixture(repo)
    (repo / "source/link").symlink_to(tmp_path)
    with pytest.raises(ValueError, match="symlink"):
        export_sources(repo, manifest, tmp_path / "new")
    assert not (tmp_path / "new").exists()


def test_output_inside_exported_source_is_rejected(tmp_path):
    repo = tmp_path / "repo"
    manifest = _fixture(repo)
    with pytest.raises(ValueError, match="inside"):
        export_sources(repo, manifest, repo / "source/new")
    assert not (repo / "source/new").exists()
