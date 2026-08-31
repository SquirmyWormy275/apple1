"""Deterministic logical-agent scheduling, selection, migration, and evaluation."""

from __future__ import annotations

import random
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from statistics import fmean, stdev

from .core import Neural1Error
from .models import ModelProvider
from .world import VirtualApple1World, WozMonSession


@dataclass
class LogicalAgent:
    agent_id: str
    provider_key: str
    private_context: list[str] = field(default_factory=list)
    turns: int = 0

    def reset_context(self) -> None:
        self.private_context.clear()


@dataclass(frozen=True)
class AgentTurn:
    agent_id: str
    provider_key: str
    seed: int
    prompt: str
    response: str
    monitor_outputs: tuple[str, ...]


class PopulationScheduler:
    def __init__(self, world: VirtualApple1World, agents: Sequence[LogicalAgent], providers: Mapping[str, ModelProvider], *, seed: int) -> None:
        if len({agent.agent_id for agent in agents}) != len(agents):
            raise Neural1Error("agent IDs must be unique")
        if any(agent.provider_key not in providers for agent in agents):
            raise Neural1Error("agent references an unknown provider")
        self.world, self.agents, self.providers, self.seed = world, list(agents), dict(providers), seed
        self.round_number = 0

    def round(self, objective: str, command_parser: Callable[[str], Sequence[str]]) -> list[AgentTurn]:
        rng = random.Random(f"{self.seed}:{self.round_number}")  # noqa: S311 - reproducible schedule, not cryptography
        turns = []
        for agent in sorted(self.agents, key=lambda item: item.agent_id):
            turn_seed = rng.randrange(0, 2**31)
            prompt = "\n".join([objective, *agent.private_context[-8:]])
            result = self.providers[agent.provider_key].generate(prompt, agent_id=agent.agent_id, seed=turn_seed)
            commands = command_parser(result.text)
            session = WozMonSession(self.world)
            outputs = tuple(session.transact(command) for command in commands)
            agent.private_context.extend([f"MODEL:{result.text}", *[f"WOZMON:{item}" for item in outputs]])
            agent.turns += 1
            turns.append(AgentTurn(agent.agent_id, agent.provider_key, turn_seed, prompt, result.text, outputs))
        self.round_number += 1
        return turns

    def rotate_provider(self, agent_id: str, provider_key: str) -> None:
        if provider_key not in self.providers:
            raise Neural1Error("unknown provider")
        next(agent for agent in self.agents if agent.agent_id == agent_id).provider_key = provider_key


@dataclass(frozen=True)
class MigrationRecord:
    source_colony: str
    destination_colony: str
    address: int
    length: int
    artifact_sha256: str


def migrate(source_id: str, source: VirtualApple1World, destination_id: str, destination: VirtualApple1World, address: int, length: int) -> MigrationRecord:
    from .core import sha256_bytes
    payload = source.host_read(address, length)
    destination.host_write(address, payload)
    return MigrationRecord(source_id, destination_id, address, length, sha256_bytes(payload))


@dataclass(frozen=True)
class ArchaeologyScore:
    exact_bytes_identified: int
    total_bytes: int
    calling_convention_identified: bool
    memory_map_identified: bool

    @property
    def byte_accuracy(self) -> float:
        return self.exact_bytes_identified / self.total_bytes if self.total_bytes else 0.0


@dataclass(frozen=True)
class SummaryStatistics:
    count: int
    mean: float | None
    standard_deviation: float | None
    minimum: float | None
    maximum: float | None


def summarize(values: Sequence[float]) -> SummaryStatistics:
    if not values:
        return SummaryStatistics(0, None, None, None, None)
    return SummaryStatistics(len(values), fmean(values), stdev(values) if len(values) > 1 else 0.0, min(values), max(values))


@dataclass(frozen=True)
class NewcomerMetrics:
    turns_to_protocol: int | None
    turns_to_message: int | None
    turns_to_routine: int | None
    turns_to_contribution: int | None
    failures: tuple[str, ...]
