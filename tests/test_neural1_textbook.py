"""Verify teaching coverage, recorded examples, and the off-device contract."""

from __future__ import annotations

import ast
import json
import shutil
import socket
from pathlib import Path

import pytest

from neural1.console_ui import ALIASES, COMMAND_HELP
from neural1.field_library import LessonCorpus
from tools import textbook

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "docs/textbook"
RECORDS = textbook.catalog()


@pytest.mark.parametrize("record", RECORDS, ids=lambda r: r["id"])
def test_each_example_reproduces_its_capture_without_network(record, monkeypatch):
    def refuse_connection(*args, **kwargs):
        raise AssertionError("A textbook example attempted a real network connection")

    monkeypatch.setattr(socket.socket, "connect", refuse_connection)
    assert textbook.run(record["id"]) == (BOOK / "captures" / f"{record['id']}.txt").read_text()


def test_every_existing_lesson_has_a_worked_companion_and_unique_source():
    actual = {name.split("-")[0] for name in LessonCorpus(ROOT / "docs/field-library").lessons()}
    lessons = [record for record in RECORDS if record["lesson"]]
    assert {record["id"] for record in lessons} == actual
    assert len(lessons) == len(actual) == 42
    assert len({record["id"] for record in RECORDS}) == len(RECORDS)
    assert {path.stem for path in (BOOK / "examples").glob("*.py")} == {r["id"] for r in RECORDS}
    for record in RECORDS:
        identifier = record["id"]
        guide = ROOT / record["lesson"] / "WORKED.md" if record["lesson"] else BOOK / "features" / f"{identifier}.md"
        text = guide.read_text()
        assert (BOOK / "examples" / f"{identifier}.py").read_text().rstrip() in text
        assert (BOOK / "captures" / f"{identifier}.txt").read_text().rstrip() in text
        assert f"captures/{identifier}.png" in text
        assert record["challenge"] in text and record["answer"] in text


def test_captures_match_source_and_image_hashes():
    textbook.verify(BOOK / "captures", rerun=False)
    for record in RECORDS:
        image = (BOOK / "captures" / f"{record['id']}.png").read_bytes()
        assert image.startswith(b"\x89PNG\r\n\x1a\n")


@pytest.mark.parametrize("extension", ["txt", "png"])
def test_tampered_capture_is_rejected(tmp_path, extension):
    target = tmp_path / "captures"
    shutil.copytree(BOOK / "captures", target)
    (target / f"C01.{extension}").write_bytes(b"altered")
    with pytest.raises(ValueError, match="Changed (transcript|image)"):
        textbook.verify(target, rerun=False)


@pytest.mark.parametrize("identifier", ["../../outside", "UNKNOWN", "S03.py", "S03 extra"])
def test_unknown_or_escaping_example_ids_are_refused(identifier):
    with pytest.raises(ValueError, match="Unknown lab ID"):
        textbook.run(identifier)


def test_capture_refuses_existing_output_before_writing(tmp_path):
    before = tmp_path / "keep.txt"
    before.write_text("retain me")
    with pytest.raises(ValueError, match="new output directory"):
        textbook.capture(tmp_path, images=False)
    assert before.read_text() == "retain me" and list(tmp_path.iterdir()) == [before]


def test_command_surface_inventory_matches_actual_parser_declarations():
    actual = []
    for directory in ("neural1", "tools"):
        for path in sorted((ROOT / directory).glob("*.py")):
            tree = ast.parse(path.read_text())
            if not any(isinstance(node, ast.FunctionDef) and node.name == "main" for node in tree.body):
                continue
            commands = []
            flags = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in {"add_parser", "add_argument"}:
                    for arg in node.args:
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            if node.func.attr == "add_parser":
                                commands.append(arg.value)
                                break
                            if arg.value.startswith("-"):
                                flags.append(arg.value)
            actual.append({"path": path.relative_to(ROOT).as_posix(), "subcommands": sorted(set(commands)), "flags": sorted(set(flags))})
    retained = json.loads((BOOK / "public-surfaces.json").read_text())
    assert [{key: value for key, value in r.items() if key != "teaching_route"} for r in retained] == actual
    console = json.loads((BOOK / "console-surfaces.json").read_text())
    assert console == {"commands": COMMAND_HELP, "aliases": ALIASES}


def test_reset_vector_erratum_uses_the_reset_vector_not_irq():
    from py65.devices.mpu6502 import MPU

    assert MPU.RESET == 0xFFFC and MPU.IRQ == 0xFFFE and MPU.NMI == 0xFFFA
    notes = (ROOT / "docs/field-library/SOURCES.md").read_text()
    assert "RESET `$FFFC/$FFFD`" in notes and "IRQ/BRK `$FFFE/$FFFF`" in notes
    assert "6500-50A_MCS6500pgmManJan76.pdf" in notes


def test_corrected_primary_source_key_is_available_to_lesson_grounding():
    notes = (ROOT / "docs/field-library/SOURCES.md").read_text()
    assert "M-RESET-CORRECT" in LessonCorpus.source_keys(notes)
