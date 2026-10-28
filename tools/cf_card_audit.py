"""Read-only inventory and independent byte/metadata check of a ProDOS CF image.

Only the first volume is interpreted. All remaining device bytes are preserved
and compared separately. This module cannot format or write a physical device.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


def inventory(image: bytes) -> dict[str, dict]:
    def word(offset: int) -> int:
        return struct.unpack_from("<H", image, offset)[0]

    total = word(2 * 512 + 41)
    if not 22 < total <= 65535 or total * 512 > len(image):
        raise ValueError("invalid first-volume size")
    if image[1028] >> 4 != 15 or image[1059:1061] != bytes([39, 13]):
        raise ValueError("not a supported ProDOS root directory")

    def block(number: int) -> bytes:
        if not 0 < number < total:
            raise ValueError(f"block outside volume: {number}")
        return image[number * 512:(number + 1) * 512]

    def pointers(number: int) -> list[int]:
        data = block(number)
        return [data[i] | (data[i + 256] << 8) for i in range(256)]

    def contents(kind: int, key: int, length: int) -> bytes:
        if kind == 1:
            blocks = [key] + [0] * 255  # A sparse logical tail may extend past block 0.
        elif kind == 2:
            blocks = pointers(key)
        elif kind == 3:
            blocks = [n for index in pointers(key) for n in (pointers(index) if index else [0] * 256)]
        else:
            raise ValueError(f"unsupported file storage kind: {kind}")
        if len(blocks) * 512 < length:
            raise ValueError("file length exceeds its block index")
        return b"".join(block(n) if n else bytes(512) for n in blocks[:(length + 511) // 512])[:length]

    records: dict[str, dict] = {}
    seen_directories: set[int] = set()

    def directory(first: int, prefix: str = "") -> None:
        current, previous = first, 0
        found = 0
        header = block(first)
        expected = int.from_bytes(header[37:39], "little")
        while current:
            if current in seen_directories:
                raise ValueError("directory cycle or crosslink")
            seen_directories.add(current)
            data = block(current)
            if int.from_bytes(data[:2], "little") != previous:
                raise ValueError("invalid directory backward link")
            for i in range(13):
                entry = data[4 + 39 * i:4 + 39 * (i + 1)]
                kind, namelen = entry[0] >> 4, entry[0] & 15
                if not kind or kind in (14, 15):
                    continue
                name = entry[1:1 + namelen].decode("ascii")
                path = prefix + name
                if path in records:
                    raise ValueError("duplicate directory entry")
                key = int.from_bytes(entry[17:19], "little")
                length = int.from_bytes(entry[21:24], "little")
                record = dict(file_type=entry[16], aux_type=int.from_bytes(entry[31:33], "little"),
                              bytes=length, storage_kind=kind, key_block=key,
                              blocks_used=int.from_bytes(entry[19:21], "little"),
                              entry_hex=entry.hex())
                records[path] = record
                found += 1
                if kind == 13:
                    directory(key, path + "/")
                else:
                    try:
                        record["sha256"] = hashlib.sha256(contents(kind, key, length)).hexdigest()
                    except ValueError as error:
                        raise ValueError(f"{path}: {error}") from error
            previous, current = current, int.from_bytes(data[2:4], "little")
        if found != expected:
            raise ValueError(f"directory count mismatch: {prefix} {found} != {expected}")

    directory(2)
    return records


def verify(before: bytes, after: bytes, manifest: dict) -> dict:
    if len(before) != len(after):
        raise ValueError("device size changed")
    old, new = inventory(before), inventory(after)
    for path, record in old.items():
        if path not in new or record != new[path]:
            raise ValueError(f"original entry, metadata or contents changed: {path}")
    volume_end = int.from_bytes(before[1065:1067], "little") * 512
    if before[:1024] != after[:1024] or before[volume_end:] != after[volume_end:]:
        raise ValueError("boot blocks or bytes beyond the original volume changed")
    expected = {record["path"]: record for record in manifest["files"]}
    # BUILD.JSON describes all other payloads; it cannot hash itself.
    if "HOSTSRC/BUILD.JSON" not in expected:
        manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        expected["HOSTSRC/BUILD.JSON"] = dict(bytes=len(manifest_bytes), sha256=hashlib.sha256(manifest_bytes).hexdigest(),
                                                 file_type=0, aux_type=0)
    for path, record in expected.items():
        for field in ("bytes", "sha256", "file_type", "aux_type"):
            if new.get(path, {}).get(field) != record[field]:
                raise ValueError(f"payload verification failed: {path} {field}")
    new_files = {p for p, r in new.items() if r["storage_kind"] != 13} - set(old)
    if new_files != set(expected):
        raise ValueError("unexpected or missing installed files")
    return dict(original_files=sum("sha256" in r for r in old.values()), added_files=len(expected),
                original_entries_unchanged=True, boot_blocks_unchanged=True,
                trailing_bytes_unchanged=True, size_bytes=len(after),
                before_sha256=hashlib.sha256(before).hexdigest(), after_sha256=hashlib.sha256(after).hexdigest())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--build", type=Path)
    args = parser.parse_args()
    if args.before and args.build:
        result = verify(args.before.read_bytes(), args.image.read_bytes(), json.loads(args.build.read_text()))
    elif args.before or args.build:
        parser.error("--before and --build must be supplied together")
    else:
        result = inventory(args.image.read_bytes())
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
