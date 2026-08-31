"""One shared manifest/snapshot/fork/replay runtime for all experiments."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from .core import SCHEMA_VERSION, Maturity, ModelRecord, Target, stable_id
from .storage import ArtifactRecord, ArtifactStore, EventLog
from .world import VirtualApple1World, WorldSnapshot


@dataclass(frozen=True)
class RunManifest:
    schema_version: str
    run_id: str
    experiment_id: str
    seed: int
    target: Target
    maturity: Maturity
    model: ModelRecord
    config: Mapping[str, Any]
    parent_run_id: str | None = None
    fork_point: str | None = None
    changed_factor: str | None = None

    @classmethod
    def create(cls, experiment_id: str, seed: int, model: ModelRecord, config: Mapping[str, Any]) -> RunManifest:
        identity = {"schema": SCHEMA_VERSION, "experiment": experiment_id, "seed": seed, "model": asdict(model), "config": config}
        return cls(SCHEMA_VERSION, stable_id("N1R", identity), experiment_id, seed, Target.VIRTUAL, Maturity.PROTOTYPE, model, dict(config))


class ExperimentRuntime:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.artifacts = ArtifactStore(self.root / "artifacts")

    def start(self, manifest: RunManifest) -> EventLog:
        run = self.root / "runs" / manifest.run_id
        run.mkdir(parents=True, exist_ok=True)
        (run / "manifest.json").write_text(__import__("json").dumps(asdict(manifest), indent=2, sort_keys=True, default=str) + "\n", encoding="ascii")
        events = EventLog(run / "events.jsonl")
        events.append("run_started", {"run_id": manifest.run_id, "target": manifest.target})
        return events

    def snapshot(self, world: VirtualApple1World) -> ArtifactRecord:
        snapshot = world.snapshot()
        header = f"N1SNAP1 {snapshot.ram_start} {snapshot.ram_budget} {snapshot.generation}\n".encode("ascii")
        return self.artifacts.put(header + snapshot.memory, media_type="application/x-neural1-snapshot")

    def restore(self, record: ArtifactRecord) -> VirtualApple1World:
        payload = Path(record.path).read_bytes()
        header, memory = payload.split(b"\n", 1)
        magic, start, budget, generation = header.decode("ascii").split()
        if magic != "N1SNAP1":
            raise ValueError("unsupported snapshot schema")
        return VirtualApple1World.restore(WorldSnapshot(memory, int(start), int(budget), int(generation)))

    def fork(self, base: RunManifest, *, fork_point: str, changed_factor: str, config: Mapping[str, Any]) -> RunManifest:
        candidate = RunManifest.create(base.experiment_id, base.seed, base.model, config)
        return replace(candidate, parent_run_id=base.run_id, fork_point=fork_point, changed_factor=changed_factor)

    def replay(self, manifest: RunManifest) -> RunManifest:
        return RunManifest.create(manifest.experiment_id, manifest.seed, manifest.model, manifest.config)
