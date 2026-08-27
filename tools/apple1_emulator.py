"""ROM-free Apple-1 RAM-program emulator harness.

This executes the repository's small 6502 Monitor programs with the Py65 NMOS
6502 model.  It models only the keyboard registers and Monitor ECHO/warm-entry
calls those programs need; it does not emulate the Replica 1 Plus, its
Propeller, serial hardware, or an Apple-1 ROM image.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Sequence

from py65.devices.mpu6502 import MPU


PROGRAM_ADDRESS = 0x0300
KEYBOARD_DATA = 0xD010
KEYBOARD_STATUS = 0xD011
MONITOR_ECHO = 0xFFEF
MONITOR_WARM_ENTRY = 0xFF1F
MAX_INSTRUCTIONS = 100_000


class ProgramFormatError(ValueError):
    """A repository RAM-program artifact is not a valid byte sequence."""


class ProgramExecutionError(RuntimeError):
    """The constrained harness cannot complete the requested program run."""


@dataclass(frozen=True)
class EmulatorResult:
    screen_text: str
    buffer_text: str
    returned_to_monitor: bool
    instructions: int


def load_hex_program(path: str | Path) -> bytes:
    """Load an address-free, whitespace-separated byte list."""
    source = Path(path)
    try:
        tokens = source.read_text(encoding="ascii").split()
    except OSError as error:
        raise ProgramFormatError(f"cannot read program: {source}") from error
    if not tokens:
        raise ProgramFormatError("program contains no bytes")
    try:
        payload = bytes(int(token, 16) for token in tokens)
    except ValueError as error:
        raise ProgramFormatError(f"program has a non-hex byte: {source}") from error
    if any(len(token) != 2 or not 0 <= byte <= 0xFF for token, byte in zip(tokens, payload, strict=True)):
        raise ProgramFormatError(f"program has an invalid byte width: {source}")
    return payload


class Apple1RamHarness:
    """Execute one of the repository's RAM-only Monitor programs."""

    def __init__(self, program: bytes, *, address: int = PROGRAM_ADDRESS) -> None:
        if not program:
            raise ProgramFormatError("program contains no bytes")
        if address < 0 or address + len(program) > 0x10000:
            raise ProgramFormatError("program does not fit in 64 KiB memory")
        self.program = program
        self.address = address

    @classmethod
    def from_program_file(cls, path: str | Path) -> Apple1RamHarness:
        return cls(load_hex_program(path))

    def run_keyboard_line(self, text: str) -> EmulatorResult:
        try:
            incoming = deque(byte | 0x80 for byte in text.encode("ascii", errors="strict"))
        except UnicodeEncodeError as error:
            raise ProgramExecutionError("keyboard input must be seven-bit ASCII") from error
        if not incoming or incoming[-1] != 0x8D:
            raise ProgramExecutionError("keyboard input must end with carriage return")

        mpu = MPU()
        mpu.memory[self.address : self.address + len(self.program)] = self.program
        mpu.memory[MONITOR_ECHO] = 0x60  # RTS after the harness records A.
        mpu.pc = self.address
        screen: list[int] = []

        for instruction in range(1, MAX_INSTRUCTIONS + 1):
            if mpu.pc == MONITOR_WARM_ENTRY:
                return EmulatorResult(
                    screen_text=bytes(screen).decode("ascii"),
                    buffer_text=self._buffer_text(mpu),
                    returned_to_monitor=True,
                    instructions=instruction - 1,
                )
            if not incoming and mpu.pc == self.address and screen:
                return EmulatorResult(
                    screen_text=bytes(screen).decode("ascii"),
                    buffer_text=self._buffer_text(mpu),
                    returned_to_monitor=False,
                    instructions=instruction - 1,
                )
            if mpu.pc == MONITOR_ECHO:
                screen.append(mpu.a & 0x7F)

            self._prepare_keyboard_read(mpu, incoming)
            mpu.step()

        raise ProgramExecutionError(f"program exceeded {MAX_INSTRUCTIONS} instructions")

    @staticmethod
    def _prepare_keyboard_read(mpu: MPU, incoming: deque[int]) -> None:
        mpu.memory[KEYBOARD_STATUS] = 0x80 if incoming else 0x00
        if mpu.memory[mpu.pc] == 0xAD and mpu.memory[mpu.pc + 1] == 0x10 and mpu.memory[mpu.pc + 2] == 0xD0:
            if not incoming:
                raise ProgramExecutionError("program read keyboard data without a ready byte")
            mpu.memory[KEYBOARD_DATA] = incoming.popleft()
            mpu.memory[KEYBOARD_STATUS] = 0x80 if incoming else 0x00

    @staticmethod
    def _buffer_text(mpu: MPU) -> str:
        buffer = bytearray()
        for offset in range(128):
            byte = mpu.memory[0x0400 + offset]
            buffer.append(byte & 0x7F)
            if byte == 0x8D:
                break
        return bytes(buffer).decode("ascii")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", type=Path, help="address-free RAM-program byte list")
    parser.add_argument("--input", required=True, help="seven-bit keyboard text ending with CR")
    args = parser.parse_args(argv)
    result = Apple1RamHarness.from_program_file(args.program).run_keyboard_line(args.input)
    print(json.dumps(result.__dict__, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
