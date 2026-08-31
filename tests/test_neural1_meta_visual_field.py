from __future__ import annotations

from neural1.field_library import FieldLibraryAssistant, LessonCorpus, UNSUPPORTED
from neural1.interface import Mode, Portal
from neural1.meta import ClaimGraph, compile_experiment, falsification_plan, proof_capsule
from neural1.models import FakeProvider
from neural1.visualization import lint_provenance, rom_genome, run_sigil, validate_frame


def test_claim_graph_capsule_and_falsification_are_traceable() -> None:
    graph = ClaimGraph()
    claim = graph.create_claim("FIXTURE EFFECT", {"experiment": "test"})
    evidence = graph.add_evidence("result", "a" * 64, ["RUN-1"], "fixture")
    graph.relate(evidence.evidence_id, "supports", claim.claim_id)
    capsule = proof_capsule(claim, graph, dataset_hash="b" * 64, analysis_version="1", reproduction_command="pytest")
    assert capsule["run_ids"] == ["RUN-1"]
    assert falsification_plan(claim, factor="X", control="0", treatment="1", metric="Y", seeds=[1], sample_count=2)["estimated_compute_cost"] == "UNBENCHMARKED"


def test_experiment_compiler_requires_controls_and_replicable_fields() -> None:
    spec = compile_experiment("DOES X CHANGE Y?", factor="X", levels=["A", "B"], controls={"model": "fixed"}, metrics=["Y"], seeds=[1, 2], analysis="paired", stopping_rule="N=2")
    assert spec.target == "VIRTUAL"
    assert spec.experiment_id.startswith("N1-X-")


def test_visuals_are_deterministic_and_apple1_safe() -> None:
    assert run_sigil("RUN") == run_sigil("RUN")
    assert run_sigil("RUN") != run_sigil("OTHER")
    assert validate_frame(run_sigil("RUN")) == []
    assert len(rom_genome(bytes(256)).splitlines()) == 16
    assert lint_provenance("art/provenance") == []


def test_portal_keeps_computer_explicit_and_virtual() -> None:
    portal = Portal()
    assert portal.select("1") == "[V] COMPUTER / MODELED WOZMON"
    assert portal.mode is Mode.COMPUTER


def test_field_library_trace_uses_emulator_evidence() -> None:
    assistant = FieldLibraryAssistant(LessonCorpus(), FakeProvider(default="EXPLAINS THE RECORDED RESULT."))
    answer = assistant.explain_program("M03", "software/ram-only/line-input-0300.hex", "HI\r")
    assert answer.deterministic_evidence["screen_text"] == "HI\r"
    assert answer.deterministic_evidence["returned_to_monitor"] is True
