"""Bounded local-provider qualification before any real-model campaign."""

from __future__ import annotations

import json
import platform
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .core import sha256_bytes
from .provider_factory import provider_for
from .registry import ModelRegistry


@dataclass(frozen=True)
class QualificationResult:
    model_id: str
    backend: str
    digest: str
    nonempty: bool
    repeat_identical: bool
    completion_tokens: int | None
    token_bound_respected: bool
    first_response_sha256: str
    second_response_sha256: str
    first_latency_ms: float | None
    second_latency_ms: float | None
    qualified_at: str


def qualify_registry(registry_path: str | Path, destination: str | Path) -> dict[str, Any]:
    registry = ModelRegistry.load(registry_path)
    results = []
    prompt = "Return exactly one WozMon deposit command that stores byte 00 at address 0200. No prose."
    for model_id in sorted(registry.models):
        model = registry.require(model_id)
        provider = provider_for(model)
        first = provider.generate(prompt, agent_id="QUAL-A", seed=1976)
        second = provider.generate(prompt, agent_id="QUAL-A", seed=1976)
        limit = int(model.generation_defaults.get("max_tokens", 0))
        token_ok = first.completion_tokens is None or not limit or first.completion_tokens <= limit
        result = QualificationResult(
            model_id,
            model.backend,
            model.digest,
            bool(first.text.strip() and second.text.strip()),
            first.text == second.text,
            first.completion_tokens,
            token_ok,
            sha256_bytes(first.text.encode("utf-8")),
            sha256_bytes(second.text.encode("utf-8")),
            first.latency_ms,
            second.latency_ms,
            datetime.now(UTC).isoformat(),
        )
        results.append(asdict(result))
    payload = {
        "schema_version": "neural1-provider-qualification-0.1",
        "runtime": {"python": platform.python_version(), "platform": platform.platform()},
        "registry": str(Path(registry_path)),
        "results": results,
        "qualified": all(item["nonempty"] and item["token_bound_respected"] for item in results),
        "note": "repeat_identical is measured, not required; some local kernels are not bit-deterministic",
    }
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload
