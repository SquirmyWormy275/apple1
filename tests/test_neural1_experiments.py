from __future__ import annotations

from neural1.experiments import FourKMind, HistoricalComponent, MachineGenome, MultiverseValidator, RamRepublic, RomUniverse, SelfHost
from neural1.world import VirtualApple1World


def test_4k_context_reset_persists_only_world_state() -> None:
    world = VirtualApple1World()
    experiment = FourKMind(world)
    first = experiment.generation({"A": ["0200: CA FE"]})
    experiment = FourKMind(VirtualApple1World.restore(world.snapshot()))
    second = experiment.generation({"NEW-CONTEXT": ["0200.0201"]})
    assert first["generation"] == 1
    assert second["transcript"]["NEW-CONTEXT"] == ["0200: CA FE"]


def test_ram_republic_uses_shared_ram_not_agent_chat() -> None:
    world = VirtualApple1World(ram_budget=1024)
    republic = RamRepublic(world, {"A": lambda _: ["0200: 4D 53 47"], "B": lambda _: ["0200.0202"]})
    output = republic.round()
    assert output["B"] == ["0200: 4D 53 47"]


def test_rom_budget_is_exact_and_tests_are_deterministic() -> None:
    evaluator = RomUniverse()
    assert evaluator.evaluate(bytes(255), {}).passed is False
    score = evaluator.evaluate(bytes(range(256)), {"last-byte": lambda rom: rom[-1] == 255})
    assert score.passed is True


def test_selfhost_stage_four_requires_exact_rebuild() -> None:
    selfhost = SelfHost()
    selfhost.qualify(1, "RAW")
    selfhost.qualify(2, "ASM", parents=("RAW",))
    selfhost.qualify(3, "LANG", parents=("ASM",))
    assert selfhost.qualify(4, "BAD", parents=("LANG",), rebuild=lambda: b"x", expected=b"y").passed is False
    assert selfhost.qualify(4, "GOOD", parents=("LANG",), rebuild=lambda: b"x", expected=b"x").passed is True


def test_multiverse_rejects_unsourced_or_unknown_components() -> None:
    corpus = {"SYN-CPU": HistoricalComponent("SYN-CPU", "CPU", "SYNTHETIC", None, (), {}, False)}
    genome = MachineGenome("TEST", ("SYN-CPU", "MISSING"), (), {}, ())
    errors = MultiverseValidator().validate(genome, corpus)
    assert errors == ["unknown component: MISSING", "unsourced component: SYN-CPU"]
