from __future__ import annotations

import json

import pytest

from tools.apple1_emulator import Apple1RamHarness, ProgramFormatError, load_hex_program, main


def test_line_input_program_runs_on_an_nmos_6502_and_returns_to_monitor() -> None:
    harness = Apple1RamHarness.from_program_file("software/ram-only/line-input-0300.hex")

    result = harness.run_keyboard_line("HI\r")

    assert result.screen_text == "HI\r"
    assert result.buffer_text == "HI\r"
    assert result.returned_to_monitor is True


def test_echo_program_replays_the_buffer_through_the_monitor_echo_stub() -> None:
    harness = Apple1RamHarness.from_program_file("software/ram-only/line-input-echo-0300.hex")

    result = harness.run_keyboard_line("OK\r")

    assert result.screen_text == "OK\rOK\r"
    assert result.buffer_text == "OK\r"


def test_loader_rejects_non_hex_and_oversized_programs(tmp_path) -> None:
    malformed = tmp_path / "bad.hex"
    malformed.write_text("A0 nope", encoding="utf-8")
    with pytest.raises(ProgramFormatError):
        load_hex_program(malformed)


def test_command_line_runner_emits_a_reproducible_result(capsys) -> None:
    assert main(["software/ram-only/line-input-0300.hex", "--input", "GO\r"]) == 0

    result = json.loads(capsys.readouterr().out)
    assert result["screen_text"] == "GO\r"
    assert result["returned_to_monitor"] is True
