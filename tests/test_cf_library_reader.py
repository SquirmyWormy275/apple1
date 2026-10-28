"""Exercise the actual generated machine code, including back/quit and paging."""
from __future__ import annotations

from collections import deque

import pytest
from py65.devices.mpu6502 import MPU

from tools.build_cf_library import ORIGIN, ascii_text, compile_book, encode_screen, pages_for


def execute(program: bytes, keys: str, *, decimal: bool = False) -> tuple[list[bytes], set[int], int]:
    class Memory(list):
        def __init__(self):
            super().__init__([0] * 65536)
            self.writes: set[int] = set()

        def __setitem__(self, key, value):
            if isinstance(key, int):
                self.writes.add(key)
            super().__setitem__(key, value)

    memory = Memory()
    memory[ORIGIN:ORIGIN + len(program)] = program
    memory[0xFFEF] = 0x60  # Monitor ECHO returns without modifying registers.
    mpu = MPU(memory=memory)
    mpu.pc = ORIGIN
    if decimal:
        mpu.p |= mpu.DECIMAL
    incoming = deque(keys.encode("ascii"))
    screens: list[bytearray] = [bytearray()]
    waiting = False
    memory.writes.clear()
    for steps in range(8_000_000):
        if mpu.pc == 0xFF1F:
            return [bytes(s) for s in screens if s], memory.writes, steps
        if mpu.pc == 0xFFEF:
            if waiting:
                screens.append(bytearray())
                waiting = False
            screens[-1].append(mpu.a & 127)
        # Supply bytes only when a complete page is waiting for keyboard input.
        memory[0xD011] = 0x80 if incoming else 0
        if memory[mpu.pc:mpu.pc + 3] == [0xAD, 0x10, 0xD0]:
            if not incoming:
                raise AssertionError("reader attempted a keyboard read without ready data")
            memory[0xD010] = incoming.popleft() | 0x80
            waiting = True
        mpu.step()
    raise AssertionError("reader did not return to Monitor")


def test_reader_runs_forward_backward_and_quits_with_decimal_mode_set():
    pages = pages_for("\n".join(f"ROW {i:03}" for i in range(61)), "NAVIGATION")
    program = compile_book(pages)
    screens, writes, _ = execute(program, " B Q", decimal=True)
    assert screens == [encode_screen(pages[i])[:-1] for i in (0, 1, 0, 1)]
    assert writes <= set(range(0x100, 0x200)) | {0xF8, 0xF9, 0xFA, 0xFB, 0xD010, 0xD011}


def test_previous_on_first_page_and_next_on_final_page():
    pages = pages_for("ONE PAGE", "BOUNDARIES")
    screens, _, _ = execute(compile_book(pages), "B ")
    assert screens == [encode_screen(pages[0])[:-1]] * 2


def test_full_width_line_does_not_get_a_second_carriage_return():
    lines = ["X" * 40, "NEXT", *([""] * 21), "END"]
    screen = encode_screen(lines)
    assert screen.startswith(b"\r" + b"X" * 40 + b"NEXT\r")
    # Model the original terminal's column-40 automatic wrap.
    rows: list[str] = []
    row = ""
    for byte in screen[1:-1]:
        if byte == 13:
            rows.append(row)
            row = ""
        else:
            row += chr(byte)
            if len(row) == 40:
                rows.append(row)
                row = ""
    rows.append(row)
    assert rows == lines


def test_books_cannot_overwrite_rom_or_cffa_memory():
    with pytest.raises(ValueError, match="32K"):
        compile_book([["Z" * 39] * 24] * 35)


def test_screen_rejects_non_ascii_and_bottom_right_autoscroll():
    with pytest.raises(ValueError):
        encode_screen(["lowercase"])
    with pytest.raises(ValueError):
        encode_screen([""] * 23 + ["X" * 40])


def test_reading_copy_uses_original_display_glyphs_and_labels_lowercase():
    text = ascii_text("`a` is $61; A is $41. | {x} ~ `code`")
    assert "LOWERCASE A IS $61; A IS $41" in text
    assert all(0x20 <= ord(c) <= 0x5F for c in text)
    with pytest.raises(ValueError, match="alphabet"):
        encode_screen(["VERTICAL |"])


def test_markdown_reflows_editor_breaks_but_preserves_code_columns():
    pages = pages_for("One sentence\ncontinues.\n\n```text\nA  B\n1  2\n```", "READ", reflow=True)
    assert pages[0][2] == "ONE SENTENCE CONTINUES."
    assert "A  B" in pages[0] and "1  2" in pages[0]
    assert not any("TEXT" in row for row in pages[0][2:])
