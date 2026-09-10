"""Regression checks for live transport and recoverable isolated campaign turns."""
from __future__ import annotations

import json
from dataclasses import replace

import pytest

from neural1.campaign import CampaignEngine, CampaignSpec
from neural1.core import Neural1Error
from neural1.models import FakeProvider, GenerationResult, OllamaHttpProvider
from neural1.provider_factory import provider_for
from neural1.registry import ModelRegistry, RegisteredModel


def setup(tmp_path, provider=None, **overrides):
    model = RegisteredModel("test", "fixture", "test", "fake", "fake", "0", "NONE", 4096, "fixture", "TEST-ONLY", {})
    registry = ModelRegistry()
    registry.add(model)
    settings = dict(experiments=["ram-republic"], model_ids=["test"], seeds=[1], generations=2, agents_per_cell=2, ram_budget=4096, max_tokens=32, generation_settings={}, matched_control="synthetic regression", wall_clock_limit_seconds=60)
    settings.update(overrides)
    return CampaignEngine(tmp_path, registry, {"test": provider or FakeProvider(default="0200: 01")}), CampaignSpec.create(**settings)


def run(engine, spec, **kwargs):
    return engine.run(spec, objective_factory=lambda cell, generation: "monitor only", command_parser=lambda text: [text], **kwargs)


def test_endpoint_is_transport_not_generation_option(tmp_path):
    engine, _ = setup(tmp_path)
    model = replace(engine.registry.require("test"), backend="ollama", digest="a" * 64, generation_defaults={"base_url": "http://127.0.0.1:11439", "max_tokens": 32})
    provider = provider_for(model)
    assert isinstance(provider, OllamaHttpProvider)
    assert provider.base_url == "http://127.0.0.1:11439"
    assert "base_url" not in provider.options
    assert provider.options["num_predict"] == 32
    with pytest.raises(Neural1Error, match="local"):
        provider_for(replace(model, generation_defaults={"base_url": "http://example.com"}))


class ParticipantProvider(FakeProvider):
    def generate(self, prompt, *, agent_id, seed):
        return GenerationResult("0200: " + ("AA" if agent_id.endswith("001") else "BB"))


def test_feedback_is_private_and_persisted(tmp_path):
    engine, spec = setup(tmp_path, ParticipantProvider())
    run(engine, spec)
    records = [json.loads(line) for line in next(tmp_path.rglob("transcript.jsonl")).read_text().splitlines()]
    assert "WOZMON:0200: AA" in records[2]["prompt"]
    assert "WOZMON:0200: BB" not in records[2]["prompt"]
    assert "CURRENT SHARED MONITOR EXAMINATION:\n0200: BB" in records[2]["prompt"]
    assert "WOZMON:0200: BB" in records[3]["prompt"]
    assert "WOZMON:0200: AA" not in records[3]["prompt"]


def test_rejections_never_count_as_completed(tmp_path):
    engine, spec = setup(tmp_path, FakeProvider(default="not monitor text"))
    assert run(engine, spec).status == "INCOMPLETE"
    checkpoint = json.loads(next(tmp_path.rglob("checkpoint.json")).read_text())
    assert checkpoint["status"] == "NO_ACCEPTED_COMMANDS"


def test_cancel_mid_generation_resume_preserves_committed_turn(tmp_path):
    engine, spec = setup(tmp_path)
    class CancelAfterFirst(FakeProvider):
        def generate(self, prompt, *, agent_id, seed):
            engine.cancel(spec.campaign_id)
            return super().generate(prompt, agent_id=agent_id, seed=seed)
    engine.providers["test"] = CancelAfterFirst(default="0200: AA")
    assert run(engine, spec).status == "DEADLINE_OR_CANCELLED"
    transcript = next(tmp_path.rglob("transcript.jsonl"))
    first = transcript.read_text()
    assert len(first.splitlines()) == 1
    engine.providers["test"] = FakeProvider(default="0200: BB")
    assert run(engine, spec, resume=True).status == "COMPLETED"
    assert transcript.read_text().startswith(first)
    assert len(transcript.read_text().splitlines()) == 4


def test_resource_stop_occurs_before_provider(tmp_path):
    engine, spec = setup(tmp_path)
    def stop():
        raise Neural1Error("thermal threshold")
    assert run(engine, spec, safety_check=stop).status == "INCOMPLETE"
    assert not list(tmp_path.rglob("transcript.jsonl"))
    assert json.loads(next(tmp_path.rglob("checkpoint.json")).read_text())["status"] == "RESOURCE_STOP"
    assert run(engine, spec, resume=True).status == "COMPLETED"
    recovered = json.loads(next(tmp_path.rglob("checkpoint.json")).read_text())
    assert recovered["errors"][0]["type"] == "ResourceStop"


def test_resume_refuses_foreign_cancel_marker(tmp_path):
    engine, spec = setup(tmp_path)
    root = engine.campaign_path(spec.campaign_id)
    root.mkdir(parents=True)
    (root / "CANCEL").write_text("owned by someone else")
    with pytest.raises(Neural1Error, match="unowned"):
        run(engine, spec, resume=True)


def test_parser_failure_preserves_real_response(tmp_path):
    engine, spec = setup(tmp_path, FakeProvider(default="a malformed but real provider response"))
    def reject(text):
        raise Neural1Error("strict parser rejected response")
    assert engine.run(spec, objective_factory=lambda c, g: "monitor", command_parser=reject).status == "INCOMPLETE"
    records = [json.loads(line) for line in next(tmp_path.rglob("transcript.jsonl")).read_text().splitlines()]
    assert records[0]["response"] == "a malformed but real provider response"
    assert records[0]["error"]["type"] == "Neural1Error"


def test_context_reset_preserves_ram_but_clears_feedback(tmp_path):
    engine, spec = setup(tmp_path, generation_settings={"context_reset_generations": 1})
    run(engine, spec)
    records = [json.loads(line) for line in next(tmp_path.rglob("transcript.jsonl")).read_text().splitlines()]
    assert all("OBSERVATIONS" not in record["prompt"] for record in records)


def test_crash_tail_is_preserved_without_replaying_committed_turns(tmp_path):
    engine, spec = setup(tmp_path)
    run(engine, spec)
    transcript = next(tmp_path.rglob("transcript.jsonl"))
    committed = transcript.read_bytes()
    with transcript.open("ab") as stream:
        stream.write(b'{"uncommitted": true}\n')
    run(engine, spec)
    assert transcript.read_bytes() == committed
    orphan = next(tmp_path.rglob("uncommitted-*.jsonl"))
    assert orphan.read_bytes() == b'{"uncommitted": true}\n'


def test_multiverse_dispatches_design_validator_not_monitor(tmp_path, monkeypatch):
    from neural1 import family_runner
    proposals = []
    def process(text):
        proposals.append(text)
        return {"accepted_proposals": 0, "genome": None, "errors": ["unsupported component"], "outputs": ["unsupported component"]}
    monkeypatch.setattr(family_runner, "process_multiverse_response", process, raising=False)
    monkeypatch.setattr(family_runner, "evaluate_family", lambda family, world, records: {"family": family, "status": "EVALUATED", "passed": False})
    engine, spec = setup(tmp_path, FakeProvider(default='{"cpu":"unsupported"}'), experiments=["1976-multiverse"], agents_per_cell=1)
    def no_monitor(text):
        pytest.fail("historical genome entered monitor parser")
    summary = engine.run(spec, objective_factory=lambda c, g: "propose JSON", command_parser=no_monitor)
    assert summary.status == "COMPLETED"
    assert len(proposals) == 2
    records = [json.loads(line) for line in next(tmp_path.rglob("transcript.jsonl")).read_text().splitlines()]
    assert "DESIGN VALIDATOR:unsupported component" in records[1]["prompt"]
    assert records[0]["proposal"]["accepted_proposals"] == 0
    assert "accepted_commands" not in records[0]
