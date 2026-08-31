"""Deterministic two-pass lesson assembler and bounded execution traces."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from py65.assembler import Assembler
from py65.devices.mpu6502 import MPU

from .core import Neural1Error
from .world import ExecutionResult, VirtualApple1World


@dataclass(frozen=True)
class AssemblyDiagnostic:
    line: int
    severity: str
    message: str


@dataclass(frozen=True)
class AssemblyResult:
    origin: int
    payload: bytes
    symbols: dict[str, int]
    diagnostics: tuple[AssemblyDiagnostic, ...]


_LABEL = re.compile(r"^[A-Z_][A-Z0-9_]*$")
_TOKEN = re.compile(r"(?<![$0-9])\b[A-Z_][A-Z0-9_]*\b")


class LessonAssembler:
    def __init__(self) -> None:
        self._assembler = Assembler(MPU())

    def assemble(self, source: str, *, origin: int = 0x0200) -> AssemblyResult:
        statements = self._parse(source)
        symbols: dict[str, int] = {}
        diagnostics: list[AssemblyDiagnostic] = []
        pc = origin
        for line, label, statement in statements:
            if label:
                if label in symbols:
                    diagnostics.append(AssemblyDiagnostic(line, "ERROR", f"duplicate label: {label}"))
                else:
                    symbols[label] = pc
            if statement:
                try:
                    pc += len(self._encode(statement, pc, {}, unresolved=True))
                except (SyntaxError, ValueError, OverflowError):
                    diagnostics.append(AssemblyDiagnostic(line, "ERROR", f"cannot size instruction: {statement}"))
        payload = bytearray()
        pc = origin
        if not diagnostics:
            for line, _, statement in statements:
                if not statement:
                    continue
                try:
                    encoded = self._encode(statement, pc, symbols, unresolved=False)
                    payload.extend(encoded)
                    pc += len(encoded)
                except (SyntaxError, ValueError, OverflowError, KeyError):
                    diagnostics.append(AssemblyDiagnostic(line, "ERROR", f"cannot assemble: {statement}"))
        if origin < 0 or origin + len(payload) > 0x10000:
            diagnostics.append(AssemblyDiagnostic(0, "ERROR", "assembled program exceeds address space"))
        return AssemblyResult(origin, bytes(payload) if not diagnostics else b"", symbols, tuple(diagnostics))

    def assemble_and_run(self, source: str, *, origin: int = 0x0200, ram_budget: int = 4096, max_instructions: int = 10_000) -> tuple[AssemblyResult, ExecutionResult | None]:
        assembled = self.assemble(source, origin=origin)
        if assembled.diagnostics:
            return assembled, None
        world = VirtualApple1World(ram_start=origin, ram_budget=ram_budget)
        world.host_write(origin, assembled.payload)
        return assembled, world.execute(origin, max_instructions=max_instructions)

    def _encode(self, statement: str, pc: int, symbols: dict[str, int], *, unresolved: bool) -> bytes:
        upper = statement.upper().strip()
        if upper.startswith(".BYTE "):
            values = [item.strip() for item in upper[6:].split(",")]
            return bytes(self._number(value, symbols, unresolved) & 0xFF for value in values)
        parts = upper.split(maxsplit=1)
        if len(parts) == 2:
            mnemonic, operand = parts
            for token in set(_TOKEN.findall(operand)):
                if token in {"A", "X", "Y"}:
                    continue
                value = symbols.get(token, 0 if unresolved else None)
                if value is None:
                    raise KeyError(token)
                operand = re.sub(rf"\b{re.escape(token)}\b", f"${value:04X}", operand)
            upper = f"{mnemonic} {operand}"
        return bytes(self._assembler.assemble(upper, pc=pc))

    @staticmethod
    def _number(value: str, symbols: dict[str, int], unresolved: bool) -> int:
        if value in symbols:
            return symbols[value]
        if _LABEL.fullmatch(value):
            if unresolved:
                return 0
            raise KeyError(value)
        return int(value[1:], 16) if value.startswith("$") else int(value, 0)

    @staticmethod
    def _parse(source: str) -> list[tuple[int, str | None, str]]:
        result = []
        for number, raw in enumerate(source.splitlines(), 1):
            text = raw.split(";", 1)[0].strip()
            if not text:
                continue
            label = None
            if ":" in text:
                candidate, text = text.split(":", 1)
                candidate = candidate.strip().upper()
                if not _LABEL.fullmatch(candidate):
                    raise Neural1Error(f"invalid label on line {number}")
                label = candidate
                text = text.strip()
            result.append((number, label, text))
        return result


def trace_records(result: ExecutionResult) -> list[dict[str, int]]:
    return [asdict(entry) for entry in result.trace]
