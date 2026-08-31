from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from neural1.analysis import break_invariant, detect_phase_changes, mine_invariants, score_scientist_task
from neural1.assembler import LessonAssembler
from neural1.policies import CandidateMetrics, SelectionPolicy, convergence, extinct, memory_conflicts, mutate_rom


def test_two_pass_assembler_resolves_labels_and_runs_trace() -> None:
    source = """
START: LDX #$02
LOOP:  DEX
       BNE LOOP
       LDA #$41
       JSR $FFEF
       JMP $FF1F
"""
    assembled, execution = LessonAssembler().assemble_and_run(source)
    assert assembled.diagnostics == ()
    assert assembled.symbols["START"] == 0x0200
    assert assembled.symbols["LOOP"] == 0x0202
    assert execution is not None
    assert execution.screen_text == "A"
    assert execution.stop_reason == "MONITOR_WARM_ENTRY"


def test_assembler_reports_duplicate_and_unknown_labels() -> None:
    duplicate = LessonAssembler().assemble("X: NOP\nX: BRK")
    assert duplicate.payload == b""
    assert "duplicate label" in duplicate.diagnostics[0].message
    unknown = LessonAssembler().assemble("JMP MISSING")
    assert unknown.payload == b""
    assert "cannot assemble" in unknown.diagnostics[0].message


@given(seed=st.integers(min_value=0, max_value=2**31 - 1), count=st.integers(min_value=0, max_value=32))
def test_rom_mutation_is_deterministic_and_exact(seed: int, count: int) -> None:
    one, record_one = mutate_rom(bytes(256), seed=seed, mutation_count=count)
    two, record_two = mutate_rom(bytes(256), seed=seed, mutation_count=count)
    assert one == two and record_one == record_two
    assert len(one) == 256
    assert sum(byte != 0 for byte in one) == count


def test_selection_extinction_convergence_and_conflict_metrics() -> None:
    candidates = [CandidateMetrics("A", .5, 1, 10, 20, 1), CandidateMetrics("B", 1, .5, 20, 10, .5)]
    assert SelectionPolicy(correctness_weight=1).select(candidates, 1)[0].candidate_id == "B"
    assert extinct(candidates, minimum_correctness=1.1) is True
    assert convergence({"C1": ["HASH"], "C2": ["HASH"]})["converged"] is True
    conflicts = memory_conflicts([("A", 0x200, b"AB"), ("B", 0x201, b"C")])
    assert conflicts[0].address == 0x201


def test_invariants_discoveries_and_scientist_bench_are_explicit() -> None:
    records = [{"successful": True, "checksum": True, "model": "A"}, {"successful": True, "checksum": True, "model": "B"}]
    invariant = next(item for item in mine_invariants(records) if item.feature == "checksum")
    assert invariant.support_fraction == 1
    assert break_invariant(invariant, records) == ()
    assert detect_phase_changes([0, 0.1, 2.0], threshold=1)[0].record_indices == (1, 2)
    assert score_scientist_task("T", {"factor": "X", "metric": "Y"}, {"factor": "X", "metric": "Z"}).score == .5
