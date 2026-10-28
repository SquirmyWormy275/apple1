import json
from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.core import sha256_bytes
from neural1.selfhost_workflow import SelfHostArchive, verify_export
from neural1.world import VirtualApple1World, WozMonSession

with TemporaryDirectory() as d:
    root = Path(d)
    run = root / "run"
    cell = run / "cells/CELL"
    cell.mkdir(parents=True)
    commands = ["0200: A9 41 20 EF FF 4C 1F FF", "0200R"]
    world = VirtualApple1World()
    record = {
        "generation": 0,
        "agent_id": "SYNTHETIC",
        "response": "\n".join(commands),
        "outputs": [WozMonSession(world).transact(c) for c in commands],
    }
    transcript = (json.dumps(record) + "\n").encode()
    (cell / "transcript.jsonl").write_bytes(transcript)
    (cell / "checkpoint.json").write_text(json.dumps({"status": "COMPLETED", "transcript_sha256": sha256_bytes(transcript)}))
    (cell / "family-result.json").write_text(
        json.dumps({"family": "selfhost1", "passed": True, "artifact_sha256": sha256_bytes(world.host_read(0x200, 4096))})
    )
    (run / "spec.json").write_text(json.dumps({"experiments": ["selfhost1"], "ram_budget": 4096}))
    (run / "effective-registry.json").write_text(json.dumps({"models": [{"backend": "fake"}]}))
    archive = SelfHostArchive(root / "archive")
    artifact = archive.ingest_run(run)[0]
    print("Evidence class:", artifact["evidence_class"])
    print("Stage:", artifact["stage"], "rebuild:", archive.rebuild(artifact["artifact_id"])["passed"])
    archive.export(root / "export", [artifact["artifact_id"]])
    print("Export valid:", verify_export(root / "export")["valid"])
    assert artifact["stage"] == 1 and verify_export(root / "export")["valid"]
