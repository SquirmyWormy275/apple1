"""Resume retains original model transport and objective semantics."""
import io
import json
from dataclasses import replace

import pytest

from neural1.application import check_model, execution_objective, preset, registry_for_execution
from neural1.core import Neural1Error
from neural1.family_runner import family_objective, legacy_rom_objective
from neural1.registry import ModelRegistry, RegisteredModel


def test_resume_retains_registry_bytes_and_checks_recorded_live_identity(tmp_path, monkeypatch):
    model = RegisteredModel('test', 'phi', 'test', 'ollama', 'phi:test', '3.8B', 'Q4_K_M', 4096, 'a' * 64, 'SYNTHETIC', {'timeout_seconds': 570, 'num_thread': 1, 'max_tokens': 1024, 'api': 'chat'})
    recorded = ModelRegistry({'test': model})
    path = tmp_path / 'effective-registry.json'
    recorded.save(path)
    original = path.read_bytes()
    current = ModelRegistry({'test': replace(model, digest='b' * 64, generation_defaults={'timeout_seconds': 180, 'num_thread': 2})})
    spec = preset('256-byte-universe', 'test', seed=1)
    selected = registry_for_execution(current, spec, tmp_path, resume=True)
    assert selected.require('test') == model
    assert path.read_bytes() == original
    monkeypatch.setattr('neural1.application.urlopen', lambda *a, **kw: io.StringIO(json.dumps({'models': [{'name': 'phi:test', 'digest': 'a' * 64}]})))
    assert check_model(selected, 'test')['digest'] == 'a' * 64
    with pytest.raises(Neural1Error, match='identity differs'):
        check_model(current, 'test')
    with pytest.raises(Neural1Error, match='resume this run'):
        registry_for_execution(current, spec, tmp_path, resume=False)
    path.unlink()
    with pytest.raises(Neural1Error, match='original effective registry'):
        registry_for_execution(current, spec, tmp_path, resume=True)


def test_legacy_rom_resumes_recorded_constant_objective_not_new_stages(tmp_path):
    staged = preset('256-byte-universe', 'test', seed=1)
    assert staged.generation_settings['objective_protocol'] == 'staged-rom-v4'
    legacy = replace(staged, generations=3, max_tokens=1024, generation_settings={'context_reset_generations': 2})
    transcript = tmp_path / 'cells/CELL/transcript.jsonl'
    transcript.parent.mkdir(parents=True)
    original = 'Actual historical complete256 objective, unmodified.'
    transcript.write_text(json.dumps({'generation': 0, 'prompt': original}) + '\n')
    for generation in (1, 2):
        assert execution_objective(legacy, tmp_path, '256-byte-universe', generation) == original
    assert execution_objective(staged, tmp_path, '256-byte-universe', 2) == family_objective('256-byte-universe', 2)
    transcript.unlink()
    assert execution_objective(legacy, tmp_path, '256-byte-universe', 2) == legacy_rom_objective()
    assert 'exactly eighteen lines' in legacy_rom_objective()
    assert 'Staged instruction-guided' not in legacy_rom_objective()
    unknown = replace(staged, generation_settings={'objective_protocol': 'future-version'})
    with pytest.raises(Neural1Error, match='compatible release'):
        execution_objective(unknown, tmp_path, '256-byte-universe', 0)
