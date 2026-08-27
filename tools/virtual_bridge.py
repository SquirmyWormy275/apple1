"""Virtual Apple-1/LLM bridge with no physical serial-device code path."""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Protocol, Sequence

try:  # Support both ``python -m tools.virtual_bridge`` and documented script use.
    from tools.apple1_emulator import Apple1RamHarness
    from tools.apple1_text import format_for_apple1
except ModuleNotFoundError:  # pragma: no cover - exercised by the direct-script smoke test
    from apple1_emulator import Apple1RamHarness
    from apple1_text import format_for_apple1


class BridgeError(RuntimeError):
    """The virtual bridge cannot create a complete, reviewable response."""


class ModelClient(Protocol):
    def complete(self, prompt: str) -> str: ...


@dataclass(frozen=True)
class StaticModelClient:
    """Deterministic model replacement for demos and automated tests."""

    response: str

    def complete(self, prompt: str) -> str:
        return self.response


@dataclass(frozen=True)
class OllamaModelClient:
    """Explicit, opt-in local Ollama client; it has no serial dependency."""

    model: str
    runner: Callable[[list[str]], str] | None = None

    def complete(self, prompt: str) -> str:
        command = ["ollama", "run", self.model, "--think=false", prompt]
        response = self.runner(command) if self.runner is not None else self._run(command)
        if not response.strip():
            raise BridgeError("model returned an empty response")
        return response

    @staticmethod
    def _run(command: list[str]) -> str:
        try:
            completed = subprocess.run(command, check=True, capture_output=True, text=True)
        except (OSError, subprocess.CalledProcessError) as error:
            raise BridgeError("Ollama invocation failed") from error
        return completed.stdout


@dataclass(frozen=True)
class VirtualBridgeResult:
    timestamp_utc: str
    program: str
    prompt: str
    keyboard_echo: str
    returned_to_monitor: bool
    response_lines: tuple[str, ...]
    serial_opened: bool = False


class VirtualApple1Bridge:
    """Run a RAM-program rehearsal and render a response for a 40-column display."""

    def __init__(self, model: ModelClient, *, width: int = 40) -> None:
        self.model = model
        self.width = width

    def run(self, program: str | Path, prompt: str) -> VirtualBridgeResult:
        emulator_result = Apple1RamHarness.from_program_file(program).run_keyboard_line(prompt)
        response = self.model.complete(prompt)
        return VirtualBridgeResult(
            timestamp_utc=datetime.now(UTC).isoformat(),
            program=str(program),
            prompt=prompt,
            keyboard_echo=emulator_result.screen_text,
            returned_to_monitor=emulator_result.returned_to_monitor,
            response_lines=tuple(format_for_apple1(response, width=self.width)),
        )


def write_transcript(path: str | Path, result: VirtualBridgeResult) -> None:
    """Append one explicit virtual-only session record to a JSONL file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("a", encoding="utf-8") as transcript:
        transcript.write(json.dumps(asdict(result), sort_keys=True) + "\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--program", type=Path, required=True)
    parser.add_argument("--input", required=True, help="keyboard text ending with CR")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--reply", help="deterministic virtual response")
    source.add_argument("--ollama", metavar="MODEL", help="explicitly invoke a local Ollama model")
    parser.add_argument("--transcript", type=Path)
    args = parser.parse_args(argv)

    model: ModelClient = StaticModelClient(args.reply) if args.reply is not None else OllamaModelClient(args.ollama)
    result = VirtualApple1Bridge(model).run(args.program, args.input)
    if args.transcript is not None:
        write_transcript(args.transcript, result)
    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
