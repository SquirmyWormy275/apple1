"""Content-addressed artifacts and append-only run evidence."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
import json
import os
from pathlib import Path
from typing import Any, Iterator

from .core import canonical_json, sha256_bytes


@dataclass(frozen=True)
class ArtifactRecord:
    sha256: str
    size: int
    media_type: str
    retention: str
    path: str


class ArtifactStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def put(self, payload: bytes, *, media_type: str, retention: str = "canonical") -> ArtifactRecord:
        if retention not in {"canonical", "derived", "cache", "discardable"}:
            raise ValueError("invalid retention tier")
        digest = sha256_bytes(payload)
        destination = self.root / "sha256" / digest[:2] / digest
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            temporary = destination.with_suffix(".tmp")
            temporary.write_bytes(payload)
            os.replace(temporary, destination)
        return ArtifactRecord(digest, len(payload), media_type, retention, str(destination))

    def put_json(self, value: Any, *, retention: str = "canonical") -> ArtifactRecord:
        return self.put(canonical_json(value).encode("ascii"), media_type="application/json", retention=retention)


class EventLog:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def append(self, event_type: str, payload: Any) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {"recorded_at": datetime.now(UTC).isoformat(), "type": event_type, "payload": payload}
        with self.path.open("a", encoding="ascii") as stream:
            stream.write(canonical_json(record) + "\n")

    def records(self) -> Iterator[dict[str, Any]]:
        if not self.path.exists():
            return
        with self.path.open(encoding="ascii") as stream:
            for line in stream:
                yield json.loads(line)
