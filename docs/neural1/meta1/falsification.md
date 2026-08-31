# Falsification and counterfactual replay

`FALSIFY` emits a structured null hypothesis, factor, control, treatment,
seeds, sample count, primary metric, stopping rule, and compute estimate. Unknown
hardware/model costs are labeled `UNBENCHMARKED`. Counterfactual replay forks
the nearest valid snapshot, preserves base run and seed relationship, and names
one changed factor. The result may oppose, limit, or support a claim.
