"""Hardware-neutral benchmark harness; makes no Raspberry Pi performance claims."""

from __future__ import annotations

import json
import platform
import sys
from dataclasses import asdict
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
    return {"environment": {"platform": platform.platform(), "machine": platform.machine(), "python": sys.version.split()[0]}, "iterations": iterations, "world_seconds": world_seconds, "world_operations_per_second": iterations / world_seconds, "snapshot_restore_seconds": snapshot_seconds, "snapshot_bytes": record.size, "restored_sha256": restored.snapshot().sha256, "model_metrics": "NOT MEASURED", "claim_scope": "DEVELOPMENT_HOST_ONLY"}


def benchmark_provider(provider, *, prompts: list[str], agent_id: str = "BENCH", seed: int = 0) -> dict[str, object]:
    latencies = []
    prompt_tokens = completion_tokens = errors = 0
    for prompt in prompts:
        try:
            result = provider.generate(prompt, agent_id=agent_id, seed=seed)
            if result.latency_ms is not None:
                latencies.append(result.latency_ms)
            prompt_tokens += result.prompt_tokens or 0
            completion_tokens += result.completion_tokens or 0
        except Exception:
            errors += 1
    return {"model": asdict(provider.record), "prompts": len(prompts), "errors": errors, "latency_ms": {"count": len(latencies), "mean": sum(latencies) / len(latencies) if latencies else None}, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "tokens_per_second": "NOT AVAILABLE WITHOUT BACKEND TIMING"}


def benchmark_world_scaling(*, world_counts: tuple[int, ...] = (1, 4, 16), operations_per_world: int = 100) -> list[dict[str, float | int]]:
    results = []
    for count in world_counts:
        worlds = [WozMonSession(VirtualApple1World()) for _ in range(count)]
        start = perf_counter()
        for index in range(operations_per_world):
            for session in worlds:
                session.transact(f"{0x0200 + index % 256:04X}: {index & 0xFF:02X}")
        seconds = perf_counter() - start
        operations = count * operations_per_world
        results.append({"worlds": count, "operations": operations, "seconds": seconds, "operations_per_second": operations / seconds})
    return results


if __name__ == "__main__":
    print(json.dumps(benchmark("out/neural1-benchmark"), indent=2, sort_keys=True))
