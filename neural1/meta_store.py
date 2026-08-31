"""Persistent, queryable META/1 research state using a local SQLite index."""

from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable, Mapping
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .core import canonical_json, stable_id
from .meta import Claim, Evidence


@dataclass(frozen=True)
class QueueItem:
    question_id: str
    question: str
    uncertainty: float
    novelty: float
    information_gain: float
    cross_experiment_relevance: float
    normalized_compute_cost: float
    priority: float
    status: str = "OPEN"


class ResearchDatabase:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._migrate()

    def close(self) -> None:
        self.connection.close()

    def _migrate(self) -> None:
        self.connection.executescript("""
        CREATE TABLE IF NOT EXISTS claims (claim_id TEXT PRIMARY KEY, statement TEXT NOT NULL, payload TEXT NOT NULL, updated_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS evidence (evidence_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS edges (source TEXT NOT NULL, relation TEXT NOT NULL, target TEXT NOT NULL, UNIQUE(source, relation, target));
        CREATE TABLE IF NOT EXISTS events (sequence INTEGER PRIMARY KEY AUTOINCREMENT, recorded_at TEXT NOT NULL, event_type TEXT NOT NULL, object_id TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS queue (question_id TEXT PRIMARY KEY, payload TEXT NOT NULL, priority REAL NOT NULL, status TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS forecasts (forecast_id TEXT PRIMARY KEY, question TEXT NOT NULL, probability REAL NOT NULL, payload TEXT NOT NULL, revealed INTEGER NOT NULL DEFAULT 0, outcome INTEGER, brier_score REAL);
        CREATE TABLE IF NOT EXISTS blind_reviews (review_id TEXT PRIMARY KEY, payload TEXT NOT NULL, revealed INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE IF NOT EXISTS discoveries (discovery_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS concepts (occurrence_id TEXT PRIMARY KEY, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS role_reviews (review_id TEXT PRIMARY KEY, claim_id TEXT NOT NULL, role TEXT NOT NULL, payload TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS counterfactuals (counterfactual_id TEXT PRIMARY KEY, payload TEXT NOT NULL, status TEXT NOT NULL);
        """)
        self.connection.commit()

    @staticmethod
    def _now() -> str:
        return datetime.now(UTC).isoformat()

    def _event(self, event_type: str, object_id: str, payload: Mapping[str, Any]) -> None:
        self.connection.execute("INSERT INTO events(recorded_at,event_type,object_id,payload) VALUES(?,?,?,?)", (self._now(), event_type, object_id, canonical_json(payload)))

    def put_claim(self, claim: Claim) -> None:
        payload = asdict(claim)
        now = self._now()
        self.connection.execute("INSERT INTO claims VALUES(?,?,?,?) ON CONFLICT(claim_id) DO UPDATE SET statement=excluded.statement,payload=excluded.payload,updated_at=excluded.updated_at", (claim.claim_id, claim.statement, canonical_json(payload), now))
        self._event("claim_revision", claim.claim_id, payload)
        self.connection.commit()

    def put_evidence(self, evidence: Evidence) -> None:
        payload = asdict(evidence)
        self.connection.execute("INSERT OR IGNORE INTO evidence VALUES(?,?)", (evidence.evidence_id, canonical_json(payload)))
        self._event("evidence_added", evidence.evidence_id, payload)
        self.connection.commit()

    def relate(self, source: str, relation: str, target: str) -> None:
        self.connection.execute("INSERT OR IGNORE INTO edges VALUES(?,?,?)", (source, relation, target))
        self._event("relation_added", target, {"source": source, "relation": relation, "target": target})
        self.connection.commit()

    def claim(self, claim_id: str) -> dict[str, Any] | None:
        row = self.connection.execute("SELECT payload FROM claims WHERE claim_id=?", (claim_id,)).fetchone()
        return json.loads(row[0]) if row else None

    def claim_history(self, claim_id: str, *, through_sequence: int | None = None) -> list[dict[str, Any]]:
        sql = "SELECT sequence,recorded_at,payload FROM events WHERE object_id=? AND event_type='claim_revision'"
        params: list[Any] = [claim_id]
        if through_sequence is not None:
            sql += " AND sequence<=?"
            params.append(through_sequence)
        sql += " ORDER BY sequence"
        return [{"sequence": row[0], "recorded_at": row[1], "claim": json.loads(row[2])} for row in self.connection.execute(sql, params)]

    def enqueue(self, question: str, *, uncertainty: float, novelty: float, information_gain: float, cross_experiment_relevance: float, normalized_compute_cost: float) -> QueueItem:
        values = (uncertainty, novelty, information_gain, cross_experiment_relevance, normalized_compute_cost)
        if any(not 0 <= value <= 1 for value in values):
            raise ValueError("priority factors must be normalized to 0..1")
        priority = uncertainty + novelty + information_gain + cross_experiment_relevance - normalized_compute_cost
        item = QueueItem(stable_id("N1-Q", {"question": question, "factors": values}), question, *values, priority)
        self.connection.execute("INSERT OR REPLACE INTO queue VALUES(?,?,?,?)", (item.question_id, canonical_json(asdict(item)), item.priority, item.status))
        self._event("question_enqueued", item.question_id, asdict(item))
        self.connection.commit()
        return item

    def research_queue(self) -> list[dict[str, Any]]:
        return [json.loads(row[0]) for row in self.connection.execute("SELECT payload FROM queue WHERE status='OPEN' ORDER BY priority DESC, question_id")]

    def forecast(self, question: str, probability: float, expected_effect: str, confidence: str) -> str:
        if not 0 <= probability <= 1:
            raise ValueError("probability must be 0..1")
        payload = {"question": question, "probability": probability, "expected_effect": expected_effect, "confidence": confidence, "created_at": self._now()}
        forecast_id = stable_id("N1-F", payload)
        self.connection.execute("INSERT INTO forecasts(forecast_id,question,probability,payload) VALUES(?,?,?,?)", (forecast_id, question, probability, canonical_json(payload)))
        self._event("forecast_sealed", forecast_id, payload)
        self.connection.commit()
        return forecast_id

    def reveal_forecast(self, forecast_id: str, outcome: bool) -> float:
        row = self.connection.execute("SELECT probability,revealed FROM forecasts WHERE forecast_id=?", (forecast_id,)).fetchone()
        if row is None or row[1]:
            raise ValueError("unknown or already revealed forecast")
        score = (row[0] - int(outcome)) ** 2
        self.connection.execute("UPDATE forecasts SET revealed=1,outcome=?,brier_score=? WHERE forecast_id=?", (int(outcome), score, forecast_id))
        self._event("forecast_revealed", forecast_id, {"outcome": outcome, "brier_score": score})
        self.connection.commit()
        return score

    def blind_review(self, subject_id: str, hidden_fields: Iterable[str], review: str) -> str:
        payload = {"subject_id": subject_id, "hidden_fields": sorted(set(hidden_fields)), "review": review, "created_at": self._now()}
        review_id = stable_id("N1-BR", payload)
        self.connection.execute("INSERT INTO blind_reviews VALUES(?,?,0)", (review_id, canonical_json(payload)))
        self._event("blind_review_created", review_id, payload)
        self.connection.commit()
        return review_id

    def reveal_review(self, review_id: str) -> None:
        changed = self.connection.execute("UPDATE blind_reviews SET revealed=1 WHERE review_id=? AND revealed=0", (review_id,)).rowcount
        if not changed:
            raise ValueError("unknown or already revealed review")
        self._event("blind_review_revealed", review_id, {})
        self.connection.commit()

    def discovery(self, detector: str, dataset_hash: str, summary: str) -> str:
        payload = {"detector": detector, "dataset_hash": dataset_hash, "summary": summary, "status": "CANDIDATE"}
        discovery_id = stable_id("N1-D", payload)
        self.connection.execute("INSERT OR IGNORE INTO discoveries VALUES(?,?,?)", (discovery_id, canonical_json(payload), "CANDIDATE"))
        self._event("candidate_discovery", discovery_id, payload)
        self.connection.commit()
        return discovery_id

    def tribunal(self, claim_id: str, *, minimum_causal_level: int = 0) -> dict[str, Any]:
        rows = self.connection.execute("SELECT e.payload,x.relation FROM edges x JOIN evidence e ON e.evidence_id=x.source WHERE x.target=?", (claim_id,)).fetchall()
        support = [json.loads(row[0]) for row in rows if row[1] == "supports"]
        oppose = [json.loads(row[0]) for row in rows if row[1] in {"opposes", "contradicts"}]
        qualifying = [item for item in support if item["causal_level"] >= minimum_causal_level]
        verdict = "SUPPORTED" if qualifying and not oppose else "CONTESTED" if qualifying and oppose else "INSUFFICIENT_EVIDENCE"
        return {"claim_id": claim_id, "verdict": verdict, "rule": {"minimum_causal_level": minimum_causal_level, "opposing_evidence_blocks_unqualified_support": True}, "supporting": [item["evidence_id"] for item in support], "opposing": [item["evidence_id"] for item in oppose]}

    def record_concept(self, concept: str, artifact_id: str, run_id: str, classification: str, classifier_version: str) -> str:
        if classification not in {"INHERITED", "INDEPENDENT", "UNCERTAIN"}:
            raise ValueError("invalid concept relationship classification")
        payload = {"concept": concept, "artifact_id": artifact_id, "run_id": run_id, "classification": classification, "classifier_version": classifier_version}
        occurrence_id = stable_id("N1-CO", payload)
        self.connection.execute("INSERT OR IGNORE INTO concepts VALUES(?,?)", (occurrence_id, canonical_json(payload)))
        self._event("concept_recorded", occurrence_id, payload)
        self.connection.commit()
        return occurrence_id

    def concept_occurrences(self, concept: str) -> list[dict[str, Any]]:
        return [payload for (raw,) in self.connection.execute("SELECT payload FROM concepts ORDER BY occurrence_id") if (payload := json.loads(raw))["concept"] == concept]

    def role_review(self, claim_id: str, role: str, findings: Mapping[str, Any]) -> str:
        if role not in {"ADVOCATE", "SKEPTIC", "REPLICATOR", "EVIDENCE_JUDGE"}:
            raise ValueError("invalid tribunal role")
        payload = {"claim_id": claim_id, "role": role, "findings": dict(findings), "recorded_at": self._now()}
        review_id = stable_id("N1-TR", payload)
        self.connection.execute("INSERT INTO role_reviews VALUES(?,?,?,?)", (review_id, claim_id, role, canonical_json(payload)))
        self._event("tribunal_role_review", claim_id, {"review_id": review_id, **payload})
        self.connection.commit()
        return review_id

    def counterfactual(self, base_run_id: str, fork_point: str, changed_factor: str, seed_relationship: str) -> str:
        payload = {"base_run_id": base_run_id, "fork_point": fork_point, "changed_factor": changed_factor, "seed_relationship": seed_relationship, "target": "VIRTUAL", "status": "PLANNED"}
        counterfactual_id = stable_id("N1-CF", payload)
        self.connection.execute("INSERT OR IGNORE INTO counterfactuals VALUES(?,?,?)", (counterfactual_id, canonical_json(payload), "PLANNED"))
        self._event("counterfactual_planned", counterfactual_id, payload)
        self.connection.commit()
        return counterfactual_id
