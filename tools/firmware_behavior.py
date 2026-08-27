"""Executable contract models for a future, single-writer firmware change.

This is not firmware and does not make claims about the installed EEPROM.  It
exists to make desired producer ordering, overload, and byte-contract behavior
testable before any Plus source is modified or compiled.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque

from tools.apple1_text import TextContractError


class QueueFullStop(RuntimeError):
    """A producer must stop; data may not be silently dropped or reordered."""


def serial_stimulus(text: str) -> bytes:
    """Encode the only currently planned initial monitor stimulus.

    The safe pre-characterization contract is seven-bit, printable uppercase
    ASCII plus carriage return.  It intentionally rejects lower-case and LF
    rather than applying undocumented transformations.
    """
    try:
        payload = text.encode("ascii", errors="strict")
    except UnicodeEncodeError as error:
        raise TextContractError("serial stimulus must be seven-bit ASCII") from error
    if not payload or any(not (byte == 0x0D or 0x20 <= byte <= 0x5F) for byte in payload):
        raise TextContractError("serial stimulus permits uppercase printable ASCII and CR only")
    return payload


@dataclass
class SingleWriterQueue:
    """FIFO model for producers feeding one keyboard-bus service path."""

    capacity: int
    event_limit: int = 256
    _pending: Deque[tuple[str, bytes]] = field(default_factory=deque, init=False)
    events: Deque[dict[str, object]] = field(default_factory=deque, init=False)

    def __post_init__(self) -> None:
        if self.capacity < 1:
            raise ValueError("capacity must be positive")
        if self.event_limit < 1:
            raise ValueError("event_limit must be positive")
        self.events = deque(maxlen=self.event_limit)

    def enqueue(self, producer: str, payload: bytes) -> None:
        if producer not in {"ps2", "serial"}:
            raise ValueError("producer must be ps2 or serial")
        if len(payload) != 1:
            raise ValueError("queue accepts one byte per bus-service event")
        if len(self._pending) >= self.capacity:
            self.events.append({"event": "queue_full_stop", "producer": producer, "depth": len(self._pending)})
            raise QueueFullStop("queue is full; stop capture and re-characterize pacing")
        self._pending.append((producer, payload))
        self.events.append({"event": "enqueued", "producer": producer, "payload_hex": payload.hex()})

    def service_one(self) -> tuple[str, bytes] | None:
        if not self._pending:
            return None
        producer, payload = self._pending.popleft()
        self.events.append({"event": "single_writer_service", "producer": producer, "payload_hex": payload.hex()})
        return producer, payload
