"""Pi-side single-use, no-transmit worker for the Propeller capture job."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import socket
import stat
from datetime import UTC, datetime
from pathlib import Path

from tools.serial_owner import PySerialTransport, SerialOwner, TargetIdentity


def source_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in ("serial_owner.py", "propeller_remote_owner.py")}


def durable_json(path: Path, data: object) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(data, stream, sort_keys=True)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def execute_once(target: TargetIdentity, root: Path, run_id: str, transport: object,
                 *, physical: bool, settle_seconds: float = 0.2) -> dict:
    """The durable run directory is consumed before any transport is opened.

    Target/host/source/character-device checks belong to main's live preflight.
    Injection here lets tests and the simulator exercise this exact lifecycle.
    """
    if re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{7,79}", run_id) is None:
        raise ValueError("run-id must contain 8-80 letters, digits, hyphens or underscores")
    root.mkdir(parents=True, exist_ok=True)
    run = root / run_id
    run.mkdir()  # Never reuse an attempted run, even after timeout/SSH loss.
    descriptor = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    durable_json(run / "attempt.json", {"run_id": run_id, "utc": datetime.now(UTC).isoformat(),
                                       "physical_device_access": physical})
    owner = SerialOwner(target, Path("/tmp/apple1-serial-owner.lock") if physical else root / "fake-owner.lock",  # noqa: S108 -- shared existing owner lock
                        transport, run / "owner.jsonl", settle_seconds=settle_seconds)
    error = None
    try:
        owner.acquire_and_open()
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
    finally:
        try:
            owner.close()
        except Exception as exc:
            error = f"cleanup {type(exc).__name__}: {exc}"
        finally:
            # SerialOwner's evidence recording may fail if identity disappears.
            # Always close the transport and release our own lock in that case.
            try:
                transport.close()
            finally:
                owner.lock.release()
    log = run / "owner.jsonl"
    records = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
    result = {"run_id": run_id, "hostname": socket.gethostname(), "source_hashes": source_hashes(),
              "physical_device_access": physical, "error": error, "owner_records": records,
              "remote_directory": str(run), "retry_count": 0}
    durable_json(run / "result.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("probe", "session", "collect"))
    parser.add_argument("--hostname", required=True)
    parser.add_argument("--owner-sha", required=True)
    parser.add_argument("--worker-sha", required=True)
    parser.add_argument("--by-id", type=Path, required=True)
    parser.add_argument("--by-path", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    if socket.gethostname() != args.hostname:
        raise ValueError("Pi hostname differs from the configured host")
    expected = {"serial_owner.py": args.owner_sha, "propeller_remote_owner.py": args.worker_sha}
    if source_hashes() != expected:
        raise ValueError("Pi worker/SerialOwner bytes differ from the P1 checkout")
    if not args.root.is_absolute() or re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{7,79}", args.run_id) is None:
        raise ValueError("root must be absolute and run-id must be valid")
    if args.command == "collect":
        # Read-only recovery after an ambiguous SSH outcome. Never reopens.
        result = args.root / args.run_id / "result.json"
        print(result.read_text() if result.is_file() else json.dumps({"run_id": args.run_id, "result_missing": True}))
        return 0
    target = TargetIdentity(args.by_id, args.by_path)
    device = target.validate()
    if not stat.S_ISCHR(device.stat().st_mode):
        raise ValueError("the configured serial identity is not a character device")
    version = importlib.metadata.version("pyserial")
    if args.command == "probe":
        if (args.root / args.run_id).exists():
            raise FileExistsError("this run-id has already been attempted on the Pi")
        print(json.dumps({"hostname": socket.gethostname(), "identity": target.as_record(),
                          "source_hashes": source_hashes(), "pyserial_version": version,
                          "python_version": platform.python_version(),
                          "serial_opened": False}))
        return 0
    result = execute_once(target, args.root, args.run_id, PySerialTransport(device), physical=True)
    print(json.dumps(result, sort_keys=True))
    return 1 if result["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
