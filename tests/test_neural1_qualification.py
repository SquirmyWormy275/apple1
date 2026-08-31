from __future__ import annotations

from neural1.qualification import qualify_registry
from neural1.registry import ModelRegistry, RegisteredModel


def test_fake_provider_qualification_is_bounded_and_recorded(tmp_path) -> None:
    registry = ModelRegistry()
    registry.add(RegisteredModel("fake", "fixture", "test", "fake", "fake-v1", "0", "NONE", 512, "fixture", "TEST-ONLY", {"default": "0200: 00", "max_tokens": 8}))
    path = tmp_path / "registry.json"
    registry.save(path)
    result = qualify_registry(path, tmp_path / "qualification.json")
    assert result["qualified"] is True
    assert result["results"][0]["repeat_identical"] is True
    assert result["results"][0]["first_response_sha256"] == result["results"][0]["second_response_sha256"]
