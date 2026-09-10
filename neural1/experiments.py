"""Executable prototype experiment families sharing the NEURAL1 substrate."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import date
from typing import Any

from .core import Neural1Error, sha256_bytes
from .lineage import LineageGraph
from .world import VirtualApple1World, WozMonSession

EXPERIMENTS = ("4k-mind", "1976-multiverse", "selfhost1", "256-byte-universe", "ram-republic")


@dataclass(frozen=True)
class Score:
    passed: bool
    metrics: Mapping[str, float | int | str]


class FourKMind:
    """Generation/inheritance prototype; agents receive only a WozMon session."""

    def __init__(self, world: VirtualApple1World) -> None:
        self.world = world
        self.lineage = LineageGraph()

    def generation(self, actions: Mapping[str, list[str]]) -> dict[str, Any]:
        transcript: dict[str, list[str]] = {}
        for agent_id in sorted(actions):
            session = WozMonSession(self.world)
            transcript[agent_id] = [session.transact(command) for command in actions[agent_id]]
        self.world.generation += 1
        image = self.world.host_read(self.world.ram_start, self.world.ram_budget)
        parents = tuple(self.lineage.nodes)[-1:]
        node = self.lineage.add("ram-culture", sha256_bytes(image), parents=parents, mutation=f"generation {self.world.generation}")
        return {"generation": self.world.generation, "transcript": transcript, "lineage": node.node_id, "ram_sha256": node.artifact_hash}

    def catastrophe(self, address: int, length: int, *, kind: str = "delete") -> dict[str, Any]:
        if kind not in {"delete", "xor-ff"}:
            raise Neural1Error("unsupported catastrophe")
        self.world.intervene(address, length, xor_mask=0 if kind == "delete" else 0xFF)
        return {"kind": kind, "address": address, "length": length, "generation": self.world.generation}


@dataclass(frozen=True)
class HistoricalComponent:
    """Schema only. Synthetic fixtures must set authoritative=False."""

    part_id: str
    category: str
    manufacturer: str
    available_by: str | None
    source_ids: tuple[str, ...]
    attributes: Mapping[str, Any]
    authoritative: bool = False


@dataclass(frozen=True)
class MachineGenome:
    genome_id: str
    components: tuple[str, ...]
    interconnections: tuple[str, ...]
    memory_map: Mapping[str, str]
    timing_assumptions: tuple[str, ...]
    firmware_hash: str | None = None


class MultiverseValidator:
    def validate(self, genome: MachineGenome, corpus: Mapping[str, HistoricalComponent]) -> list[str]:
        errors = [f"unknown component: {part}" for part in genome.components if part not in corpus]
        errors.extend(f"unsourced component: {part}" for part in genome.components if part in corpus and not corpus[part].source_ids)
        return errors

    def validate_authoritative(self, genome: MachineGenome, corpus: Mapping[str, HistoricalComponent]) -> list[str]:
        errors = self.validate(genome, corpus)
        if not genome.components:
            errors.append("empty machine genome")
        if not genome.interconnections or not genome.memory_map or not genome.timing_assumptions:
            errors.append("machine structure is incomplete")
        for part in genome.components:
            component = corpus.get(part)
            if component is None:
                continue
            if not component.authoritative:
                errors.append(f"non-authoritative component: {part}")
            try:
                if component.available_by is None or date.fromisoformat(component.available_by) > date(1976, 12, 31):
                    errors.append(f"unqualified availability: {part}")
            except ValueError:
                errors.append(f"invalid availability: {part}")
        return errors


class SelfHost:
    STAGES = {1: "RAW_MACHINE_CODE", 2: "MODEL_CREATED_ASSEMBLER", 3: "MODEL_CREATED_LANGUAGE", 4: "SELF_HOSTING"}

    def __init__(self) -> None:
        self.artifacts: dict[str, dict[str, Any]] = {}

    def qualify(self, stage: int, artifact_id: str, *, parents: tuple[str, ...] = (), rebuild: Callable[[], bytes] | None = None, expected: bytes | None = None) -> Score:
        if stage not in self.STAGES or any(parent not in self.artifacts for parent in parents):
            raise Neural1Error("stage or bootstrap ancestry is invalid")
        if artifact_id in self.artifacts:
            raise Neural1Error("artifact identity already exists")
        if any(not self.artifacts[parent]["qualified"] for parent in parents):
            raise Neural1Error("bootstrap ancestry contains an unqualified artifact")
        parent_stages = {self.artifacts[parent]["stage"] for parent in parents}
        if (stage == 1 and parents) or (stage > 1 and (stage - 1 not in parent_stages or any(value >= stage for value in parent_stages))):
            raise Neural1Error("bootstrap ancestry violates legal stage progression")
        passed = stage < 4 or (rebuild is not None and expected is not None and bool(expected) and rebuild() == expected)
        self.artifacts[artifact_id] = {"stage": stage, "parents": parents, "qualified": passed}
        return Score(passed, {"stage": stage, "criterion": self.STAGES[stage]})


class RomUniverse:
    def evaluate(
        self, rom: bytes, tests: Mapping[str, Callable[[bytes], bool]], *,
        known_good: bytes | None = None, known_bad: bytes | None = None,
    ) -> Score:
        if len(rom) != 256:
            return Score(False, {"bytes": len(rom), "budget": 256, "reason": "EXACT_BUDGET_FAILED"})
        if not tests or any(not name.strip() for name in tests):
            return Score(False, {"reason": "MEANINGFUL_TESTS_REQUIRED"})
        if known_good is None or known_bad is None or len(known_good) != 256 or len(known_bad) != 256:
            return Score(False, {"reason": "EXACT_SIZE_CONTROLS_REQUIRED"})
        try:
            controls = all(bool(test(known_good)) and not bool(test(known_bad)) for test in tests.values())
            if not controls:
                return Score(False, {"reason": "BEHAVIORAL_CONTROLS_FAILED"})
            results = {name: bool(test(rom)) for name, test in sorted(tests.items())}
        except Exception as error:
            return Score(False, {"reason": "BEHAVIORAL_TEST_ERROR", "error_type": type(error).__name__})
        return Score(all(results.values()), {"bytes": 256, "controls_passed": 1, **{name: int(value) for name, value in results.items()}})


class RamRepublic:
    """Round-robin logical agents communicate only through the shared session."""

    def __init__(self, world: VirtualApple1World, agents: Mapping[str, Callable[[WozMonSession], list[str]]]) -> None:
        self.world = world
        self.agents = dict(agents)
        self.turn = 0

    def round(self) -> dict[str, list[str]]:
        output: dict[str, list[str]] = {}
        for agent_id in sorted(self.agents):
            session = WozMonSession(self.world)
            output[agent_id] = [session.transact(command) for command in self.agents[agent_id](session)]
        self.turn += 1
        return output
