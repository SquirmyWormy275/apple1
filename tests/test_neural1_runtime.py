from __future__ import annotations

import pytest

from neural1.core import Neural1Error
from neural1.lineage import LineageGraph
from neural1.models import FakeProvider
from neural1.physical import PhysicalQualificationAdapter
from neural1.runtime import ExperimentRuntime, RunManifest
from neural1.world import VirtualApple1World, WozMonSession


def test_run_identity_and_replay_are_stable() -> None:
    provider = FakeProvider(default="OK")
    one = RunManifest.create("4k-mind", 7, provider.record, {"ram_budget": 4096})
    two = RunManifest.create("4k-mind", 7, provider.record, {"ram_budget": 4096})
    assert one.run_id == two.run_id


def test_wozmon_is_the_only_agent_surface_and_enforces_budget() -> None:
    session = WozMonSession(VirtualApple1World(ram_budget=1024))
    assert session.transact("0200: A9 41 60") == "0200: A9 41 60"
    assert session.transact("0200.0202") == "0200: A9 41 60"
    assert session.transact("0600") == "ERR RANGE OR SYNTAX"


def test_wozmon_executes_deposited_6502_with_a_hard_bound() -> None:
    world = VirtualApple1World(ram_budget=1024)
    session = WozMonSession(world, max_instructions=20)
    # LDA #$2A; STA $0300; BRK
    assert session.transact("0200: A9 2A 8D 00 03 00") == "0200: A9 2A 8D 00 03 00"
    assert session.transact("0200R") == "0200: STOP=BRK STEPS=2"
    assert session.transact("0300") == "0300: 2A"


def test_execution_trace_is_verifier_evidence_not_agent_memory_api() -> None:
    world = VirtualApple1World()
    world.host_write(0x0200, bytes.fromhex("A9 41 20 EF FF 4C 1F FF"))
    result = world.execute(0x0200)
    assert result.stop_reason == "MONITOR_WARM_ENTRY"
    assert result.screen_text == "A"
    assert [entry.pc for entry in result.trace[:2]] == [0x0200, 0x0202]


def test_snapshot_restore_and_counterfactual_metadata(tmp_path) -> None:
    provider = FakeProvider()
    base = RunManifest.create("4k-mind", 9, provider.record, {"pressure": "bytes"})
    runtime = ExperimentRuntime(tmp_path)
    world = VirtualApple1World()
    WozMonSession(world).transact("0200: 01 02 03")
    artifact = runtime.snapshot(world)
    assert runtime.restore(artifact).host_read(0x0200, 3) == b"\x01\x02\x03"
    fork = runtime.fork(base, fork_point="GEN 12", changed_factor="REMOVE CHK-1", config={"pressure": "robustness"})
    assert fork.parent_run_id == base.run_id
    assert fork.fork_point == "GEN 12"


def test_lineage_requires_known_parents() -> None:
    graph = LineageGraph()
    root = graph.add("routine", "a" * 64)
    child = graph.add("routine", "b" * 64, parents=(root.node_id,), mutation="one byte")
    assert graph.ancestors(child.node_id) == {root.node_id}
    with pytest.raises(Neural1Error):
        graph.add("routine", "c" * 64, parents=("UNKNOWN",))


def test_physical_adapter_is_disabled_by_default() -> None:
    adapter = PhysicalQualificationAdapter()
    assert adapter.available is False
    with pytest.raises(Neural1Error, match="disabled"):
        adapter.launch("anything")
