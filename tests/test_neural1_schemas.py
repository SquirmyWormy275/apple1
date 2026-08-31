from __future__ import annotations

import json
from pathlib import Path

from neural1.models import FakeProvider
from neural1.runtime import RunManifest


def test_machine_readable_schemas_and_synthetic_fixture_are_valid_json() -> None:
    for path in Path("schemas/neural1").glob("*.json"):
        assert json.loads(path.read_text(encoding="utf-8"))["$schema"].endswith("2020-12/schema")
    fixture = json.loads(Path("neural1/fixtures/1976-components.synthetic.json").read_text(encoding="utf-8"))
    assert fixture["fixture_status"] == "SYNTHETIC_TEST_ONLY_NOT_HISTORICAL_EVIDENCE"
    assert all(component["authoritative"] is False for component in fixture["components"])


def test_manifest_fields_match_schema_contract() -> None:
    manifest = RunManifest.create("4k-mind", 1, FakeProvider().record, {})
    assert manifest.schema_version == "neural1-0.1"
    assert manifest.run_id.startswith("N1R-")
