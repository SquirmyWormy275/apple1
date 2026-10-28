"""Capture two bounded local-model proposals, or verify their retained evidence offline."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
from dataclasses import asdict
from datetime import UTC, datetime
from importlib.metadata import version
from pathlib import Path
from urllib.request import urlopen

from neural1.core import canonical_json
from neural1.drivers import parse_commands
from neural1.models import OllamaHttpProvider
from neural1.world import VirtualApple1World, WozMonSession

PROMPTS = {
    "unassisted": (
        "Write NMOS 6502 machine code at $0300 that fills exactly $0400 through $0404 "
        "with $2A, leaves all other memory unchanged, then JMP $FF1F. "
        "Return only Woz Monitor deposit lines (0300: XX XX ...) and 0300R. "
        "No prose. At most 256 program bytes. No hardware is connected."
    ),
    "scaffolded": (
        "Write NMOS 6502 machine code at $0300. Use this algorithm: LDY #$00; "
        "LDA #$2A; LOOP: STA $0400,Y; INY; CPY #$05; BNE LOOP; JMP $FF1F. "
        "Opcode reference: LDY immediate A0 nn, LDA immediate A9 nn, STA absolute,Y "
        "99 lo hi, INY C8, CPY immediate C0 nn, BNE D0 signed-offset-from-next-PC, "
        "JMP absolute 4C lo hi. Compute all bytes and the branch offset. "
        "Return only Woz Monitor deposit lines (0300: XX XX ...) and 0300R. "
        "No prose. At most 256 program bytes. No hardware is connected."
    ),
}


def evaluate(text: str) -> dict:
    """Check a proposal by fresh execution, including write boundaries and sentinels."""
    world = VirtualApple1World(ram_start=0x300, ram_budget=1024)
    world.host_write(0x3FF, b"\xA5")
    world.host_write(0x405, b"\xA5")
    commands = list(parse_commands(text))
    rejected = []
    deposited = 0
    run_requests = 0
    monitor = WozMonSession(world, execute_runs=False)
    for command in commands:
        match = re.fullmatch(r"([0-9A-F]{1,4}):\s*([0-9A-F ]+)", command)
        if match:
            address = int(match[1], 16)
            payload = bytes.fromhex(match[2])
            if not 0x300 <= address < address + len(payload) <= 0x400:
                rejected.append(command)
                continue
            deposited += len(payload)
            monitor.transact(command)
        elif command == "0300R":
            run_requests += 1
        else:
            rejected.append(command)
    writes: list[int] = []
    result = world.execute(0x300, max_instructions=200, trace_limit=200, write_observer=writes.append)
    memory = world.host_read(0x3FF, 7)
    checks = {
        "program_deposited": 0 < deposited <= 256,
        "one_run_request": run_requests == 1,
        "no_disallowed_commands": not rejected,
        "monitor_return": result.stop_reason == "MONITOR_WARM_ENTRY",
        "five_correct_bytes_and_sentinels": memory == b"\xA5" + b"\x2A" * 5 + b"\xA5",
        "writes_exactly_once_to_each_destination": sorted(writes) == list(range(0x400, 0x405)),
    }
    return {
        "passed": all(checks.values()), "checks": checks, "commands": commands,
        "rejected_commands": rejected, "memory_03ff_0405": memory.hex(" ").upper(),
        "writes": writes, "execution": asdict(result),
    }


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def capture(destination: Path, models: Path, model: str, base_url: str, api: str = "generate") -> None:
    if destination.exists():
        raise ValueError("Use a new output directory; captures are never overwritten")
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+:[a-zA-Z0-9_.-]+", model):
        raise ValueError("Use an explicitly installed library model with name:tag")
    name, tag = model.split(":")
    manifest = models / "manifests/registry.ollama.ai/library" / name / tag
    identity = json.loads(manifest.read_text())
    blobs = []
    for layer in [identity["config"], *identity["layers"]]:
        expected = layer["digest"].removeprefix("sha256:")
        path = models / "blobs" / f"sha256-{expected}"
        if not re.fullmatch(r"[0-9a-f]{64}", expected) or digest(path) != expected or path.stat().st_size != layer["size"]:
            raise ValueError("Cached model blob identity mismatch")
        blobs.append({"sha256": expected, "bytes": layer["size"], "media_type": layer["mediaType"]})
    # No downloads, daemon changes, model qualification or physical I/O here.
    provider = OllamaHttpProvider(
        model, base_url=base_url, timeout_seconds=90, keep_alive=0, api=api,
        options={"temperature": 0, "num_predict": 192, "num_gpu": 0, "num_thread": 4},
        context_limit=2048, model_hash=digest(manifest),
    )
    def get(path):
        with urlopen(f"{provider.base_url.rstrip('/')}/api/{path}", timeout=5) as response:  # noqa: S310 - provider validated loopback HTTP
            return json.load(response)

    runtime = get("version")
    listed = next((item for item in get("tags")["models"] if item["name"] == model), None)
    if listed is None or listed["digest"] != digest(manifest):
        raise ValueError("Running server model differs from identified cached manifest")
    provider.quantization = listed.get("details", {}).get("quantization_level", "UNAVAILABLE")
    destination.mkdir(parents=True)
    sources = destination / "sources"
    sources.mkdir()
    for relative in ("tools/textbook_native.py", "neural1/world.py", "neural1/models.py", "neural1/drivers.py", "neural1/core.py"):
        source = Path(__file__).parents[1] / relative
        (sources / source.name).write_bytes(source.read_bytes())
    (destination / "model-manifest.json").write_bytes(manifest.read_bytes())
    board_path = Path("/proc/device-tree/model")
    board = board_path.read_text().rstrip("\0") if board_path.exists() else None
    receipt = {
        "schema": "textbook-native/v1", "target": "REAL_PI_LOCAL_MODEL_VIRTUAL_6502" if board and board.startswith("Raspberry Pi") else "WORKSTATION_LOCAL_MODEL_VIRTUAL_6502",
        "started_utc": datetime.now(UTC).isoformat(), "machine": platform.machine(),
        "python": platform.python_version(), "model": asdict(provider.record), "blobs": blobs,
        "runtime": runtime, "server_model": listed, "board": board, "py65": version("py65"),
        "serial_opened": False, "download_requested": False,
        "source_sha256": {p.name: digest(p) for p in sources.iterdir()},
        "trials": [],
    }
    control_prompt = "What is 2 + 2? Answer with one number."
    print("Generating arithmetic health control", flush=True)
    control = provider.generate(control_prompt, agent_id="textbook-control", seed=7)
    (destination / "health-control.json").write_text(json.dumps({"prompt": control_prompt, "generation": asdict(control), "expected": "4", "passed": control.text.strip() == "4"}, indent=2, sort_keys=True) + "\n")
    for label, prompt in PROMPTS.items():
        print(f"Generating {label} with {model} (90 second request limit)", flush=True)
        result = provider.generate(prompt, agent_id="textbook", seed=7)
        trial = {"label": label, "prompt": prompt, "generation": asdict(result), "evaluation": evaluate(result.text)}
        (destination / f"{label}.json").write_text(json.dumps(trial, indent=2, sort_keys=True) + "\n")
        receipt["trials"].append(label)
        print(f"{label}: task passed={trial['evaluation']['passed']}", flush=True)
    receipt["finished_utc"] = datetime.now(UTC).isoformat()
    receipt["files_sha256"] = {p.relative_to(destination).as_posix(): digest(p) for p in sorted(destination.rglob("*")) if p.is_file()}
    (destination / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")


def verify(directory: Path) -> dict:
    receipt = json.loads((directory / "receipt.json").read_text())
    for name, expected in receipt["files_sha256"].items():
        path = (directory / name).resolve()
        if not path.is_relative_to(directory.resolve()) or digest(path) != expected:
            raise ValueError("Retained evidence hash mismatch")
    if digest(directory / "model-manifest.json") != receipt["model"]["hash"]:
        raise ValueError("Model manifest identity mismatch")
    for label in receipt["trials"]:
        trial = json.loads((directory / f"{label}.json").read_text())
        if canonical_json(evaluate(trial["generation"]["text"])) != canonical_json(trial["evaluation"]):
            raise ValueError("Retained proposal evaluation differs")
        metadata = trial["generation"]["provider_metadata"]
        raw = metadata["raw_response_utf8"]
        if hashlib.sha256(raw.encode()).hexdigest() != metadata["raw_response_sha256"]:
            raise ValueError("Provider response identity mismatch")
        payload = json.loads(raw)
        response_text = payload.get("message", {}).get("content") if metadata["api"] == "chat" else payload.get("response")
        if response_text != trial["generation"]["text"]:
            raise ValueError("Retained response text differs from raw provider response")
    return receipt


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    collect = sub.add_parser("capture")
    collect.add_argument("--model", required=True)
    collect.add_argument("--models-dir", type=Path, required=True)
    collect.add_argument("--base-url", default="http://127.0.0.1:11434")
    collect.add_argument("--api", choices=("generate", "chat"), default="generate")
    collect.add_argument("--out", type=Path, required=True)
    check = sub.add_parser("verify")
    check.add_argument("directory", type=Path)
    args = parser.parse_args(argv)
    if args.command == "capture":
        capture(args.out, args.models_dir, args.model, args.base_url, args.api)
    else:
        receipt = verify(args.directory)
        print(f"Verified {len(receipt['trials'])} retained real-model proposals and fresh virtual evaluations; no inference requested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
