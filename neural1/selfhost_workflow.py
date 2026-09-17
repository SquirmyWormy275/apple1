"""Persistent SELFHOST qualification from actual saved virtual run artifacts.

Evidence executes only bounded 6502 programs. No Python callbacks, shell code,
network providers, or automatic compiler claims are accepted from input files.
"""

from __future__ import annotations

import fcntl
import json
import os
import re
import shutil
import tempfile
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from .core import Neural1Error, canonical_json, sha256_bytes, stable_id
from .drivers import parse_commands
from .experiments import SelfHost
from .world import VirtualApple1World, WozMonSession

SCHEMA = "neural1-selfhost-archive-1"


def _json(path: Path) -> Any:
    if path.stat().st_size > 4 * 1024**2:
        raise Neural1Error("SELFHOST evidence exceeds 4 MiB")
    return json.loads(path.read_text())


def _replay(evidence: Mapping[str, Any]) -> bytes:
    world = VirtualApple1World()
    for record in evidence["transcript"]:
        if "error" in record:
            raise Neural1Error("cannot qualify a transcript containing failed provider turns")
        commands = list(parse_commands(record["response"]))
        outputs = [WozMonSession(world).transact(command) for command in commands]
        if outputs != record["outputs"]:
            raise Neural1Error("recorded monitor output differs from independent replay")
    return world.host_read(0x200, 4096)


def _execute(image: bytes, plan: Mapping[str, Any], *, expected: bool = False) -> tuple[bytes, dict[str, Any]]:
    required = {"input_hex", "input_address", "entrypoint", "output_address", "max_instructions", "expected_hex" if expected else "output_bytes"}
    if set(plan) != required:
        raise Neural1Error("virtual build/test plan keys do not match the documented schema")
    if any(type(plan[key]) is not int for key in ("input_address", "entrypoint", "output_address", "max_instructions")):
        raise Neural1Error("virtual addresses and instruction bound must be integers")
    if not isinstance(plan["input_hex"], str):
        raise Neural1Error("build input must be hexadecimal text")
    source = bytes.fromhex(plan["input_hex"])
    if not source or len(source) > 2048:
        raise Neural1Error("build input requires 1..2048 source bytes")
    if expected:
        if not isinstance(plan["expected_hex"], str):
            raise Neural1Error("test expectation must be hexadecimal text")
        output_length = len(bytes.fromhex(plan["expected_hex"]))
    else:
        output_length = plan["output_bytes"]
    if type(output_length) is not int or not 1 <= output_length <= 4096 or not 1 <= plan["max_instructions"] <= 100_000:
        raise Neural1Error("virtual output or execution bound is invalid")
    world = VirtualApple1World()
    world.host_write(0x200, image)
    # Loading source must not erase retained nonzero bootstrap bytes. The source
    # region is declared workspace, not an opportunity to install a new builder.
    prior = world.host_read(plan["input_address"], len(source))
    if any(prior):
        raise Neural1Error("source loading overlaps retained bootstrap/candidate bytes")
    output_start = plan["output_address"]
    before_input = world.host_read(output_start, output_length)
    if expected and max(plan["input_address"], output_start) < min(plan["input_address"] + len(source), output_start + output_length):
        raise Neural1Error("behavioral input and output regions must be disjoint")
    world.host_write(plan["input_address"], source)
    written: set[int] = set()
    result = world.execute(plan["entrypoint"], max_instructions=plan["max_instructions"], trace_limit=16, write_observer=written.add)
    output = world.host_read(plan["output_address"], output_length)
    # Behavioral outputs must all be written by the candidate. A rebuild may
    # retain unchanged bootstrap bytes, but every changed final byte must have
    # a CPU write, even when source loading already supplied its final value.
    required_writes = set(range(output_start, output_start + output_length)) if expected else {output_start + offset for offset, (before, after) in enumerate(zip(before_input, output, strict=True)) if before != after}
    produced = bool(written.intersection(range(output_start, output_start + output_length))) and required_writes <= written
    return output, {"stop_reason": result.stop_reason, "instructions": result.instructions, "output_sha256": sha256_bytes(output), "screen_text": result.screen_text,
                    "production_policy": "cpu-writes-v1", "execution_produced_output": produced,
                    "cpu_written_addresses": sorted(written), "required_written_addresses": sorted(required_writes),
                    "missing_written_addresses": sorted(required_writes - written), "before_input_output_sha256": sha256_bytes(before_input)}


class SelfHostArchive:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    @contextmanager
    def _lock(self) -> Iterator[None]:
        self.root.mkdir(parents=True, exist_ok=True)
        with (self.root / ".lock").open("a") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            yield

    def _directory(self, artifact_id: str) -> Path:
        if not re.fullmatch(r"N1-SH-[A-Za-z0-9-]+", artifact_id):
            raise Neural1Error("invalid SELFHOST artifact ID")
        path = self.root / artifact_id
        if path.is_symlink():
            raise Neural1Error("SELFHOST artifact directory must not be a symlink")
        return path

    def _load(self, artifact_id: str) -> tuple[dict[str, Any], dict[str, Any], bytes]:
        path = self._directory(artifact_id)
        if any((path / name).is_symlink() for name in ("record.json", "evidence.json", "image.bin")):
            raise Neural1Error("SELFHOST artifact files must not be symlinks")
        record = dict(_json(path / "record.json"))
        evidence = dict(_json(path / "evidence.json"))
        image = (path / "image.bin").read_bytes()
        if record.get("schema") != SCHEMA or record.get("artifact_id") != artifact_id or len(image) != 4096 or sha256_bytes(image) != record["image_sha256"] or sha256_bytes(canonical_json(evidence).encode()) != record["evidence_sha256"]:
            raise Neural1Error("SELFHOST archive artifact/evidence identity mismatch")
        identity = {key: value for key, value in record.items() if key != "artifact_id"}
        if stable_id("N1-SH", identity) != artifact_id:
            raise Neural1Error("SELFHOST record identity mismatch")
        return record, evidence, image

    def records(self) -> list[dict[str, Any]]:
        return [self._load(path.name)[0] for path in sorted(self.root.glob("N1-SH-*")) if path.is_dir()]

    def _write(self, record: dict[str, Any], evidence: dict[str, Any], image: bytes) -> dict[str, Any]:
        record.update(schema=SCHEMA, image_sha256=sha256_bytes(image), evidence_sha256=sha256_bytes(canonical_json(evidence).encode()))
        artifact_id = stable_id("N1-SH", record)
        record["artifact_id"] = artifact_id
        destination = self._directory(artifact_id)
        if destination.exists():
            return self._load(artifact_id)[0]
        with tempfile.TemporaryDirectory(prefix=".partial-", dir=self.root) as temporary:
            stage = Path(temporary) / "artifact"
            stage.mkdir()
            for name, payload in (("record.json", canonical_json(record).encode()), ("evidence.json", canonical_json(evidence).encode()), ("image.bin", image)):
                with (stage / name).open("xb") as stream:
                    stream.write(payload)
                    stream.flush()
                    os.fsync(stream.fileno())
            os.rename(stage, destination)
            directory_fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        return record

    def ingest_run(self, campaign_root: str | Path) -> list[dict[str, Any]]:
        campaign = Path(campaign_root)
        spec = _json(campaign / "spec.json")
        if "selfhost1" not in spec["experiments"] or spec["ram_budget"] != 4096:
            raise Neural1Error("SELFHOST ingestion requires an actual 4K SELFHOST campaign")
        registry = _json(campaign / "effective-registry.json")
        evidence_class = "SYNTHETIC_OR_REPLAY" if any(item["backend"] in {"fake", "replay"} for item in registry["models"]) else "RECORDED_PROVIDER_RUN"
        results = []
        with self._lock():
            for cell in sorted((campaign / "cells").iterdir()):
                family = _json(cell / "family-result.json")
                if family.get("family") != "selfhost1" or not family.get("passed"):
                    continue
                checkpoint = _json(cell / "checkpoint.json")
                transcript_bytes = (cell / "transcript.jsonl").read_bytes()
                if checkpoint["status"] != "COMPLETED" or sha256_bytes(transcript_bytes) != checkpoint["transcript_sha256"]:
                    raise Neural1Error("SELFHOST requires completed hash-consistent run evidence")
                evidence = {"kind": "RAW_TRANSCRIPT_REBUILD", "registry": registry, "spec": spec, "transcript_sha256": checkpoint["transcript_sha256"], "transcript": [json.loads(line) for line in transcript_bytes.splitlines()]}
                image = _replay(evidence)
                if sha256_bytes(image) != family["artifact_sha256"] or not evidence["transcript"]:
                    raise Neural1Error("replayed full artifact differs from qualified run")
                check = VirtualApple1World()
                check.host_write(0x200, image)
                execution = check.execute(0x200, max_instructions=128, trace_limit=0)
                if execution.screen_text != "A" or execution.stop_reason != "MONITOR_WARM_ENTRY":
                    raise Neural1Error("raw starting task failed independent behavior check")
                qualified = SelfHost().qualify(1, sha256_bytes(image)).passed
                record = {"stage": 1, "parents": [], "qualified": qualified, "origin_run_id": campaign.name, "origin_cell_id": cell.name, "evidence_class": evidence_class, "rebuilt_sha256": sha256_bytes(image), "criterion": "raw machine entry, transcript replay and independent output/return"}
                results.append(self._write(record, evidence, image))
        if not results:
            raise Neural1Error("no successfully evaluated SELFHOST starting artifact in run")
        return results

    def rebuild(self, artifact_id: str) -> dict[str, Any]:
        record, evidence, image = self._load(artifact_id)
        if record["stage"] == 1:
            rebuilt = _replay(evidence)
            result: dict[str, Any] = {"method": "raw transcript replay"}
        else:
            parent, _, builder = self._load(evidence["builder_parent"])
            if not parent["qualified"]:
                raise Neural1Error("retained builder parent is no longer qualified")
            rebuilt, result = _execute(builder, evidence["build"])
        return {"artifact_id": artifact_id, "stage": record["stage"], "qualified": record["qualified"], "passed": rebuilt == image and (record["stage"] == 1 or result["execution_produced_output"]), "expected_sha256": sha256_bytes(image), "rebuilt_sha256": sha256_bytes(rebuilt), "evidence_class": record["evidence_class"], **result}

    def qualify(self, evidence_path: str | Path) -> dict[str, Any]:
        evidence = dict(_json(Path(evidence_path)))
        required = {"stage", "candidate_artifact", "parents", "builder_parent", "build", "tests", "language_contract"}
        if evidence.get("stage") == 4:
            required.add("compiler_region")
        if set(evidence) != required or type(evidence["stage"]) is not int or evidence["stage"] not in {2, 3, 4}:
            raise Neural1Error("later-stage qualification evidence schema is invalid")
        if not isinstance(evidence["language_contract"], str) or not evidence["language_contract"].strip():
            raise Neural1Error("declare the assembler/language syntax and semantic task")
        if not isinstance(evidence["parents"], list) or not evidence["parents"] or not all(isinstance(item, str) for item in evidence["parents"]):
            raise Neural1Error("qualified parent IDs are required")
        tests = evidence["tests"]
        if not isinstance(tests, list) or not 2 <= len(tests) <= 8 or not all(isinstance(item, dict) for item in tests):
            raise Neural1Error("two to eight meaningful behavioral vectors are required")
        if len({item.get("input_hex") for item in tests}) < 2 or len({item.get("expected_hex") for item in tests}) < 2:
            raise Neural1Error("behavioral vectors require distinct inputs and expected outputs")
        convention = ("input_address", "entrypoint", "output_address")
        if any(tuple(vector.get(key) for key in convention) != tuple(tests[0].get(key) for key in convention) for vector in tests[1:]):
            raise Neural1Error("all behavioral vectors require one fixed calling convention")
        if evidence["stage"] == 2:
            from .assembler import LessonAssembler
            for vector in tests:
                try:
                    source = bytes.fromhex(vector["input_hex"]).decode("ascii")
                    expected_bytes = bytes.fromhex(vector["expected_hex"])
                    reference = LessonAssembler().assemble(source, origin=vector["output_address"])
                except (KeyError, ValueError, TypeError) as error:
                    raise Neural1Error("stage-two vectors require ASCII 6502 source and exact assembler expectations") from error
                if reference.diagnostics or not reference.payload or source.lstrip().upper().startswith(".BYTE") or reference.payload != expected_bytes:
                    raise Neural1Error("stage-two expectations must match independently assembled instructions")
        with self._lock():
            candidate, _, image = self._load(evidence["candidate_artifact"])
            if not candidate["qualified"]:
                raise Neural1Error("candidate requires qualified raw run provenance")
            graph = SelfHost()
            records = {item["artifact_id"]: item for item in self.records()}
            graph.artifacts = {key: {"stage": item["stage"], "parents": tuple(item["parents"]), "qualified": item["qualified"]} for key, item in records.items()}
            builder_id = evidence["builder_parent"]
            if builder_id not in evidence["parents"] or builder_id not in records or records[builder_id]["stage"] != evidence["stage"] - 1:
                raise Neural1Error("retained builder must be a qualified immediate previous-stage parent")
            _, _, builder = self._load(builder_id)
            if not records[builder_id]["qualified"]:
                raise Neural1Error("retained builder ancestry is unqualified")
            if builder == image:
                raise Neural1Error("current candidate compiler cannot serve as its own retained bootstrap")
            if evidence["stage"] == 4:
                region = evidence["compiler_region"]
                if not isinstance(region, dict) or set(region) != {"address", "length"} or any(type(value) is not int for value in region.values()):
                    raise Neural1Error("stage four requires a declared compiler address/length")
                offset = region["address"] - 0x200
                length = region["length"]
                if offset < 0 or length < 8 or offset + length > 4096:
                    raise Neural1Error("declared compiler region must contain 8..4096 candidate bytes")
                compiler = image[offset:offset + length]
                build_source = bytes.fromhex(evidence["build"]["input_hex"])
                if not any(compiler) or compiler in builder or compiler in build_source:
                    raise Neural1Error("current compiler region remains in retained bootstrap or build input")
            # Validate ancestry before executing any supplied program.
            graph.qualify(evidence["stage"], "PENDING", parents=tuple(evidence["parents"]), rebuild=lambda: b"", expected=image)
            rebuilt, build_result = _execute(builder, evidence["build"])
            repeated, repeated_result = _execute(builder, evidence["build"])
            exact = rebuilt == image and repeated == image and build_result["execution_produced_output"] and repeated_result["execution_produced_output"] and build_result["instructions"] > 0 and build_result["stop_reason"] in {"BRK", "MONITOR_WARM_ENTRY"}
            outcomes = []
            for vector in tests:
                output, execution = _execute(image, vector, expected=True)
                bad_output, bad_execution = _execute(bytes(4096), vector, expected=True)
                expected_output = bytes.fromhex(vector["expected_hex"])
                good = output == expected_output and execution["execution_produced_output"] and execution["instructions"] > 0 and execution["stop_reason"] in {"BRK", "MONITOR_WARM_ENTRY"}
                bad_rejected = bad_output != expected_output or not bad_execution["execution_produced_output"] or bad_execution["instructions"] == 0
                outcomes.append({"passed": good and bad_rejected, "execution": execution, "zero_candidate_control_rejected": bad_rejected})
            graph.artifacts.pop("PENDING")
            score = graph.qualify(evidence["stage"], "QUALIFIED", parents=tuple(evidence["parents"]), rebuild=lambda: rebuilt, expected=image)
            passed = score.passed and exact and all(item["passed"] for item in outcomes)
            sources = [candidate, *(records[key] for key in evidence["parents"])]
            evidence_class = "SYNTHETIC_OR_REPLAY" if any(item["evidence_class"] == "SYNTHETIC_OR_REPLAY" for item in sources) else "RECORDED_PROVIDER_RUN"
            record = {"stage": evidence["stage"], "parents": evidence["parents"], "qualified": passed, "origin_run_id": candidate["origin_run_id"], "origin_cell_id": candidate["origin_cell_id"], "candidate_artifact": evidence["candidate_artifact"], "evidence_class": evidence_class, "rebuilt_sha256": sha256_bytes(rebuilt), "exact_rebuild": exact, "build": build_result, "repeat_build": repeated_result, "behavioral_tests": outcomes, "criterion": evidence["language_contract"], "scope": "bounded declared language vectors and exact reconstruction; no general compiler correctness claim"}
            return self._write(record, evidence, image)

    def export(self, destination: str | Path, artifact_ids: Sequence[str] | None = None) -> dict[str, Any]:
        """Export immutable records and dependency closure; opening it uses this class."""
        target = Path(destination)
        if target.exists():
            raise Neural1Error("SELFHOST export destination already exists")
        pending = list(artifact_ids) if artifact_ids is not None else [record["artifact_id"] for record in self.records()]
        selected: set[str] = set()
        while pending:
            artifact_id = pending.pop()
            if artifact_id in selected:
                continue
            record, _, _ = self._load(artifact_id)
            selected.add(artifact_id)
            pending.extend(record["parents"])
            if record.get("candidate_artifact"):
                pending.append(record["candidate_artifact"])
        target.mkdir(parents=True)
        for artifact_id in sorted(selected):
            shutil.copytree(self._directory(artifact_id), target / artifact_id)
        reopened = SelfHostArchive(target)
        return {"destination": str(target), "records": reopened.records(), "rebuilds": [reopened.rebuild(artifact_id) for artifact_id in sorted(selected)]}


def verify_export(path: str | Path) -> dict[str, Any]:
    archive = SelfHostArchive(path)
    records = archive.records()
    if not records:
        raise Neural1Error("SELFHOST export contains no artifacts")
    rebuilds = [archive.rebuild(record["artifact_id"]) for record in records]
    return {"valid": all(item["passed"] or not item["qualified"] for item in rebuilds), "records": records, "rebuilds": rebuilds}
