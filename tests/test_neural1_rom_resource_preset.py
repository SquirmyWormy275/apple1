"""Bounded resource configuration, not a claim of live model qualification."""
from neural1.application import ApplicationConfig, effective_run_registry, preset
from neural1.registry import ModelRegistry, RegisteredModel


def test_rom_gets_one_long_bounded_request_without_mutating_source_registry():
    source = RegisteredModel('test', 'phi', 'test', 'ollama', 'phi:test', '3.8B', 'Q4_K_M', 4096, 'a' * 64, 'SYNTHETIC CONFIG TEST', {'timeout_seconds': 180, 'num_thread': 2, 'api': 'chat'})
    registry = ModelRegistry({'test': source})
    spec = preset('256-byte-universe', 'test', seed=1)
    assert spec.generations == 1 and spec.agents_per_cell == 1
    assert spec.max_tokens == 1024 and spec.wall_clock_limit_seconds == 600
    configured = effective_run_registry(registry, spec).require('test')
    assert configured.generation_defaults['timeout_seconds'] == 570
    assert configured.generation_defaults['num_thread'] == 1
    assert configured.generation_defaults['max_tokens'] == 1024
    assert source.generation_defaults['timeout_seconds'] == 180
    assert source.generation_defaults['num_thread'] == 2
    assert ApplicationConfig.__dataclass_fields__['temperature_limit'].default == 75.0
    for family in ('4k-mind', '1976-multiverse', 'selfhost1', 'ram-republic'):
        other = preset(family, 'test', seed=1)
        assert other.generations == 3
        settings = effective_run_registry(registry, other).require('test').generation_defaults
        assert settings['timeout_seconds'] == 180 and settings['num_thread'] == 2
