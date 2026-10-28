"""Canonical records and identities shared by every NEURAL1 subsystem."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from dataclasses import asdict, dataclass, is_dataclass
from enum import StrEnum
from typing import Any, cast

SCHEMA_VERSION = "neural1-0.1"


class Neural1Error(RuntimeError):
    """A structured, user-actionable runtime failure."""


class Target(StrEnum):
    VIRTUAL = "VIRTUAL"
    PHYSICAL_QUALIFICATION = "PHYSICAL_QUALIFICATION"


class Maturity(StrEnum):
    DESIGN = "DESIGN"
    PROTOTYPE = "PROTOTYPE"
    VIRTUAL_VALIDATED = "VIRTUAL-VALIDATED"
    MODEL_VALIDATED = "MODEL-VALIDATED"
    PHYSICAL_PENDING = "PHYSICAL-QUALIFICATION-PENDING"
    PHYSICAL_VERIFIED = "PHYSICAL-VERIFIED"


def canonical_json(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(cast(Any, value))
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def stable_id(prefix: str, value: Any, *, length: int = 16) -> str:
    digest = sha256_bytes(canonical_json(value).encode("ascii"))[:length].upper()
    return f"{prefix}-{digest}"


@dataclass(frozen=True)
class ModelRecord:
    provider: str
    family: str
    name: str
    version: str = "UNAVAILABLE"
    hash: str = "UNAVAILABLE"
    quantization: str = "UNAVAILABLE"
    context_limit: int | None = None
    generation: Mapping[str, Any] | None = None


@dataclass(frozen=True)
class GenerationResult:
    text: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    latency_ms: float | None = None
    provider_metadata: Mapping[str, Any] | None = None
