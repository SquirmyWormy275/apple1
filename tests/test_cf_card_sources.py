from __future__ import annotations

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
