from __future__ import annotations

import json

import pytest

from neural1.bundle import export_bundle, verify_bundle
from neural1.campaign import CampaignEngine, CampaignSpec
from neural1.core import Neural1Error
from neural1.models import FakeProvider, GenerationResult
from neural1.registry import ModelRegistry, RegisteredModel


def fixture_registry() -> ModelRegistry:
    registry = ModelRegistry()
    registry.add(RegisteredModel("fake-small", "fixture", "test", "fake", "fake-v1", "0", "NONE", 2048, "fixture", "TEST-ONLY", {"temperature": 0}))
    return registry


def fixture_spec() -> CampaignSpec:
    return CampaignSpec.create(experiments=["4k-mind", "ram-republic"], model_ids=["fake-small"], seeds=[3, 7], generations=2, agents_per_cell=2, ram_budget=1024, max_tokens=32, generation_settings={"temperature": 0}, matched_control="same initial zero RAM", wall_clock_limit_seconds=60)


def test_campaign_matrix_and_identity_are_stable() -> None:
    one, two = fixture_spec(), fixture_spec()
    assert one.campaign_id == two.campaign_id
    assert len(one.cells) == 4
    assert [cell.cell_id for cell in one.cells] == [cell.cell_id for cell in two.cells]


def test_campaign_runs_checkpoints_and_resume_is_idempotent(tmp_path) -> None:
    spec = fixture_spec()
    engine = CampaignEngine(tmp_path, fixture_registry(), {"fake-small": FakeProvider(default="0200: A9 01 00")})
    first = engine.run(spec, objective_factory=lambda cell, generation: f"{cell.experiment_id}:{generation}", command_parser=lambda text: [text])
    transcripts = {path: path.read_bytes() for path in (tmp_path / "campaigns" / spec.campaign_id).rglob("transcript.jsonl")}
    second = engine.run(spec, objective_factory=lambda cell, generation: "MUST NOT RUN", command_parser=lambda text: [text])
    assert first.status == second.status == "COMPLETED"
    assert first.completed_cells == second.completed_cells
    assert transcripts == {path: path.read_bytes() for path in transcripts}
    for checkpoint_path in (tmp_path / "campaigns" / spec.campaign_id).rglob("checkpoint.json"):
        checkpoint = json.loads(checkpoint_path.read_text())
        assert checkpoint["generation"] == 2 and checkpoint["status"] == "COMPLETED"


def test_registry_does_not_encode_model_size_in_experiment_definition() -> None:
    registry = fixture_registry()
    registry.add(RegisteredModel("future-strong", "future-family", "general", "fake", "fake-v2", "4B", "Q4", 8192, "fixture", "TEST-ONLY", {}))
    spec = CampaignSpec.create(experiments=["4k-mind"], model_ids=["future-strong"], seeds=[1], generations=1, agents_per_cell=1, ram_budget=4096, max_tokens=32, generation_settings={}, matched_control="fixed", wall_clock_limit_seconds=10)
    assert spec.model_ids == ("future-strong",)
    assert not hasattr(spec, "parameter_count")
    assert registry.require("future-strong").parameter_count == "4B"


def test_bundle_round_trip_and_tamper_detection(tmp_path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "record.json").write_text('{"value":1}\n')
    bundle = export_bundle(source, tmp_path / "bundle", reproduction_command="neural1 campaign replay")
    assert verify_bundle(bundle).valid is True
    (bundle / "records" / "record.json").write_text("tampered")
    result = verify_bundle(bundle)
    assert result.valid is False
    assert "identity mismatch" in result.errors[0]


def test_bundle_rejects_unlisted_files(tmp_path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "record").write_text("fixed")
    bundle = export_bundle(source, tmp_path / "bundle", reproduction_command="replay")
    (bundle / "records" / "injected").write_text("not listed")
    assert "unlisted file: records/injected" in verify_bundle(bundle).errors


def test_campaign_rejects_unregistered_provider(tmp_path) -> None:
    with pytest.raises(Neural1Error, match="provider"):
        CampaignEngine(tmp_path, fixture_registry(), {}).validate(fixture_spec())


class CancellingProvider(FakeProvider):
    def __init__(self, cancel_path) -> None:
        super().__init__(default="0200: A9 01 00")
        self.cancel_path = cancel_path
        self.calls = 0

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        result = super().generate(prompt, agent_id=agent_id, seed=seed)
        self.calls += 1
        if self.calls == 1:
            self.cancel_path.touch()
        return result


def test_checkpoint_resume_matches_uninterrupted_execution(tmp_path) -> None:
    spec = CampaignSpec.create(experiments=["4k-mind"], model_ids=["fake-small"], seeds=[3], generations=3, agents_per_cell=1, ram_budget=1024, max_tokens=32, generation_settings={"temperature": 0}, matched_control="fixed", wall_clock_limit_seconds=60)
    interrupted_root = tmp_path / "interrupted"
    campaign_root = interrupted_root / "campaigns" / spec.campaign_id
    campaign_root.mkdir(parents=True)
    first = CampaignEngine(interrupted_root, fixture_registry(), {"fake-small": CancellingProvider(campaign_root / "CANCEL")}).run(spec, objective_factory=lambda cell, generation: f"G{generation}", command_parser=lambda text: [text])
    assert first.status == "DEADLINE_OR_CANCELLED"
    (campaign_root / "CANCEL").unlink()
    resumed = CampaignEngine(interrupted_root, fixture_registry(), {"fake-small": FakeProvider(default="0200: A9 01 00")}).run(spec, objective_factory=lambda cell, generation: f"G{generation}", command_parser=lambda text: [text])

    uninterrupted_root = tmp_path / "uninterrupted"
    uninterrupted = CampaignEngine(uninterrupted_root, fixture_registry(), {"fake-small": FakeProvider(default="0200: A9 01 00")}).run(spec, objective_factory=lambda cell, generation: f"G{generation}", command_parser=lambda text: [text])
    assert resumed.status == uninterrupted.status == "COMPLETED"
    interrupted_cell = next((campaign_root / "cells").iterdir())
    uninterrupted_cell = next((uninterrupted_root / "campaigns" / spec.campaign_id / "cells").iterdir())
    assert (interrupted_cell / "transcript.jsonl").read_bytes() == (uninterrupted_cell / "transcript.jsonl").read_bytes()
    resumed_checkpoint = json.loads((interrupted_cell / "checkpoint.json").read_text())
    reference_checkpoint = json.loads((uninterrupted_cell / "checkpoint.json").read_text())
    assert resumed_checkpoint["snapshot_sha256"] == reference_checkpoint["snapshot_sha256"]
    assert not resumed_checkpoint["snapshot_path"].startswith("/")


def test_campaign_rejects_provider_token_limit_above_spec(tmp_path) -> None:
    registry = ModelRegistry()
    registry.add(RegisteredModel("fake-small", "fixture", "test", "fake", "fake-v1", "0", "NONE", 2048, "fixture", "TEST-ONLY", {"max_tokens": 64}))
    with pytest.raises(Neural1Error, match="max_tokens"):
        CampaignEngine(tmp_path, registry, {"fake-small": FakeProvider()}).validate(fixture_spec())
