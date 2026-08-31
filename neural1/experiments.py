"""Executable prototype experiment families sharing the NEURAL1 substrate."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Mapping

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
        node = self.lineage.add("ram-culture", sha256_bytes(image), mutation=f"generation {self.world.generation}")
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


class SelfHost:
    STAGES = {1: "RAW_MACHINE_CODE", 2: "MODEL_CREATED_ASSEMBLER", 3: "MODEL_CREATED_LANGUAGE", 4: "SELF_HOSTING"}

    def __init__(self) -> None:
        self.artifacts: dict[str, dict[str, Any]] = {}

    def qualify(self, stage: int, artifact_id: str, *, parents: tuple[str, ...] = (), rebuild: Callable[[], bytes] | None = None, expected: bytes | None = None) -> Score:
        if stage not in self.STAGES or any(parent not in self.artifacts for parent in parents):
            raise Neural1Error("stage or bootstrap ancestry is invalid")
        passed = stage < 4 or (rebuild is not None and expected is not None and rebuild() == expected)
        self.artifacts[artifact_id] = {"stage": stage, "parents": parents, "qualified": passed}
        return Score(passed, {"stage": stage, "criterion": self.STAGES[stage]})


class RomUniverse:
    def evaluate(self, rom: bytes, tests: Mapping[str, Callable[[bytes], bool]]) -> Score:
        if len(rom) != 256:
            return Score(False, {"bytes": len(rom), "budget": 256, "reason": "EXACT_BUDGET_FAILED"})
        results = {name: bool(test(rom)) for name, test in sorted(tests.items())}
        return Score(all(results.values()), {"bytes": 256, **{name: int(value) for name, value in results.items()}})


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
