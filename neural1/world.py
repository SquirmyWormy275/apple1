"""Deterministic Apple-1 memory world and constrained WozMon interaction."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .core import Neural1Error, sha256_bytes


MEMORY_SIZE = 0x10000
DEFAULT_START = 0x0200


@dataclass(frozen=True)
class WorldSnapshot:
    memory: bytes
    ram_start: int
    ram_budget: int
    generation: int

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.memory)


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
    def restore(cls, snapshot: WorldSnapshot) -> "VirtualApple1World":
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


class WozMonSession:
    """Small modeled monitor surface: examine, block examine, deposit, and run intent."""

    _HEX = re.compile(r"^[0-9A-F]{1,4}$")

    def __init__(self, world: VirtualApple1World) -> None:
        self._world = world

    def transact(self, command: str) -> str:
        command = command.strip().upper()
        if not command or any(ord(ch) < 0x20 or ord(ch) > 0x7E for ch in command):
            return "ERR SYNTAX"
        try:
            if command.endswith("R"):
                address = self._address(command[:-1])
                self._world._check(address)
                return f"{address:04X}: RUN REQUEST RECORDED"
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
