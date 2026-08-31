"""Model-provider abstraction; tests and demonstrations require no real model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Protocol

from .core import GenerationResult, ModelRecord, Neural1Error


class ModelProvider(Protocol):
    @property
    def record(self) -> ModelRecord: ...
    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult: ...


@dataclass
class FakeProvider:
    """Deterministic provider keyed by exact prompt, with a safe default."""

    responses: Mapping[str, str] = field(default_factory=dict)
    default: str = ""

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="fake", family="deterministic-fixture", name="fake-v1", version="1")

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        text = self.responses.get(prompt, self.default)
        return GenerationResult(text=text, provider_metadata={"agent_id": agent_id, "seed": seed})


@dataclass
class ReplayProvider:
    """Replays exact recorded responses and refuses unrecorded prompts."""

    responses: Mapping[tuple[str, str, int], GenerationResult]

    @property
    def record(self) -> ModelRecord:
        return ModelRecord(provider="replay", family="recorded", name="replay-v1", version="1")

    def generate(self, prompt: str, *, agent_id: str, seed: int) -> GenerationResult:
        try:
            return self.responses[(prompt, agent_id, seed)]
        except KeyError as error:
            raise Neural1Error("replay has no exact prompt/agent/seed record") from error
