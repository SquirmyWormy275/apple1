"""Synthetic transport checks; no model response rewriting or live inference."""
import json

import pytest

from neural1.application import effective_run_registry, preset
from neural1.core import Neural1Error
from neural1.models import OllamaHttpProvider
from neural1.provider_factory import provider_for
from neural1.registry import ModelRegistry, RegisteredModel


def model() -> RegisteredModel:
    return RegisteredModel('test', 'phi', 'test', 'ollama', 'phi:test', '3.8B', 'Q4_K_M', 2048, 'a' * 64, 'SYNTHETIC TRANSPORT TEST', {'api': 'chat'})


@pytest.mark.parametrize('api', ['chat', 'generate'])
def test_json_format_is_top_level_and_response_is_unchanged(api):
    raw_text = '```json\n{"invalid_fixture":true}\n```'
    def opener(request, timeout):
        body = json.loads(request.data)
        assert body['format'] == 'json'
        assert 'format' not in body['options']
        return json.dumps({'message': {'content': raw_text}, 'response': raw_text}).encode()
    provider = OllamaHttpProvider('x', api=api, format='json', opener=opener)
    result = provider.generate('Return JSON', agent_id='a', seed=1)
    assert result.text == raw_text  # Even a nonconforming provider is never repaired.
    assert result.provider_metadata['format'] == 'json'
    assert provider.record.generation['format'] == 'json'


def test_multiverse_effective_registry_only_sets_json_for_its_ollama_run(tmp_path):
    original = ModelRegistry({'test': model()})
    effective = effective_run_registry(original, preset('1976-multiverse', 'test', seed=1))
    effective.save(tmp_path / 'effective-registry.json')
    restored = ModelRegistry.load(tmp_path / 'effective-registry.json')
    provider = provider_for(restored.require('test'))
    assert isinstance(provider, OllamaHttpProvider)
    assert provider.format == 'json'
    assert 'format' not in provider.options
    assert 'format' not in original.require('test').generation_defaults
    for family in ('4k-mind', 'selfhost1', '256-byte-universe', 'ram-republic'):
        assert 'format' not in effective_run_registry(original, preset(family, 'test', seed=1)).require('test').generation_defaults


def test_rejects_misplaced_or_unsupported_format():
    with pytest.raises(Neural1Error, match='transport'):
        OllamaHttpProvider('x', options={'format': 'json'})
    with pytest.raises(Neural1Error, match='format'):
        OllamaHttpProvider('x', format='xml')
