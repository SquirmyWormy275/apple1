from __future__ import annotations

from pathlib import Path

from neural1.demos import run_all
from neural1.history import load_research_index
from tools.neural1_validate import validate_repository


ROOT = Path(__file__).resolve().parents[1]


def test_repository_validator_passes_current_tree() -> None:
    assert validate_repository(ROOT) == []


def test_historical_research_remains_staging_only() -> None:
    payload = load_research_index(ROOT / "data/neural1/history/1976-research-index.json")
    assert payload["status"] == "RESEARCH_STAGING"
    assert payload["authoritative_runtime_records"] == 0
    assert payload["runtime_authoritative_component_ids"] == []


def test_deterministic_demo_never_opens_physical_serial(tmp_path) -> None:
    result = run_all(tmp_path / "neural1-demo")
    assert result["serial_opened"] is False
    physical = result["physical_qualification"]
    assert physical["ready"] is False
    assert "serial_open" in physical["prohibited_actions"]
