"""Record bounded host-only performance telemetry; never probes Apple-1 I/O."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import time
from datetime import UTC, datetime
from pathlib import Path


def sample() -> dict[str, object]:
    temperatures = {}
    for path in sorted(Path("/sys/class/thermal").glob("thermal_zone*/temp")):
        try:
            temperatures[path.parent.name] = int(path.read_text().strip()) / 1000
        except (OSError, ValueError):
            continue
    gpu: dict[str, object] = {}
    try:
        executable = shutil.which("nvidia-smi")
        if executable is None:
            raise OSError("nvidia-smi is unavailable")
        completed = subprocess.run(  # noqa: S603 - resolved fixed diagnostic executable; no user arguments
            [executable, "--query-gpu=temperature.gpu,power.draw,utilization.gpu,memory.used", "--format=csv,noheader,nounits"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )
        values = [part.strip() for part in completed.stdout.splitlines()[0].split(",")]
        gpu = dict(zip(("temperature_c", "power_w", "utilization_percent", "memory_used_mib"), values, strict=True))
    except (OSError, subprocess.SubprocessError, IndexError, ValueError):
        gpu = {"status": "UNAVAILABLE"}
    return {"recorded_at": datetime.now(UTC).isoformat(), "monotonic_seconds": time.monotonic(), "thermal_zones_c": temperatures, "nvidia": gpu}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--interval", type=float, default=30.0)
    parser.add_argument("--duration", type=float, required=True)
    args = parser.parse_args()
    if args.interval <= 0 or args.duration <= 0:
        parser.error("interval and duration must be positive")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + args.duration
    with args.output.open("a", encoding="utf-8") as stream:
        while time.monotonic() < deadline:
            stream.write(json.dumps(sample(), sort_keys=True) + "\n")
            stream.flush()
            time.sleep(min(args.interval, max(0, deadline - time.monotonic())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
