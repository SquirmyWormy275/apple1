"""One bounded P1/analyzer -> Pi/SerialOwner cycle, with a file-only simulator."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import signal
import socket
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from tools.propeller_remote_owner import durable_json, source_hashes
from tools.sigrok_summary import regular_file, summarize, write_json

CONFIG_KEYS = {"local_hostname", "analyzer_sysfs", "sigrok_cli", "ssh", "pi_ssh_host", "pi_hostname",
               "pi_repo", "pi_python", "pi_output_root", "serial_by_id", "serial_by_path", "setup_record"}
CHANNELS = ("TX-O", "RX-I", "RESn")
BAD_LEVELS = bytes(int(value & 7 != 7) for value in range(256))


class JobStop(RuntimeError):
    pass


@dataclass(frozen=True)
class Timing:
    rate: int = 4_000_000
    baseline: float = 12
    duration: float = 30
    pre: float = 5
    post: float = 5
    startup: float = 10
    stall: float = 3
    owner: float = 12
    poll: float = 0.02


LIVE_TIMING = Timing()


@contextmanager
def job_lock(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        os.close(descriptor)


def code_hashes() -> dict[str, str]:
    root = Path(__file__).resolve().parent
    return {**source_hashes(), **{name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                 for name in ("propeller_capture_job.py", "sigrok_summary.py")}}


def read_config(path: Path) -> dict:
    regular_file(path)
    config = json.loads(path.read_text())
    if not isinstance(config, dict) or set(config) != CONFIG_KEYS:
        raise ValueError("configuration must contain exactly the documented keys")
    for key, value in config.items():
        if not isinstance(value, str) or not value.strip() or "REPLACE" in value or "\n" in value or "\0" in value:
            raise ValueError(f"fill the actual {key}; placeholders are not executable")
    for key in CONFIG_KEYS - {"local_hostname", "pi_hostname", "pi_ssh_host"}:
        if not Path(config[key]).is_absolute():
            raise ValueError(f"{key} must be an absolute path")
    if re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_.@-]*", config["pi_ssh_host"]) is None:
        raise ValueError("pi_ssh_host must be an existing SSH alias or user@host")
    if not config["serial_by_id"].startswith("/dev/serial/by-id/") or not config["serial_by_path"].startswith("/dev/serial/by-path/"):
        raise ValueError("bind both /dev/serial/by-id and /dev/serial/by-path")
    setup = regular_file(Path(config["setup_record"]))
    if not 1 <= setup.stat().st_size <= 65536:
        raise ValueError("setup_record must be a nonempty record of at most 64 KiB")
    return config


def fingerprint(config: dict) -> str:
    material = {"config": config, "code": code_hashes(),
                "setup_sha256": hashlib.sha256(Path(config["setup_record"]).read_bytes()).hexdigest()}
    return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()


def remote_command(config: dict, action: str, run_id: str) -> list[str]:
    hashes = source_hashes()
    worker = ["timeout", "--signal=TERM", "--kill-after=2s", "5s", config["pi_python"],
              "-m", "tools.propeller_remote_owner", action, "--hostname", config["pi_hostname"],
              "--owner-sha", hashes["serial_owner.py"], "--worker-sha", hashes["propeller_remote_owner.py"],
              "--by-id", config["serial_by_id"], "--by-path", config["serial_by_path"],
              "--root", config["pi_output_root"], "--run-id", run_id]
    command = "cd -- " + shlex.quote(config["pi_repo"]) + " && exec " + shlex.join(worker)
    return [config["ssh"], "-T", "-oBatchMode=yes", "-oStrictHostKeyChecking=yes", "-oConnectTimeout=5",
            "-oConnectionAttempts=1", "-oServerAliveInterval=2", "-oServerAliveCountMax=2",
            "-oClearAllForwardings=yes", config["pi_ssh_host"], command]


def service_command(config_path: Path, root: Path, mode: str, qualification: Path | None) -> list[str]:
    launcher = shutil.which("systemd-run")
    inhibitor = shutil.which("systemd-inhibit")
    if launcher is None or inhibitor is None:
        raise ValueError("systemd-run and systemd-inhibit are required on P1")
    if re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{7,79}", root.name) is None:
        raise ValueError("invalid run ID for the service unit")
    if mode == "unattended" and qualification is None:
        raise ValueError("unattended launch needs an attended qualification receipt")
    argv = [launcher, "--user", "--collect", "--service-type=exec", "--expand-environment=no",
            f"--unit=propeller-{root.name}", f"--working-directory={Path(__file__).resolve().parents[1]}",
            "--property=Restart=no", "--property=RuntimeMaxSec=180", "--property=TimeoutStopSec=5",
            "--property=KillMode=control-group"]
    if "SSH_AUTH_SOCK" in os.environ:
        argv.append("--setenv=SSH_AUTH_SOCK=" + os.environ["SSH_AUTH_SOCK"])
    argv.extend([inhibitor, "--what=sleep", "--mode=block", "--no-ask-password", "--why=Propeller diagnostic capture",
                 sys.executable, "-m", "tools.propeller_capture_job", "run", "--config", str(config_path.resolve()),
                 "--out", str(root), "--mode", mode])
    if qualification is not None:
        argv.extend(["--qualification", str(qualification.resolve())])
    return argv


def stop_process(process: subprocess.Popen | None) -> None:
    if process is None or process.poll() is not None:
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        try:
            os.killpg(process.pid, sig)
        except ProcessLookupError:
            return
        try:
            process.wait(timeout=1)
            return
        except subprocess.TimeoutExpired:
            continue
    raise JobStop("child did not exit after termination")


def start_process(argv: list[str], stdout: Path, stderr: Path) -> subprocess.Popen:
    with stdout.open("xb") as output, stderr.open("xb") as errors:
        return subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=output, stderr=errors,  # noqa: S603 -- constructed argv, no local shell
                                start_new_session=True)


def bounded_command(argv: list[str], prefix: Path, seconds: float = 12) -> str:
    process = start_process(argv, prefix.with_suffix(".stdout"), prefix.with_suffix(".stderr"))
    try:
        if process.wait(timeout=seconds) != 0:
            raise JobStop(f"{prefix.name} failed; see retained stdout/stderr")
        path = prefix.with_suffix(".stdout")
        if path.stat().st_size > 1024 * 1024:
            raise JobStop("oversized command output")
        return path.read_text()
    except subprocess.TimeoutExpired as exc:
        raise JobStop(f"{prefix.name} timed out") from exc
    finally:
        stop_process(process)


class LiveBackend:
    physical = True

    def __init__(self, config: dict) -> None:
        self.config = config

    def check_analyzer(self) -> None:
        # sysfs descriptor reads only; no global sigrok/serial-device scan.
        matches = []
        for vendor in Path("/sys/bus/usb/devices").glob("*/idVendor"):
            try:
                if vendor.read_text().strip() == "0925" and (vendor.parent / "idProduct").read_text().strip() == "3881":
                    matches.append(vendor.parent.resolve())
            except FileNotFoundError:
                continue
        if matches != [Path(self.config["analyzer_sysfs"]).resolve()]:
            raise JobStop("expected exactly one 0925:3881 analyzer at the recorded USB location")

    def preflight(self, root: Path, run_id: str) -> dict:
        if socket.gethostname() != self.config["local_hostname"]:
            raise JobStop("run this configuration on its recorded P1 host")
        if shutil.disk_usage(root).free < 1024**3:
            raise JobStop("at least 1 GiB of free capture storage is required")
        self.check_analyzer()
        version = bounded_command([self.config["sigrok_cli"], "--version"], root / "sigrok-version")
        details = bounded_command([self.config["sigrok_cli"], "--driver", "fx2lafw:conn=0925.3881", "--show"],
                                  root / "analyzer-details")
        if set(re.findall(r"\bD\d+\b", details)) != {f"D{n}" for n in range(8)}:
            raise JobStop("expected the recorded eight-channel D0-D7 analyzer layout")
        self.check_analyzer()
        probe = json.loads(bounded_command(remote_command(self.config, "probe", run_id), root / "pi-probe"))
        if probe.get("hostname") != self.config["pi_hostname"] or probe.get("source_hashes") != source_hashes() or probe.get("serial_opened") is not False:
            raise JobStop("Pi probe did not establish the expected host and code without a serial open")
        return {"sigrok_version": version, "analyzer_details": details, "pi_probe": probe,
                "p1_python": platform.python_version()}

    def capture(self, root: Path, name: str, samples: int, seconds: float) -> list[str]:
        self.check_analyzer()
        return [self.config["sigrok_cli"], "--driver", "fx2lafw:conn=0925.3881",
                "--config", "samplerate=4000000", "--channels", "D0,D1,D2", "--samples", str(samples),
                "--output-format", "binary", "--loglevel", "2"]

    def owner(self, root: Path, run_id: str) -> list[str]:
        return remote_command(self.config, "session", run_id)


def validate_owner(value: dict, run_id: str, *, physical: bool) -> list[dict]:
    if value.get("run_id") != run_id or value.get("physical_device_access") is not physical or value.get("error"):
        raise JobStop("owner returned an error or wrong run identity")
    if value.get("source_hashes") != source_hashes() or value.get("retry_count") != 0:
        raise JobStop("owner code or retry policy differs")
    records = value.get("owner_records", [])
    if [record.get("event") for record in records] != ["opened", "startup_drained", "closed"]:
        raise JobStop("owner log does not establish exactly one open/drain/close")
    if records[0].get("control_policy") != {"dtr": False, "rts": False} or records[1].get("payload_hex") != "":
        raise JobStop("unexpected control policy or received startup bytes")
    return records


def capture_cycle(root: Path, name: str, backend: object, timing: Timing, state: dict, event) -> None:
    is_event = name == "event"
    duration = timing.duration if is_event else timing.baseline
    expected = int(duration * timing.rate)
    raw = root / f"{name}.bin"
    capture = start_process(backend.capture(root, name, expected, duration), raw, root / f"{name}.stderr")
    owner = None
    count = 0
    start = time.monotonic()
    last_data = start
    first_data = None
    owner_start = None
    owner_done = None
    receipt_count = None
    event("capture_started", capture=name, expected_samples=expected)
    try:
        with raw.open("rb") as stream:
            while True:
                now = time.monotonic()
                data = stream.read(1024 * 1024)
                if data:
                    count += len(data)
                    last_data = now
                    if first_data is None:
                        first_data = now
                    if count > expected:
                        raise JobStop(f"{name}: too many samples for the requested layout/count")
                    if data.translate(BAD_LEVELS).count(b"\x01"):
                        raise JobStop(f"{name}: observed UART low or RESn assertion; preserve and inspect")
                if now - start > duration + timing.startup:
                    raise JobStop(f"{name}: capture deadline exceeded")
                if now - last_data > (timing.startup if first_data is None else timing.stall):
                    raise JobStop(f"{name}: capture stalled")
                for log in root.glob("*.stderr"):
                    if log.stat().st_size > 1024 * 1024:
                        raise JobStop("child error log exceeded 1 MiB")
                if owner is not None and owner_done is None:
                    if owner.poll() is not None:
                        if owner.returncode != 0:
                            raise JobStop("Pi session failed or disconnected; outcome may be unknown; do not retry")
                        result_path = root / "owner-result.json"
                        if result_path.stat().st_size > 1024 * 1024:
                            raise JobStop("oversized owner result")
                        value = json.loads(result_path.read_text())
                        records = validate_owner(value, root.name, physical=backend.physical)
                        with (root / "owner.jsonl").open("x") as log:
                            log.writelines(json.dumps(record, sort_keys=True) + "\n" for record in records)
                        owner_done = now
                        receipt_count = count
                        state["owner_confirmed_closed"] = True
                        event("owner_receipt", received_samples=count)
                    elif now - owner_start > timing.owner:
                        raise JobStop("Pi session deadline exceeded; outcome may be unknown; do not retry")
                if capture.poll() is not None and not data:
                    if capture.returncode != 0 or count != expected:
                        raise JobStop(f"{name}: incomplete acquisition ({count}/{expected} samples)")
                    if is_event and (owner_done is None or now - owner_done < timing.post or count - receipt_count < timing.post * timing.rate):
                        raise JobStop("insufficient confirmed post-owner capture coverage")
                    event("capture_complete", capture=name, samples=count)
                    return
                if is_event and owner is None and first_data is not None and count >= timing.pre * timing.rate and now - first_data >= timing.pre:
                    if capture.poll() is not None or count > (duration - timing.post - timing.owner) * timing.rate:
                        raise JobStop("event capture is too far advanced to start the owner")
                    # Persist the attempt before starting SSH. Lost SSH never means
                    # that a physical open did not occur.
                    state["owner_attempted"] = True
                    durable_json(root / "owner-attempt.json", {"run_id": root.name, "samples_before_ssh": count,
                                                               "utc": datetime.now(UTC).isoformat()})
                    event("owner_invoked", samples_before_ssh=count)
                    owner_start = now
                    owner = start_process(backend.owner(root, root.name), root / "owner-result.json", root / "owner.stderr")
                if not data:
                    time.sleep(timing.poll)
    finally:
        try:
            stop_process(owner)
        finally:
            stop_process(capture)
            event("capture_stopped", capture=name, received_samples=count, saved_bytes=raw.stat().st_size)


def export_capture(raw: Path, rate: int) -> dict:
    """Retain raw driver bytes; export a separately labelled sigrok v2 view."""
    if raw.stat().st_size > 512 * 1024 * 1024:
        raise JobStop("raw capture exceeds export bound")
    sr = raw.with_suffix(".sr")
    with ZipFile(sr, "x", ZIP_DEFLATED) as archive:
        archive.writestr("version", "2")
        archive.writestr("metadata", "[global]\nsigrok version=derived-binary-export\n[device 1]\n"
                         f"capturefile=logic-1\nunitsize=1\ntotal probes=8\ntotal analog=0\nsamplerate={rate} Hz\n"
                         + "".join(f"probe{n + 1}={label}\n" for n, label in enumerate(CHANNELS)))
        with raw.open("rb") as stream:
            number = 1
            while data := stream.read(1024 * 1024):
                archive.writestr(f"logic-1-{number}", data)
                number += 1
    result = summarize(sr, expected_samples=raw.stat().st_size)
    result["provenance"] = "Derived from retained raw binary; metadata states requested rate and verified eight-bit layout."
    write_json(raw.with_suffix(".summary.json"), result)
    return result


def run_job(root: Path, config: dict, backend: object, *, mode: str, timing: Timing = LIVE_TIMING,
            qualification: Path | None = None) -> dict:
    if mode not in {"attended", "unattended", "simulation"} or (backend.physical and mode == "simulation"):
        raise ValueError("invalid job mode")
    if re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{7,79}", root.name) is None:
        raise ValueError("output directory name is the single-use run ID: 8-80 letters/digits/hyphens/underscores")
    identity = fingerprint(config)
    if mode == "unattended":
        if qualification is None:
            raise ValueError("unattended mode needs an attended qualification receipt")
        receipt = json.loads(regular_file(qualification).read_text())
        age = (datetime.now(UTC) - datetime.fromisoformat(receipt["qualified_utc"])).total_seconds()
        if receipt.get("fingerprint") != identity or receipt.get("display_stable") is not True or not 0 <= age <= 86400:
            raise ValueError("qualification must match this setup/code and be from the last 24 hours")
    root.mkdir(parents=True, exist_ok=False)
    state = {"run_id": root.name, "mode": mode, "evidence_class": "LIVE_CAPTURE" if backend.physical else "TEST_FIXTURE",
             "fingerprint": identity, "source_hashes": code_hashes(), "owner_attempted": False,
             "owner_confirmed_closed": False, "retry_count": 0, "display_result": "UNOBSERVED",
             "result": "STOP", "started_utc": datetime.now(UTC).isoformat(), "captures": []}
    write_json(root / "config.json", config)
    (root / "setup-record.md").write_bytes(Path(config["setup_record"]).read_bytes())
    started = time.monotonic()

    def event(name: str, **details) -> None:
        with (root / "events.jsonl").open("a") as log:
            log.write(json.dumps({"event": name, "utc": datetime.now(UTC).isoformat(),
                                  "elapsed_seconds": time.monotonic() - started, **details}, sort_keys=True) + "\n")

    try:
        state["environment"] = backend.preflight(root, root.name)
        if mode == "unattended" and state["environment"] != receipt.get("environment"):
            raise JobStop("host, analyzer, dependency versions or Pi identity changed since qualification")
        event("preflight_passed")
        capture_cycle(root, "baseline", backend, timing, state, event)
        capture_cycle(root, "event", backend, timing, state, event)
        state["result"] = "COMPLETE_DIGITAL_QUIET"
    except (Exception, KeyboardInterrupt) as exc:
        state["error"] = f"{type(exc).__name__}: {exc}"
        event("stop", reason=state["error"])
    finally:
        for name in ("baseline", "event"):
            raw = root / f"{name}.bin"
            if raw.exists() and raw.stat().st_size:
                try:
                    state["captures"].append(export_capture(raw, timing.rate))
                except Exception as exc:
                    state["result"] = "STOP"
                    state.setdefault("export_errors", []).append(f"{name}: {exc}")
        state["finished_utc"] = datetime.now(UTC).isoformat()
        state["elapsed_seconds"] = time.monotonic() - started
        state["scientific_result"] = "INCONCLUSIVE_ROOT_CAUSE"
        state["limits"] = ["Display was not observed by this runner; no camera or automatic visual diagnosis.",
                           "No exact shared timebase; sample offsets describe bytes received on P1.",
                           "Requested rate and byte counts do not independently prove no upstream sample loss.",
                           "Digital samples do not establish analog supply or ground stability.",
                           "A lost owner receipt leaves the physical-open outcome unknown; never retry automatically."]
        write_json(root / "result.json", state)
        lines = [f"# Propeller capture job: {state['result']}", "", f"Run: {root.name}",
                 f"Evidence: {state['evidence_class']}", f"Owner attempted: {state['owner_attempted']}",
                 f"Owner confirmed closed: {state['owner_confirmed_closed']}", "Display: UNOBSERVED",
                 "Root cause: INCONCLUSIVE", "", state.get("error", "One capture cycle completed; no repair claim."),
                 "", "Keep this directory, including partial binary files and stderr. Do not rerun an attempted run ID."]
        (root / "report.md").write_text("\n".join(lines) + "\n")
        hashes = {}
        for path in sorted(root.iterdir()):
            if path.is_file():
                with path.open("rb") as stream:
                    hashes[path.name] = hashlib.file_digest(stream, "sha256").hexdigest()
        write_json(root / "hashes.json", hashes)
    return state


def qualify(root: Path, *, display_stable: bool) -> Path:
    state = json.loads(regular_file(root / "result.json").read_text())
    if not display_stable or state.get("mode") != "attended" or state.get("evidence_class") != "LIVE_CAPTURE":
        raise ValueError("qualification requires an attended hardware capture and observed stable display")
    if state.get("result") != "COMPLETE_DIGITAL_QUIET" or state.get("owner_confirmed_closed") is not True:
        raise ValueError("a stopped or unconfirmed capture cannot qualify unattended operation")
    age = (datetime.now(UTC) - datetime.fromisoformat(state["finished_utc"])).total_seconds()
    if not 0 <= age <= 86400:
        raise ValueError("the attended run must have finished within the last 24 hours")
    config = read_config(root / "config.json")
    if fingerprint(config) != state["fingerprint"]:
        raise ValueError("code/setup changed after the attended run")
    for name, digest in json.loads((root / "hashes.json").read_text()).items():
        path = Path(name)
        if path.name != name:
            raise ValueError("invalid packet hash entry")
        with regular_file(root / name).open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != digest:
                raise ValueError(f"attended evidence changed: {name}")
    result = root / "qualification.json"
    write_json(result, {"fingerprint": state["fingerprint"], "attended_run_id": state["run_id"],
                        "environment": state["environment"],
                        "qualified_utc": datetime.now(UTC).isoformat(), "display_stable": True,
                        "meaning": "Operator observation, not a software measurement of the display."})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "run", "launch"):
        sub = commands.add_parser(name)
        sub.add_argument("--config", type=Path, required=True)
        sub.add_argument("--out", type=Path, required=True)
        if name in {"run", "launch"}:
            sub.add_argument("--mode", choices=("attended", "unattended"), required=True)
            sub.add_argument("--qualification", type=Path)
    sub = commands.add_parser("qualify")
    sub.add_argument("--run-dir", type=Path, required=True)
    sub.add_argument("--display-stable", action="store_true", help="operator observed stability throughout the attended cycle")
    sub = commands.add_parser("rehearse")
    sub.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "qualify":
        print(qualify(args.run_dir.resolve(), display_stable=args.display_stable))
        return 0
    if args.command == "rehearse":
        from tools.propeller_job_simulation import rehearse_all
        return rehearse_all(args.out.resolve())
    config = read_config(args.config)
    root = args.out.resolve()
    if args.command == "plan":
        print(json.dumps({"device_access": False, "run_id": root.name, "fingerprint": fingerprint(config),
                          "baseline_samples": 48000000, "event_samples": 120000000,
                          "pi_probe_argv": remote_command(config, "probe", root.name),
                          "pi_session_argv": remote_command(config, "session", root.name),
                          "pi_collect_argv": remote_command(config, "collect", root.name)}, indent=2))
        return 0
    if args.command == "launch":
        if socket.gethostname() != config["local_hostname"] or root.exists():
            raise ValueError("launch requires the recorded P1 host and a new output directory")
        argv = service_command(args.config, root, args.mode, args.qualification)
        subprocess.run(argv, check=True, timeout=15)  # noqa: S603 -- explicit systemd argv; no shell
        print(json.dumps({"service": f"propeller-{root.name}.service", "output": str(root),
                          "status": "START_REQUESTED; inspect journal and result.json for execution outcome"}))
        return 0
    def interrupted(signum, frame):
        raise KeyboardInterrupt(f"signal {signum}")

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGHUP, interrupted)
    with job_lock(Path.home() / ".cache/apple1/propeller-capture.lock"):
        result = run_job(root, config, LiveBackend(config), mode=args.mode, qualification=args.qualification)
    print(json.dumps({key: result[key] for key in ("run_id", "result", "owner_attempted", "owner_confirmed_closed")}))
    return 0 if result["result"] == "COMPLETE_DIGITAL_QUIET" else 1


if __name__ == "__main__":
    raise SystemExit(main())
