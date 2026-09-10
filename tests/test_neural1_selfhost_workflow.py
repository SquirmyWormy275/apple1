from __future__ import annotations

import json
from pathlib import Path

import pytest

from neural1.core import Neural1Error, sha256_bytes
from neural1.selfhost_workflow import SelfHostArchive, verify_export
from neural1.world import VirtualApple1World, WozMonSession


def raw_run(root: Path, name: str, marker: str, opcode: str = "A9") -> Path:
    campaign = root / name
    cell = campaign / "cells" / "CELL"
    cell.mkdir(parents=True)
    commands = [
        "0200: A9 41 20 EF FF 4C 1F FF",
        # Synthetic retained builder changes one declared data byte then clears source.
        "0240: AD 00 04 8D 00 03 AD 01 04 F0 03 8D 61 02 A9 00 8D 00 04 8D 01 04 00",
        # Synthetic bounded assembler supports single-digit LDA immediate only.
        f"0260: A9 {opcode} 8D 00 05 AD 07 04 38 E9 30 8D 01 05 00",
        f"0300: {marker}", "0200R",
    ]
    world = VirtualApple1World()
    record = {"generation": 0, "agent_id": "SYNTHETIC", "response": "\n".join(commands), "outputs": [WozMonSession(world).transact(command) for command in commands]}
    transcript = (json.dumps(record) + "\n").encode()
    (cell / "transcript.jsonl").write_bytes(transcript)
    (cell / "checkpoint.json").write_text(json.dumps({"status": "COMPLETED", "transcript_sha256": sha256_bytes(transcript)}))
    (cell / "family-result.json").write_text(json.dumps({"family": "selfhost1", "passed": True, "artifact_sha256": sha256_bytes(world.host_read(0x200, 4096))}))
    (campaign / "spec.json").write_text(json.dumps({"experiments": ["selfhost1"], "ram_budget": 4096}))
    (campaign / "effective-registry.json").write_text(json.dumps({"models": [{"backend": "fake"}]}))
    return campaign


def evidence(parent: str, candidate: str) -> dict:
    return {"stage": 2, "candidate_artifact": candidate, "parents": [parent], "builder_parent": parent,
            "build": {"input_hex": "02", "input_address": 0x400, "entrypoint": 0x240, "output_address": 0x200, "output_bytes": 4096, "max_instructions": 100},
            "tests": [{"input_hex": f"LDA #$0{i}".encode().hex(), "input_address": 0x400, "entrypoint": 0x260, "output_address": 0x500, "expected_hex": f"A9 0{i}", "max_instructions": 100} for i in (1, 2)],
            "language_contract": "SYNTHETIC TEST: LDA immediate single decimal digit; no general assembler claim"}


def test_raw_artifact_rebuild_persists_and_exports(tmp_path: Path) -> None:
    archive = SelfHostArchive(tmp_path / "archive")
    run = raw_run(tmp_path, "RUN", "01")
    record = archive.ingest_run(run)[0]
    assert record["stage"] == 1 and record["qualified"]
    assert record["evidence_class"] == "SYNTHETIC_OR_REPLAY"
    assert SelfHostArchive(archive.root).rebuild(record["artifact_id"])["passed"]
    export = archive.export(tmp_path / "export", [record["artifact_id"]])
    assert export["rebuilds"][0]["passed"]
    assert verify_export(tmp_path / "export")["valid"]
    # Archive alone contains all reconstruction evidence.
    (run / "cells" / "CELL" / "transcript.jsonl").unlink()
    assert archive.rebuild(record["artifact_id"])["passed"]


def test_later_stage_requires_exact_rebuild_behavior_and_qualified_ancestry(tmp_path: Path) -> None:
    archive = SelfHostArchive(tmp_path / "archive")
    parent = archive.ingest_run(raw_run(tmp_path, "PARENT", "01"))[0]
    candidate = archive.ingest_run(raw_run(tmp_path, "CANDIDATE", "02"))[0]
    plan = evidence(parent["artifact_id"], candidate["artifact_id"])
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps(plan))
    qualified = archive.qualify(path)
    assert qualified["qualified"] and qualified["stage"] == 2
    assert qualified["exact_rebuild"]
    assert all(test["zero_candidate_control_rejected"] for test in qualified["behavioral_tests"])
    assert archive.rebuild(qualified["artifact_id"])["passed"]
    archive.export(tmp_path / "export", [qualified["artifact_id"]])
    assert len(verify_export(tmp_path / "export")["records"]) == 3
    plan["build"]["input_hex"] = "03"
    path.write_text(json.dumps(plan))
    failure = archive.qualify(path)
    assert not failure["qualified"] and not failure["exact_rebuild"]
    plan.update(stage=3, parents=[failure["artifact_id"]], builder_parent=failure["artifact_id"])
    path.write_text(json.dumps(plan))
    with pytest.raises(Neural1Error, match="unqualified"):
        archive.qualify(path)


def test_rejects_tampered_archive_and_vacuous_or_false_assembler_vectors(tmp_path: Path) -> None:
    archive = SelfHostArchive(tmp_path / "archive")
    parent = archive.ingest_run(raw_run(tmp_path, "PARENT", "01"))[0]
    candidate = archive.ingest_run(raw_run(tmp_path, "CANDIDATE", "02"))[0]
    plan = evidence(parent["artifact_id"], candidate["artifact_id"])
    path = tmp_path / "bad.json"
    plan["tests"][0]["expected_hex"] = "EA"
    path.write_text(json.dumps(plan))
    with pytest.raises(Neural1Error, match="independently assembled"):
        archive.qualify(path)
    record_path = archive.root / parent["artifact_id"] / "record.json"
    record = json.loads(record_path.read_text())
    record["stage"] = 4
    record_path.write_text(json.dumps(record))
    with pytest.raises(Neural1Error, match="record identity"):
        archive.rebuild(parent["artifact_id"])


def test_stage_four_removes_declared_compiler_and_rebuilds_exactly(tmp_path: Path) -> None:
    archive = SelfHostArchive(tmp_path / "archive")
    raw = [archive.ingest_run(raw_run(tmp_path, f"RAW{i}", f"0{i}", "A2" if i == 4 else "A9"))[0] for i in range(1, 5)]
    previous = raw[0]
    path = tmp_path / "stages.json"
    for stage in (2, 3, 4):
        plan = evidence(previous["artifact_id"], raw[stage - 1]["artifact_id"])
        plan["stage"] = stage
        plan["build"]["input_hex"] = f"0{stage}"
        if stage == 4:
            plan["compiler_region"] = {"address": 0x260, "length": 15}
            # Without reconstructing the changed compiler opcode, exact rebuild fails.
            plan["tests"] = [{**test, "input_hex": bytes.fromhex(test["input_hex"]).replace(b"LDA", b"LDX").hex(), "expected_hex": test["expected_hex"].replace("A9", "A2")} for test in plan["tests"]]
            path.write_text(json.dumps(plan))
            assert not archive.qualify(path)["qualified"]
            plan["build"]["input_hex"] += " A2"
        path.write_text(json.dumps(plan))
        previous = archive.qualify(path)
        assert previous["qualified"], previous
    assert previous["stage"] == 4 and archive.rebuild(previous["artifact_id"])["passed"]
    retained = evidence(previous["parents"][0], raw[2]["artifact_id"])
    retained.update(stage=4, compiler_region={"address": 0x260, "length": 15})
    path.write_text(json.dumps(retained))
    with pytest.raises(Neural1Error, match="own retained bootstrap|compiler region remains"):
        archive.qualify(path)


def test_behavioral_vectors_cannot_select_prefilled_output_tables(tmp_path: Path) -> None:
    plan = evidence("N1-SH-parent", "N1-SH-candidate")
    plan["tests"][1]["output_address"] = 0x510
    path = tmp_path / "table.json"
    path.write_text(json.dumps(plan))
    with pytest.raises(Neural1Error, match="fixed calling convention"):
        SelfHostArchive(tmp_path / "archive").qualify(path)


def test_execution_provenance_rejects_prefilled_nop_and_accepts_identical_cpu_writes() -> None:
    from neural1.selfhost_workflow import _execute

    image = bytearray(4096)
    image[0x60:0x62] = bytes.fromhex("EA 00")
    image[0x300:0x302] = bytes.fromhex("A9 01")
    vector = evidence("parent", "candidate")["tests"][0]
    output, result = _execute(bytes(image), vector, expected=True)
    assert output == bytes.fromhex("A9 01") and not result["execution_produced_output"]
    image[0x60:0x6B] = bytes.fromhex("A9 A9 8D 00 05 A9 01 8D 01 05 00")
    output, result = _execute(bytes(image), vector, expected=True)
    assert output == bytes.fromhex("A9 01") and result["execution_produced_output"]
    assert result["cpu_written_addresses"] == [0x500, 0x501]


def test_host_input_cannot_supply_rebuilt_artifact_or_behavioral_output() -> None:
    from neural1.selfhost_workflow import _execute

    image = bytearray(4096)
    image[0x40:0x42] = bytes.fromhex("EA 00")
    plan = evidence("parent", "candidate")["build"]
    plan["input_address"] = 0x300
    output, result = _execute(bytes(image), plan)
    assert output[0x100] == 2
    assert not result["execution_produced_output"]
    assert result["missing_written_addresses"] == [0x300]
    vector = evidence("parent", "candidate")["tests"][0]
    vector["input_address"] = vector["output_address"]
    with pytest.raises(Neural1Error, match="must be disjoint"):
        _execute(bytes(image), vector, expected=True)


def test_write_observer_preserves_exact_candidate_memory_policy() -> None:
    world = VirtualApple1World()
    world.host_write(0x200, bytes.fromhex("A9 01 8D 00 03 00"))
    written: set[int] = set()
    result = world.execute(0x200, candidate_limit=256, write_observer=written.add)
    assert result.stop_reason == "EXECUTION_MEMORY_POLICY"
    assert 0x300 not in written
