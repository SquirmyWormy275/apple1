"""Crash-safe experiment matrices with deterministic checkpoint/resume behavior."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic
from typing import Any

from .core import Neural1Error, canonical_json, sha256_bytes, stable_id
from .models import ModelProvider
from .registry import ModelRegistry
from .runtime import ExperimentRuntime
from .world import VirtualApple1World, WozMonSession

CAMPAIGN_SCHEMA = "neural1-campaign-0.1"
CHECKPOINT_SCHEMA = "neural1-checkpoint-0.1"


@dataclass(frozen=True)
class CampaignSpec:
    campaign_id: str
    experiments: tuple[str, ...]
    model_ids: tuple[str, ...]
    seeds: tuple[int, ...]
    generations: int
    agents_per_cell: int
    ram_budget: int
    max_tokens: int
    generation_settings: Mapping[str, Any]
    matched_control: str
    wall_clock_limit_seconds: int
    schema_version: str = CAMPAIGN_SCHEMA

    @classmethod
    def create(
        cls,
        *,
        experiments: Sequence[str],
        model_ids: Sequence[str],
        seeds: Sequence[int],
        generations: int,
        agents_per_cell: int,
        ram_budget: int,
        max_tokens: int,
        generation_settings: Mapping[str, Any],
        matched_control: str,
        wall_clock_limit_seconds: int,
    ) -> CampaignSpec:
        experiment_values = tuple(experiments)
        model_values = tuple(model_ids)
        seed_values = tuple(seeds)
        settings = dict(generation_settings)
        body = {"experiments": experiment_values, "model_ids": model_values, "seeds": seed_values, "generations": generations, "agents_per_cell": agents_per_cell, "ram_budget": ram_budget, "max_tokens": max_tokens, "generation_settings": settings, "matched_control": matched_control, "wall_clock_limit_seconds": wall_clock_limit_seconds}
        spec = cls(stable_id("N1-P", body), experiment_values, model_values, seed_values, generations, agents_per_cell, ram_budget, max_tokens, settings, matched_control, wall_clock_limit_seconds)
        spec.validate()
        return spec

    def validate(self) -> None:
        from .experiments import EXPERIMENTS
        if not self.experiments or set(self.experiments) - set(EXPERIMENTS):
            raise Neural1Error("campaign contains no experiments or an unknown experiment")
        if not self.model_ids or not self.seeds or len(set(self.seeds)) != len(self.seeds):
            raise Neural1Error("campaign requires models and unique seeds")
        if self.generations <= 0 or self.agents_per_cell <= 0 or self.max_tokens <= 0 or self.wall_clock_limit_seconds <= 0:
            raise Neural1Error("campaign bounds must be positive")
        if self.ram_budget not in {1024, 2048, 3072, 4096}:
            raise Neural1Error("campaign RAM budget must be 1K, 2K, 3K, or 4K")

    @property
    def cells(self) -> tuple[CampaignCell, ...]:
        return tuple(CampaignCell(self.campaign_id, experiment, model_id, seed) for experiment in self.experiments for model_id in self.model_ids for seed in self.seeds)

    def save(self, path: str | Path) -> None:
        CampaignEngine._atomic_json(Path(path), asdict(self))

    @classmethod
    def load(cls, path: str | Path) -> CampaignSpec:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
        if payload.get("schema_version") != CAMPAIGN_SCHEMA:
            raise Neural1Error("unsupported campaign schema")
        for key in ("experiments", "model_ids", "seeds"):
            payload[key] = tuple(payload[key])
        spec = cls(**payload)
        spec.validate()
        expected = cls.create(experiments=spec.experiments, model_ids=spec.model_ids, seeds=spec.seeds, generations=spec.generations, agents_per_cell=spec.agents_per_cell, ram_budget=spec.ram_budget, max_tokens=spec.max_tokens, generation_settings=spec.generation_settings, matched_control=spec.matched_control, wall_clock_limit_seconds=spec.wall_clock_limit_seconds)
        if expected.campaign_id != spec.campaign_id:
            raise Neural1Error("campaign ID does not match canonical specification")
        return spec


@dataclass(frozen=True)
class CampaignCell:
    campaign_id: str
    experiment_id: str
    model_id: str
    seed: int

    @property
    def cell_id(self) -> str:
        return stable_id("N1-CELL", asdict(self))


@dataclass
class CellCheckpoint:
    cell_id: str
    generation: int
    status: str
    snapshot_sha256: str
    snapshot_path: str
    transcript_sha256: str
    token_use: int = 0
    errors: list[Mapping[str, Any]] = field(default_factory=list)
    updated_at: str = ""
    schema_version: str = CHECKPOINT_SCHEMA


@dataclass(frozen=True)
class CampaignSummary:
    campaign_id: str
    status: str
    completed_cells: tuple[str, ...]
    incomplete_cells: tuple[str, ...]
    cancelled_cells: tuple[str, ...]
    elapsed_seconds: float


class CampaignEngine:
    def __init__(self, root: str | Path, registry: ModelRegistry, providers: Mapping[str, ModelProvider]) -> None:
        self.root = Path(root)
        self.registry = registry
        self.providers = dict(providers)
        self.runtime = ExperimentRuntime(self.root)

    def validate(self, spec: CampaignSpec) -> None:
        spec.validate()
        for model_id in spec.model_ids:
            model = self.registry.require(model_id)
            if model_id not in self.providers:
                raise Neural1Error(f"campaign has no provider instance for {model_id}")
            configured_limit = model.generation_defaults.get("max_tokens")
            if configured_limit is not None and int(configured_limit) > spec.max_tokens:
                raise Neural1Error(
                    f"model {model_id} max_tokens exceeds the campaign bound"
                )

    def run(self, spec: CampaignSpec, *, objective_factory: Callable[[CampaignCell, int], str], command_parser: Callable[[str], Sequence[str]]) -> CampaignSummary:
        self.validate(spec)
        campaign_root = self.root / "campaigns" / spec.campaign_id
        campaign_root.mkdir(parents=True, exist_ok=True)
        self._atomic_json(campaign_root / "spec.json", asdict(spec))
        started = monotonic()
        deadline = started + spec.wall_clock_limit_seconds
        completed: list[str] = []
        cancelled: list[str] = []
        for cell in spec.cells:
            if monotonic() >= deadline or (campaign_root / "CANCEL").exists():
                cancelled.extend(item.cell_id for item in spec.cells if item.cell_id not in completed)
                break
            checkpoint = self._run_cell(spec, cell, deadline, objective_factory, command_parser)
            if checkpoint.status == "COMPLETED":
                completed.append(cell.cell_id)
            elif checkpoint.status == "CANCELLED":
                cancelled.append(cell.cell_id)
        incomplete = [cell.cell_id for cell in spec.cells if cell.cell_id not in completed and cell.cell_id not in cancelled]
        status = "COMPLETED" if len(completed) == len(spec.cells) else "DEADLINE_OR_CANCELLED" if cancelled else "INCOMPLETE"
        summary = CampaignSummary(spec.campaign_id, status, tuple(sorted(completed)), tuple(sorted(incomplete)), tuple(sorted(set(cancelled))), monotonic() - started)
        self._atomic_json(campaign_root / "summary.json", asdict(summary))
        return summary

    def _run_cell(self, spec: CampaignSpec, cell: CampaignCell, deadline: float, objective_factory: Callable[[CampaignCell, int], str], command_parser: Callable[[str], Sequence[str]]) -> CellCheckpoint:
        cell_root = self.root / "campaigns" / spec.campaign_id / "cells" / cell.cell_id
        cell_root.mkdir(parents=True, exist_ok=True)
        checkpoint_path = cell_root / "checkpoint.json"
        checkpoint = self._load_checkpoint(checkpoint_path)
        if checkpoint and checkpoint.status == "COMPLETED":
            return checkpoint
        world = self._restore_checkpoint(checkpoint) if checkpoint else VirtualApple1World(ram_budget=spec.ram_budget)
        generation = checkpoint.generation if checkpoint else 0
        transcript_path = cell_root / "transcript.jsonl"
        token_use = checkpoint.token_use if checkpoint else 0
        errors = list(checkpoint.errors) if checkpoint else []
        while generation < spec.generations:
            if monotonic() >= deadline or (self.root / "campaigns" / spec.campaign_id / "CANCEL").exists():
                return self._checkpoint(cell, world, generation, "CANCELLED", transcript_path, token_use, errors, checkpoint_path)
            for agent_index in range(spec.agents_per_cell):
                agent_id = f"{cell.cell_id}-A{agent_index + 1:03d}"
                prompt = objective_factory(cell, generation)
                try:
                    result = self.providers[cell.model_id].generate(prompt, agent_id=agent_id, seed=cell.seed + generation * 1009 + agent_index)
                    outputs = [WozMonSession(world).transact(command) for command in command_parser(result.text)]
                    token_use += (result.prompt_tokens or 0) + (result.completion_tokens or 0)
                    record = {"generation": generation, "agent_id": agent_id, "prompt": prompt, "response": result.text, "outputs": outputs, "result": asdict(result)}
                except Exception as error:
                    failure = {"generation": generation, "agent_id": agent_id, "type": type(error).__name__, "message": str(error)}
                    errors.append(failure)
                    record = {"generation": generation, "agent_id": agent_id, "error": failure}
                self._append_jsonl(transcript_path, record)
            generation += 1
            world.generation = generation
            self._checkpoint(cell, world, generation, "RUNNING", transcript_path, token_use, errors, checkpoint_path)
        return self._checkpoint(cell, world, generation, "COMPLETED", transcript_path, token_use, errors, checkpoint_path)

    def _checkpoint(self, cell: CampaignCell, world: VirtualApple1World, generation: int, status: str, transcript_path: Path, token_use: int, errors: list[Mapping[str, Any]], path: Path) -> CellCheckpoint:
        snapshot = self.runtime.snapshot(world)
        transcript_hash = sha256_bytes(transcript_path.read_bytes()) if transcript_path.exists() else sha256_bytes(b"")
        snapshot_path = Path(snapshot.path)
        try:
            stored_path = snapshot_path.relative_to(self.root).as_posix()
        except ValueError as error:
            raise Neural1Error("snapshot escaped the campaign root") from error
        checkpoint = CellCheckpoint(cell.cell_id, generation, status, snapshot.sha256, stored_path, transcript_hash, token_use, errors, datetime.now(UTC).isoformat())
        self._atomic_json(path, asdict(checkpoint))
        return checkpoint

    def _restore_checkpoint(self, checkpoint: CellCheckpoint) -> VirtualApple1World:
        from .storage import ArtifactRecord
        relative_path = Path(checkpoint.snapshot_path)
        if relative_path.is_absolute() or ".." in relative_path.parts:
            raise Neural1Error("checkpoint snapshot path is not portable")
        path = self.root / relative_path
        payload = path.read_bytes()
        if sha256_bytes(payload) != checkpoint.snapshot_sha256:
            raise Neural1Error("checkpoint snapshot hash mismatch")
        return self.runtime.restore(ArtifactRecord(checkpoint.snapshot_sha256, len(payload), "application/x-neural1-snapshot", "canonical", str(path)))

    @staticmethod
    def _load_checkpoint(path: Path) -> CellCheckpoint | None:
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != CHECKPOINT_SCHEMA:
            raise Neural1Error("unsupported checkpoint schema")
        return CellCheckpoint(**payload)

    @staticmethod
    def _append_jsonl(path: Path, value: Mapping[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as stream:
            stream.write(canonical_json(value) + "\n")
            stream.flush()
            os.fsync(stream.fileno())

    @staticmethod
    def _atomic_json(path: Path, value: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
        os.replace(temporary, path)
