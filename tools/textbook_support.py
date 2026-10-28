"""Shared host-only helpers for the textbook's readable worked examples."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from neural1.assembler import LessonAssembler
from neural1.world import VirtualApple1World
from tools.apple1_emulator import Apple1RamHarness

ROOT = Path(__file__).resolve().parents[1]


def emit(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, default=str))


def cpu(source: str, *, inspect: tuple[int, ...] = (0x400,), trace: bool = False):
    """Assemble at 0300, execute the existing NMOS virtual world, inspect bytes."""
    assembled = LessonAssembler().assemble(source, origin=0x300)
    if assembled.diagnostics:
        raise ValueError(str(assembled.diagnostics))
    world = VirtualApple1World(ram_start=0x300)
    world.host_write(0x300, assembled.payload)
    result = world.execute(0x300, max_instructions=1000)
    print("Program bytes:", assembled.payload.hex(" ").upper())
    if trace:
        print("Before instruction: PC    A  X  Y  P")
        for row in result.trace[:16]:
            print(f"                    {row.pc:04X} {row.a:02X} {row.x:02X} {row.y:02X} {row.p:02X}")
    print(f"Stop: {result.stop_reason}; instructions: {result.instructions}")
    print(f"Final A={result.final_a:02X} X={result.final_x:02X} Y={result.final_y:02X}")
    if result.screen_text:
        print("Screen:", repr(result.screen_text))
    for address in inspect:
        print(f"{address:04X}: {world.host_read(address)[0]:02X}")
    return world, result, assembled


def echo(text: str, *, variant: bool = False):
    filename = "line-input-echo-0300.hex" if variant else "line-input-0300.hex"
    result = Apple1RamHarness.from_program_file(ROOT / "software/ram-only" / filename).run_keyboard_line(text)
    emit(result.__dict__)
    return result
