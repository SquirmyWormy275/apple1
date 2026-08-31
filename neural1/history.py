"""Source-disciplined historical corpus ingestion for 1976 MULTIVERSE."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

from .core import Neural1Error, canonical_json, sha256_bytes
from .experiments import HistoricalComponent


@dataclass(frozen=True)
class HistoricalSource:
    source_id: str
    title: str
    author_or_issuer: str
    publication_date: str
    url_or_archive_path: str
    retrieved_date: str
    sha256: str
    source_type: str
    rights_status: str
    notes: str = ""


class HistoricalCorpus:
    def __init__(self) -> None:
        self.sources: dict[str, HistoricalSource] = {}
        self.components: dict[str, HistoricalComponent] = {}

    def add_source(self, source: HistoricalSource) -> None:
        if len(source.sha256) != 64 or any(character not in "0123456789abcdefABCDEF" for character in source.sha256):
            raise Neural1Error("historical source requires a SHA-256 identity")
        date.fromisoformat(source.publication_date)
        date.fromisoformat(source.retrieved_date)
        self.sources[source.source_id] = source

    def add_component(self, component: HistoricalComponent) -> None:
        missing = set(component.source_ids) - self.sources.keys()
        if missing:
            raise Neural1Error(f"component references unknown sources: {sorted(missing)}")
        if component.authoritative and (not component.source_ids or component.available_by is None):
            raise Neural1Error("authoritative components require sources and availability evidence")
        if component.available_by is not None:
            availability = date.fromisoformat(component.available_by)
            if availability > date(1976, 12, 31):
                raise Neural1Error("component falls outside the configured 1976 source-date constraint")
        self.components[component.part_id] = component

    def export(self, path: str | Path) -> str:
        payload = {"schema_version": "neural1-history-0.1", "sources": [asdict(self.sources[key]) for key in sorted(self.sources)], "components": [asdict(self.components[key]) for key in sorted(self.components)]}
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        destination.write_text(text, encoding="utf-8")
        return sha256_bytes(canonical_json(payload).encode("ascii"))


def load_research_index(path: str | Path) -> dict[str, Any]:
    """Load the non-authoritative historical research staging index.

    This is deliberately separate from :class:`HistoricalCorpus`: staged research
    may describe strong evidence, but it must not become runtime-authoritative until
    its source artifacts and extracted claims pass the ingestion gate.
    """

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if payload.get("schema_version") != "neural1-historical-research-index-0.1":
        raise Neural1Error("unsupported historical research index schema")
    date.fromisoformat(str(payload.get("cutoff_date", "")))
    runtime_ids = payload.get("runtime_authoritative_component_ids", [])
    if not isinstance(runtime_ids, list):
        raise Neural1Error("runtime_authoritative_component_ids must be a list")
    authoritative_count = payload.get("authoritative_runtime_records")
    if authoritative_count != len(runtime_ids):
        raise Neural1Error("authoritative runtime record count does not match component IDs")
    if payload.get("status") == "RESEARCH_STAGING" and runtime_ids:
        raise Neural1Error("research staging index cannot promote authoritative runtime components")
    policy = payload.get("promotion_policy")
    if not isinstance(policy, dict) or not all(policy.get(key) is True for key in ("requires_sha256", "requires_claim_review", "requires_cutoff_validation", "missing_prices_remain_null", "no_llm_estimates")):
        raise Neural1Error("historical research promotion policy is incomplete or unsafe")
    return payload


def research_status(path: str | Path) -> dict[str, Any]:
    payload = load_research_index(path)
    return {
        "world_id": payload["world_id"],
        "cutoff_date": payload["cutoff_date"],
        "status": payload["status"],
        "authoritative_runtime_records": payload["authoritative_runtime_records"],
        "research_inputs": len(payload["research_inputs"]),
        "unresolved_high_impact": len(payload["unresolved_high_impact"]),
    }


def verify_local_source(path: str | Path, expected_sha256: str) -> bool:
    return sha256_bytes(Path(path).read_bytes()).lower() == expected_sha256.lower()
