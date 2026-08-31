"""Deterministic Apple-1 memory world and constrained WozMon interaction."""

from __future__ import annotations

import re
from dataclasses import dataclass

from py65.devices.mpu6502 import MPU

from .core import Neural1Error, sha256_bytes

MEMORY_SIZE = 0x10000
DEFAULT_START = 0x0200
MONITOR_ECHO = 0xFFEF
MONITOR_WARM_ENTRY = 0xFF1F


@dataclass(frozen=True)
class WorldSnapshot:
    memory: bytes
    ram_start: int
    ram_budget: int
    generation: int

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.memory)


@dataclass(frozen=True)
class ExecutionTraceEntry:
    step: int
    pc: int
    opcode: int
    a: int
    x: int
    y: int
    sp: int
    p: int


@dataclass(frozen=True)
class ExecutionResult:
    start_address: int
    stop_reason: str
    instructions: int
    screen_text: str
    final_pc: int
    final_a: int
    final_x: int
    final_y: int
    final_sp: int
    final_p: int
    trace: tuple[ExecutionTraceEntry, ...]


class VirtualApple1World:
    """A byte-exact world; it makes no claim about physical Replica behavior."""

    def __init__(self, *, ram_budget: int = 4096, ram_start: int = DEFAULT_START) -> None:
        if ram_budget not in {1024, 2048, 3072, 4096}:
            raise Neural1Error("RAM budget must be one of 1K, 2K, 3K, or 4K")
        if ram_start + ram_budget > MEMORY_SIZE:
            raise Neural1Error("RAM region exceeds address space")
        self.ram_start = ram_start
        self.ram_budget = ram_budget
        self.generation = 0
        self._memory = bytearray(MEMORY_SIZE)

    @property
    def ram_end(self) -> int:
        return self.ram_start + self.ram_budget

    def snapshot(self) -> WorldSnapshot:
        return WorldSnapshot(bytes(self._memory), self.ram_start, self.ram_budget, self.generation)

    @classmethod
    def restore(cls, snapshot: WorldSnapshot) -> VirtualApple1World:
        world = cls(ram_budget=snapshot.ram_budget, ram_start=snapshot.ram_start)
        if len(snapshot.memory) != MEMORY_SIZE:
            raise Neural1Error("snapshot is not a 64 KiB memory image")
        world._memory[:] = snapshot.memory
        world.generation = snapshot.generation
        return world

    def _check(self, address: int, length: int = 1) -> None:
        if length < 0 or address < self.ram_start or address + length > self.ram_end:
            raise Neural1Error("access outside configured experimental RAM")

    def host_read(self, address: int, length: int = 1) -> bytes:
        """Privileged verifier API. Never expose this object directly to an agent."""
        self._check(address, length)
        return bytes(self._memory[address : address + length])

    def host_write(self, address: int, payload: bytes) -> None:
        self._check(address, len(payload))
        self._memory[address : address + len(payload)] = payload

    def intervene(self, address: int, length: int, *, xor_mask: int = 0) -> None:
        self._check(address, length)
        for index in range(address, address + length):
            self._memory[index] = 0 if xor_mask == 0 else self._memory[index] ^ xor_mask

    def execute(self, address: int, *, max_instructions: int = 10_000, trace_limit: int = 2_000) -> ExecutionResult:
        """Execute deposited NMOS 6502 bytes under a bounded virtual policy.

        This is deterministic software evidence, not cycle/electrical hardware
        evidence. Execution stops at BRK, Monitor warm entry, budget escape, or
        the instruction bound. Only the Monitor ECHO stub exists outside RAM.
        """
        self._check(address)
        if not 1 <= max_instructions <= 1_000_000 or trace_limit < 0:
            raise Neural1Error("invalid execution bound")
        mpu = MPU(memory=list(self._memory))
        mpu.memory[MONITOR_ECHO] = 0x60
        mpu.pc = address
        screen: list[int] = []
        trace: list[ExecutionTraceEntry] = []
        reason = "INSTRUCTION_LIMIT"
        completed = 0
        for step in range(max_instructions):
            if mpu.pc == MONITOR_WARM_ENTRY:
                reason = "MONITOR_WARM_ENTRY"
                break
            if mpu.pc != MONITOR_ECHO and not self.ram_start <= mpu.pc < self.ram_end:
                reason = "EXECUTION_LEFT_ALLOWED_RAM"
                break
            opcode = mpu.memory[mpu.pc]
            if len(trace) < trace_limit:
                trace.append(ExecutionTraceEntry(step, mpu.pc, opcode, mpu.a, mpu.x, mpu.y, mpu.sp, mpu.p))
            if opcode == 0x00:
                reason = "BRK"
                break
            if mpu.pc == MONITOR_ECHO:
                screen.append(mpu.a & 0x7F)
            mpu.step()
            completed += 1
        self._memory[self.ram_start : self.ram_end] = bytes(mpu.memory[self.ram_start : self.ram_end])
        return ExecutionResult(address, reason, completed, bytes(screen).decode("ascii", errors="replace"), mpu.pc, mpu.a, mpu.x, mpu.y, mpu.sp, mpu.p, tuple(trace))


class WozMonSession:
    """Small modeled monitor surface: examine, block examine, deposit, and run intent."""

    _HEX = re.compile(r"^[0-9A-F]{1,4}$")

    def __init__(self, world: VirtualApple1World, *, execute_runs: bool = True, max_instructions: int = 10_000) -> None:
        self._world = world
        self._execute_runs = execute_runs
        self._max_instructions = max_instructions

    def transact(self, command: str) -> str:
        command = command.strip().upper()
        if not command or any(ord(ch) < 0x20 or ord(ch) > 0x7E for ch in command):
            return "ERR SYNTAX"
        try:
            if command.endswith("R"):
                address = self._address(command[:-1])
                self._world._check(address)
                if not self._execute_runs:
                    return f"{address:04X}: RUN REQUEST RECORDED"
                result = self._world.execute(address, max_instructions=self._max_instructions, trace_limit=0)
                suffix = f" OUTPUT={result.screen_text!r}" if result.screen_text else ""
                return f"{address:04X}: STOP={result.stop_reason} STEPS={result.instructions}{suffix}"
            if ":" in command:
                head, values = command.split(":", 1)
                address = self._address(head)
                payload = bytes(int(token, 16) for token in values.split())
                if not payload or any(len(token) != 2 for token in values.split()):
                    raise ValueError
                self._world.host_write(address, payload)
                return f"{address:04X}: " + " ".join(f"{byte:02X}" for byte in payload)
            if "." in command:
                first, last = (self._address(value) for value in command.split(".", 1))
                if last < first or last - first >= 256:
                    raise Neural1Error("block examine is limited to 256 bytes")
                payload = self._world.host_read(first, last - first + 1)
                return self._render(first, payload)
            address = self._address(command)
            return self._render(address, self._world.host_read(address))
        except (ValueError, Neural1Error):
            return "ERR RANGE OR SYNTAX"

    def _address(self, text: str) -> int:
        if not self._HEX.fullmatch(text):
            raise ValueError
        return int(text, 16)

    @staticmethod
    def _render(address: int, payload: bytes) -> str:
        lines = []
        for offset in range(0, len(payload), 8):
            chunk = payload[offset : offset + 8]
            lines.append(f"{address + offset:04X}: " + " ".join(f"{byte:02X}" for byte in chunk))
        return "\n".join(lines)
