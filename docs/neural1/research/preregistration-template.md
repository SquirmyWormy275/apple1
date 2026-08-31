# NEURAL1 Experiment Pre-Registration Template

Use this before launching a confirmatory NEURAL1 campaign. Exploratory runs may use a lighter record, but any claim intended for publication should state whether it originated from pre-registered or exploratory work.

---

# Experiment identity

**Experiment ID:** `UNASSIGNED`  
**Experiment family:** `4K MIND / SELFHOST1 / 256-BYTE / RAM REPUBLIC / 1976 MULTIVERSE / META1 / CROSS-EXPERIMENT`  
**Registration timestamp:** `UNFILLED`  
**Repository commit:** `UNFILLED`  
**Runtime/schema version:** `UNFILLED`  
**Research status:** `CONFIRMATORY / EXPLORATORY / REPLICATION / FALSIFICATION`  

# Research question

State one primary question in falsifiable form.

`UNFILLED`

# Motivation

Why is this question specifically interesting under Apple-1 constraints?

`UNFILLED`

# Primary hypothesis

`UNFILLED`

# Null / competing hypotheses

1. `UNFILLED`
2. `UNFILLED`

# Evidence that would change our mind

State what result would weaken or falsify the primary hypothesis.

`UNFILLED`

# Experimental world

**ROM / monitor:** `UNFILLED`  
**RAM budget:** `UNFILLED`  
**Apple-1 world version:** `UNFILLED`  
**Allowed agent interface:** `UNFILLED`  
**Context-reset policy:** `UNFILLED`  
**Inheritance policy:** `UNFILLED`  
**Physical target:** `VIRTUAL`  

# Models

For each model record:

- exact model name;
- provider/backend;
- model digest/hash if available;
- quantization;
- context limit;
- generation parameters;
- maximum token budget;
- model-specific prompt differences, if any.

`UNFILLED`

# Factors and treatments

| Factor | Levels | Purpose |
|---|---|---|
| `UNFILLED` | `UNFILLED` | `UNFILLED` |

# Controlled variables

List values intentionally held constant.

- `UNFILLED`

# Seeds

**Seed-generation rule:** `UNFILLED`  
**Predeclared seeds:** `UNFILLED`  

Do not silently drop failed seeds. Record incomplete/failed cells.

# Sample size / stopping rule

**Planned cells:** `UNFILLED`  
**Runs per cell:** `UNFILLED`  
**Maximum generations:** `UNFILLED`  
**Maximum wall-clock time:** `UNFILLED`  
**Early-stop rule:** `UNFILLED`  

If formal power analysis is not meaningful for the metric, state that rather than inventing one.

# Primary outcome

Define exactly one primary metric where practical.

**Metric:** `UNFILLED`  
**Operational definition:** `UNFILLED`  

# Secondary outcomes

1. `UNFILLED`
2. `UNFILLED`

# Failure / extinction definition

Define failure before execution.

`UNFILLED`

# Intervention definition

For causal experiments, define the intervention precisely.

`UNFILLED / NOT APPLICABLE`

# Blinding

State whether any of the following are hidden from analytical agents until after analysis:

- model identity;
- treatment identity;
- final outcome;
- fitness;
- historical reference design.

`UNFILLED`

# Historical-source policy

Required for 1976 MULTIVERSE.

**Historical cutoff:** `UNFILLED`  
**Allowed source classes:** `UNFILLED`  
**Price evidence classes:** `UNFILLED`  
**Known unavailable fields:** `UNFILLED`  

No model-memory fact becomes historical ground truth.

# Planned analysis

Define before viewing outcomes:

- aggregation;
- effect measurement;
- uncertainty reporting;
- multiple-comparison handling if needed;
- convergence classifier/version;
- missing-run treatment;
- failure treatment.

`UNFILLED`

# META/1 claim rules

What result is sufficient for:

**OBSERVED:** `UNFILLED`  
**CORRELATED:** `UNFILLED`  
**REPLICATED:** `UNFILLED`  
**INTERVENTION SUPPORTED:** `UNFILLED`  

Do not allow the narrative layer to upgrade the evidence state.

# Counterexamples

All qualifying counterexamples must be retained and surfaced in the final report.

# Negative-result policy

Null or failed results will be recorded in:

`docs/neural1/research/negative-results.md` or the campaign's corresponding negative-results artifact.

# Reproducibility requirements

The run is not complete until the retained bundle identifies:

- repository/runtime commit;
- experiment manifest;
- model record;
- seeds;
- prompts/policies;
- snapshots required for replay;
- artifacts and hashes;
- analysis version;
- proof capsule where a claim is generated.

# Deviations

After execution, record every deviation from this registration. Do not silently edit the pre-registration to match what was actually run.

`NONE YET`
