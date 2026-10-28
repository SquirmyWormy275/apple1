"""Regression checks for instruction translation and the native lesson's evaluator."""

from neural1.assembler import LessonAssembler
from neural1.field_library import FieldLibraryAssistant, LessonCorpus
from neural1.models import FakeProvider
from tools.neural1_validate import _validate_markdown_links
from tools.textbook_native import evaluate


def test_forward_absolute_label_uses_final_instruction_size():
    source = "LDA DATA\nSTA $0400\nJMP $FF1F\nDATA: .BYTE $41"
    assembled, execution = LessonAssembler().assemble_and_run(source, origin=0x300)
    assert not assembled.diagnostics and assembled.symbols["DATA"] == 0x309
    assert assembled.payload[:3] == bytes.fromhex("AD 09 03")
    assert execution is not None and execution.final_a == 0x41


def test_branch_range_endpoints_and_out_of_range_are_not_silently_wrapped():
    assembler = LessonAssembler()
    for target in (0x282, 0x381):
        assert not assembler.assemble(f"BNE ${target:04X}", origin=0x300).diagnostics
    for target in (0x281, 0x382, 0x400):
        assert assembler.assemble(f"BNE ${target:04X}", origin=0x300).diagnostics
    for operand in ("381", "0x381", "$0381", "%1110000001"):
        result = assembler.assemble(f"BNE {operand}", origin=0x300)
        assert not result.diagnostics and result.payload == bytes.fromhex("D0 7F")


def test_native_task_evaluator_requires_execution_and_memory_boundaries():
    positive = "0300: A0 00 A9 2A 99 00 04 C8 C0 05 D0 F8 4C 1F FF\n0300R"
    assert evaluate(positive)["passed"]
    assert not evaluate(positive.replace("C0 05", "C0 06"))["passed"]
    assert not evaluate("0400: 2A 2A 2A 2A 2A\n0300: 4C 1F FF\n0300R")["passed"]
    assert not evaluate(positive.replace("0300R", ""))["passed"]
    assert not evaluate("0300: 4C 00 03\n0300R")["passed"]


def test_native_observed_abstention_is_not_reported_as_grounded():
    reply = "The three basic Monitor functions are not established by the available library sources."
    assistant = FieldLibraryAssistant(LessonCorpus(), FakeProvider(default=reply))
    result = assistant.answer("ASK", "M01", "What are the three basic Monitor functions?")
    assert not result.grounded and result.text == reply
    assert "inspect the selected sources" in result.support_note


def test_monitor_function_excerpt_contains_the_actual_three_functions():
    text, _ = LessonCorpus().excerpts("M01", "What are the three basic Monitor functions?", budget=1500, primary_limit=1)
    assert "inspect memory, change memory, and\nrun a program" in text


def test_manual_links_decode_url_escaped_spaces_and_still_reject_missing_files(tmp_path):
    (tmp_path / "Apple1 Manual.pdf").write_bytes(b"scan fixture")
    page = tmp_path / "README.md"
    page.write_text("[Manual](Apple1%20Manual.pdf#page=2)\n[Missing](Absent%20Manual.pdf)\n")
    errors = _validate_markdown_links(tmp_path, page)
    assert len(errors) == 1 and "Absent%20Manual.pdf" in errors[0]
