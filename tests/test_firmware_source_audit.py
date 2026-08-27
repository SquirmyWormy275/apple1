"""Provenance checks for the immutable Replica 1 Plus firmware candidate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VENDOR_DIR = REPO_ROOT / "firmware" / "vendor" / "110REV03"
MANIFEST_PATH = VENDOR_DIR / "provenance.json"


def test_vendor_candidate_has_complete_hash_verified_provenance() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["status"] == "candidate-not-eeprom-readback"
    assert manifest["source_url"].startswith("https://")
    assert manifest["retrieved_on"]

    expected_files = {
        "replica 110REV03.spin",
        "Serial_IO.spin",
        "FullDuplex.spin",
        "Keyboard.spin",
        "AiGeneric_Driver.spin",
        "AiGeneric_Driver_002.spin",
        "AiGeneric_Driver_TV.spin",
        "Font_Atari.spin",
        "_README_.txt",
    }
    assert set(manifest["files"]) == expected_files

    for filename, expected_hash in manifest["files"].items():
        content = (VENDOR_DIR / filename).read_bytes()
        assert hashlib.sha256(content).hexdigest().upper() == expected_hash


def test_manifest_records_the_candidate_pin_and_serial_assumptions() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    assert manifest["observed_candidate_properties"] == {
        "rx_pin": 31,
        "tx_pin": 30,
        "clear_pin": 9,
        "clock_pin": 15,
        "serial_baud": 9600,
        "serial_strobe_ms": 7,
        "serial_input_filter": "serdata < 96",
        "receive_ring_bytes": 16,
    }
