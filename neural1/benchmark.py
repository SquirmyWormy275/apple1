"""Hardware-neutral benchmark harness; makes no Raspberry Pi performance claims."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence
from contextlib import suppress
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from .core import Neural1Error
from .models import ModelProvider
from .runtime import ExperimentRuntime
from .world import VirtualApple1World, WozMonSession


def benchmark(root: str | Path, iterations: int = 1000) -> dict[str, object]:
    if not 1 <= iterations <= 100_000:
        raise Neural1Error("benchmark iterations must be between 1 and 100000")
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


def benchmark_provider(provider: ModelProvider, *, prompts: list[str], agent_id: str = "BENCH", seed: int = 0, check: Callable[[], None] | None = None) -> dict[str, object]:
    if not 1 <= len(prompts) <= 4:
        raise Neural1Error("provider benchmark requires 1 to 4 prompts")
    latencies = []
    prompt_tokens = completion_tokens = errors = 0
    for prompt in prompts:
        if check:
            check()
        try:
            result = provider.generate(prompt, agent_id=agent_id, seed=seed)
            if result.latency_ms is not None:
                latencies.append(result.latency_ms)
            prompt_tokens += result.prompt_tokens or 0
            completion_tokens += result.completion_tokens or 0
        except Exception:
            errors += 1
        if check:
            check()
    return {"model": asdict(provider.record), "prompts": len(prompts), "errors": errors, "latency_ms": {"count": len(latencies), "mean": sum(latencies) / len(latencies) if latencies else None}, "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "tokens_per_second": "NOT AVAILABLE WITHOUT BACKEND TIMING"}


def benchmark_world_scaling(*, world_counts: tuple[int, ...] = (1, 4, 16), operations_per_world: int = 100) -> list[dict[str, float | int]]:
    if not world_counts or any(not 1 <= count <= 64 for count in world_counts) or not 1 <= operations_per_world <= 10000:
        raise Neural1Error("invalid bounded scaling workload")
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


def hardware_report(path: Path) -> dict[str, Any]:
    """Read native host diagnostics, never infer that this host is the target Pi."""
    def read_optional(location: str) -> str | None:
        try:
            return Path(location).read_text().strip().rstrip("\x00")
        except OSError:
            return None

    memory = {}
    for line in (read_optional("/proc/meminfo") or "").splitlines():
        key, value = line.split(":", 1)
        if key in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
            memory[key + "_bytes"] = int(value.split()[0]) * 1024
    temperatures = {}
    for zone in sorted(Path("/sys/class/thermal").glob("thermal_zone*/temp")):
        try:
            temperatures[zone.parent.name] = int(zone.read_text()) / 1000
        except (OSError, ValueError):
            continue
    governor = read_optional("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    revision = None
    with suppress(OSError, subprocess.SubprocessError):
        revision = subprocess.run(  # noqa: S603 - fixed read-only command
            ["/usr/bin/git", "rev-parse", "HEAD"], cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, check=True, timeout=5,
        ).stdout.strip()
    throttling = "UNAVAILABLE"
    executable = shutil.which("vcgencmd")
    if executable:
        with suppress(OSError, subprocess.SubprocessError):
            throttling = subprocess.run([executable, "get_throttled"], capture_output=True, text=True, check=True, timeout=5).stdout.strip()  # noqa: S603 - fixed diagnostic arguments
    ancestor = path.resolve()
    while not ancestor.exists():
        ancestor = ancestor.parent
    return {
        "recorded_at": datetime.now(UTC).isoformat(), "platform": platform.platform(), "machine": platform.machine(),
        "device_model": read_optional("/proc/device-tree/model"), "python": sys.version.split()[0], "revision": revision,
        "memory": memory, "thermal_zones_c": temperatures, "cpu_governor": governor, "throttling": throttling,
        "output_filesystem_free_bytes": shutil.disk_usage(ancestor).free,
        "power_supply_and_cooling": "REQUIRE_OPERATOR_OBSERVATION", "claim_scope": "OBSERVED_NATIVE_HOST_ONLY; target identity not established by benchmark",
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="absolute new JSON report path")
    parser.add_argument("--hardware-report", action="store_true", help="read native diagnostics only; no workload or inference")
    parser.add_argument("--ssd-root", type=Path)
    parser.add_argument("--expected-uuid")
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--registry", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--temperature-limit", type=float, default=75)
    args = parser.parse_args(argv)
    if not args.output.is_absolute() or args.output.exists():
        parser.error("output must be an absolute new file path")
    if not 1 <= args.iterations <= 100_000 or not 40 <= args.temperature_limit <= 80:
        parser.error("iterations 1..100000 and temperature limit 40..80 required")
    if bool(args.registry) != bool(args.model):
        parser.error("registry and model must be supplied together")
    if args.hardware_report and args.model:
        parser.error("hardware-report cannot run a provider")
    if bool(args.ssd_root) != bool(args.expected_uuid) or (not args.hardware_report and not args.ssd_root):
        parser.error("workloads require --ssd-root and --expected-uuid; provide both together")

    def check() -> None:
        if args.ssd_root:
            from .deployment import verify_storage
            verify_storage(args.ssd_root, args.expected_uuid, write_paths=(args.output, args.output.with_suffix(".artifacts")), min_free_bytes=512 * 1024**2)
        sample = hardware_report(args.output)
        temperatures = sample["thermal_zones_c"]
        if temperatures and max(temperatures.values()) >= args.temperature_limit:
            raise Neural1Error("benchmark stopped at configured temperature limit")
        available = sample["memory"].get("MemAvailable_bytes")
        if available is not None and available < 256 * 1024**2:
            raise Neural1Error("benchmark stopped: less than 256 MiB available RAM")

    started = perf_counter()
    report: dict[str, Any] = {"status": "RUNNING", "before": hardware_report(args.output), "hardware_report_only": args.hardware_report}
    try:
        if not args.hardware_report:
            check()
            report["world"] = benchmark(args.output.with_suffix(".artifacts"), args.iterations)
            check()
            report["world_scaling"] = benchmark_world_scaling(world_counts=(1, 4, 16), operations_per_world=min(args.iterations, 100))
            check()
            if args.registry:
                from .provider_factory import provider_for
                from .registry import ModelRegistry
                model = ModelRegistry.load(args.registry).require(args.model)
                settings = dict(model.generation_defaults)
                settings.update(max_tokens=64, timeout_seconds=30)
                provider = provider_for(replace(model, generation_defaults=settings), record_path=args.output.with_suffix(".artifacts") / "provider.jsonl")
                report["provider"] = benchmark_provider(provider, prompts=["Return only the uppercase word READY."], check=check)
                report["provider_limit"] = "one response; 64 tokens; 30-second transport timeout; thermal checks between stages (not continuous provider thermal control)"
                if report["provider"]["errors"]:
                    raise Neural1Error("provider benchmark recorded an error")
        report["status"] = "RECORDED"
    except (OSError, ValueError, Neural1Error) as error:
        report.update(status="STOPPED", error=str(error))
    report.update(after=hardware_report(args.output), elapsed_seconds=perf_counter() - started)
    # Refuse fallback report writes when the commissioned volume disappeared.
    if args.ssd_root:
        from .deployment import verify_storage
        verify_storage(args.ssd_root, args.expected_uuid, write_paths=(args.output,), min_free_bytes=0)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({"status": report["status"], "output": str(args.output)}))
    return 0 if report["status"] == "RECORDED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
