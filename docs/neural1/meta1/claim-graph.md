# META/1 claim graph

Claims carry statement, scope, review status, causal status, effect size,
uncertainty, counterexamples, falsifier, and revision history. Evidence carries
kind, artifact hash, runs, summary, and causal level. Typed edges are `supports`,
`opposes`, `limits`, `derived_from`, `replicates`, `contradicts`, and
`depends_on`. Explanations must traverse these records. If support is absent,
META returns `INSUFFICIENT EVIDENCE` and may propose an experiment.
