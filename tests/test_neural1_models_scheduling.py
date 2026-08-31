from __future__ import annotations

import json
from pathlib import Path

import pytest

from neural1.core import Neural1Error
from neural1.models import FakeProvider, LlamaCppProvider, OllamaHttpProvider, RecordingProvider
from neural1.scheduling import LogicalAgent, PopulationScheduler, migrate, summarize
from neural1.world import VirtualApple1World


def test_ollama_adapter_records_tokens_without_network() -> None:
    def opener(request, timeout):
        assert request.full_url == "http://127.0.0.1:11434/api/generate"
        payload = json.loads(request.data)
        assert payload["options"]["seed"] == 7
        return json.dumps({"response": "0200: 00", "prompt_eval_count": 3, "eval_count": 2}).encode()
    result = OllamaHttpProvider("tiny:test", opener=opener).generate("P", agent_id="A", seed=7)
    assert result.prompt_tokens == 3 and result.completion_tokens == 2


def test_ollama_adapter_refuses_nonlocal_or_unbounded_endpoints() -> None:
    with pytest.raises(Neural1Error, match="local"):
        OllamaHttpProvider("model", base_url="https://example.com")
    with pytest.raises(Neural1Error, match="timeout"):
        OllamaHttpProvider("model", timeout_seconds=0)


def test_llama_cpp_uses_argument_array_and_timeout() -> None:
    seen = []
    provider = LlamaCppProvider(Path("llama-cli"), Path("model.gguf"), "a" * 64, runner=lambda command, timeout: (seen.append((command, timeout)) or ("OK", "")))
    assert provider.generate("PROMPT", agent_id="A", seed=4).text == "OK"
    assert seen[0][0][:3] == ["llama-cli", "-m", "model.gguf"]


def test_recording_provider_round_trips_to_replay(tmp_path) -> None:
    path = tmp_path / "record.jsonl"
    wrapped = RecordingProvider(FakeProvider(default="ANSWER"), path)
    expected = wrapped.generate("PROMPT", agent_id="A", seed=2)
    replay = RecordingProvider.load_replay(path)
    assert replay.generate("PROMPT", agent_id="A", seed=2) == expected
    with pytest.raises(Neural1Error):
        replay.generate("OTHER", agent_id="A", seed=2)


def test_scheduler_is_deterministic_and_contexts_are_isolated() -> None:
    def run():
        world = VirtualApple1World(ram_budget=1024)
        agents = [LogicalAgent("A", "shared"), LogicalAgent("B", "shared")]
        scheduler = PopulationScheduler(world, agents, {"shared": FakeProvider(default="0200: 01")}, seed=9)
        turns = scheduler.round("OBJECTIVE", lambda response: [response])
        return turns, agents
    one, agents = run()
    two, _ = run()
    assert one == two
    assert agents[0].private_context is not agents[1].private_context


def test_migration_and_statistics_are_explicit() -> None:
    source, destination = VirtualApple1World(), VirtualApple1World()
    source.host_write(0x0200, b"ABC")
    record = migrate("C1", source, "C2", destination, 0x0200, 3)
    assert destination.host_read(0x0200, 3) == b"ABC"
    assert len(record.artifact_sha256) == 64
    assert summarize([1.0, 2.0, 3.0]).mean == 2.0
