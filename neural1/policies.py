"""Deterministic experiment policies and metrics shared by campaign runners."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from .core import Neural1Error, sha256_bytes


@dataclass(frozen=True)
class CandidateMetrics:
    candidate_id: str
    correctness: float
    robustness: float
    bytes_used: int
    execution_cost: int
    recoverability: float


@dataclass(frozen=True)
class SelectionPolicy:
    correctness_weight: float = 1.0
    robustness_weight: float = 0.0
    byte_weight: float = 0.0
    execution_weight: float = 0.0
    recoverability_weight: float = 0.0

    def score(self, metrics: CandidateMetrics) -> float:
        return self.correctness_weight * metrics.correctness + self.robustness_weight * metrics.robustness + self.recoverability_weight * metrics.recoverability - self.byte_weight * metrics.bytes_used - self.execution_weight * metrics.execution_cost

    def select(self, candidates: Sequence[CandidateMetrics], count: int) -> tuple[CandidateMetrics, ...]:
        if count < 0:
            raise Neural1Error("selection count cannot be negative")
        return tuple(sorted(candidates, key=lambda item: (-self.score(item), item.candidate_id))[:count])


def extinct(candidates: Sequence[CandidateMetrics], *, minimum_correctness: float) -> bool:
    return not any(candidate.correctness >= minimum_correctness for candidate in candidates)


def convergence(groups: Mapping[str, Sequence[str]]) -> dict[str, object]:
    sets = {key: set(values) for key, values in groups.items()}
    common = set.intersection(*sets.values()) if sets else set()
    return {"groups": len(sets), "common_artifacts": sorted(common), "converged": bool(common)}


@dataclass(frozen=True)
class RomMutation:
    parent_sha256: str
    child_sha256: str
    offsets: tuple[int, ...]
    xor_masks: tuple[int, ...]


def mutate_rom(rom: bytes, *, seed: int, mutation_count: int) -> tuple[bytes, RomMutation]:
    if len(rom) != 256 or not 0 <= mutation_count <= 256:
        raise Neural1Error("ROM mutation requires 256 bytes and a bounded count")
    rng = random.Random(seed)  # noqa: S311 - reproducible experiment mutation, not cryptography
    offsets = tuple(sorted(rng.sample(range(256), mutation_count)))
    masks = tuple(rng.randrange(1, 256) for _ in offsets)
    child = bytearray(rom)
    for offset, mask in zip(offsets, masks, strict=True):
        child[offset] ^= mask
    payload = bytes(child)
    return payload, RomMutation(sha256_bytes(rom), sha256_bytes(payload), offsets, masks)


@dataclass(frozen=True)
class MemoryConflict:
    address: int
    previous_agent: str
    current_agent: str


def memory_conflicts(writes: Sequence[tuple[str, int, bytes]]) -> tuple[MemoryConflict, ...]:
    owners: dict[int, str] = {}
    conflicts = []
    for agent_id, address, payload in writes:
        for offset in range(len(payload)):
            location = address + offset
            previous = owners.get(location)
            if previous is not None and previous != agent_id:
                conflicts.append(MemoryConflict(location, previous, agent_id))
            owners[location] = agent_id
    return tuple(conflicts)
