"""Hardware-neutral benchmark harness; makes no Raspberry Pi performance claims."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from time import perf_counter

from .runtime import ExperimentRuntime
from .world import VirtualApple1World, WozMonSession


def benchmark(root: str | Path, iterations: int = 1000) -> dict[str, object]:
    world = VirtualApple1World()
    session = WozMonSession(world)
    start = perf_counter()
    for index in range(iterations):
        address = 0x0200 + (index % 256)
        session.transact(f"{address:04X}: {index & 0xFF:02X}")
    world_seconds = perf_counter() - start
    runtime = ExperimentRuntime(root)
    start = perf_counter()
    record = runtime.snapshot(world)
    restored = runtime.restore(record)
    snapshot_seconds = perf_counter() - start
    return {"iterations": iterations, "world_seconds": world_seconds, "world_operations_per_second": iterations / world_seconds, "snapshot_restore_seconds": snapshot_seconds, "snapshot_bytes": record.size, "restored_sha256": restored.snapshot().sha256, "model_metrics": "NOT MEASURED"}


if __name__ == "__main__":
    print(json.dumps(benchmark("out/neural1-benchmark"), indent=2, sort_keys=True))
