"""Exact candidate boundaries hold during actual model turns, before evaluation."""
import json

import pytest

from neural1.campaign import CampaignEngine, CampaignSpec
from neural1.drivers import parse_commands
from neural1.models import FakeProvider
from neural1.registry import ModelRegistry, RegisteredModel
from neural1.world import VirtualApple1World, WozMonSession


@pytest.mark.parametrize("command", ["0300: 41", "02FF: 41 42", "0300", "02FF.0300", "0300R", "0100", "FFEF", "FFEFR"])
def test_monitor_rejects_outside_candidate(command):
    world = VirtualApple1World()
    world.host_write(0x300, b"Q")
    session = WozMonSession(world, candidate_limit=256)
    assert session.transact(command).startswith("ERR")
    assert world.host_read(0x300) == b"Q"
    assert WozMonSession(world).transact("0300") == "0300: 51"


def test_exact_candidate_valid_program_and_alternate_entrypoint_escape():
    world = VirtualApple1World()
    session = WozMonSession(world, candidate_limit=256)
    session.transact("0200: A9 41 20 EF FF 4C 1F FF")
    assert session.transact("0200R") == "0200: STOP=MONITOR_WARM_ENTRY STEPS=4 OUTPUT='A'"
    session.transact("0280: AD 00 03 00")
    assert session.transact("0280R") == "ERR EXACT CANDIDATE MEMORY POLICY"


def test_model_escape_turn_has_error_feedback_and_fails_family(tmp_path):
    registry = ModelRegistry()
    registry.add(RegisteredModel("test", "fixture", "test", "fake", "fake", "0", "NONE", 4096, "fixture", "TEST-ONLY", {}))
    # This model-authored candidate attempts to load external data as output.
    image = bytes.fromhex("AD 00 03 20 EF FF 4C 1F FF") + bytes(247)
    response = "\n".join(f"{0x200+i:04X}: " + image[i:i+16].hex(' ').upper() for i in range(0, 256, 16)) + "\n0200R"
    engine = CampaignEngine(tmp_path, registry, {"test": FakeProvider(default=response)})
    spec = CampaignSpec.create(experiments=["256-byte-universe"], model_ids=["test"], seeds=[1], generations=2, agents_per_cell=1, ram_budget=4096, max_tokens=32, generation_settings={}, matched_control="SYNTHETIC escape regression", wall_clock_limit_seconds=60)
    engine.run(spec, objective_factory=lambda cell, generation: "monitor only", command_parser=parse_commands)
    records = [json.loads(line) for line in next(tmp_path.rglob("transcript.jsonl")).read_text().splitlines()]
    assert records[0]["outputs"][-1] == "ERR EXACT CANDIDATE MEMORY POLICY"
    assert records[0]["accepted_commands"] == 16
    assert "ERR EXACT CANDIDATE MEMORY POLICY" in records[1]["prompt"]
    family = json.loads(next(tmp_path.rglob("family-result.json")).read_text())
    assert not family["passed"]
    assert family["independent_execution"]["stop_reason"] == "EXECUTION_MEMORY_POLICY"
