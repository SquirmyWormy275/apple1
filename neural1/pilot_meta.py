"""Ingest a completed pilot into META/1 without inflating evidence strength."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .core import canonical_json, sha256_bytes
from .evaluation import evaluate_campaign
from .meta import CausalStatus, ClaimGraph
from .meta_store import ResearchDatabase


def ingest_pilot(campaign_root: str | Path, database_path: str | Path) -> dict[str, Any]:
    root = Path(campaign_root)
    summary = json.loads((root / "summary.json").read_text(encoding="utf-8"))
    evaluation = evaluate_campaign(root)
    dataset_hash = sha256_bytes(canonical_json(evaluation).encode("ascii"))
    graph = ClaimGraph()
    claim = graph.create_claim(
        "PILOT 001 COMPLETED THE CELLS LISTED IN ITS AUTHORITATIVE SUMMARY.",
        {"campaign": summary["campaign_id"], "scope": "infrastructure"},
    )
    claim.status = "SUPPORTED"
    claim.causal_status = CausalStatus.OBSERVED
    claim.uncertainty = "CELL COMPLETION ONLY; NO SCIENTIFIC EFFECT CLAIMED"
    evidence = graph.add_evidence(
        "campaign-summary",
        dataset_hash,
        summary.get("completed_cells", ()),
        "Aggregate generated from hashed cell checkpoints and transcripts.",
        causal_level=0,
    )
    database = ResearchDatabase(database_path)
    try:
        database.put_claim(claim)
        database.put_evidence(evidence)
        database.relate(evidence.evidence_id, "supports", claim.claim_id)
        database.role_review(claim.claim_id, "SKEPTIC", {"finding": "Completion does not establish experimental effects or generality."})
        database.role_review(claim.claim_id, "EVIDENCE_JUDGE", {"verdict": "OBSERVATION_ONLY", "causal_level": 0})
        discoveries = [
            database.discovery("phase-change-candidate-v1", dataset_hash, item["description"])
            for item in evaluation["candidate_discoveries"]
        ]
        queue = database.enqueue(
            "WHICH PILOT 001 OBSERVATIONS SURVIVE HELD-OUT-SEED CONTROLLED REPLAY?",
            uncertainty=1.0,
            novelty=0.5,
            information_gain=0.9,
            cross_experiment_relevance=0.8,
            normalized_compute_cost=0.4,
        )
        verdict = database.tribunal(claim.claim_id, minimum_causal_level=0)
    finally:
        database.close()
    return {
        "claim_id": claim.claim_id,
        "evidence_id": evidence.evidence_id,
        "causal_status": claim.causal_status,
        "dataset_hash": dataset_hash,
        "candidate_discovery_ids": discoveries,
        "research_question_id": queue.question_id,
        "tribunal": verdict,
    }
