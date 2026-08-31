"""Deterministic demonstrations. Outputs are prototype evidence, not findings."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Sequence

from .core import sha256_bytes
from .experiments import FourKMind, RamRepublic, RomUniverse, SelfHost
from .field_library import FieldLibraryAssistant, LessonCorpus
from .meta import ClaimGraph, proof_capsule
from .models import FakeProvider
from .runtime import ExperimentRuntime, RunManifest
from .visualization import memory_map, rom_genome, run_sigil, selfhost_tower
from .world import VirtualApple1World


def run_all(root: str | Path) -> dict[str, object]:
    provider = FakeProvider(default="DETERMINISTIC EXPLANATION FROM RECORDED RESULT.")
    runtime = ExperimentRuntime(root)
    manifest = RunManifest.create("4k-mind", 275, provider.record, {"ram_budget": 4096, "agents": 2})
    events = runtime.start(manifest)
    world = VirtualApple1World()
    fourk = FourKMind(world)
    g1 = fourk.generation({"AGENT-001": ["0200: A9 41 60"], "AGENT-002": ["0200.0202"]})
    snapshot = runtime.snapshot(world)
    events.append("generation", g1)

    republic_world = VirtualApple1World(ram_budget=1024)
    republic = RamRepublic(republic_world, {"A": lambda _: ["0200: 4D 53 47"], "B": lambda _: ["0200.0202"]})
    republic_result = republic.round()

    rom = bytes(range(256))
    rom_score = RomUniverse().evaluate(rom, {"nonempty-reset-vector-fixture": lambda image: image[-1] != 0})

    selfhost = SelfHost()
    selfhost.qualify(1, "RAW")
    selfhost.qualify(2, "ASM", parents=("RAW",))
    selfhost.qualify(3, "LANG", parents=("ASM",))
    expected = b"COMPILER-FIXTURE"
    selfhost_score = selfhost.qualify(4, "SELF", parents=("LANG",), rebuild=lambda: expected, expected=expected)

    graph = ClaimGraph()
    claim = graph.create_claim("THE FIXTURE GENERATION PRESERVED A ROUTINE.", {"experiment": "4k-mind", "status": "DEMO_ONLY"})
    evidence = graph.add_evidence("deterministic-demo", snapshot.sha256, [manifest.run_id], "Snapshot contains deposited fixture bytes.", causal_level=0)
    graph.relate(evidence.evidence_id, "supports", claim.claim_id)
    capsule = proof_capsule(claim, graph, dataset_hash=snapshot.sha256, analysis_version="demo-1", reproduction_command="python -m neural1.demos --out out/neural1-demo")

    field = FieldLibraryAssistant(LessonCorpus(), provider).explain_program("M03", "software/ram-only/line-input-0300.hex", "HI\r")
    return {"label": "DETERMINISTIC PROTOTYPE DEMO - NOT A RESEARCH FINDING", "run_id": manifest.run_id, "run_sigil": run_sigil(manifest.run_id), "4k_mind": g1, "4k_memory": memory_map(world.host_read(world.ram_start, world.ram_budget)), "ram_republic": republic_result, "rom_universe": {"score": asdict(rom_score), "genome": rom_genome(rom)}, "selfhost1": {"score": asdict(selfhost_score), "tower": selfhost_tower(SelfHost.STAGES.values(), achieved=selfhost_score.passed)}, "meta1": capsule, "field_library": asdict(field), "serial_opened": False}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("out/neural1-demo"))
    args = parser.parse_args(argv)
    result = run_all(args.out)
    args.out.mkdir(parents=True, exist_ok=True)
    destination = args.out / "summary.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + "\n", encoding="ascii")
    print(json.dumps({"run_id": result["run_id"], "summary": str(destination), "serial_opened": False}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
