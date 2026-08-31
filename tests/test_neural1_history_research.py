from __future__ import annotations

import json
from pathlib import Path

import pytest

from neural1.core import Neural1Error
from neural1.history import load_research_index, research_status


def _write_index(path: Path, *, runtime_ids: list[str] | None = None, count: int = 0) -> None:
    payload = {
        "schema_version": "neural1-historical-research-index-0.1",
        "world_id": "DESIGN_1976_03_10",
        "cutoff_date": "1976-03-10",
        "status": "RESEARCH_STAGING",
        "authoritative_runtime_records": count,
        "runtime_authoritative_component_ids": runtime_ids or [],
        "promotion_policy": {
            "requires_sha256": True,
            "requires_claim_review": True,
            "requires_cutoff_validation": True,
            "missing_prices_remain_null": True,
            "no_llm_estimates": True,
        },
        "research_inputs": [{"path": "source.json", "role": "test", "authority_status": "RESEARCH_ONLY"}],
        "unresolved_high_impact": ["unknown price"],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_research_status_reports_staging_without_promotion(tmp_path: Path) -> None:
    index = tmp_path / "index.json"
    _write_index(index)
    assert research_status(index) == {
        "world_id": "DESIGN_1976_03_10",
        "cutoff_date": "1976-03-10",
        "status": "RESEARCH_STAGING",
        "authoritative_runtime_records": 0,
        "research_inputs": 1,
        "unresolved_high_impact": 1,
    }


def test_staging_index_cannot_promote_runtime_components(tmp_path: Path) -> None:
    index = tmp_path / "index.json"
    _write_index(index, runtime_ids=["6502"], count=1)
    with pytest.raises(Neural1Error, match="cannot promote"):
        load_research_index(index)


def test_research_index_requires_safe_promotion_policy(tmp_path: Path) -> None:
    index = tmp_path / "index.json"
    _write_index(index)
    payload = json.loads(index.read_text(encoding="utf-8"))
    payload["promotion_policy"]["no_llm_estimates"] = False
    index.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(Neural1Error, match="promotion policy"):
        load_research_index(index)
