from __future__ import annotations

from pathlib import Path

from test_neural1_campaign_bundle import fixture_registry, fixture_spec

from neural1.campaign import CampaignEngine
from neural1.drivers import objective, parse_commands
from neural1.models import FakeProvider
from neural1.pilot_report import generate_pilot_001
from tools.neural1_validate import validate_repository


def test_pilot_report_is_generated_from_authoritative_fixture_records(tmp_path) -> None:
    spec = fixture_spec()
    registry = fixture_registry()
    registry_path = tmp_path / "registry.json"
    registry.save(registry_path)
    root = tmp_path / "runtime"
    CampaignEngine(root, registry, {"fake-small": FakeProvider(default="0200: 01")}).run(spec, objective_factory=objective, command_parser=parse_commands)
    report = generate_pilot_001(root / "campaigns" / spec.campaign_id, registry_path, tmp_path / "pilot-001")
    assert report["completed"] == 4
    required = {"README.md", "methodology.md", "experiment-matrix.md", "model-comparison.md", "experiment-results.md", "meta-findings.md", "negative-results.md", "anomalies-and-discoveries.md", "limitations.md", "follow-up-experiments.md", "reproducibility.md"}
    assert required <= {path.name for path in (tmp_path / "pilot-001").iterdir()}
    assert "NOT AUTOMATICALLY ESTABLISHED" in (tmp_path / "pilot-001" / "README.md").read_text()
    assert list((tmp_path / "pilot-001" / "proof-capsules").glob("*.json"))


def test_repository_validator_passes_current_tree() -> None:
    assert validate_repository(Path(__file__).resolve().parents[1]) == []
