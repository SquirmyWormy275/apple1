# NEURAL1

NEURAL1 uses the Apple-1 architecture as a constrained experimental world for
small local language models. Models propose commands; deterministic execution
checks what those commands actually do. Persistent RAM, lineage, and META/1
make the resulting behavior inspectable rather than relying on a model's
account of its own success.

## Working state

**Virtual Apple-1 execution; native Pi operation recorded; physical Replica
integration not qualified.** These describe different parts of the system.

The repository includes the terminal application, shared runtime, five
experiment families, deterministic demonstrations, campaign tools, and META/1.
The [native Pi closeout](operations/pi-closeout-2026-09-10.md) records the
installed application's identity and acceptance results. On the commissioned
Pi, launch with `neural1`; the [operator guide](operations/terminal-application.md)
explains its commands. A GitHub merge does not reinstall the Pi or reproduce
its private configuration and SSD state in a fresh development checkout.

```text
PORTAL -> COMPUTER       NO MODEL CALLS
       -> FIELD LIBRARY  SOURCES + DETERMINISTIC RESULTS -> EXPLANATION
       -> NEURAL1        SHARED RUNTIME -> FIVE EXPERIMENTS -> META/1
```

## The five experiments

| Family | Implemented foundation |
|---|---|
| [4K MIND](experiments/4k-mind.md) | WozMon-only deposits/examines, persistent RAM, context-reset rehearsal, lineage, and recorded catastrophes |
| [1976 MULTIVERSE](experiments/1976-multiverse.md) | Provenance-aware component and machine-genome schemas with deterministic validation |
| [SELFHOST/1](experiments/selfhost1.md) | Ancestry-checked stages and an exact rebuild criterion |
| [256-BYTE UNIVERSE](experiments/256-byte-universe.md) | Exact 256-byte enforcement and deterministic acceptance tests |
| [RAM REPUBLIC](experiments/ram-republic.md) | Isolated participants using one shared RAM world, without an agent-to-agent chat channel |

All families share providers, run manifests, virtual worlds, WozMon sessions,
artifact hashes, event records, snapshots, forks, lineage, and evidence
conventions. [META/1](meta1/claim-graph.md) records claims, supporting evidence,
relations, falsification definitions, and proof capsules.

An exercised family is not automatically a successful scientific result. The
Pi closeout preserves positive controls and rejected/negative outcomes.
[Historical Pilot 001](research/pilot-001/README.md) remains separate, with its
original incomplete matrix, thermal stop, and parser failures.

## Find the right guide

- **Understand the design:** [system overview](architecture/system-overview.md),
  [research agenda](research/research-agenda.md), [data formats](data/schemas.md),
  and [portal interface](interface/portal.md).
- **Operate the Pi:** [terminal commands](operations/terminal-application.md),
  [current status](../STATUS.md#neural1-on-the-pi),
  [closeout and recovery context](operations/pi-closeout-2026-09-10.md),
  [storage lifecycle](architecture/storage-lifecycle.md), and
  [SSD layout](architecture/storage-layout.md).
- **Read preservation and setup history:** [Pi image baseline](operations/pi-image-baseline.md),
  [image archaeology](preservation/pi-image-archaeology-2026-08-30.md),
  [Pi recovery](operations/pi-recovery.md), and
  [SSD commissioning](operations/ssd-commissioning.md).
- **Run or review research:** [methodology](research/methodology.md),
  [controls](research/experimental-controls.md),
  [reproducibility](research/reproducibility.md),
  [threats to validity](research/threats-to-validity.md), and
  [initial technical report](publications/technical-report.md).
- **Develop and test:** [off-device validation commands](../../README.md#development-and-validation)
  and the [project map](../PROJECT-MAP.md).

## Interpret the evidence

`[V]` means virtual Apple-1 execution. `[P]` is reserved for explicitly
commissioned physical qualification; a real Pi host alone does not earn that
label. `[M]` identifies a META result.

A model response is not execution evidence. Fake-provider demonstrations are
software tests, not LLM research findings. Synthetic fixtures are not historical
facts. The broad staged historical corpus and the console's reviewed year-end
CPU/RAM records have separate [provenance scopes](history/console-corpus-review.md).
Unknown prices remain null.

Development and CI do not authorize serial opens, firmware/EEPROM/CFFA1 writes,
GPIO, or physical Replica commissioning.
