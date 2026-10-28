"""Run the preserved Apple-1 Integer BASIC on an NMOS 6502, entirely on the host.

This is execution of an identified interpreter, not a Python BASIC translation.
The PIA is a deliberately small behavioral model; electrical timing is not modeled.
"""

from __future__ import annotations

import argparse
import hashlib
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from py65.devices.mpu6502 import MPU

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "preservation/software/apple1-reference/apple1-basic.bin"
ROM_SHA256 = "5d8a3fe3c20c42903b226d67430c840ea5119557f88774c069e2e4dd80ad2c67"


class BasicMemory(list):
    """64 KiB address space with high-bit keyboard input and ready display."""

    def __init__(self) -> None:
        super().__init__([0] * 65536)
        self.incoming: deque[int] = deque()
        self.output = bytearray()

    def __getitem__(self, address):
        if address == 0xD011:
            return 0x80 if self.incoming else 0
        if address == 0xD010:
            return self.incoming.popleft() | 0x80 if self.incoming else 0
        if address == 0xD012:
            return 0  # ready; no display timing claim
        return super().__getitem__(address)

    def __setitem__(self, address, value):
        if address == 0xD012 and super().__getitem__(0xD013) & 4:
            self.output.append(value & 0x7F)
        return super().__setitem__(address, value)


@dataclass
class BasicSession:
    transcript: str
    stop: str
    instructions: int
    memory: BasicMemory
    cpu: MPU
    commands_consumed: int

    @property
    def lomem(self) -> int:
        return self.memory[0x4A] | self.memory[0x4B] << 8

    @property
    def himem(self) -> int:
        return self.memory[0x4C] | self.memory[0x4D] << 8


def run_session(lines: list[str], *, max_instructions: int = 2_000_000) -> BasicSession:
    """Feed complete lines only at this ROM's blocking keyboard input poll.

    BASIC checks for a break key while running. Preloading the whole script into
    the keyboard would let those checks eat later commands. Releasing one line
    at $E003 also supports program INPUT without faking its result.
    """
    rom = ROM.read_bytes()
    if len(rom) != 4096 or hashlib.sha256(rom).hexdigest() != ROM_SHA256:
        raise ValueError("BASIC ROM identity does not match the preservation record")
    memory = BasicMemory()
    memory[0xE000:0xF000] = rom
    memory[0xD013] = 0xA7  # modeled PIA display data register enabled
    return _execute(memory, lines, start=0xE000, max_instructions=max_instructions)


def resume_session(memory: BasicMemory, lines: list[str], *, max_instructions: int = 2_000_000) -> BasicSession:
    """Warm start an independently saved/restored interpreter state in host RAM."""
    if hashlib.sha256(bytes(memory[0xE000:0xF000])).hexdigest() != ROM_SHA256:
        raise ValueError("warm session requires the identified BASIC ROM")
    memory.output.clear()
    memory.incoming.clear()
    return _execute(memory, lines, start=0xE2B3, max_instructions=max_instructions)


def _execute(memory: BasicMemory, lines: list[str], *, start: int, max_instructions: int) -> BasicSession:
    if max_instructions < 1:
        raise ValueError("max_instructions must be positive")
    for line in lines:
        if any(not (0x20 <= ord(c) <= 0x5F) for c in line):
            raise ValueError("session lines require uppercase Apple-1 printable ASCII without line breaks")
    cpu = MPU(memory=memory, pc=start)
    pending = deque(lines)
    stop = "instruction-limit"
    consumed = 0
    steps = 0
    while steps < max_instructions:
        if cpu.pc == 0xE003 and not memory.incoming:
            if not pending:
                stop = "waiting-for-input"
                break
            memory.incoming.extend(pending.popleft().encode("ascii") + b"\r")
            consumed += 1
        if cpu.pc in (0xFF00, 0xFF1F):
            stop = "monitor-exit"
            break
        cpu.step()
        steps += 1
    return BasicSession(memory.output.decode("ascii").replace("\r", "\n"), stop, steps, memory, cpu, consumed)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", type=Path, help="uppercase text: numbered program, RUN, then INPUT replies")
    parser.add_argument("--max-instructions", type=int, default=2_000_000)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = run_session(args.session.read_text(encoding="ascii").splitlines(), max_instructions=args.max_instructions)
    print(result.transcript, end="")
    print(f"[NMOS 6502; {result.stop}; {result.instructions} instructions; ROM {ROM_SHA256}]")
    return 0 if result.stop == "waiting-for-input" else 1


if __name__ == "__main__":
    raise SystemExit(main())
