from __future__ import annotations

import hashlib
import json
import struct

import pytest

from tools.cf_card_audit import inventory, verify


def fixture_image() -> bytearray:
    image = bytearray(80 * 512)
    image[1028:1033] = b"\xf4TEST"
    image[1059:1061] = bytes([39, 13])
    struct.pack_into("<H", image, 1061, 1)  # root file count
    struct.pack_into("<H", image, 1065, 64)  # first-volume size
    add_entry(image, 1, "ORIGINAL", 22, b"PRESERVE ME")
    return image


def add_entry(image, slot, name, key, data, *, first=2):
    offset = first * 512 + 4 + 39 * slot
    image[offset] = 0x10 | len(name)
    image[offset + 1:offset + 1 + len(name)] = name.encode()
    image[offset + 16] = 6
    struct.pack_into("<HH", image, offset + 17, key, 1)
    image[offset + 21:offset + 24] = len(data).to_bytes(3, "little")
    struct.pack_into("<H", image, offset + 31, 0x1000)
    image[key * 512:key * 512 + len(data)] = data


def augmented():
    before = fixture_image()
    after = bytearray(before)
    add_entry(after, 2, "ADDITION", 23, b"NEW BOOK")
    struct.pack_into("<H", after, 1061, 3)
    manifest = {"files": [{"path": "ADDITION", "file_type": 6, "aux_type": 0x1000,
                           "bytes": 8, "sha256": hashlib.sha256(b"NEW BOOK").hexdigest()}]}
    add_entry(after, 3, "HOSTSRC", 24, bytes(512))
    after[1028 + 39 * 3] = 0xD7
    after[24 * 512 + 4:24 * 512 + 12] = b"\xe7HOSTSRC"
    struct.pack_into("<H", after, 24 * 512 + 37, 1)
    data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    add_entry(after, 1, "BUILD.JSON", 25, data, first=24)
    after[24 * 512 + 4 + 39 + 16] = 0
    struct.pack_into("<H", after, 24 * 512 + 4 + 39 + 31, 0)
    return bytes(before), after, manifest


def test_inventory_reads_bytes_and_detects_directory_count_errors():
    before = fixture_image()
    assert inventory(before)["ORIGINAL"]["sha256"] == hashlib.sha256(b"PRESERVE ME").hexdigest()
    struct.pack_into("<H", before, 1061, 2)
    with pytest.raises(ValueError, match="count mismatch"):
        inventory(before)


@pytest.mark.parametrize("change", ["contents", "metadata", "boot", "tail"])
def test_verifier_rejects_changes_to_original_material(change):
    before, after, manifest = augmented()
    if change == "contents":
        after[22 * 512] ^= 1
    elif change == "metadata":
        after[1028 + 39 + 31] ^= 1
    elif change == "boot":
        after[0] ^= 1
    else:
        after[70 * 512] ^= 1
    with pytest.raises(ValueError, match="original|boot blocks"):
        verify(before, after, manifest)


def test_verifier_accepts_addition_and_checks_load_address():
    before, after, manifest = augmented()
    assert verify(before, after, manifest)["added_files"] == 2
    struct.pack_into("<H", after, 1028 + 39 * 2 + 31, 0x9000)
    with pytest.raises(ValueError, match="aux_type"):
        verify(before, after, manifest)


def test_combined_inventory_can_record_the_component_manifest_explicitly():
    before, after, component_manifest = augmented()
    component_bytes = (json.dumps(component_manifest, indent=2, sort_keys=True) + "\n").encode()
    combined = {"files": [*component_manifest["files"],
                          {"path": "HOSTSRC/BUILD.JSON", "file_type": 0, "aux_type": 0,
                           "bytes": len(component_bytes), "sha256": hashlib.sha256(component_bytes).hexdigest()}]}
    assert verify(before, after, combined)["added_files"] == 2


def test_auditor_rejects_out_of_volume_pointers():
    image = fixture_image()
    struct.pack_into("<H", image, 1028 + 39 + 17, 65)
    with pytest.raises(ValueError, match="outside volume"):
        inventory(image)
