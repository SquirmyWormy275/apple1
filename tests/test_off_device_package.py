from __future__ import annotations

import json
import hashlib
import zipfile
from pathlib import Path

import pytest

from tools.apple1_text import TextContractError, format_for_apple1
from tools.firmware_behavior import QueueFullStop, SingleWriterQueue, serial_stimulus
from tools.support_bundle import SupportBundleError, build_support_bundle


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_serial_stimulus_only_accepts_measured_safe_monitor_text() -> None:
    assert serial_stimulus("TEST\r") == b"TEST\r"

    with pytest.raises(TextContractError):
        serial_stimulus("test\r")
    with pytest.raises(TextContractError):
        serial_stimulus("TEST\n")


def test_single_writer_queue_preserves_order_and_stops_when_full() -> None:
    queue = SingleWriterQueue(capacity=2)
    queue.enqueue("ps2", b"A")
    queue.enqueue("serial", b"B")

    assert queue.service_one() == ("ps2", b"A")
    assert queue.service_one() == ("serial", b"B")

    queue.enqueue("serial", b"A")
    queue.enqueue("serial", b"B")
    with pytest.raises(QueueFullStop):
        queue.enqueue("serial", b"C")
    assert queue.events[-1]["event"] == "queue_full_stop"


def test_single_writer_queue_bounds_its_review_history() -> None:
    queue = SingleWriterQueue(capacity=1, event_limit=2)
    queue.enqueue("serial", b"A")
    queue.service_one()
    queue.enqueue("serial", b"B")

    assert len(queue.events) == 2
    assert queue.events[0]["event"] == "single_writer_service"


def test_formatter_is_uppercase_ascii_and_40_columns() -> None:
    lines = format_for_apple1("Hello, café world", width=10)

    assert lines == ["HELLO, CAF", "? WORLD"]
    assert all(len(line) <= 10 for line in lines)


def test_formatter_preserves_logical_lines_before_normalizing_characters() -> None:
    assert format_for_apple1("A\nB") == ["A", "B"]


def test_support_bundle_hashes_only_explicit_evidence(tmp_path: Path) -> None:
    evidence = tmp_path / "capture.jsonl"
    evidence.write_text('{"event":"opened"}\n', encoding="utf-8")
    output = tmp_path / "support.zip"

    build_support_bundle(output, [evidence], tool_version="test")

    with zipfile.ZipFile(output) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        assert archive.read("evidence/capture.jsonl") == evidence.read_bytes()

    assert manifest["tool_version"] == "test"
    assert manifest["files"][0]["sha256"] == hashlib.sha256(evidence.read_bytes()).hexdigest()


def test_support_bundle_rejects_missing_evidence(tmp_path: Path) -> None:
    with pytest.raises(SupportBundleError):
        build_support_bundle(tmp_path / "support.zip", [tmp_path / "missing.jsonl"])


def test_support_bundle_rejects_ambiguous_or_overwritten_evidence(tmp_path: Path) -> None:
    first = tmp_path / "first" / "capture.jsonl"
    second = tmp_path / "second" / "capture.jsonl"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")
    output = tmp_path / "support.zip"

    with pytest.raises(SupportBundleError, match="unique basename"):
        build_support_bundle(output, [first, second])
    output.write_bytes(b"previous archive")
    with pytest.raises(SupportBundleError, match="output archive"):
        build_support_bundle(output, [output])


def test_off_device_documents_preserve_the_firmware_and_hardware_boundary() -> None:
    preservation = (REPO_ROOT / "docs" / "preservation-dossier.md").read_text(encoding="utf-8")
    recovery = (REPO_ROOT / "docs" / "recovery-evidence-ledger.md").read_text(encoding="utf-8")
    library = (REPO_ROOT / "docs" / "apple1-software-library.md").read_text(encoding="utf-8")

    assert "No firmware load, EEPROM write, or physical modification" in preservation
    assert "not eligible for EEPROM programming" in recovery
    assert "RAM-only" in library
