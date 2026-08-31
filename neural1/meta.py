"""META/1 claim graph, causal status, proof capsules, and experiment compiler."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

from .core import SCHEMA_VERSION, stable_id


class CausalStatus(StrEnum):
    UNKNOWN = "UNKNOWN"
    OBSERVED = "OBSERVED"
    CORRELATED = "CORRELATED"
    INFERRED = "INFERRED"
    INTERVENTION_SUPPORTED = "INTERVENTION SUPPORTED"


CAUSAL_LEVELS = {0: "OBSERVATION", 1: "MATCHED_COMPARISON", 2: "CONTROLLED_REPLAY", 3: "REMOVAL_INTERVENTION", 4: "CROSS_SEED_REPLICATION", 5: "CROSS_MODEL_REPLICATION"}
RELATIONS = {"supports", "opposes", "limits", "derived_from", "replicates", "contradicts", "depends_on"}


@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    kind: str
    artifact_hash: str
    run_ids: tuple[str, ...]
    summary: str
    causal_level: int = 0


@dataclass
class Claim:
    claim_id: str
    statement: str
    scope: Mapping[str, str]
    status: str = "OPEN"
    causal_status: CausalStatus = CausalStatus.UNKNOWN
    effect_size: float | None = None
    uncertainty: str = "UNQUANTIFIED"
    counterexamples: list[str] = field(default_factory=list)
    potential_falsifier: str = "NOT YET SPECIFIED"
    revisions: list[Mapping[str, Any]] = field(default_factory=list)


class ClaimGraph:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path) if path else None
        self.claims: dict[str, Claim] = {}
        self.evidence: dict[str, Evidence] = {}
        self.edges: list[tuple[str, str, str]] = []

    def create_claim(self, statement: str, scope: Mapping[str, str]) -> Claim:
        claim = Claim(stable_id("N1-C", {"statement": statement, "scope": scope}), statement, dict(scope))
        self.claims.setdefault(claim.claim_id, claim)
        return self.claims[claim.claim_id]

    def add_evidence(self, kind: str, artifact_hash: str, run_ids: Iterable[str], summary: str, *, causal_level: int = 0) -> Evidence:
        if causal_level not in CAUSAL_LEVELS:
            raise ValueError("invalid causal level")
        data = {"kind": kind, "hash": artifact_hash, "runs": sorted(run_ids), "summary": summary, "level": causal_level}
        evidence = Evidence(stable_id("N1-E", data), kind, artifact_hash, tuple(sorted(run_ids)), summary, causal_level)
        self.evidence.setdefault(evidence.evidence_id, evidence)
        return evidence

    def relate(self, source: str, relation: str, target: str) -> None:
        if relation not in RELATIONS:
            raise ValueError("invalid claim-graph relation")
        if source not in self.claims and source not in self.evidence:
            raise ValueError("unknown source")
        if target not in self.claims and target not in self.evidence:
            raise ValueError("unknown target")
        edge = (source, relation, target)
        if edge not in self.edges:
            self.edges.append(edge)

    def support_for(self, claim_id: str) -> list[Evidence]:
        ids = {source for source, relation, target in self.edges if target == claim_id and relation == "supports"}
        return [self.evidence[item] for item in sorted(ids) if item in self.evidence]

    def save(self) -> None:
        if self.path is None:
            raise ValueError("claim graph has no storage path")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"schema_version": SCHEMA_VERSION, "claims": [asdict(self.claims[key]) for key in sorted(self.claims)], "evidence": [asdict(self.evidence[key]) for key in sorted(self.evidence)], "edges": sorted(self.edges)}
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="ascii")


@dataclass(frozen=True)
class ExperimentDefinition:
    experiment_id: str
    question: str
    factor: str
    levels: tuple[str, ...]
    controls: Mapping[str, Any]
    metrics: tuple[str, ...]
    seeds: tuple[int, ...]
    analysis: str
    stopping_rule: str
    target: str = "VIRTUAL"


def compile_experiment(question: str, *, factor: str, levels: Iterable[str], controls: Mapping[str, Any], metrics: Iterable[str], seeds: Iterable[int], analysis: str, stopping_rule: str) -> ExperimentDefinition:
    values = tuple(levels)
    if len(values) < 2 or not tuple(metrics) or not tuple(seeds):
        raise ValueError("experiment requires at least two levels, a metric, and a seed")
    data = {"question": question, "factor": factor, "levels": values, "controls": controls, "metrics": tuple(metrics), "seeds": tuple(seeds), "analysis": analysis, "stop": stopping_rule}
    return ExperimentDefinition(stable_id("N1-X", data), question, factor, values, dict(controls), tuple(metrics), tuple(seeds), analysis, stopping_rule)


def falsification_plan(claim: Claim, *, factor: str, control: str, treatment: str, metric: str, seeds: Iterable[int], sample_count: int) -> dict[str, Any]:
    return {"claim_id": claim.claim_id, "hypothesis": f"NO EFFECT ON: {claim.statement}", "factor": factor, "control": control, "treatment": treatment, "seeds": list(seeds), "sample_count": sample_count, "primary_metric": metric, "stop_criteria": "PRE-REGISTERED SAMPLE COMPLETE", "estimated_compute_cost": "UNBENCHMARKED"}


def proof_capsule(claim: Claim, graph: ClaimGraph, *, dataset_hash: str, analysis_version: str, reproduction_command: str) -> dict[str, Any]:
    evidence = graph.support_for(claim.claim_id)
    capsule = {"schema_version": SCHEMA_VERSION, "claim": asdict(claim), "dataset_hash": dataset_hash, "run_ids": sorted({run for item in evidence for run in item.run_ids}), "evidence_ids": [item.evidence_id for item in evidence], "artifact_hashes": [item.artifact_hash for item in evidence], "analysis_version": analysis_version, "effect_size": claim.effect_size, "uncertainty": claim.uncertainty, "counterexamples": claim.counterexamples, "causal_tests": [CAUSAL_LEVELS[item.causal_level] for item in evidence], "reproduction_command": reproduction_command, "generated_at": datetime.now(UTC).isoformat()}
    capsule["capsule_id"] = stable_id("N1-PC", {key: value for key, value in capsule.items() if key != "generated_at"})
    return capsule
