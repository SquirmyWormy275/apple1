from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from neural1.core import Neural1Error, sha256_bytes
from neural1.models import OllamaHttpProvider, RecordingProvider
from neural1.provider_factory import provider_for
from neural1.registry import RegisteredModel


def registered(**settings) -> RegisteredModel:
    return RegisteredModel("review-control", "qwen", "test", "ollama", "qwen:test", "1.5B", "Q4_K_M", 2048, "a" * 64, "SYNTHETIC HTTP TEST", settings)


def test_generate_default_preserves_request_and_exact_raw_text() -> None:
    text = "\n0200: A9 41\r\n0200R\n"
    raw = json.dumps({"response": text, "done": True, "done_reason": "stop", "eval_count": 5}, indent=2).encode()
    def opener(request, timeout):
        assert request.full_url.endswith("/api/generate")
        assert json.loads(request.data) == {"model": "model", "prompt": "P", "stream": False, "options": {"seed": 9}}
        return raw
    provider = OllamaHttpProvider("model", opener=opener)
    result = provider.generate("P", agent_id="A", seed=9)
    assert result.text == text  # no strip, JSON-command extraction or response replacement
    assert result.provider_metadata["raw_response_utf8"].encode() == raw
    assert result.provider_metadata["raw_response_sha256"] == sha256_bytes(raw)
    assert provider.record.hash == "UNAVAILABLE"
    assert provider.record.context_limit is None


def test_explicit_chat_and_top_level_keepalive_preserve_private_prompt() -> None:
    seen = []
    def opener(request, timeout):
        assert request.full_url == "http://127.0.0.1:11439/api/chat"
        body = json.loads(request.data)
        seen.append(body)
        assert body["keep_alive"] == 0
        assert "keep_alive" not in body["options"] and "api" not in body["options"]
        assert "prompt" not in body
        return b'{"message":{"role":"assistant","content":"not a command"},"done":true}'
    provider = provider_for(registered(api="chat", keep_alive=0, base_url="http://127.0.0.1:11439", max_tokens=64))
    assert isinstance(provider, OllamaHttpProvider)
    provider.opener = opener
    assert provider.generate("PRIVATE A", agent_id="A", seed=1).text == "not a command"
    provider.generate("PRIVATE B", agent_id="B", seed=2)
    assert seen[0]["messages"] == [{"role": "user", "content": "PRIVATE A"}]
    assert seen[1]["messages"] == [{"role": "user", "content": "PRIVATE B"}]
    assert provider.record.hash == "a" * 64
    assert provider.record.quantization == "Q4_K_M"
    assert provider.record.context_limit == 2048
    assert provider.record.generation["api"] == "chat"
    assert provider.options["num_predict"] == 64


def test_generate_keepalive_and_effective_context_are_recorded() -> None:
    provider = provider_for(registered(keep_alive="30s", num_ctx=3072))
    assert isinstance(provider, OllamaHttpProvider)
    assert provider.api == "generate"
    assert provider.record.context_limit == 3072
    def opener(request, timeout):
        body = json.loads(request.data)
        assert body["keep_alive"] == "30s" and body["options"]["num_ctx"] == 3072
        return b'{"response":"OK"}'
    provider.opener = opener
    provider.generate("P", agent_id="A", seed=0)


def test_chat_does_not_fallback_to_generate_or_decode_model_json(tmp_path: Path) -> None:
    with pytest.raises(Neural1Error, match="api"):
        OllamaHttpProvider("x", api="unknown")
    with pytest.raises(Neural1Error, match="transport"):
        OllamaHttpProvider("x", options={"keep_alive": 0})
    with pytest.raises(Neural1Error, match="recorded context"):
        OllamaHttpProvider("x", context_limit=2048, options={"num_ctx": 8192})
    with pytest.raises(Neural1Error, match="SHA-256"):
        provider_for(replace(registered(), digest="not-a-qualified-digest"))
    calls = []
    def missing_message(request, timeout):
        calls.append(request.full_url)
        return b'{"response":"0200R"}'
    provider = OllamaHttpProvider("x", api="chat", opener=missing_message)
    with pytest.raises(Neural1Error, match="assistant message"):
        provider.generate("P", agent_id="A", seed=0)
    assert len(calls) == 1
    original = '{"commands":["0200R"]}'
    provider.opener = lambda request, timeout: json.dumps({"message": {"content": original}}).encode()
    recording = RecordingProvider(provider, tmp_path / "http.jsonl")
    assert recording.generate("P", agent_id="A", seed=0).text == original
    record = json.loads((tmp_path / "http.jsonl").read_text())
    assert record["result"]["text"] == original
    assert record["result"]["provider_metadata"]["api"] == "chat"
