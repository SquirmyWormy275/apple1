"""Rights-clearance registry for heritage and original artwork."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .core import Neural1Error


@dataclass(frozen=True)
class ArtworkCandidate:
    asset_id: str
    concept: str
    origin: str
    source_ids: tuple[str, ...]
    author: str
    license_status: str
    permission_evidence: tuple[str, ...]
    attribution: str
    publishable: bool = False


class RightsRegistry:
    REQUIRED_CONCEPTS = {"APPLE_EMBLEM", "WOZNIAK_PORTRAIT", "JOBS_PORTRAIT", "JOBS_WOZ_PLATE", "APPLE1_ORIGINS"}

    def __init__(self) -> None:
        self.assets: dict[str, ArtworkCandidate] = {}

    def add(self, asset: ArtworkCandidate) -> None:
        if asset.origin not in {"original", "external", "derivative"}:
            raise Neural1Error("invalid artwork origin")
        if asset.publishable and (asset.license_status in {"NOT_ESTABLISHED", "UNKNOWN"} or not asset.permission_evidence):
            raise Neural1Error("publication requires established rights evidence")
        if asset.origin in {"external", "derivative"} and (not asset.source_ids or not asset.attribution):
            raise Neural1Error("external/derivative artwork requires source and attribution")
        self.assets[asset.asset_id] = asset

    def concept_status(self) -> dict[str, str]:
        return {concept: "CLEARED" if any(asset.concept == concept and asset.publishable for asset in self.assets.values()) else "BLOCKED" for concept in sorted(self.REQUIRED_CONCEPTS)}

    def save(self, path: str | Path) -> None:
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps({"assets": [asdict(self.assets[key]) for key in sorted(self.assets)], "concept_status": self.concept_status()}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
