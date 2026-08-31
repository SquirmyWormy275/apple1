"""Deterministic META/1 analysis primitives; outputs are candidates, not facts."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .core import stable_id


@dataclass(frozen=True)
class InvariantCandidate:
    invariant_id: str
    feature: str
    value: str
    support: int
    population: int
    support_fraction: float


def mine_invariants(records: Sequence[Mapping[str, Any]], *, outcome_key: str = "successful", minimum_fraction: float = 1.0) -> tuple[InvariantCandidate, ...]:
    successful = [record for record in records if record.get(outcome_key) is True]
    if not successful:
        return ()
    candidates = []
    keys = set.intersection(*(set(record) for record in successful)) - {outcome_key}
    for key in sorted(keys):
        values = {str(record[key]) for record in successful}
        for value in sorted(values):
            support = sum(str(record[key]) == value for record in successful)
            fraction = support / len(successful)
            if fraction >= minimum_fraction:
                data = {"feature": key, "value": value, "population": len(successful), "support": support}
                candidates.append(InvariantCandidate(stable_id("N1-I", data), key, value, support, len(successful), fraction))
    return tuple(candidates)


def break_invariant(candidate: InvariantCandidate, records: Sequence[Mapping[str, Any]]) -> tuple[Mapping[str, Any], ...]:
    return tuple(record for record in records if record.get("successful") is True and str(record.get(candidate.feature)) != candidate.value)


@dataclass(frozen=True)
class DiscoveryCandidate:
    discovery_id: str
    detector: str
    summary: str
    record_indices: tuple[int, ...]
    status: str = "CANDIDATE"


def detect_phase_changes(values: Sequence[float], *, threshold: float) -> tuple[DiscoveryCandidate, ...]:
    output = []
    for index in range(1, len(values)):
        difference = values[index] - values[index - 1]
        if abs(difference) >= threshold:
            data = {"detector": "adjacent-difference", "index": index, "difference": difference, "threshold": threshold}
            output.append(DiscoveryCandidate(stable_id("N1-D", data), "adjacent-difference", f"CHANGE {difference:+.6g} AT INDEX {index}", (index - 1, index)))
    return tuple(output)


@dataclass(frozen=True)
class ScientistBenchScore:
    task_id: str
    exact_fields: int
    total_fields: int
    score: float


def score_scientist_task(task_id: str, expected: Mapping[str, Any], submitted: Mapping[str, Any]) -> ScientistBenchScore:
    correct = sum(submitted.get(key) == value for key, value in expected.items())
    return ScientistBenchScore(task_id, correct, len(expected), correct / len(expected) if expected else 1.0)
