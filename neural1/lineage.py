"""Explicit artifact, routine, language, and concept ancestry."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import asdict, dataclass

from .core import Neural1Error, stable_id


@dataclass(frozen=True)
class LineageNode:
    node_id: str
    kind: str
    artifact_hash: str
    parents: tuple[str, ...] = ()
    mutation: str | None = None


class LineageGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, LineageNode] = {}

    def add(self, kind: str, artifact_hash: str, *, parents: Iterable[str] = (), mutation: str | None = None) -> LineageNode:
        parent_ids = tuple(sorted(parents))
        missing = set(parent_ids) - self.nodes.keys()
        if missing:
            raise Neural1Error(f"unknown lineage parents: {sorted(missing)}")
        data = {"kind": kind, "artifact_hash": artifact_hash, "parents": parent_ids, "mutation": mutation}
        node = LineageNode(stable_id("LIN", data), kind, artifact_hash, parent_ids, mutation)
        self.nodes.setdefault(node.node_id, node)
        return node

    def ancestors(self, node_id: str) -> set[str]:
        if node_id not in self.nodes:
            raise Neural1Error("unknown lineage node")
        found: set[str] = set()
        pending = list(self.nodes[node_id].parents)
        while pending:
            item = pending.pop()
            if item not in found:
                found.add(item)
                pending.extend(self.nodes[item].parents)
        return found

    def records(self) -> list[dict[str, object]]:
        return [asdict(self.nodes[key]) for key in sorted(self.nodes)]
