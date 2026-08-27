from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.virtual_bridge import (
    BridgeError,
    OllamaModelClient,
    StaticModelClient,
    VirtualApple1Bridge,
    write_transcript,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_virtual_bridge_runs_a_keyboard_program_and_formats_a_model_reply() -> None:
    bridge = VirtualApple1Bridge(StaticModelClient("hello, café"))

    result = bridge.run("software/ram-only/line-input-0300.hex", "ASK\r")

    assert result.keyboard_echo == "ASK\r"
    assert result.returned_to_monitor is True
    assert result.response_lines == ("HELLO, CAF?",)
    assert result.serial_opened is False


def test_ollama_adapter_requires_an_explicit_runner_and_preserves_arguments() -> None:
    seen: list[list[str]] = []
    client = OllamaModelClient("phi4-mini", runner=lambda command: seen.append(command) or "reply")

    assert client.complete("PROMPT") == "reply"
    assert seen == [["ollama", "run", "phi4-mini", "--think=false", "PROMPT"]]


def test_ollama_adapter_rejects_an_empty_response() -> None:
    client = OllamaModelClient("phi4-mini", runner=lambda command: "")

    with pytest.raises(BridgeError, match="empty"):
        client.complete("PROMPT")


def test_transcript_is_explicit_and_contains_no_hardware_action(tmp_path) -> None:
    bridge = VirtualApple1Bridge(StaticModelClient("OK"))
    result = bridge.run("software/ram-only/line-input-0300.hex", "GO\r")
    transcript = tmp_path / "virtual.jsonl"

    write_transcript(transcript, result)

    record = json.loads(transcript.read_text(encoding="utf-8"))
    assert record["serial_opened"] is False
    assert record["response_lines"] == ["OK"]


def test_documented_direct_script_command_runs_without_package_installation() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "tools/virtual_bridge.py",
            "--program",
            "software/ram-only/line-input-0300.hex",
            "--input",
            "GO\r",
            "--reply",
            "ready",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["response_lines"] == ["READY"]
