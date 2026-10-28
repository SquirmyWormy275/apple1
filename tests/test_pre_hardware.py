"""Meaningful interpreter, filesystem and reader boundaries; no physical I/O."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.apple1_basic import ROM, resume_session, run_session
from tools.card_book import compile_books, decode_book, encode_book, reading_lines
from tools.card_image import build, reader_step, rehearse_reader
from tools.cffa1_model import Cffa1Machine, blank_virtual_card
from tools.prodos import ProdosImage

ROOT = Path(__file__).resolve().parents[1]


def test_real_basic_arithmetic_limits_and_syntax():
    result = run_session(["PRINT 38/9", "PRINT 38 MOD 9", "PRINT 1+2*3", "PRINT (1+2)*3",
                          "PRINT 2.54", "PRINT 32767+1", "PRINT -32767", "PRINT -32768", "SUM=12"])
    assert "\n4\n" in result.transcript and "\n2\n" in result.transcript
    assert "\n7\n" in result.transcript and "\n9\n" in result.transcript
    assert result.transcript.count("*** SYNTAX ERR") == 2
    assert result.transcript.count("*** >32767 ERR") == 2
    assert "\n-32767\n" in result.transcript
    assert result.stop == "waiting-for-input"


def test_program_input_is_not_confused_with_immediate_input_or_break_polling():
    result = run_session(['INPUT "NAME?",N$', '10 DIM N$(20)', '20 INPUT "NAME?",N$', '30 PRINT N$',
                          '40 END', 'RUN', 'TOM', 'PRINT 6*7'])
    assert result.transcript.count("*** SYNTAX ERR") == 1
    assert "NAME??TOM\n\nTOM\n" in result.transcript
    assert "\n42\n" in result.transcript
    assert result.commands_consumed == 8


@pytest.mark.parametrize("value,expected", [("0", "0 INCHES IS 0 CM"), ("129", "129 INCHES IS 327 CM"),
    ("130", "USE AN INTEGER FROM 0 TO 129"), ("-1", "USE AN INTEGER FROM 0 TO 129")])
def test_conversion_guard_prevents_intermediate_overflow(value, expected):
    source = (ROOT / "software/basic/CONVERT.bas").read_text().splitlines()
    result = run_session([*source, "RUN", value])
    assert expected in result.transcript.split(">RUN\n")[1] and "***" not in result.transcript


def test_actual_basic_array_indices_are_one_based():
    result = run_session(["DIM A(5)", "A(1)=7", "A(5)=9", "PRINT A(1)+A(5)", "A(0)=1", "A(6)=1"])
    assert "\n16\n" in result.transcript and result.transcript.count("*** RANGE ERR") == 2


def test_basic_instruction_bound_stops_an_infinite_program():
    result = run_session(["10 GOTO 10", "RUN"], max_instructions=100_000)
    assert result.stop == "instruction-limit" and result.instructions == 100_000


def test_basic_rejects_control_characters_and_lowercase():
    for line in ("print 2", "PRINT 2\rPRINT 3", "\x1b", "PRINT \u03bb"):
        with pytest.raises(ValueError):
            run_session([line])


def test_real_ba1_save_clear_load_and_execute():
    machine = blank_virtual_card()
    machine.save_basic("HELLO", (ROOT / "software/basic/HELLO.bas").read_text())
    image = ProdosImage(machine.memory.materialize())
    assert image.entries["/HELLO"].file_type == 0xF1
    assert image.read("/HELLO").startswith(b"A1\0")
    machine.memory[0x4A:0x100] = [0] * 182
    machine.memory[0x800:0x1000] = [0] * 2048
    machine.memory[0xE000:0xF000] = ROM.read_bytes()
    machine.api(0x26, name="HELLO")
    result = resume_session(machine.memory, ["RUN", "TOM"])
    assert "HELLO TOM" in result.transcript and "***" not in result.transcript


def test_basic_save_accepts_stars_in_source_and_rejects_interpreter_errors():
    machine = blank_virtual_card()
    machine.save_basic("STARS", '10 PRINT "***"\n20 END\n')
    assert machine.read_file("STARS").startswith(b"A1" + bytes([0]))
    with pytest.raises(ValueError, match="failed to enter"):
        machine.save_basic("INVALID", "10 THIS IS INVALID\n")


def test_firmware_handles_seedling_sapling_and_directory_extension():
    machine = blank_virtual_card()
    machine.api(0x2C, name="LESSONS")
    machine.prefix("LESSONS")
    for i in range(15):
        data = bytes([i]) * (1500 if i == 14 else 23)
        machine.write_file(f"FILE{i}", data)
        assert machine.read_file(f"FILE{i}") == data
    image = ProdosImage(machine.memory.materialize())
    assert image.entries["/LESSONS"].blocks == 2
    assert image.entries["/LESSONS/FILE14"].storage == 2
    assert image.read("/LESSONS/FILE14") == bytes([14]) * 1500


def test_independent_reader_rejects_corrupt_bitmap_and_directory_links():
    machine = blank_virtual_card()
    machine.write_file("TEST", b"DATA")
    original = machine.memory.materialize()
    image = ProdosImage(original)
    broken = bytearray(original)
    key = image.entries["/TEST"].key
    broken[image.bitmap * 512 + key // 8] |= 0x80 >> (key % 8)
    with pytest.raises(ValueError, match="marked free"):
        ProdosImage(bytes(broken))
    broken = bytearray(original)
    broken[1026:1028] = (2).to_bytes(2, "little")
    with pytest.raises(ValueError, match="shared"):
        ProdosImage(bytes(broken))


def test_all_card_pages_round_trip_and_fit_display_and_ram():
    payloads, pages, manifest = compile_books()
    assert len(pages) == 50 and len(payloads) == 51
    assert {r["name"] for r in manifest["books"]} == set(pages)
    for record in manifest["books"]:
        decoded, answer = decode_book(payloads[record["name"]])
        assert decoded == pages[record["name"]]
        if record["number"] in range(1, 43):
            assert answer is not None
        assert len(payloads[record["name"]]) <= 0x7000


def test_retained_card_edition_matches_its_source_compiler():
    import json

    payloads, pages, manifest = compile_books()
    assert json.loads((ROOT / "cf-card/education/manifest.json").read_text()) == manifest
    for name, data in payloads.items():
        assert (ROOT / "cf-card/education/payloads" / name).read_bytes() == data
    for name, texts in pages.items():
        for number, text in enumerate(texts, 1):
            assert (ROOT / "cf-card/education/pages" / name / f"{number:03}.txt").read_text() == text + "\n"


def test_corrupt_page_format_and_display_overflow_are_rejected():
    for pages in (["A" * 41], ["\n".join(["X"] * 25)], ["lower"], ["A\x1bB"]):
        with pytest.raises(ValueError):
            encode_book(pages)
    valid = encode_book(["HELLO"])
    for data in (valid + b"JUNK", valid[:-1], valid[:9] + b"\x00\x00" + valid[11:]):
        with pytest.raises(ValueError):
            decode_book(data)


def test_full_width_plate_wrap_and_lowercase_explanation_are_preserved():
    page = "X" * 40 + "\n" + "Y" * 40 + "\nLAST LINE"
    assert decode_book(encode_book([page]))[0] == [page]
    assert b"X" * 40 + b"Y" * 40 + b"LAST LINE" in encode_book([page])
    assert reading_lines("`a` is $61; `A` is $41")[0] == "LOWERCASE A IS $61; A IS $41"
    with pytest.raises(ValueError):
        encode_book(["\n".join(["X" * 40] * 24)])


def test_reading_copy_reflows_prose_but_preserves_diagram_coordinates():
    assert reading_lines("A sentence broken\nacross source lines.") == ["A SENTENCE BROKEN ACROSS SOURCE LINES."]
    assert reading_lines("```text\n  A | B\n```\n\nNext paragraph.") == ["  A ! B", "", "NEXT PARAGRAPH."]
    assert reading_lines("  A | B\n    |", preserve_layout=True) == ["  A ! B", "    !"]


def test_review_record_covers_all_original_packets_and_answer_parts():
    import json

    from tools.field_library_review import review_packets

    retained = json.loads((ROOT / "docs/field-library/review/packets.json").read_text())
    assert review_packets() == retained
    assert len(retained["records"]) == 42


def test_actual_reader_navigation_and_missing_prefix():
    assert rehearse_reader()["select"] == "LESSON S01"


def test_ram_reader_rejects_oversized_book_before_loading_payload():
    machine = blank_virtual_card()
    machine.api(0x2C, name="EDUCATION")
    machine.prefix("EDUCATION")
    machine.write_file("READFIRST", b"X" * 0x7000)
    # Corrupt only the virtual directory EOF, as an untrusted-media case.
    machine.api(0x14, name="READFIRST")
    entry = machine.memory[11] | machine.memory[12] << 8
    block = machine.memory[13] | machine.memory[14] << 8
    offset = entry - 0x8C00
    data = bytearray(machine.memory.block(block))
    data[offset + 21:offset + 24] = (0x7100).to_bytes(3, "little")
    machine.memory.changed[block] = bytes(data)
    before = machine.memory.writes
    assert "INVALID BOOK" in reader_step(machine, start=True)
    assert machine.memory.writes == before


@pytest.mark.parametrize("data", [
    b"A1BK\x01" + (127).to_bytes(2, "little") + b"\xff\xff" + (11).to_bytes(2, "little") + b"\0",
    b"A1BK\x01\x01\x00\xff\xff\x00\x00\0",
    b"A1BK\x01\x01\x00\xff\xff\x0b\x00",
])
def test_actual_reader_rejects_truncated_table_and_header_offsets(data):
    machine = blank_virtual_card()
    machine.api(0x2C, name="EDUCATION")
    machine.prefix("EDUCATION")
    machine.write_file("READFIRST", data)
    assert "INVALID BOOK" in reader_step(machine, start=True)


def test_build_rejects_existing_output_and_wrong_baseline_without_mutation(tmp_path):
    path = tmp_path / "bad.img"
    path.write_bytes(bytes(512 * 8))
    with pytest.raises(FileExistsError):
        build(path, tmp_path)
    with pytest.raises(ValueError, match="identity"):
        build(path, tmp_path / "new")
    assert not (tmp_path / "new").exists()
    assert path.read_bytes() == bytes(512 * 8)
    with pytest.raises(ValueError, match="complete"):
        Cffa1Machine(b"bad")
