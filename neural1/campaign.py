"""Crash-safe experiment matrices with deterministic checkpoint/resume behavior."""

from __future__ import annotations

import fcntl
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
    next_agent: int = 0


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

    def campaign_path(self, campaign_id: str) -> Path:
        if not campaign_id or Path(campaign_id).name != campaign_id or campaign_id in {".", ".."}:
            raise Neural1Error("invalid campaign ID")
        return self.root / "campaigns" / campaign_id

    def cancel(self, campaign_id: str) -> None:
        root = self.campaign_path(campaign_id)
        if not (root / "spec.json").is_file():
            raise Neural1Error("unknown campaign")
        if not (root / "CANCEL").exists():
            self._atomic_json(root / "CANCEL", {"owner": "neural1-campaign", "campaign_id": campaign_id})

    def resume(self, spec: CampaignSpec, **kwargs: Any) -> CampaignSummary:
        return self.run(spec, resume=True, **kwargs)

    def run(self, spec: CampaignSpec, *, objective_factory: Callable[[CampaignCell, int], str], command_parser: Callable[[str], Sequence[str]], resume: bool = False, safety_check: Callable[[], None] | None = None) -> CampaignSummary:
        root = self.campaign_path(spec.campaign_id)
        root.mkdir(parents=True, exist_ok=True)
        with (root / "run.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise Neural1Error("campaign is already running") from error
            marker = root / "CANCEL"
            if resume and marker.exists():
                try:
                    owned = json.loads(marker.read_text())
                except ValueError as error:
                    raise Neural1Error("cannot remove an unowned cancellation marker") from error
                if owned != {"owner": "neural1-campaign", "campaign_id": spec.campaign_id}:
                    raise Neural1Error("cannot remove an unowned cancellation marker")
                marker.unlink()
            return self._run(spec, objective_factory=objective_factory, command_parser=command_parser, safety_check=safety_check)

    def _run(self, spec: CampaignSpec, *, objective_factory: Callable[[CampaignCell, int], str], command_parser: Callable[[str], Sequence[str]], safety_check: Callable[[], None] | None) -> CampaignSummary:
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
            checkpoint = self._run_cell(spec, cell, deadline, objective_factory, command_parser, safety_check)
            if checkpoint.status == "COMPLETED":
                completed.append(cell.cell_id)
            elif checkpoint.status == "CANCELLED":
                cancelled.append(cell.cell_id)
        incomplete = [cell.cell_id for cell in spec.cells if cell.cell_id not in completed and cell.cell_id not in cancelled]
        status = "COMPLETED" if len(completed) == len(spec.cells) else "DEADLINE_OR_CANCELLED" if cancelled else "INCOMPLETE"
        summary = CampaignSummary(spec.campaign_id, status, tuple(sorted(completed)), tuple(sorted(incomplete)), tuple(sorted(set(cancelled))), monotonic() - started)
        self._atomic_json(campaign_root / "summary.json", asdict(summary))
        return summary

    def _run_cell(self, spec: CampaignSpec, cell: CampaignCell, deadline: float, objective_factory: Callable[[CampaignCell, int], str], command_parser: Callable[[str], Sequence[str]], safety_check: Callable[[], None] | None) -> CellCheckpoint:
        cell_root = self.campaign_path(spec.campaign_id) / "cells" / cell.cell_id
        cell_root.mkdir(parents=True, exist_ok=True)
        checkpoint_path = cell_root / "checkpoint.json"
        checkpoint = self._load_checkpoint(checkpoint_path)
        world = self._restore_checkpoint(checkpoint) if checkpoint else VirtualApple1World(ram_budget=spec.ram_budget)
        generation = checkpoint.generation if checkpoint else 0
        next_agent = checkpoint.next_agent if checkpoint else 0
        transcript_path = cell_root / "transcript.jsonl"
        records = self._recover_transcript(transcript_path, checkpoint)
        if checkpoint and checkpoint.status == "COMPLETED":
            return checkpoint
        token_use = checkpoint.token_use if checkpoint else 0
        errors = list(checkpoint.errors) if checkpoint else []
        while generation < spec.generations:
            for agent_index in range(next_agent, spec.agents_per_cell):
                if monotonic() >= deadline or (self.campaign_path(spec.campaign_id) / "CANCEL").exists():
                    return self._checkpoint(cell, world, generation, "CANCELLED", transcript_path, token_use, errors, checkpoint_path, agent_index)
                if safety_check:
                    try:
                        safety_check()
                    except Neural1Error as error:
                        errors.append({"generation": generation, "type": "ResourceStop", "message": str(error)})
                        return self._checkpoint(cell, world, generation, "RESOURCE_STOP", transcript_path, token_use, errors, checkpoint_path, agent_index)
                agent_id = f"{cell.cell_id}-A{agent_index + 1:03d}"
                objective = objective_factory(cell, generation)
                observations = []
                if cell.experiment_id == "ram-republic":
                    # A declared public RAM examination is the sole cross-participant channel.
                    observations = [{"command": "0200.020F", "output": WozMonSession(world).transact("0200.020F")}]
                    objective += "\nCURRENT SHARED MONITOR EXAMINATION:\n" + observations[0]["output"]
                reset_every = int(spec.generation_settings.get("context_reset_generations", 0))
                since = generation - generation % reset_every if reset_every else 0
                private = [record for record in records if record["agent_id"] == agent_id and record["generation"] >= since][-4:]
                feedback: list[str] = []
                for previous in private:
                    if "outputs" in previous:
                        channel = "DESIGN VALIDATOR" if cell.experiment_id == "1976-multiverse" else "WOZMON"
                        feedback.extend(f"{channel}:{output}" for output in previous["outputs"])
                        if not previous["outputs"]:
                            feedback.append(f"{channel}: previous response contained no valid command; follow the required output grammar.")
                    elif "error" in previous:
                        feedback.append("WOZMON: previous turn was rejected; emit strict monitor commands.")
                # Conservative character bound; never expose another participant's transcript.
                budget = max(0, self.registry.require(cell.model_id).context_limit - spec.max_tokens - len(objective) - 128)
                history = "\n".join(feedback)[-budget:] if budget else ""
                prompt = objective + ("\nYOUR PRIVATE MONITOR OBSERVATIONS:\n" + history if history else "")
                result = None
                try:
                    result = self.providers[cell.model_id].generate(prompt, agent_id=agent_id, seed=cell.seed + generation * 1009 + agent_index)
                    token_use += (result.prompt_tokens or 0) + (result.completion_tokens or 0)
                    if cell.experiment_id == "1976-multiverse":
                        from .family_runner import process_multiverse_response
                        proposal = process_multiverse_response(result.text)
                        record = {"generation": generation, "agent_id": agent_id, "prompt": prompt, "response": result.text, "proposal": proposal, "outputs": proposal["outputs"], "accepted_proposals": proposal["accepted_proposals"], "result": asdict(result)}
                    else:
                        commands = list(command_parser(result.text))
                        outputs = [WozMonSession(world).transact(command) for command in commands]
                        accepted = sum(not output.startswith("ERR") for output in outputs)
                        record = {"generation": generation, "agent_id": agent_id, "prompt": prompt, "response": result.text, "commands": commands, "outputs": outputs, "observations": observations, "accepted_commands": accepted, "result": asdict(result)}
                except Exception as error:
                    failure = {"generation": generation, "agent_id": agent_id, "type": type(error).__name__, "message": str(error)}
                    errors.append(failure)
                    record = {"generation": generation, "agent_id": agent_id, "prompt": prompt, "error": failure}
                    if result is not None:
                        record.update(response=result.text, result=asdict(result))
                self._append_jsonl(transcript_path, record)
                records.append(record)
                self._checkpoint(cell, world, generation, "RUNNING", transcript_path, token_use, errors, checkpoint_path, agent_index + 1)
            generation += 1
            next_agent = 0
            world.generation = generation
            self._checkpoint(cell, world, generation, "RUNNING", transcript_path, token_use, errors, checkpoint_path)
        from .family_runner import evaluate_family

        family_result = evaluate_family(cell.experiment_id, world, records)
        self._atomic_json(cell_root / "family-result.json", family_result)
        accepted_total = sum(record.get("accepted_commands", sum(not output.startswith("ERR") for output in record.get("outputs", []))) for record in records)
        if cell.experiment_id == "1976-multiverse":
            # A parsed, scientifically rejected genome is a completed negative
            # evaluation. A malformed response never supplied a candidate.
            accepted_total = sum(isinstance(proposal, Mapping) and isinstance(proposal.get("genome"), Mapping) for record in records if (proposal := record.get("proposal")) is not None)
        terminal_errors = [error for error in errors if error.get("type") != "ResourceStop"]
        status = "COMPLETED" if accepted_total and not terminal_errors else "FAILED" if terminal_errors else "NO_ACCEPTED_COMMANDS"
        if family_result.get("status") == "BLOCKED":
            status = "BLOCKED"
        return self._checkpoint(cell, world, generation, status, transcript_path, token_use, errors, checkpoint_path)

    @staticmethod
    def _recover_transcript(path: Path, checkpoint: CellCheckpoint | None) -> list[dict[str, Any]]:
        payload = path.read_bytes() if path.exists() else b""
        expected = checkpoint.transcript_sha256 if checkpoint else sha256_bytes(b"")
        if sha256_bytes(payload) != expected:
            # Only discard a tail after a verified committed prefix. Preserve it for audit.
            prefix = b""
            for line in payload.splitlines(keepends=True):
                if sha256_bytes(prefix) == expected:
                    break
                prefix += line
            if sha256_bytes(prefix) != expected:
                raise Neural1Error("checkpoint transcript hash mismatch")
            orphan = path.with_name("uncommitted-" + sha256_bytes(payload) + ".jsonl")
            orphan.write_bytes(payload[len(prefix):])
            path.write_bytes(prefix)
            payload = prefix
        return [json.loads(line) for line in payload.splitlines()]

    def _checkpoint(self, cell: CampaignCell, world: VirtualApple1World, generation: int, status: str, transcript_path: Path, token_use: int, errors: list[Mapping[str, Any]], path: Path, next_agent: int = 0) -> CellCheckpoint:
        snapshot = self.runtime.snapshot(world)
        transcript_hash = sha256_bytes(transcript_path.read_bytes()) if transcript_path.exists() else sha256_bytes(b"")
        snapshot_path = Path(snapshot.path)
        try:
            stored_path = snapshot_path.relative_to(self.root).as_posix()
        except ValueError as error:
            raise Neural1Error("snapshot escaped the campaign root") from error
        checkpoint = CellCheckpoint(cell.cell_id, generation, status, snapshot.sha256, stored_path, transcript_hash, token_use, errors, datetime.now(UTC).isoformat(), next_agent=next_agent)
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
        with temporary.open("w", encoding="utf-8") as stream:
            stream.write(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
