"""Exclusive, evidence-first owner for the Replica 1 Plus FT232R device.

`probe` never opens the serial port.  A future `session` invocation is the
only path that may open it, and it starts with DTR and RTS requested low.
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Protocol


DEFAULT_BY_ID = Path("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_00000000-if00-port0")
DEFAULT_BY_PATH = Path("/dev/serial/by-path/platform-xhci-hcd.0-usbv2-0:2:1.0-port0")


class DeviceIdentityError(RuntimeError):
    """The recorded USB identities do not resolve to the same device."""


class TargetLockedError(RuntimeError):
    """Another serial-owner process holds the target lock."""


class SerialTransport(Protocol):
    def configure(self, **settings: object) -> None: ...

    def open(self) -> None: ...

    def close(self) -> None: ...

    def read_available(self) -> bytes: ...

    def write(self, payload: bytes) -> int: ...


@dataclass(frozen=True)
class TargetIdentity:
    by_id: Path
    by_path: Path

    def validate(self) -> Path:
        try:
            by_id_device = self.by_id.resolve(strict=True)
            by_path_device = self.by_path.resolve(strict=True)
        except FileNotFoundError as error:
            raise DeviceIdentityError(f"missing recorded target identity: {error.filename}") from error
        if by_id_device != by_path_device:
            raise DeviceIdentityError(
                f"identity mismatch: {self.by_id} -> {by_id_device}; "
                f"{self.by_path} -> {by_path_device}"
            )
        return by_id_device

    def as_record(self) -> dict[str, str]:
        return {"by_id": str(self.by_id), "by_path": str(self.by_path), "device": str(self.validate())}


class ExclusiveLock:
    """A fail-closed lock; stale locks require an explicit operator decision."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.held = False

    def acquire(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError as error:
            raise TargetLockedError(
                f"owner lock exists at {self.path}; inspect its PID before removing it"
            ) from error
        with os.fdopen(descriptor, "w", encoding="utf-8") as lock_file:
            lock_file.write(f"pid={os.getpid()}\n")
        self.held = True

    def release(self) -> None:
        if self.held:
            self.path.unlink(missing_ok=True)
            self.held = False


class PySerialTransport:
    """Lazy pyserial wrapper so probe and tests never need to import pyserial."""

    def __init__(self, device: Path) -> None:
        self.device = device
        self._serial: object | None = None

    def configure(self, **settings: object) -> None:
        try:
            import serial
        except ImportError as error:  # pragma: no cover - exercised on the Pi
            raise RuntimeError("pyserial is required for an opened serial session") from error
        serial_settings = {key: value for key, value in settings.items() if key not in {"dtr", "rts"}}
        self._serial = serial.Serial(port=None, timeout=0.2, **serial_settings)
        self._serial.dtr = bool(settings["dtr"])
        self._serial.rts = bool(settings["rts"])

    def open(self) -> None:
        if self._serial is None:
            raise RuntimeError("transport must be configured before it is opened")
        self._serial.port = str(self.device)

    def close(self) -> None:
        if self._serial is not None and self._serial.is_open:
            self._serial.close()

    def read_available(self) -> bytes:
        if self._serial is None:
            raise RuntimeError("transport is not configured")
        return self._serial.read(self._serial.in_waiting)

    def write(self, payload: bytes) -> int:
        if self._serial is None:
            raise RuntimeError("transport is not configured")
        return self._serial.write(payload)


class SerialOwner:
    SETTINGS = {
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

    def __init__(
        self,
        target: TargetIdentity,
        lock_path: Path,
        transport: SerialTransport,
        capture_path: Path | None = None,
        settle_seconds: float = 0.2,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.target = target
        self.lock = ExclusiveLock(lock_path)
        self.transport = transport
        self.capture_path = capture_path
        self.settle_seconds = settle_seconds
        self.sleep = sleep
        self.quarantined = False
        self.opened = False

    def acquire(self) -> None:
        self.target.validate()
        self.lock.acquire()

    def acquire_and_open(self) -> None:
        self.acquire()
        try:
            self.transport.configure(**self.SETTINGS)
            self.transport.open()
            self.opened = True
            self._record("opened", control_policy={"dtr": False, "rts": False})
            self.sleep(self.settle_seconds)
            startup_bytes = self.transport.read_available()
            self._record("startup_drained", payload_hex=startup_bytes.hex())
        except Exception:
            self.close()
            raise

    def handle_reconnect(self) -> None:
        self.quarantined = True
        self._record("reconnect_quarantined")

    def reidentify(self) -> None:
        self.target.validate()
        self.quarantined = False
        self._record("reidentified")

    def transmit(self, payload: bytes) -> None:
        if not self.opened:
            raise DeviceIdentityError("target is not open through the serial owner")
        if self.quarantined:
            raise DeviceIdentityError("target is quarantined; re-identification is required before transmit")
        self.transport.write(payload)
        self._record("transmit", payload_hex=payload.hex())

    def close(self) -> None:
        if self.opened:
            self.transport.close()
            self._record("closed")
            self.opened = False
        self.lock.release()

    def _record(self, event: str, **details: object) -> None:
        if self.capture_path is None:
            return
        self.capture_path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event": event,
            "identity": self.target.as_record(),
            **details,
        }
        with self.capture_path.open("a", encoding="utf-8") as capture_file:
            capture_file.write(json.dumps(record, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("probe", "session"))
    parser.add_argument("--by-id", type=Path, default=DEFAULT_BY_ID)
    parser.add_argument("--by-path", type=Path, default=DEFAULT_BY_PATH)
    parser.add_argument("--lock", type=Path, default=Path("/tmp/apple1-serial-owner.lock"))
    parser.add_argument("--capture", type=Path, default=Path("captures/serial-owner.jsonl"))
    parser.add_argument("--transmit", type=str, help="Explicit text to transmit during a session")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = TargetIdentity(args.by_id, args.by_path)
    if args.command == "probe":
        print(json.dumps(target.as_record(), sort_keys=True))
        return 0

    owner = SerialOwner(target, args.lock, PySerialTransport(target.validate()), args.capture)
    owner.acquire_and_open()
    try:
        if args.transmit is not None:
            owner.transmit(args.transmit.encode("ascii", errors="strict"))
    finally:
        owner.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
