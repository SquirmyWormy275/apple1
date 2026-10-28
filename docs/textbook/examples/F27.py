from neural1.policies import CandidateMetrics, SelectionPolicy, convergence, memory_conflicts, mutate_rom

one, record = mutate_rom(bytes(256), seed=7, mutation_count=3)
two, other = mutate_rom(bytes(256), seed=7, mutation_count=3)
assert one == two and record == other
print("Changed bytes:", sum(a != b for a, b in zip(bytes(256), one, strict=True)))
candidates = [CandidateMetrics("A", 0.5, 1, 10, 20, 1), CandidateMetrics("B", 1, 0.5, 20, 10, 0.5)]
print("Correctness-only selection:", SelectionPolicy().select(candidates, 1)[0].candidate_id)
print("Common fixture artifact:", convergence({"A": ["HASH"], "B": ["HASH"]})["converged"])
print("Conflicting address:", hex(memory_conflicts([("A", 0x400, b"AB"), ("B", 0x401, b"C")])[0].address))
