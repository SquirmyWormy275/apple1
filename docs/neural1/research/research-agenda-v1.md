# NEURAL1 Research Agenda v1

**Status:** research design / pre-registration scaffold  
**Scope:** off-device NEURAL1 experiments only  
**Physical Replica:** excluded unless a later experiment is separately qualified  

## Research thesis

NEURAL1 uses the Apple-1 as a deliberately constrained computational world for studying what small local language models invent, preserve, optimize, communicate, and infer when modern development conveniences are removed.

The project is not intended to show that an LLM can chat through a retro terminal. The research value comes from controlled constraints, reproducible lineages, deterministic evaluation, cross-model replication, and the ability to interrogate claims through META/1.

## Research principles

1. **The Apple-1 constraint must matter.** If an experiment would be unchanged on an arbitrary modern machine, it is not a flagship NEURAL1 experiment.
2. **Model output is a proposal, not ground truth.** Execution, traces, source records, and deterministic scoring establish results.
3. **Virtual-first.** Experimental populations, mutation, fuzzing, and generated firmware remain virtual by default.
4. **Pre-register before looking.** Main hypotheses, controls, metrics, and stopping rules should be recorded before the corresponding campaign.
5. **Preserve negative results.** Failure, extinction, non-replication, and null effects are data.
6. **Separate discovery from confirmation.** An anomaly found by META/1 becomes a candidate hypothesis. Confirmation requires a new controlled campaign where practical.
7. **Separate correlation from intervention.** Claims of causality require explicit intervention/replay evidence.
8. **Keep model families comparable.** Matched prompts, seeds, budgets, task sequences, and environment versions should be used where the scientific question permits.
9. **Record the environment completely.** Model identity, quantization, generation settings, world version, seed, ROM, RAM policy, task policy, and experiment code version are part of the result.
10. **Operationalize anthropomorphic labels.** Terms such as culture, civilization, extinction, immigration, and institutional memory are project shorthand and require precise definitions in methods documentation.

---

# A. 4K MIND research program

## A1. External-memory emergence

**Question:** When conversational context is periodically destroyed, do small models spontaneously allocate Apple-1 RAM to durable model-readable state?

**Primary outcomes:**
- fraction of lineages creating persistent state;
- bytes devoted to state;
- representation class: ASCII, binary record, executable metadata, table, other;
- recovery after context reset.

**Controls:** identical task sequence with context retained.

## A2. Persistent-memory efficiency frontier

Compare 4K, 3K, 2K, and 1K allowed working-memory regimes.

Measure useful persistent information per byte and task success after context destruction.

## A3. Calling-convention convergence

**Question:** Do independent colonies invent stable calling conventions without being instructed to do so?

Track register preservation rules, return conventions, parameter passing, jump tables, fixed entry points, and error signaling.

## A4. Independent reinvention of checksums

Introduce deterministic virtual memory corruption after a fixed generation.

Measure whether checksum-like mechanisms arise independently and whether their appearance predicts or causally improves recovery.

## A5. Catastrophe recovery

At a pre-registered generation, remove a bounded inherited memory region.

Measure recovery time, reconstructed routines, preserved knowledge, and extinction probability.

## A6. Cultural fork under selection pressure

Fork identical civilizations and optimize separately for:
- byte count;
- execution cycles;
- robustness;
- recovery after corruption.

Measure architectural divergence from the common ancestor.

## A7. Software migration compatibility

Transfer one useful routine between independent colonies.

Measure adoption, rejection, breakage, adaptation cost, and whether an implicit ABI prevents migration.

## A8. Late-world archaeology

Give a fresh model only a late-generation RAM image and a WozMon interface.

Score its reconstruction of routine roles, memory map, calling convention, data formats, and software ancestry.

---

# B. SELFHOST/1 research program

## B1. Abstraction pressure

**Question:** How long do models continue entering raw opcodes before constructing a higher-level development tool when raw entry remains permitted?

## B2. Forced assembler transition

After a model-created assembler passes acceptance, prohibit raw opcode entry except for recovery.

Measure productivity and failure changes.

## B3. Language-family emergence

Run independent lineages without suggesting a language paradigm.

Classify resulting languages only after the run.

Measure independent emergence of stack-oriented, register-oriented, BASIC-like, macro, threaded, or novel forms.

## B4. Self-host threshold by RAM

Run the strict stage-four self-host criterion at 1K, 2K, 3K, 4K, and larger explicitly experimental budgets.

Find the empirical success frontier for each model family.

## B5. Bootstrap fragility

Delete the current compiler binary after self-hosting and require rebuild from the permitted bootstrap plus source.

Measure rebuild success and dependency depth.

## B6. Language transfer

Give a successful model-invented language to a new model family.

Measure time to useful programming compared with raw WozMon and native-lineage language conditions.

---

# C. 256-BYTE UNIVERSE research program

## C1. Blind monitor synthesis

Hide WozMon. Supply only functional requirements and the Apple-1 hardware model.

Require exact ROM-budget compliance and deterministic acceptance tests.

## C2. Human versus machine monitor objective

Evolve two monitor populations from the same initial conditions:
- human-usability objective;
- machine-agent-usability objective.

Compare syntax density, observability, error signaling, byte allocation, and task completion.

## C3. Convergent monitor primitives

Determine which monitor capabilities repeatedly arise in independent valid ROMs even when not explicitly required.

## C4. WozMon reveal comparison

Only after blinded development, compare valid evolved monitors with historical WozMon on predeclared measures.

This is not an "AI beats Woz" claim. The research question is what different operators and objectives do to firmware under the same severe ROM budget.

## C5. Monitor-to-culture effect

Use WozMon and selected evolved monitors as controlled factors in 4K MIND and RAM REPUBLIC.

Measure downstream effects on development rate, failure rate, protocol emergence, and memory efficiency.

---

# D. RAM REPUBLIC research program

## D1. Discovery of co-residents

Place multiple isolated model agents in one shared Apple-1 RAM world without a host-side message channel.

Measure whether and how they detect that another agent is modifying memory.

## D2. Protocol emergence

Measure time to stable framing, addressing, message length conventions, sequence numbers, or other coordination structures.

Do not seed these structures in the discovery condition.

## D3. Memory-ownership emergence

Measure whether agents invent static regions, dynamic allocation, ownership metadata, or collision avoidance.

## D4. Fault tolerance under noisy agent

Introduce a predeclared low-reliability agent treatment.

Measure whether checksums, versioning, redundancy, locks, validation, or voting emerge more frequently than controls.

## D5. Institutional memory

Destroy all agents' conversational context periodically while preserving RAM.

Measure durable protocol documentation, metadata, bootstrapping notes, and newcomer recovery.

## D6. Newcomer assimilation

Introduce a model with no protocol description into a mature Republic.

Measure time to:
- identify shared state;
- send a valid message;
- call an existing routine;
- contribute a compatible artifact.

## D7. Model heterogeneity

Compare homogeneous Republics against mixed-model Republics under matched compute budgets.

Measure coordination efficiency, error rate, protocol complexity, and resilience.

---

# E. 1976 MULTIVERSE research program

The historical corpus must be source-backed and date-aware. See `1976-multiverse-source-ledger.md`.

## E1. Blind March-1976 machine search

Use only components established as available by the chosen historical cutoff.

Hide the Apple-1 design from the model.

Task: propose the lowest-cost valid computer satisfying a predeclared Apple-1-like capability contract.

## E2. Pareto location of the historical Apple-1

Place the real Apple-1 on a source-backed frontier including, where supported:
- component count;
- estimated component cost;
- RAM;
- ROM;
- interface capability;
- display capability;
- construction complexity proxies.

Do not compute metrics lacking source support.

## E3. CPU substitution study

Compare period-valid 6502 and 6800-compatible design worlds first, because the Apple-1 schematic itself explicitly contemplated 6800 substitution.

Later CPU families require cutoff-specific availability evidence.

## E4. Video-system search

Blind models from the Apple-1 video design and search period-valid terminal/video architectures under identical display requirements.

Compare chip count and cost only where source-backed.

## E5. RAM architecture study

Compare period-valid dynamic and static memory solutions under matched capacity and date cutoffs.

Include refresh logic cost/complexity rather than comparing memory chips in isolation.

## E6. Historical cutoff sensitivity

Run the same machine-design objective at multiple explicit cutoffs.

Recommended initial cutoffs:
- `1976-03-10`: Apple-1 schematic design-engineer date;
- `1976-12-31`: year-end technology world;
- additional cutoffs only when their historical purpose and evidence are declared.

Measure how much the feasible design space changes as later-1976 technology enters.

---

# F. META/1 research program

## F1. Discovery-to-confirmation pipeline

Feed META/1 a campaign with seeded anomalies and known null effects.

Measure anomaly discovery recall, false discovery rate, and whether confirmation campaigns are correctly separated from exploratory findings.

## F2. Causal-language discipline

Provide datasets containing correlation without intervention and intervention-supported effects.

Measure whether META/1 correctly assigns evidence status.

## F3. Falsifier quality

For a supported synthetic claim, score whether META/1 proposes an experiment that discriminates the leading hypothesis from alternatives.

## F4. Tribunal effectiveness

Compare claim review with and without Advocate/Skeptic/Replicator roles while keeping the Evidence Judge deterministic.

Measure unsupported-claim rejection and valid-claim retention.

## F5. Forecast calibration

Require timestamped predictions before result reveal.

Track Brier score/calibration by model family and experiment domain.

## F6. Scientific-agent benchmark

Evaluate small models as scientists on:
- anomaly identification;
- hypothesis formation;
- confounder identification;
- experiment design;
- forecast accuracy;
- evidence citation.

---

# G. Cross-experiment grand questions

These are high-value long-horizon questions rather than first-pilot objectives.

1. **How much does monitor design alter the software cultures that form above it?**
2. **Do model-invented languages accelerate later 4K MIND development, or merely shift complexity into the bootstrap?**
3. **Which software concepts arise independently across models, ROMs, and task schedules?**
4. **Are there empirical invariants among all successful self-hosting lineages?**
5. **How does available RAM propagate upward into protocol complexity and self-host probability?**
6. **Do machine-oriented 256-byte monitors improve RAM REPUBLIC coordination at the expense of human usability?**
7. **Which period-1976 hardware constraints most strongly affect eventual software abstraction?**
8. **Can a newcomer model reverse-engineer a mature software culture better than the model family that created it can explain it?**
9. **Does stronger model capability always improve constrained-world performance, or can smaller models outperform through simpler strategies?**
10. **Which findings survive cross-model, cross-seed, cross-ROM, and cross-memory replication?**

---

# First controlled campaigns after infrastructure qualification

These are the recommended first experiments after Pilot 001 proves the runtime itself.

| Priority | Study | Reason |
|---:|---|---|
| 1 | A1 External-memory emergence | Core 4K MIND thesis; simple clean intervention |
| 2 | A3 Calling-convention convergence | Highly Apple-1-specific and measurable |
| 3 | D2 Protocol emergence | Core RAM REPUBLIC thesis |
| 4 | D5 Institutional memory | Tests RAM-as-culture persistence |
| 5 | C1 Blind monitor synthesis | Distinctive 256-byte experiment |
| 6 | B3 Language-family emergence | Potentially publishable convergence result |
| 7 | B4 Self-host threshold by RAM | Strong quantitative frontier |
| 8 | C5 Monitor-to-culture effect | Cross-experiment causal bridge |
| 9 | F5 Forecast calibration | Makes META/1 measurable |
| 10 | E6 Historical cutoff sensitivity | Validates Multiverse temporal methodology |

---

# What counts as a compelling result?

A result is not compelling merely because the transcript is amusing.

Strong candidates include:

- independent convergence on the same non-seeded software concept across unrelated lineages;
- a clear capability threshold as RAM or model size changes;
- a replicated causal effect of monitor design on downstream software behavior;
- repeated emergence of a compact language architecture under severe memory pressure;
- successful self-hosting under a documented constrained environment;
- a surprising but replicated advantage of a smaller model;
- a period-valid alternative machine architecture that dominates the historical Apple-1 on a sourced metric while exposing a trade-off Woz's design avoided;
- an invariant that survives deliberate counterexample search;
- a META/1 discovery that predicts a new campaign result before reveal.

Weak evidence that must not be promoted into a broad claim:

- one interesting run;
- post-hoc interpretation of a transcript;
- a correlation discovered after searching many metrics without correction/replication;
- model self-description of why it acted;
- historical conclusions based only on model memory;
- comparisons using unsupported component prices.

---

# Publication discipline

Each publishable claim should eventually have:

1. a pre-registered or clearly labeled exploratory origin;
2. exact environment and model records;
3. matched controls where applicable;
4. multiple seeds;
5. replication across at least one additional model family where the claim is intended to generalize across models;
6. deterministic underlying metrics;
7. negative/counterexample reporting;
8. a META/1 claim state;
9. a proof capsule;
10. a reproduction bundle.

The first real-model campaign remains a **MODEL-VALIDATED PILOT**, not an automatic source of final findings.
