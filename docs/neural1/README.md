# NEURAL1

**Maturity: PROTOTYPE / VIRTUAL-VALIDATED COMPONENTS. Physical qualification pending.**

NEURAL1 makes the Apple-1 architecture an experimental world for studying what
small language models construct, preserve, inherit, and communicate under
severe machine constraints. The present foundation is executable and
deterministic, but its fake-provider demonstrations are not LLM research
results.

## System map

```text
PORTAL -> COMPUTER       NO MODEL CALLS
       -> FIELD LIBRARY  SOURCES + DETERMINISTIC RESULTS -> EXPLANATION
       -> NEURAL1        SHARED RUNTIME -> FIVE EXPERIMENTS -> META/1
```

All experiment families use the same run manifests, providers, virtual worlds,
WozMon sessions, artifact hashes, event records, snapshots, forks, lineage,
scoring, and evidence conventions. `TARGET=VIRTUAL` is the default and the
physical qualification adapter always refuses launch.

## What runs now

- 4K MIND: generations, WozMon-only deposits/examines, persistent RAM,
  deterministic context-reset rehearsal, lineage, and recorded catastrophes.
- 1976 MULTIVERSE: provenance-aware component and machine-genome schemas plus
  deterministic rejection of unknown/unsourced fixture parts.
- SELFHOST/1: ancestry-checked stages and an exact rebuild criterion.
- 256-BYTE UNIVERSE: exact 256-byte enforcement and pluggable acceptance tests.
- RAM REPUBLIC: isolated callbacks scheduled against one shared RAM world,
  without an agent-to-agent chat channel.
- META/1: claims, evidence, relations, causal levels, falsification definitions,
  reproducible experiment definitions, and proof capsules.

## Read by depth

- 10 minutes: [system overview](architecture/system-overview.md) and
  [research agenda](research/research-agenda.md)
- 1 hour: [methodology](research/methodology.md), [controls](research/experimental-controls.md),
  [reproducibility](research/reproducibility.md), and [threats](research/threats-to-validity.md)
- Implementation: [data formats](data/schemas.md), [interfaces](interface/portal.md),
  [experiments](experiments/4k-mind.md), and [META/1](meta1/claim-graph.md)
- Storage and recovery: [storage lifecycle](architecture/storage-lifecycle.md),
  [dedicated SSD layout](architecture/storage-layout.md),
  [Pi image baseline](operations/pi-image-baseline.md),
  [preserved-image archaeology](preservation/pi-image-archaeology-2026-08-30.md),
  [Pi recovery](operations/pi-recovery.md), and
  [SSD commissioning](operations/ssd-commissioning.md)
- Publication-shaped presentation: [technical report](publications/technical-report.md)

## Safety and truth labels

`[V]` means virtual. `[P]` is reserved for an explicitly commissioned physical
qualification. `[M]` identifies a META result. Emulator evidence is never
physical evidence. A model response is never execution evidence. Synthetic
component fixtures are never historical facts.
