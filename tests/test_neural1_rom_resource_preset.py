"""Bounded resource configuration, not a claim of live model qualification."""
from neural1.application import ApplicationConfig, effective_run_registry, preset
from neural1.registry import ModelRegistry, RegisteredModel


def test_rom_gets_seventeen_short_requests_without_mutating_source_registry():
    source = RegisteredModel('test', 'phi', 'test', 'ollama', 'phi:test', '3.8B', 'Q4_K_M', 4096, 'a' * 64, 'SYNTHETIC CONFIG TEST', {'timeout_seconds': 180, 'num_thread': 2, 'api': 'chat'})
    registry = ModelRegistry({'test': source})
    spec = preset('256-byte-universe', 'test', seed=1)
    assert spec.generations == 17 and spec.agents_per_cell == 1
    assert spec.max_tokens == 96 and spec.wall_clock_limit_seconds == 600
    configured = effective_run_registry(registry, spec).require('test')
    assert configured.generation_defaults['timeout_seconds'] == 180
    assert configured.generation_defaults['num_thread'] == 2
    assert configured.generation_defaults['max_tokens'] == 96
    assert source.generation_defaults['timeout_seconds'] == 180
    assert source.generation_defaults['num_thread'] == 2
    assert ApplicationConfig.__dataclass_fields__['temperature_limit'].default == 75.0
    for family in ('4k-mind', '1976-multiverse', 'selfhost1', 'ram-republic'):
        other = preset(family, 'test', seed=1)
        assert other.generations == 3
        settings = effective_run_registry(registry, other).require('test').generation_defaults
        assert settings['timeout_seconds'] == 180 and settings['num_thread'] == 2


def test_staged_rom_prompts_cover_each_block_then_only_execute():
    import pytest

    from neural1.core import Neural1Error
    from neural1.family_runner import family_objective

    first = family_objective('256-byte-universe', 0)
    assert '0400: A9 42' in first and '0200: A9 41' not in first
    for generation in range(1, 16):
        prompt = family_objective('256-byte-universe', generation)
        assert f'one deposit line at {0x200 + 16 * generation:04X}' in prompt
        assert 'exactly sixteen 00 padding bytes' in prompt
    final = family_objective('256-byte-universe', 16)
    assert '0200.0207 then 0200R' in final and 'Do not deposit' in final
    with pytest.raises(Neural1Error):
        family_objective('256-byte-universe', 17)


def test_staged_rom_actual_campaign_retains_model_bytes_and_exact_validation(tmp_path):
    import json

    from neural1.campaign import CampaignEngine
    from neural1.drivers import parse_commands
    from neural1.family_runner import family_objective
    from neural1.models import FakeProvider, GenerationResult

    class SyntheticStageProvider(FakeProvider):
        turn = 0

        def generate(self, prompt, *, agent_id, seed):
            generation = self.turn
            self.turn += 1
            assert prompt.startswith(family_objective('256-byte-universe', generation))
            if generation < 16:
                payload = bytes.fromhex('A9 41 20 EF FF 4C 1F FF') + bytes(8) if generation == 0 else bytes(16)
                text = f'{0x200 + generation * 16:04X}: ' + payload.hex(' ').upper()
            else:
                text = '0200.0207\n0200R'
            return GenerationResult(text)

    model = RegisteredModel('test', 'fixture', 'test', 'fake', 'test', '0', 'NONE', 4096, 'test', 'SYNTHETIC CONTROL', {})
    engine = CampaignEngine(tmp_path, ModelRegistry({'test': model}), {'test': SyntheticStageProvider()})
    spec = preset('256-byte-universe', 'test', seed=1)
    engine.run(spec, objective_factory=lambda cell, generation: family_objective(cell.experiment_id, generation), command_parser=parse_commands)
    result = json.loads(next(tmp_path.rglob('family-result.json')).read_text())
    assert result['passed'] and result['explicit_candidate_bytes'] == 256
    assert result['task'] == 'staged-rom-output-and-return-v4'
    records = next(tmp_path.rglob('transcript.jsonl')).read_text().splitlines()
    assert len(records) == 17
