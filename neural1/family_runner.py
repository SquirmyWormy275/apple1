"""Bounded family tasks and deterministic acceptance of actual campaign evidence.

These starting tasks do not claim compiler discovery, protocol emergence, or a
complete replacement monitor. Provider transcripts remain the source of bytes.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import asdict
from typing import Any

from .core import Neural1Error, sha256_bytes
from .experiments import EXPERIMENTS, FourKMind, HistoricalComponent, MachineGenome, MultiverseValidator, RamRepublic, RomUniverse, SelfHost
from .world import VirtualApple1World, WozMonSession

_COMMON = (
    "ISA-guided execution control, not a discovery task. Use the supplied NMOS 6502 baseline.\n"
    "ISA reference: LDA immediate = A9 byte; JSR absolute = 20 low-byte high-byte; "
    "JMP absolute = 4C low-byte high-byte. ASCII A = 41. "
    "Monitor ECHO = FFEF; Monitor return = FF1F.\n"
    "The complete eight-byte baseline is: A9 41 20 EF FF 4C 1F FF.\n"
    "Return uppercase Woz Monitor commands only. No prose, Markdown, fences, numbering or assembly mnemonics.\n"
)

_THREE_LINE_FORMAT = (
    "Output exactly three lines and nothing else.\n"
    "Line 1: deposit exactly the eight baseline bytes at 0200 using ADDRESS: XX XX syntax. "
    "Do not append zeros or any other bytes.\n"
    "Line 2: 0200.0207\n"
    "Line 3: 0200R\n"
)

_ROM_FORMAT = (
    "Output exactly eighteen lines and nothing else.\n"
    "The first sixteen lines deposit sixteen bytes each at addresses 0200, 0210, 0220, 0230, "
    "0240, 0250, 0260, 0270, 0280, 0290, 02A0, 02B0, 02C0, 02D0, 02E0, 02F0. "
    "Use ADDRESS: XX XX syntax. The 0200 line contains the eight baseline bytes followed by eight 00 bytes. "
    "Every other deposit line contains sixteen 00 bytes. Write every byte explicitly, with no ellipses.\n"
    "Line 17: 0200.0207\n"
    "Line 18: 0200R\n"
)


def family_objective(family: str) -> str:
    if family not in EXPERIMENTS:
        raise Neural1Error("unknown experiment family")
    if family == "1976-multiverse":
        from .history import load_console_corpus
        corpus = load_console_corpus()
        components = [{"id": item.part_id, "category": item.category, "capabilities": item.attributes} for item in corpus.components.values()]
        return (
            "YEAR_END_1976_12_31 bounded structural design. Select the documented CPU and RAM bank; "
            "propose a contiguous 4096-byte RAM placement in 16-bit address space and a CPU-to-RAM connection. "
            "Include EXTERNAL_DRAM_REFRESH_REQUIRED in timing_assumptions. This is a structural hypothesis, not electrical/cost proof. "
            "Only component capabilities are supplied; reference machine genome is withheld. "
            "Return ONLY one JSON object with keys genome_id (string), components (list of component IDs), "
            "interconnections (list of strings formatted SOURCE->DESTINATION), memory_map (object mapping RAM component ID to XXXX-YYYY uppercase hexadecimal inclusive range), "
            "timing_assumptions (list of strings explaining refresh). No prose or Markdown. "
            "Do not invent parts, device prices or maximum clock ratings. Available corpus: " + json.dumps(components, sort_keys=True)
        )
    additions = {
        "4k-mind": "Your world persists across generations within 4K. No host memory access is available.",
        "selfhost1": "Stage 1 only: establish a raw machine-code validation routine. This does not qualify an assembler or compiler.",
        "256-byte-universe": "The candidate is exactly 256 bytes at 0200 through 02FF. Code and data stay inside this range; only the NMOS call stack at 0100-01FF and declared Monitor calls are external. This ISA-guided task tests output and Monitor return, not a complete or blinded monitor.",
        "ram-republic": "Read the supplied CURRENT SHARED MONITOR EXAMINATION before answering. It is the allowed view of other participants through RAM; private contexts remain isolated. This ISA-guided routine is a shared-memory execution control, not protocol discovery.",
    }
    response_format = _ROM_FORMAT if family == "256-byte-universe" else _THREE_LINE_FORMAT
    return _COMMON + additions[family] + "\n" + response_format


def _output_task(image: bytes) -> bool:
    world = VirtualApple1World()
    world.host_write(0x200, image)
    result = world.execute(0x200, max_instructions=128, trace_limit=0, candidate_limit=256)
    return result.screen_text == "A" and result.stop_reason == "MONITOR_WARM_ENTRY"


def evaluate_family(
    family: str,
    world: VirtualApple1World,
    records: Sequence[Mapping[str, Any]],
    *,
    corpus: Mapping[str, HistoricalComponent] | None = None,
    genome: MachineGenome | None = None,
) -> dict[str, Any]:
    """Independently evaluate a bounded campaign without mutating its world.

    ``records`` must be the actual persisted transcript, in execution order.
    Historical design validation needs an explicitly supplied reviewed corpus.
    """
    from .drivers import parse_commands

    if family not in EXPERIMENTS:
        raise Neural1Error("unknown experiment family")
    guided = any("ISA-guided execution control" in str(record.get("prompt", "")) for record in records)
    base: dict[str, Any] = {"family": family, "target": "VIRTUAL", "task": "isa-guided-output-and-return-v2" if guided else "bounded-output-and-return-v1", "passed": False}
    if family == "1976-multiverse":
        base["task"] = "period-component-structure-validation-v1"
        if genome is not None and corpus is not None:
            errors = MultiverseValidator().validate_authoritative(genome, corpus)
            return {**base, "status": "EVALUATED", "passed": not errors, "errors": errors, "genome": asdict(genome)}
        proposals = [process_multiverse_response(str(record.get("response", ""))) for record in records if "error" not in record]
        unavailable = any(item.get("status") == "BLOCKED" for item in proposals)
        return {**base, "status": "BLOCKED" if unavailable else "EVALUATED", "passed": any(item["accepted_proposals"] > 0 for item in proposals), "proposals": proposals, "scope": "provenance and bounded structure only; no cost, electrical or complete-board claims"}

    commands_by_generation: dict[int, dict[str, list[str]]] = {}
    covered: set[int] = set()
    outside_rom = False
    accepted = 0
    observed_agents: set[str] = set()
    participants: set[str] = set()
    execution_requested = False
    for record in records:
        if "error" in record:
            continue
        agent = str(record.get("agent_id", ""))
        participants.add(agent)
        if any(isinstance(item, Mapping) and item.get("command") == "0200.020F" and not str(item.get("output", "ERR")).startswith("ERR") for item in record.get("observations", ())):
            observed_agents.add(agent)
        commands = list(parse_commands(str(record.get("response", ""))))
        outputs = list(record.get("outputs", ()))
        commands_by_generation.setdefault(int(record.get("generation", 0)), {}).setdefault(agent, []).extend(commands)
        for command, output in zip(commands, outputs, strict=False):
            if str(output).startswith("ERR"):
                continue
            accepted += 1
            if command == "0200R":
                execution_requested = True
            if ":" in command:
                address, values = command.split(":", 1)
                locations = set(range(int(address, 16), int(address, 16) + len(values.split())))
                covered.update(locations)
                outside_rom |= bool(locations - set(range(0x200, 0x300)))
            elif not command.endswith("R") and "." in command:
                observed_agents.add(agent)
    image = world.host_read(0x200, min(256, world.ram_budget))
    checked_world = VirtualApple1World.restore(world.snapshot())
    execution = checked_world.execute(0x200, max_instructions=128, trace_limit=16, candidate_limit=256 if family == "256-byte-universe" else None)
    behavior = execution.screen_text == "A" and execution.stop_reason == "MONITOR_WARM_ENTRY"
    base.update(status="EVALUATED", accepted_transactions=accepted, execution_requested=execution_requested, independent_execution=asdict(execution), artifact_sha256=sha256_bytes(image))
    healthy = accepted > 0 and execution_requested and not any("error" in record for record in records)

    if family == "256-byte-universe":
        # Controls belong exclusively to the evaluator; never insert them into a live world.
        good = bytes.fromhex("A9 41 20 EF FF 4C 1F FF") + bytes(248)
        score = RomUniverse().evaluate(image, {"output-A-and-return": _output_task}, known_good=good, known_bad=bytes(256))
        exact = covered == set(range(0x200, 0x300)) and not outside_rom
        return {**base, "passed": healthy and exact and score.passed, "score": asdict(score), "explicit_candidate_bytes": len(covered), "exact_deposition": exact, "memory_policy": {"candidate": "0200-02FF", "call_stack": "0100-01FF", "external_services": ["FFEF read-only ECHO stub", "FF1F stop sentinel"], "expanded_code_or_data": "REJECTED"}}
    if family == "selfhost1":
        bootstrap = SelfHost()
        artifact = world.host_read(world.ram_start, world.ram_budget)
        artifact_hash = sha256_bytes(artifact)
        score = bootstrap.qualify(1, artifact_hash)
        # Stage-one qualification additionally requires the declared executable task.
        bootstrap.artifacts[artifact_hash]["qualified"] = healthy and behavior
        return {**base, "passed": healthy and behavior and score.passed, "stage": 1, "artifact_sha256": artifact_hash, "artifact_start": world.ram_start, "artifact_bytes": len(artifact), "artifacts": bootstrap.artifacts, "later_stages": "not attempted; qualified ancestry and exact rebuild required"}
    if family == "4k-mind":
        replay = FourKMind(VirtualApple1World(ram_budget=4096))
        generations = [replay.generation(commands_by_generation[key]) for key in sorted(commands_by_generation)]
        matches = replay.world.host_read(0x200, 4096) == world.host_read(0x200, world.ram_budget)
        return {**base, "passed": healthy and behavior and world.ram_budget == 4096 and len(generations) >= 2 and matches, "generations": generations, "lineage": replay.lineage.records(), "replay_matches": matches}
    republic_world = VirtualApple1World(ram_budget=world.ram_budget)
    republic_rounds = []
    for generation in sorted(commands_by_generation):
        def actor(commands: list[str]) -> Any:
            def act(_session: WozMonSession) -> list[str]:
                return commands
            return act
        republic = RamRepublic(republic_world, {agent: actor(commands) for agent, commands in commands_by_generation[generation].items()})
        republic_rounds.append(republic.round())
    shared_state_matches = republic_world.host_read(0x200, world.ram_budget) == world.host_read(0x200, world.ram_budget)
    return {**base, "shared_state_replay_matches": shared_state_matches, "shared_rounds": republic_rounds, "passed": healthy and behavior and shared_state_matches and len(participants) >= 2 and observed_agents == participants and len(commands_by_generation) >= 2, "participants": sorted(participants), "participants_observing_ram": sorted(observed_agents), "rounds": len(commands_by_generation), "scope": "shared-memory participation; no emergent protocol claim"}


def process_multiverse_response(text: str) -> dict[str, Any]:
    """Parse a model's bounded JSON genome and apply source/structure checks."""
    from .history import load_console_corpus
    try:
        corpus = load_console_corpus()
    except (OSError, ValueError, Neural1Error) as error:
        return {"status": "BLOCKED", "accepted_proposals": 0, "genome": None, "errors": [str(error)], "outputs": ["Corpus unavailable: " + str(error)]}
    genome: MachineGenome | None = None
    errors: list[str] = []
    try:
        if len(text) > 32768:
            raise ValueError("proposal exceeds 32768 characters")
        payload = json.loads(text)
        required = {"genome_id", "components", "interconnections", "memory_map", "timing_assumptions"}
        if not isinstance(payload, dict) or set(payload) != required:
            raise ValueError("proposal keys must exactly match the declared genome schema")
        if not isinstance(payload["genome_id"], str) or not payload["genome_id"].strip():
            raise ValueError("genome_id must be a nonempty string")
        for key in ("components", "interconnections", "timing_assumptions"):
            if not isinstance(payload[key], list) or not all(isinstance(item, str) and item.strip() for item in payload[key]):
                raise ValueError(key + " must be a list of nonempty strings")
        if not isinstance(payload["memory_map"], dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in payload["memory_map"].items()):
            raise ValueError("memory_map must map component IDs to address ranges")
        genome = MachineGenome(payload["genome_id"], tuple(payload["components"]), tuple(payload["interconnections"]), payload["memory_map"], tuple(payload["timing_assumptions"]))
        errors.extend(MultiverseValidator().validate_authoritative(genome, corpus.components))
        if set(genome.components) != set(corpus.components) or len(genome.components) != len(corpus.components):
            errors.append("bounded task requires exactly one documented CPU and one RAM bank")
        if set(genome.interconnections) != {"MOS6502->DRAM4096-BANK"}:
            errors.append("declare the CPU-to-RAM connection as MOS6502->DRAM4096-BANK")
        if set(genome.memory_map) != {"DRAM4096-BANK"}:
            errors.append("map exactly the documented RAM bank")
        region = genome.memory_map.get("DRAM4096-BANK", "")
        if not re.fullmatch(r"[0-9A-F]{4}-[0-9A-F]{4}", region):
            errors.append("RAM range must be XXXX-YYYY inclusive uppercase hex")
        else:
            start, end = (int(value, 16) for value in region.split("-"))
            if end - start + 1 != 4096:
                errors.append("RAM range must contain exactly 4096 bytes")
        if "EXTERNAL_DRAM_REFRESH_REQUIRED" not in genome.timing_assumptions:
            errors.append("timing_assumptions must include EXTERNAL_DRAM_REFRESH_REQUIRED")
    except (ValueError, TypeError, KeyError) as error:
        errors.append(str(error))
    accepted = int(genome is not None and not errors)
    source_hashes = {key: source.sha256 for key, source in corpus.sources.items()}
    return {"status": "EVALUATED", "accepted_proposals": accepted, "genome": asdict(genome) if genome else None, "errors": errors, "outputs": errors or ["ACCEPTED: source-backed bounded CPU/RAM structure; physical feasibility unproven"], "source_sha256": source_hashes, "world_id": "YEAR_END_1976_12_31"}
