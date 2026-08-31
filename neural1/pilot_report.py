"""Generate the human-readable Pilot 001 package from authoritative records."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .campaign import CampaignSpec
from .core import canonical_json, sha256_bytes, stable_id
from .evaluation import evaluate_campaign
from .pilot_meta import ingest_pilot
from .registry import ModelRegistry


def _table(headers: list[str], rows: list[list[object]]) -> str:
    rendered = [[str(value) for value in row] for row in rows]
    return "\n".join(["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|", *["| " + " | ".join(row) + " |" for row in rendered]])


def generate_pilot_001(campaign_root: str | Path, registry_path: str | Path, destination: str | Path, *, runtime_metadata: str | Path | None = None, thermal_log: str | Path | None = None, meta_database: str | Path | None = None) -> dict[str, Any]:
    campaign = Path(campaign_root)
    output = Path(destination)
    output.mkdir(parents=True, exist_ok=True)
    (output / "proof-capsules").mkdir(exist_ok=True)
    spec = CampaignSpec.load(campaign / "spec.json")
    registry = ModelRegistry.load(registry_path)
    evaluation = evaluate_campaign(campaign)
    meta_result = ingest_pilot(campaign, meta_database or campaign / "meta-pilot-001.sqlite3")
    summary = json.loads((campaign / "summary.json").read_text(encoding="utf-8"))
    metrics = {item["cell_id"]: item for item in evaluation["cells"]}
    rows = []
    completed = incomplete = 0
    for cell in spec.cells:
        record = metrics.get(cell.cell_id)
        status = record["status"] if record else "NOT_STARTED"
        completed += status == "COMPLETED"
        incomplete += status != "COMPLETED"
        rows.append([cell.cell_id, cell.experiment_id, cell.model_id, cell.seed, status, record["turns"] if record else 0, record["token_use"] if record else 0, record["errors"] if record else 0])
    runtime = json.loads(Path(runtime_metadata).read_text()) if runtime_metadata and Path(runtime_metadata).exists() else {"status": "NOT_RECORDED"}
    thermal = Path(thermal_log).read_text(encoding="utf-8") if thermal_log and Path(thermal_log).exists() else "NOT RECORDED"
    model_rows = [[model.model_id, model.family, model.role, model.backend, model.backend_name, model.parameter_count, model.quantization, model.context_limit, model.digest, model.license] for model in (registry.require(model_id) for model_id in spec.model_ids)]
    totals = evaluation["totals"]
    overview = f"""# NEURAL1 Pilot 001

**Status:** MODEL-VALIDATED PILOT — NOT AUTOMATICALLY ESTABLISHED SCIENTIFIC FINDINGS

Pilot 001 exercised the frozen NEURAL1 campaign infrastructure against three local small-model families. Machine-readable campaign records and release-bundle hashes are authoritative; this package interprets them.

## Completion

- Campaign: `{spec.campaign_id}`
- Matrix cells: {len(spec.cells)}
- Completed: {completed}
- Incomplete/cancelled/not started: {incomplete}
- Seeds: {", ".join(map(str, spec.seeds))}
- Recorded turns: {totals['turns']}
- Recorded tokens: {totals['token_use']}
- Errors: {totals['errors']}
- Campaign invocation wall time: {summary.get('elapsed_seconds', 'NOT RECORDED')} seconds
- Aggregate recorded model latency: {totals['model_latency_ms'] / 1000:.3f} seconds
- Generated: {datetime.now(UTC).isoformat()}

## Evidence interpretation

All automatically summarized phenomena are **OBSERVED** or **CANDIDATE DISCOVERIES**. No correlation, anomaly, convergence, or one-off structure is upgraded to causality or generality. Intervention-supported and replicated labels require their corresponding structured records.

## Runtime metadata

```json
{json.dumps(runtime, indent=2, sort_keys=True)}
```

## Thermal/performance observations

```text
{thermal}
```

See the linked methodology, matrix, comparisons, results, META findings, negative results, limitations, reproduction record, and follow-up experiments in this directory.
"""
    documents = {
        "README.md": overview,
        "methodology.md": f"# Methodology\n\nPilot 001 used the frozen `{spec.schema_version}` specification, fixed model registry, matched control `{spec.matched_control}`, seeds {list(spec.seeds)}, {spec.generations} requested generations, {spec.agents_per_cell} logical agents per cell, {spec.ram_budget} bytes of allowed RAM, and a hard wall-clock limit of {spec.wall_clock_limit_seconds} seconds. Contexts were isolated by logical agent ID. All model responses, WozMon outputs, checkpoints, errors, and token metadata were recorded.\n",
        "experiment-matrix.md": "# Experiment matrix\n\n" + _table(["CELL", "EXPERIMENT", "MODEL", "SEED", "STATUS", "TURNS", "TOKENS", "ERRORS"], rows) + "\n",
        "model-comparison.md": "# Model comparison\n\nTinyLlama is intentionally retained as the weak/small baseline. Differences are observations within this pilot, not general model rankings. Exact locally qualified identities appear below. Per-model outcome aggregates follow.\n\n" + _table(["ID", "FAMILY", "ROLE", "BACKEND", "NAME", "PARAMETERS", "QUANT", "CONTEXT", "SHA-256", "LICENSE"], model_rows) + "\n\n" + _table(["MODEL", "CELLS", "TURNS", "TOKENS", "VALID ACTIONS", "INVALID/PROSE", "ERRORS", "MODEL SECONDS"], _model_rows(spec, metrics)) + "\n",
        "experiment-results.md": "# Experiment results\n\n" + _table(["EXPERIMENT", "COMPLETED CELLS", "TURNS", "VALID ACTIONS", "INVALID/PROSE", "ERRORS"], _experiment_rows(spec, metrics)) + "\n",
        "meta-findings.md": "# META/1 findings\n\nMETA/1 processed real experiment records. Automatically emitted discoveries remain candidates. Evidence level for the aggregate is `OBSERVED`. The sole generated claim concerns recorded infrastructure completion; no experimental scientific claim was established.\n\n```json\n" + json.dumps(meta_result, indent=2, sort_keys=True, default=str) + "\n```\n",
        "negative-results.md": "# Negative results\n\nIncomplete cells, invalid/prose-only responses, errors, timeouts, and cancellations are retained below rather than removed.\n\n" + _negative_rows(rows) + "\n",
        "anomalies-and-discoveries.md": "# Anomalies and candidate discoveries\n\nThese detector outputs are investigation targets, not facts.\n\n```json\n" + json.dumps(evaluation["candidate_discoveries"], indent=2, sort_keys=True) + "\n```\n",
        "limitations.md": "# Limitations\n\nThis is one bounded workstation pilot using three small quantized model families. It does not establish physical Apple-1 behavior, causal effects, historical facts, broad model-family generality, or autonomous culture. Missing token/backend metadata remains missing. Deadline-truncated cells are not treated as failures unless the metric defines them that way.\n",
        "follow-up-experiments.md": "# Follow-up experiments\n\n1. Replay every completed cell and verify exact model-record consumption.\n2. Fork candidate anomalies at their preceding checkpoint and remove one named factor.\n3. Replicate candidate differences across new seeds before model-family claims.\n4. Test any candidate invariant with `BREAK` against held-out cells.\n5. Add stronger 3B–4B models through registry records without changing experiment definitions.\n",
        "reproducibility.md": f"# Reproducibility\n\nAuthoritative campaign ID: `{spec.campaign_id}`. Verify the release bundle before replay. Reproduction requires the exact runtime revision, registry digests, campaign specification, provider executables, model blobs, and recorded seeds. Use `neural1 verify-bundle BUNDLE`, then `neural1 run-campaign SPEC REGISTRY --output OUTPUT` only when the exact models are available.\n",
    }
    for name, text in documents.items():
        (output / name).write_text(text.rstrip() + "\n", encoding="utf-8")
    capsule_body = {"claim": "PILOT 001 COMPLETED THE RECORDED MATRIX CELLS UNDER THE FROZEN CAMPAIGN RUNTIME.", "status": "OBSERVED", "campaign_id": spec.campaign_id, "completed_cells": completed, "incomplete_cells": incomplete, "dataset_hash": sha256_bytes(canonical_json(evaluation).encode("ascii")), "evidence": ["campaign spec", "cell checkpoints", "model recordings", "transcripts"], "causal_status": "OBSERVED", "scientific_findings": []}
    capsule_body["capsule_id"] = stable_id("N1-PC", capsule_body)
    (output / "proof-capsules" / f"{capsule_body['capsule_id']}.json").write_text(json.dumps(capsule_body, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (output / "proof-capsules" / "README.md").write_text("# Pilot 001 proof capsules\n\nCapsules here trace infrastructure observations to authoritative machine records. They do not automatically establish scientific findings.\n", encoding="utf-8")
    return {"campaign_id": spec.campaign_id, "completed": completed, "incomplete": incomplete, "documents": sorted(documents), "proof_capsule": capsule_body["capsule_id"]}


def _experiment_rows(spec: CampaignSpec, metrics: dict[str, dict[str, Any]]) -> list[list[object]]:
    rows = []
    for experiment in spec.experiments:
        records = [metrics[cell.cell_id] for cell in spec.cells if cell.experiment_id == experiment and cell.cell_id in metrics]
        rows.append([experiment, sum(item["status"] == "COMPLETED" for item in records), sum(item["turns"] for item in records), sum(item["valid_monitor_actions"] for item in records), sum(item["invalid_or_prose_responses"] for item in records), sum(item["errors"] for item in records)])
    return rows


def _negative_rows(rows: list[list[object]]) -> str:
    negatives = [row for row in rows if row[4] != "COMPLETED" or row[7] != 0]
    return _table(["CELL", "EXPERIMENT", "MODEL", "SEED", "STATUS", "TURNS", "TOKENS", "ERRORS"], negatives) if negatives else "No cell-level errors or incomplete cells were recorded. This does not imply positive scientific results."


def _model_rows(spec: CampaignSpec, metrics: dict[str, dict[str, Any]]) -> list[list[object]]:
    rows = []
    for model_id in spec.model_ids:
        records = [metrics[cell.cell_id] for cell in spec.cells if cell.model_id == model_id and cell.cell_id in metrics]
        rows.append([model_id, len(records), sum(item["turns"] for item in records), sum(item["token_use"] for item in records), sum(item["valid_monitor_actions"] for item in records), sum(item["invalid_or_prose_responses"] for item in records), sum(item["errors"] for item in records), f"{sum(item['model_latency_ms'] for item in records) / 1000:.3f}"])
    return rows
