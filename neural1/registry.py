"""Versioned, backend-independent model registry."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .core import Neural1Error, canonical_json, sha256_bytes

MODEL_REGISTRY_SCHEMA = "neural1-model-registry-0.1"


@dataclass(frozen=True)
class RegisteredModel:
    model_id: str
    family: str
    role: str
    backend: str
    backend_name: str
    parameter_count: str
    quantization: str
    context_limit: int
    digest: str
    license: str
    generation_defaults: Mapping[str, Any]
    capabilities: tuple[str, ...] = ("text",)

    def validate(self, *, allow_unqualified: bool = False) -> None:
        if self.backend not in {"fake", "replay", "ollama", "llama.cpp"}:
            raise Neural1Error(f"unsupported model backend: {self.backend}")
        if self.context_limit <= 0 or not self.model_id or not self.family:
            raise Neural1Error("model identity and context limit are required")
        if not allow_unqualified and self.backend not in {"fake", "replay"} and len(self.digest) != 64:
            raise Neural1Error("qualified local models require an exact SHA-256 digest")


class ModelRegistry:
    def __init__(self, models: Mapping[str, RegisteredModel] | None = None) -> None:
        self.models = dict(models or {})

    def add(self, model: RegisteredModel, *, allow_unqualified: bool = False) -> None:
        model.validate(allow_unqualified=allow_unqualified)
        if model.model_id in self.models and self.models[model.model_id] != model:
            raise Neural1Error(f"model ID already has a different record: {model.model_id}")
        self.models[model.model_id] = model

    def require(self, model_id: str) -> RegisteredModel:
        try:
            return self.models[model_id]
        except KeyError as error:
            raise Neural1Error(f"model is not registered: {model_id}") from error

    def save(self, path: str | Path) -> str:
        payload = {"schema_version": MODEL_REGISTRY_SCHEMA, "models": [asdict(self.models[key]) for key in sorted(self.models)]}
        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return sha256_bytes(canonical_json(payload).encode("ascii"))

    @classmethod
    def load(cls, path: str | Path, *, allow_unqualified: bool = False) -> ModelRegistry:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema_version") != MODEL_REGISTRY_SCHEMA:
            raise Neural1Error("unsupported model-registry schema")
        registry = cls()
        for record in payload.get("models", []):
            record["capabilities"] = tuple(record.get("capabilities", ("text",)))
            registry.add(RegisteredModel(**record), allow_unqualified=allow_unqualified)
        return registry
