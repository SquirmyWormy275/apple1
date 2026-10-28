"""Execute the preserved CFFA1 firmware with an in-memory ATA card.

The firmware parses and writes ProDOS itself. This host model implements only
the ATA operations that identified ROM uses. No device, serial port or mount is
opened. Writes are sparse modifications of an immutable bytes object.
"""

from __future__ import annotations

import hashlib
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from py65.devices.mpu6502 import MPU

from tools.apple1_basic import BasicMemory

ROOT = Path(__file__).resolve().parents[1]
ROM = ROOT / "preservation/software/apple1-reference/cffa1-v1.1.bin"


class AtaMemory(BasicMemory):
    def __init__(self, image: bytes) -> None:
        super().__init__()
        if not image or len(image) % 512:
            raise ValueError("image must contain complete 512-byte blocks")
        self.image = image
        self.changed: dict[int, bytes] = {}
        self.transfer: deque[int] = deque()
        self.write_buffer: bytearray | None = None
        self.write_lba = 0
        self.reads = 0
        self.writes = 0
        self.error = False

    def block(self, number: int) -> bytes:
        if not 0 <= number < len(self.image) // 512:
            raise ValueError(f"ATA block out of range: {number}")
        return self.changed.get(number, self.image[number * 512:(number + 1) * 512])

    def __getitem__(self, address):
        if address in (0xAFF6, 0xAFFF):
            return (0x58 if self.transfer or self.write_buffer is not None else 0x50) | int(self.error)
        if address in (0xAFF0, 0xAFF8):
            return self.transfer.popleft() if self.transfer else 0
        if address == 0xAFF9:
            return 4 if self.error else 0
        return super().__getitem__(address)

    def __setitem__(self, address, value):
        if address == 0xAFFF:
            self.error = False
            lba = sum(super(AtaMemory, self).__getitem__(0xAFFB + i) << (8 * i) for i in range(3))
            lba |= (super().__getitem__(0xAFFE) & 15) << 24
            if value == 0xEF:  # SET FEATURES; this ROM enables 8-bit transfers
                pass
            elif value == 0xEC:  # IDENTIFY; current and LBA sector counts
                identify = bytearray(512)
                for offset in (114, 120):
                    identify[offset:offset + 4] = (len(self.image) // 512).to_bytes(4, "little")
                self.transfer = deque(identify)
            elif value in (0x20, 0x30):
                if not 0 <= lba < len(self.image) // 512:
                    self.error = True
                elif value == 0x20:
                    self.transfer = deque(self.block(lba))
                    self.reads += 1
                else:
                    self.write_lba = lba
                    self.write_buffer = bytearray()
            else:
                raise ValueError(f"unmodeled ATA command: {value:02X}")
        elif address in (0xAFF0, 0xAFF8) and self.write_buffer is not None:
            self.write_buffer.append(value)
            if len(self.write_buffer) == 512:
                self.changed[self.write_lba] = bytes(self.write_buffer)
                self.write_buffer = None
                self.writes += 1
        super().__setitem__(address, value)

    def materialize(self) -> bytes:
        result = bytearray(self.image)
        for number, data in self.changed.items():
            result[number * 512:(number + 1) * 512] = data
        return bytes(result)


@dataclass(frozen=True)
class ApiResult:
    a: int
    carry: bool
    instructions: int


class Cffa1Machine:
    def __init__(self, image: bytes) -> None:
        import json

        provenance = json.loads((ROM.parent / "provenance.json").read_text())
        expected = next(f for f in provenance["files"] if f["file"] == ROM.name)
        rom = ROM.read_bytes()
        if len(rom) != expected["bytes"] or hashlib.sha256(rom).hexdigest() != expected["sha256"]:
            raise ValueError("CFFA1 ROM does not match preservation identity")
        self.memory = AtaMemory(image)
        self.memory[0x9000:0x9000 + len(rom)] = rom
        self.memory[0xD013] = 0xA7
        self.cpu = MPU(memory=self.memory, pc=0x900C)

    def invoke(self, entry: int, *, selector: int = 0, keys: bytes = b"", limit: int = 2_000_000) -> ApiResult:
        self.memory.incoming.extend(keys)
        self.cpu.pc = entry
        self.cpu.x = selector
        self.cpu.stPushWord(0x02FE)  # RTS returns to a host stop address at $02FF
        for count in range(limit):
            if self.cpu.pc == 0x02FF:
                return ApiResult(self.cpu.a, bool(self.cpu.p & 1), count)
            self.cpu.step()
        raise RuntimeError(f"CFFA1 instruction bound reached at {self.cpu.pc:04X}")

    def filename(self, name: str) -> None:
        import re

        if not re.fullmatch(r"[A-Z][A-Z0-9.]{0,14}", name):
            raise ValueError(f"not a ProDOS filename: {name}")
        self.memory[0x280:0x280 + len(name) + 1] = bytes([len(name)]) + name.encode("ascii")
        self.memory[2:4] = [0x80, 2]

    def api(self, selector: int, *, name: str | None = None) -> ApiResult:
        if name is not None:
            self.filename(name)
        result = self.invoke(0x900C, selector=selector)
        if result.carry:
            raise ValueError(f"CFFA1 API {selector:02X}: error {result.a:02X} ({name or ''})")
        return result

    def prefix(self, name: str) -> None:
        """Use the actual menu P command, including empty name for the root."""
        if name:
            self.filename(name)  # validates syntax
        self.invoke(0x9006, keys=b"P" + name.encode("ascii") + b"\rQ")
        if self.memory.incoming:
            raise ValueError("menu did not consume the prefix selection")
        actual = bytes(self.memory[0x87B1:0x87B1 + self.memory[0x87B0]]).decode("ascii")
        if actual != name:
            raise ValueError(f"menu prefix {actual!r} differs from requested {name!r}")

    def write_file(self, name: str, data: bytes, *, file_type: int = 6, aux: int = 0x1000) -> None:
        if not 1 <= len(data) <= 0x7000:
            raise ValueError("payload must fit modeled RAM $1000-$7FFF")
        self.memory[0x1000:0x1000 + len(data)] = data
        self.memory[0:2] = [0, 0x10]
        self.memory[6] = file_type
        self.memory[7:9] = aux.to_bytes(2, "little")
        self.memory[9:11] = len(data).to_bytes(2, "little")
        self.api(0x20, name=name)

    def read_file(self, name: str) -> bytes:
        self.api(0x14, name=name)
        entry = self.memory[11] | self.memory[12] << 8
        size = int.from_bytes(bytes(self.memory[entry + 21:entry + 24]), "little")
        if not 1 <= size <= 0x7000:
            raise ValueError("read payload outside bounded host buffer")
        self.memory[0:2] = [0, 0x10]
        self.api(0x22, name=name)
        return bytes(self.memory[0x1000:0x1000 + size])

    def save_basic(self, name: str, source: str) -> None:
        from tools.apple1_basic import run_session

        session = run_session(source.splitlines())
        if session.stop != "waiting-for-input" or "\n*** " in session.transcript:
            raise ValueError("BASIC source failed to enter cleanly")
        self.memory[0x4A:0x100] = session.memory[0x4A:0x100]
        self.memory[session.lomem:session.himem] = session.memory[session.lomem:session.himem]
        self.api(0x24, name=name)  # real SaveBASICFile constructs the A1 header


def blank_virtual_card() -> Cffa1Machine:
    """Create a small virtual-only ProDOS volume using the actual format API."""
    machine = Cffa1Machine(bytes(512 * 1024))
    machine.cpu.y = 0x77  # firmware's explicit format guard; virtual bytes only
    machine.api(0x2E, name="HOSTTEST")
    return machine
