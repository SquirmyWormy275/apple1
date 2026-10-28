from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.campaign import CampaignEngine, CampaignSpec
from neural1.models import FakeProvider
from neural1.registry import ModelRegistry, RegisteredModel

registry = ModelRegistry()
registry.add(RegisteredModel("fake", "fixture", "test", "fake", "fake-v1", "0", "NONE", 512, "fixture", "TEST-ONLY", {}))
spec = CampaignSpec.create(
    experiments=["4k-mind"],
    model_ids=["fake"],
    seeds=[7],
    generations=3,
    agents_per_cell=1,
    ram_budget=1024,
    max_tokens=32,
    generation_settings={},
    matched_control="fixed fixture",
    wall_clock_limit_seconds=20,
)
with TemporaryDirectory() as d:

    class Pausing(FakeProvider):
        def generate(self, prompt, *, agent_id, seed):
            result = super().generate(prompt, agent_id=agent_id, seed=seed)
            engine.cancel(spec.campaign_id)
            return result

    engine = CampaignEngine(d, registry, {"fake": Pausing(default="0200: 2A")})
    first = engine.run(spec, objective_factory=lambda c, g: "DEPOSIT", command_parser=lambda s: [s])
    transcript = next((Path(d) / "campaigns").rglob("transcript.jsonl"))
    prefix = transcript.read_bytes()
    resumed = CampaignEngine(d, registry, {"fake": FakeProvider(default="0200: 2A")}).resume(
        spec, objective_factory=lambda c, g: "DEPOSIT", command_parser=lambda s: [s]
    )
    print("First state:", first.status)
    print("Resumed state:", resumed.status)
    print("Committed prefix preserved:", transcript.read_bytes().startswith(prefix))
    print("Final turns:", len(transcript.read_text().splitlines()))
    assert resumed.status == "COMPLETED" and transcript.read_bytes().startswith(prefix)
    assert len(transcript.read_text().splitlines()) == 3
