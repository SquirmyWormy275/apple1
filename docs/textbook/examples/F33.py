from neural1.analysis import break_invariant, detect_phase_changes, mine_invariants

records = [{"successful": True, "checksum": True, "model": "A"}, {"successful": True, "checksum": True, "model": "B"}]
candidate = next(c for c in mine_invariants(records) if c.feature == "checksum")
print("Observed support fraction:", candidate.support_fraction)
counterexamples = break_invariant(candidate, [{"successful": True, "checksum": False}])
print("Successful counterexamples:", len(counterexamples))
print("Detected change candidates:", len(detect_phase_changes([0, 0.1, 2.0], threshold=1)))
assert len(counterexamples) == 1
