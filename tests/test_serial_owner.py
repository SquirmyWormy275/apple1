from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.serial_owner import (
    DeviceIdentityError,
    SerialOwner,
    TargetIdentity,
    TargetLockedError,
)


class FakeTransport:
    def __init__(self) -> None:
        self.opened = False
        self.closed = False
        self.settings: dict[str, object] = {}
        self.writes: list[bytes] = []
        self.in_waiting = 0

    def configure(self, **settings: object) -> None:
        self.settings = settings

    def open(self) -> None:
        self.opened = True

    def close(self) -> None:
        self.closed = True

    def read(self, size: int) -> bytes:
        return b""

    def write(self, payload: bytes) -> int:
        self.writes.append(payload)
        return len(payload)


def identity(tmp_path: Path) -> TargetIdentity:
    device = tmp_path / "ttyUSB0"
    device.touch()
    # On the Pi these are distinct udev symlinks.  Regular paths exercise the
    # same resolved-identity contract without Windows symlink privileges.
    return TargetIdentity(by_id=device, by_path=device)


def test_open_configures_8n1_without_flow_control(tmp_path: Path) -> None:
    transport = FakeTransport()
    owner = SerialOwner(identity(tmp_path), tmp_path / "owner.lock", transport)

    owner.acquire_and_open()

    assert transport.opened is True
    assert transport.settings == {
        "baudrate": 9600,
        "bytesize": 8,
        "parity": "N",
        "stopbits": 1,
        "xonxoff": False,
        "rtscts": False,
        "dsrdtr": False,
        "dtr": False,
        "rts": False,
    }
    owner.close()


def test_second_owner_cannot_acquire_same_target(tmp_path: Path) -> None:
    target = identity(tmp_path)
    first = SerialOwner(target, tmp_path / "owner.lock", FakeTransport())
    second = SerialOwner(target, tmp_path / "owner.lock", FakeTransport())

    first.acquire()
    with pytest.raises(TargetLockedError):
        second.acquire()
    first.close()


def test_reconnect_quarantines_transmit_until_reidentified(tmp_path: Path) -> None:
    target = identity(tmp_path)
    transport = FakeTransport()
    owner = SerialOwner(target, tmp_path / "owner.lock", transport)
    owner.acquire_and_open()

    owner.handle_reconnect()
    with pytest.raises(DeviceIdentityError):
        owner.transmit(b"TEST\r")

    owner.reidentify()
    owner.transmit(b"TEST\r")

    assert transport.writes == [b"TEST\r"]
    owner.close()


def test_capture_records_identity_control_policy_and_raw_bytes(tmp_path: Path) -> None:
    target = identity(tmp_path)
    capture_path = tmp_path / "capture.jsonl"
    owner = SerialOwner(target, tmp_path / "owner.lock", FakeTransport(), capture_path)
    owner.acquire_and_open()
    owner.transmit(b"T")
    owner.close()

    records = [json.loads(line) for line in capture_path.read_text().splitlines()]
    assert records[0]["event"] == "opened"
    assert records[0]["identity"]["by_id"] == str(target.by_id)
    assert records[0]["control_policy"] == {"dtr": False, "rts": False}
    assert records[1]["event"] == "transmit"
    assert records[1]["payload_hex"] == "54"


def test_mismatched_identity_paths_fail_closed(tmp_path: Path) -> None:
    first = tmp_path / "ttyUSB0"
    second = tmp_path / "ttyUSB1"
    first.touch()
    second.touch()
    with pytest.raises(DeviceIdentityError):
        TargetIdentity(by_id=first, by_path=second).validate()
