"""Read-only, bounded ProDOS inspector for the CFFA1 host build.

Supports seedling/sapling/tree files and one level of subdirectories. It does
not mount or mutate an image. CFFA1's actual ROM performs the build writes.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass


def u16(data: bytes, offset: int) -> int:
    return int.from_bytes(data[offset:offset + 2], "little")


@dataclass(frozen=True)
class Entry:
    path: str
    storage: int
    file_type: int
    aux: int
    key: int
    size: int
    blocks: int


class ProdosImage:
    def __init__(self, raw: bytes) -> None:
        self.raw = raw
        if len(raw) < 7 * 512 or len(raw) % 512:
            raise ValueError("not a complete block image")
        header = raw[1024:1536]
        self.total = u16(header, 41)
        self.bitmap = u16(header, 39)
        if header[4] >> 4 != 15 or header[35:37] != bytes([39, 13]):
            raise ValueError("invalid ProDOS volume header")
        if not 7 <= self.total <= len(raw) // 512 or not 3 <= self.bitmap < self.total:
            raise ValueError("invalid ProDOS volume bounds")
        self.owners: dict[int, str] = {}
        self._claim(0, "boot")
        self._claim(1, "boot")
        for n in range(self.bitmap, self.bitmap + (self.total + 4095) // 4096):
            self._claim(n, "bitmap")
        self.entries: dict[str, Entry] = {}
        self._directory(2, "", 0)

    def block(self, number: int) -> bytes:
        if not 0 <= number < self.total:
            raise ValueError(f"block outside volume: {number}")
        return self.raw[number * 512:(number + 1) * 512]

    def _claim(self, number: int, owner: str) -> None:
        self.block(number)
        if number in self.owners:
            raise ValueError(f"block {number} shared by {owner} and {self.owners[number]}")
        bit_offset = self.bitmap * 512 + number // 8
        if bit_offset >= len(self.raw) or self.raw[bit_offset] & (0x80 >> (number % 8)):
            raise ValueError(f"allocated block {number} marked free")
        self.owners[number] = owner

    def _directory(self, key: int, prefix: str, depth: int) -> None:
        if depth > 1:
            raise ValueError("CFFA1 edition permits only one subdirectory level")
        header = self.block(key)
        if header[4] >> 4 != (15 if depth == 0 else 14) or header[35:37] != bytes([39, 13]):
            raise ValueError("bad directory header")
        expected = u16(header, 37)
        previous = 0
        number = key
        actual = 0
        chain_length = 0
        while number:
            self._claim(number, prefix or "/")
            data = self.block(number)
            if u16(data, 0) != previous:
                raise ValueError("broken directory back link")
            for offset in range(4, 512 - 38, 39):
                entry = data[offset:offset + 39]
                storage = entry[0] >> 4
                if not storage or number == key and offset == 4:
                    continue
                name = entry[1:1 + (entry[0] & 15)].decode("ascii")
                if not re.fullmatch(r"[A-Z][A-Z0-9.]{0,14}", name):
                    raise ValueError(f"invalid filename: {name!r}")
                path = prefix + "/" + name
                if path in self.entries or u16(entry, 37) != key:
                    raise ValueError(f"duplicate name or invalid directory pointer: {path}")
                item = Entry(path, storage, entry[16], u16(entry, 31), u16(entry, 17),
                             int.from_bytes(entry[21:24], "little"), u16(entry, 19))
                self.entries[path] = item
                actual += 1
                if storage == 13:
                    self._directory(item.key, path, depth + 1)
                    sub = self.block(item.key)
                    if (u16(sub, 39), sub[41], sub[42]) != (number, (offset - 4) // 39 + 1, 39):
                        raise ValueError(f"bad subdirectory parent link: {path}")
                else:
                    self._contents(item, claim=True)
            previous, number = number, u16(data, 2)
            chain_length += 1
        if actual != expected or depth == 0 and actual > 51:
            raise ValueError(f"directory count/limit mismatch: {prefix or '/'}")
        if depth:
            item = self.entries[prefix]
            if item.size != chain_length * 512 or item.blocks != chain_length:
                raise ValueError(f"directory size mismatch: {prefix}")

    def _contents(self, item: Entry, *, claim: bool = False) -> bytes:
        count = (item.size + 511) // 512
        used: list[int] = []

        def pointers(number: int) -> list[int]:
            used.append(number)
            data = self.block(number)
            return [data[i] | data[256 + i] << 8 for i in range(256)]

        if item.storage == 1:
            if item.size > 512:
                raise ValueError("oversized seedling")
            values = [item.key]
        elif item.storage == 2:
            if item.size > 256 * 512:
                raise ValueError("oversized sapling")
            values = pointers(item.key)
        elif item.storage == 3:
            values = []
            for n in pointers(item.key)[:(count + 255) // 256]:
                values.extend(pointers(n) if n else [0] * 256)
        else:
            raise ValueError(f"unsupported storage type {item.storage}: {item.path}")
        values = values[:count]
        used.extend(n for n in values if n)
        if len(used) != item.blocks:
            raise ValueError(f"block count mismatch: {item.path}")
        if claim:
            for n in used:
                self._claim(n, item.path)
        return b"".join(self.block(n) if n else bytes(512) for n in values)[:item.size]

    def read(self, path: str) -> bytes:
        return self._contents(self.entries[path])

    def inventory(self) -> list[dict]:
        return [
            {"path": e.path, "file_type": f"{e.file_type:02X}", "aux_type": f"{e.aux:04X}", "bytes": e.size,
             "sha256": hashlib.sha256(self.read(e.path)).hexdigest()}
            for e in sorted(self.entries.values(), key=lambda item: item.path) if e.storage != 13
        ]
