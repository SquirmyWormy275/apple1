from neural1.campaign import CampaignSpec

spec = CampaignSpec.create(
    experiments=["4k-mind", "ram-republic"],
    model_ids=["fixture-a", "fixture-b"],
    seeds=[1, 2, 3],
    generations=2,
    agents_per_cell=2,
    ram_budget=1024,
    max_tokens=32,
    generation_settings={},
    matched_control="declared fixture",
    wall_clock_limit_seconds=20,
)
print("Cells:", len(spec.cells))
print("Maximum planned turns:", len(spec.cells) * spec.generations * spec.agents_per_cell)
print("Output token ceiling per turn:", spec.max_tokens)
assert len(spec.cells) == 12
