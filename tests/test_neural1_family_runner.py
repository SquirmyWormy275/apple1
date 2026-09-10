from __future__ import annotations

from typing import Any

import pytest

from neural1.core import Neural1Error
from neural1.experiments import RomUniverse, SelfHost
from neural1.family_runner import evaluate_family, family_objective
from neural1.models import FakeProvider
from neural1.scheduling import LogicalAgent, PopulationScheduler
from neural1.world import VirtualApple1World, WozMonSession

PROGRAM = "0200: A9 41 20 EF FF 4C 1F FF"


def transcript(world: VirtualApple1World, *, agents: int = 1, exact: bool = False) -> list[dict[str, Any]]:
    records = []
    for generation in range(2):
        for agent in range(agents):
            commands = [PROGRAM, "0200.020F", "0200R"]
            if exact:
                commands = ["0200: " + " ".join(f"{byte:02X}" for byte in bytes.fromhex("A9 41 20 EF FF 4C 1F FF") + bytes(248)), "0200R"]
            records.append({"generation": generation, "agent_id": str(agent), "response": "\n".join(commands), "outputs": [WozMonSession(world).transact(command) for command in commands]})
    world.generation = 2
    return records


def test_rom_rejects_empty_and_vacuous_checks() -> None:
    rom = RomUniverse()
    assert not rom.evaluate(bytes(256), {}).passed
    assert not rom.evaluate(bytes(256), {"always": lambda _: True}, known_good=bytes(256), known_bad=bytes(256)).passed
    assert not rom.evaluate(bytes(256), {"name": lambda _: True}).passed


def test_selfhost_rejects_unqualified_skipped_and_replaced_ancestry() -> None:
    sh = SelfHost()
    sh.qualify(1, "raw")
    with pytest.raises(Neural1Error, match="progression"):
        sh.qualify(3, "skip", parents=("raw",))
    sh.qualify(2, "asm", parents=("raw",))
    sh.qualify(3, "lang", parents=("asm",))
    assert not sh.qualify(4, "failed", parents=("lang",), expected=b"x", rebuild=lambda: b"y").passed
    with pytest.raises(Neural1Error, match="unqualified"):
        sh.qualify(4, "child", parents=("failed", "lang"))
    with pytest.raises(Neural1Error, match="already exists"):
        sh.qualify(1, "raw")
    with pytest.raises(Neural1Error, match="progression"):
        sh.qualify(2, "orphan")


@pytest.mark.parametrize("family,agents,exact", [("4k-mind", 1, False), ("selfhost1", 1, False), ("256-byte-universe", 1, True), ("ram-republic", 2, False)])
def test_family_evaluates_real_virtual_execution(family: str, agents: int, exact: bool) -> None:
    world = VirtualApple1World()
    records = transcript(world, agents=agents, exact=exact)
    snapshot = world.snapshot()
    result = evaluate_family(family, world, records)
    assert result["passed"]
    assert result["independent_execution"]["screen_text"] == "A"
    assert world.snapshot() == snapshot  # independent evaluator cannot alter experiment
    assert family_objective(family)


def test_exact_rom_rejects_implicit_zero_padding() -> None:
    world = VirtualApple1World()
    records = transcript(world)
    assert not evaluate_family("256-byte-universe", world, records)["passed"]


def test_ram_rejects_single_participant() -> None:
    world = VirtualApple1World()
    assert not evaluate_family("ram-republic", world, transcript(world))["passed"]


def test_multiverse_does_not_promote_empty_evidence() -> None:
    result = evaluate_family("1976-multiverse", VirtualApple1World(), [])
    assert result["status"] == "EVALUATED"
    assert not result["passed"]


def test_scheduler_observations_remain_private() -> None:
    world = VirtualApple1World()
    agents = [LogicalAgent("A", "p"), LogicalAgent("B", "p")]
    scheduler = PopulationScheduler(world, agents, {"p": FakeProvider(default="0200: 41")}, seed=1)
    scheduler.round("observe", lambda response: [response])
    agents[0].private_context.append("PRIVATE_A")
    turns = scheduler.round("observe", lambda response: [response])
    assert "WOZMON:0200: 41" in turns[0].prompt
    assert "PRIVATE_A" in turns[0].prompt
    assert "PRIVATE_A" not in turns[1].prompt
    snapshot = world.snapshot()
    agents[0].reset_context()
    assert not agents[0].private_context
    assert world.snapshot() == snapshot


def test_historical_console_corpus_and_proposal_controls() -> None:
    import json

    from neural1.family_runner import process_multiverse_response
    from neural1.history import load_console_corpus

    corpus = load_console_corpus()
    assert len(corpus.components) == 2
    assert all(item.authoritative for item in corpus.components.values())
    assert all(item.attributes["price_usd"] is None for item in corpus.components.values())
    proposal = {"genome_id": "CONTROL", "components": ["MOS6502", "DRAM4096-BANK"], "interconnections": ["MOS6502->DRAM4096-BANK"], "memory_map": {"DRAM4096-BANK": "2000-2FFF"}, "timing_assumptions": ["EXTERNAL_DRAM_REFRESH_REQUIRED"]}
    response = json.dumps(proposal)
    good = process_multiverse_response(response)
    assert good["accepted_proposals"] == 1
    assert good["source_sha256"]
    actual = evaluate_family("1976-multiverse", VirtualApple1World(), [{"response": response, "proposal": good}])
    assert actual["passed"]
    proposal["memory_map"] = {"DRAM4096-BANK": "2000-3000"}
    assert process_multiverse_response(json.dumps(proposal))["accepted_proposals"] == 0
    proposal["components"] = ["MODERN-CPU", "DRAM4096-BANK"]
    assert process_multiverse_response(json.dumps(proposal))["accepted_proposals"] == 0
    for invalid in ("not json", "[]", "null", '{"genome_id": 9}'):
        assert process_multiverse_response(invalid)["accepted_proposals"] == 0


def test_exact_256_sixteen_lines_fit_strict_parser_and_bad_code_fails() -> None:
    from neural1.drivers import parse_commands

    image = bytes.fromhex("A9 41 20 EF FF 4C 1F FF") + bytes(248)
    for candidate, passed in ((image, True), (bytes(256), False)):
        world = VirtualApple1World()
        lines = [f"{0x200 + offset:04X}: " + " ".join(f"{byte:02X}" for byte in candidate[offset:offset + 16]) for offset in range(0, 256, 16)]
        response = "\n".join([*lines, "0200.020F", "0200R"])
        commands = parse_commands(response)
        assert len(commands) == 18
        records = [{"agent_id": "A", "generation": 0, "response": response, "outputs": [WozMonSession(world).transact(command) for command in commands]}]
        result = evaluate_family("256-byte-universe", world, records)
        assert result["exact_deposition"]
        assert result["passed"] is passed


def test_exact_rom_rejects_generated_code_and_external_data_access() -> None:
    from neural1.family_runner import _output_task

    routine = bytes.fromhex("A9 41 20 EF FF 4C 1F FF")
    # Exact-size loader expands a program at 0300; this used to pass.
    loader = b"".join(bytes([0xA9, byte, 0x8D, index, 3]) for index, byte in enumerate(routine)) + bytes.fromhex("4C 00 03")
    assert not _output_task(loader + bytes(256 - len(loader)))
    # Even an irrelevant external read is outside the declared candidate workspace.
    external_read = bytes.fromhex("AD 00 03") + routine
    assert not _output_task(external_read + bytes(256 - len(external_read)))
    assert _output_task(routine + bytes(248))  # declared Monitor call stack remains available


def test_selfhost_hash_covers_dependency_beyond_first_256_bytes() -> None:
    from neural1.core import sha256_bytes

    hashes = []
    for ascii_byte, passed in (("41", True), ("42", False)):
        world = VirtualApple1World()
        commands = ["0200: 4C 00 03", f"0300: A9 {ascii_byte} 20 EF FF 4C 1F FF", "0200R"]
        records = [{"agent_id": "A", "generation": 0, "response": "\n".join(commands), "outputs": [WozMonSession(world).transact(command) for command in commands]}]
        result = evaluate_family("selfhost1", world, records)
        assert result["passed"] is passed
        assert result["artifact_bytes"] == 4096
        assert result["artifact_sha256"] == sha256_bytes(world.host_read(0x200, 4096))
        hashes.append(result["artifact_sha256"])
    assert hashes[0] != hashes[1]


def test_guided_starting_prompts_bound_response_without_provider_fallback() -> None:
    example = "0400: A9 42 20 EF FF 4C 1F FF\n0400.0407\n0400R"
    for family in ("4k-mind", "selfhost1", "ram-republic"):
        prompt = family_objective(family)
        assert example in prompt and "not a discovery task" in prompt
        assert "only the three new command lines" in prompt
        assert "Do not repeat the example, add padding" in prompt
        assert "the examination of 0200.0207, and 0200R" in prompt
        assert "0200: A9 41" not in prompt  # requested answer is not a substitute response
    rom = family_objective("256-byte-universe")
    assert example in rom and "exactly eighteen lines" in rom
    assert "only the three new command lines" not in rom
    assert "Do not repeat the example, add padding" not in rom
    assert "sixteen 00 bytes" in rom and "Line 18: 0200R" in rom
    assert "not a complete or blinded monitor" in rom


def test_guided_criterion_is_recorded_only_for_guided_actual_prompts() -> None:
    world = VirtualApple1World()
    records = transcript(world)
    assert evaluate_family("4k-mind", world, records)["task"] == "bounded-output-and-return-v1"
    for record in records:
        record["prompt"] = "ISA-guided execution control, not a discovery task."
    assert evaluate_family("4k-mind", world, records)["task"] == "isa-guided-output-and-return-v2"
    for record in records:
        record["prompt"] = family_objective("4k-mind")
    result = evaluate_family("4k-mind", world, records)
    assert result["task"] == "guided-format-output-and-return-v3"
    assert result["passed"]


def test_qualified_format_example_is_not_executed_as_the_new_program() -> None:
    world = VirtualApple1World()
    response = "0400: A9 42 20 EF FF 4C 1F FF\n0400.0407\n0400R"
    from neural1.drivers import parse_commands
    commands = parse_commands(response)
    record = {"generation": 0, "agent_id": "A", "prompt": family_objective("selfhost1"), "response": response, "outputs": [WozMonSession(world).transact(command) for command in commands]}
    result = evaluate_family("selfhost1", world, [record])
    assert not result["passed"] and not result["execution_requested"]
    assert world.host_read(0x200, 8) == bytes(8)
