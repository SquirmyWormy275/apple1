# NEURAL1: An Apple-1-Constrained Experimental Environment for Studying Small Language Model Software, Language, Protocol, and Computational-Culture Emergence

**Initial methods report. Not peer reviewed. Foundation maturity: PROTOTYPE.**

## Abstract

NEURAL1 is a virtual-first experimental framework that restricts small language
models to Apple-1 computational conditions and a modeled Woz Monitor interface.
It separates probabilistic proposals from deterministic execution, records
lineage and interventions, and makes research claims traceable through META/1
evidence graphs and proof capsules. Five composable experiment families examine
software inheritance, plausible 1976 design space, toolchain bootstrapping,
256-byte monitor design, and communication through shared RAM. This report
defines the environment and methods; it reports no emergent-model findings.

## Motivation and questions

The Apple-1 matters because its small memory, direct monitor interaction,
minimal firmware, and legible architecture expose assumptions hidden by modern
tooling. The central questions ask what models externalize into constrained RAM,
which tools and protocols recur independently, whether increasingly abstract
infrastructure can self-host, and how firmware/hardware decisions alter later
outcomes. The objective is not to make the Apple-1 a terminal for a modern AI,
but to make its constraints causal experimental factors.

## Environment and isolation

The current world is a deterministic 64 KiB image with a 1K–4K allowed RAM
window. Experimental agents receive modeled WozMon examine/deposit/run text,
not a shell, Python, assembler, debugger, semantic memory call, or privileged
host state. Logical contexts are scheduler-owned and may be destroyed while RAM
persists. Agents may share model weights without sharing context. The fake and
replay providers permit tests without a real model.

The existing Py65 RAM harness separately establishes deterministic behavior of
repository lesson programs. Neither layer claims cycle/electrical equivalence
to a physical Replica. The physical adapter is unavailable by default.

## Runs, artifacts, lineage, and interventions

Canonical scientific inputs determine run IDs. Manifests retain experiment,
model identity/configuration, seed, target, maturity, and configuration.
SHA-256-addressed artifacts preserve snapshots, images, traces, source, and
binaries. Append-only events preserve scheduling and error history. Forks name
their base, snapshot point, changed factor, and seed relationship. Lineage nodes
require existing parents and describe mutation. Catastrophes and migrations are
explicit interventions, never invisible corrections.

## Flagship experiments

4K MIND studies persistent software conventions through context reset,
inheritance, resource pressure, catastrophe, migration, and archaeology. 1976
MULTIVERSE provides source-disciplined component and machine schemas before any
historical search. SELFHOST/1 gates later stages on model-created prior tools and
requires an exact rebuild test before the label self-hosting. 256-BYTE UNIVERSE
blinds agents to WozMon and separates correctness from human/machine usability.
RAM REPUBLIC schedules isolated agents against one shared RAM medium without
host chat. Evolved firmware/languages may become controlled factors in later
experiments.

## Evaluation and causal inference

Metrics must be operationalized before inspection. Matched comparisons and
controlled replay precede removal/intervention; cross-seed and cross-model
replication widen scope. Reports retain effect sizes, uncertainty, errors,
counterexamples, and stopping rules. Counterfactual questions preferentially
compile to one-factor forks. Negative and non-replicating results remain data.

## META/1

META/1 stores claims, evidence, typed relations, causal level, counterexamples,
and falsifiers. Tribunal roles separate advocacy, skeptical review, replication,
and rule-based evidence judgment. FALSIFY compiles attempts to defeat a claim.
Time-machine queries reconstruct only contemporaneous evidence; blinded review
and sealed forecasts permit META/model scientists themselves to be evaluated.
Proof capsules link public statements to raw records through stable hashes.

## Reproducibility

A release bundle contains manifest, model record, seeds, initial snapshot,
prompts/policies, events, source/binary and RAM/ROM artifacts, lineage, analysis
version, proof capsules, and reproduction command. Current demonstrations use
deterministic fixtures and clearly state `serial_opened=false`.

## Terminology and anthropomorphism

Culture means a persistent, heritable software/documentation convention that
survives defined context reset. Civilization is memorable shorthand for a
colony exhibiting such culture; it makes no consciousness claim. Extinction is
failure of all declared lineages to meet a survival rule. Immigration is a
newcomer-agent protocol-acquisition test. Evolution means descent with recorded
variation/selection in the artifact graph. These labels are operational tools,
not biological or sociological equivalences.

## Limitations and threats

The foundation executes deposited programs under a bounded CPU/RAM/Monitor-stub
model but does not claim cycle accuracy, run commissioned autonomous model
populations, contain authoritative 1976 component data,
or establish Pi throughput. Prompt leakage, hidden affordances, simulator
mismatch, selection bias, seed dependence, classifier drift, and post-hoc
metrics remain central threats. Blinding, preregistration, intervention,
replication, versioned classifiers, and complete evidence retention mitigate but
do not eliminate them.

## Future physical qualification

Physical Reset and ordinary Monitor operation remain sovereign. A known FT232R
open STOP blocks live transport. Future physical qualification must name one
artifact and pass repository safety gates; virtual results never become physical
results by assertion. Cameras remain out of scope.
