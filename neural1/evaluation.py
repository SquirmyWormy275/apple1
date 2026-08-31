"""Campaign evidence summaries and explicit maturity/causal labels."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .analysis import detect_phase_changes
from .core import sha256_bytes


@dataclass(frozen=True)
class CellMetrics:
    cell_id: str
    status: str
    generations: int
    turns: int
    valid_monitor_actions: int
    invalid_or_prose_responses: int
    errors: int
    token_use: int
    model_latency_ms: float
    transcript_sha256: str


def evaluate_cell(cell_root: str | Path) -> CellMetrics:
    root = Path(cell_root)
    checkpoint = json.loads((root / "checkpoint.json").read_text(encoding="utf-8"))
    records = [json.loads(line) for line in (root / "transcript.jsonl").read_text(encoding="utf-8").splitlines() if line]
    actions = sum(len(record.get("outputs", ())) for record in records)
    invalid = sum("response" in record and not record.get("outputs") for record in records)
    latency = sum(float(record.get("result", {}).get("latency_ms") or 0) for record in records)
    return CellMetrics(root.name, checkpoint["status"], checkpoint["generation"], len(records), actions, invalid, len(checkpoint["errors"]), checkpoint["token_use"], latency, sha256_bytes((root / "transcript.jsonl").read_bytes()))


def evaluate_campaign(campaign_root: str | Path) -> dict[str, Any]:
    root = Path(campaign_root)
    cells = [evaluate_cell(path) for path in sorted((root / "cells").iterdir()) if (path / "checkpoint.json").exists()]
    valid_action_series = [float(cell.valid_monitor_actions) for cell in cells]
    discoveries = [asdict(item) for item in detect_phase_changes(valid_action_series, threshold=max(valid_action_series, default=0) or 1)]
    return {
        "evidence_label": "MODEL-VALIDATED PILOT" if cells else "NO MODEL EVIDENCE",
        "cells": [asdict(cell) for cell in cells],
        "totals": {"cells": len(cells), "completed": sum(cell.status == "COMPLETED" for cell in cells), "turns": sum(cell.turns for cell in cells), "valid_monitor_actions": sum(cell.valid_monitor_actions for cell in cells), "invalid_or_prose_responses": sum(cell.invalid_or_prose_responses for cell in cells), "errors": sum(cell.errors for cell in cells), "token_use": sum(cell.token_use for cell in cells), "model_latency_ms": sum(cell.model_latency_ms for cell in cells)},
        "candidate_discoveries": discoveries,
        "causal_status": "OBSERVED",
        "automatic_scientific_claims": [],
    }
