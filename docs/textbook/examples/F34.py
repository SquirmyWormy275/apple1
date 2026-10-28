from neural1.meta import ClaimGraph, compile_experiment, falsification_plan, proof_capsule

g = ClaimGraph()
claim = g.create_claim("FIXTURE EFFECT", {"experiment": "synthetic"})
evidence = g.add_evidence("fixture", "a" * 64, ["FIXTURE"], "authored evidence")
g.relate(evidence.evidence_id, "supports", claim.claim_id)
capsule = proof_capsule(
    claim, g, dataset_hash="b" * 64, analysis_version="textbook", reproduction_command="python -m tools.textbook run F34"
)
plan = falsification_plan(claim, factor="X", control="0", treatment="1", metric="Y", seeds=[1], sample_count=2)
compiled = compile_experiment(
    "DOES X CHANGE Y?",
    factor="X",
    levels=["A", "B"],
    controls={"model": "fixed"},
    metrics=["Y"],
    seeds=[1, 2],
    analysis="paired",
    stopping_rule="N=2",
)
print("Capsule run IDs:", capsule["run_ids"])
print("Compute estimate:", plan["estimated_compute_cost"])
print("Compiled target:", compiled.target)
assert capsule["run_ids"] == ["FIXTURE"] and compiled.target == "VIRTUAL"
