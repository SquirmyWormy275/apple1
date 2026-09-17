# NEURAL1

NEURAL1 uses the Apple-1 architecture as a constrained experimental world for
small local language models. Models propose commands; deterministic execution
checks what those commands actually do. Persistent RAM, lineage, and META/1
make the resulting behavior inspectable rather than relying on a model's
account of its own success.

## Working state

**Virtual execution; native Pi operation recorded; physical Replica integration
not qualified.** These describe different parts of the system.

The `main` baseline contains the shared runtime, experiment prototypes,
deterministic demonstrations, campaign tools, and META/1. The September 10
closeout records the native Pi terminal application and its acceptance runs on
`neural1/pi-completion-r3`; that branch was not merged into `main` at the
September 16 review. Use [current project status](../STATUS.md) for the pinned
operator closeout, exact deployed revision, and integration PR.

On the already commissioned Pi, launch with `neural1`. Do not assume the same
terminal application is present in a fresh `main` checkout, and do not repeat
installation just to reconcile the documentation.

```text
PORTAL -> COMPUTER       NO MODEL CALLS
       -> FIELD LIBRARY  SOURCES + DETERMINISTIC RESULTS -> EXPLANATION
       -> NEURAL1        SHARED RUNTIME -> FIVE EXPERIMENTS -> META/1
```

The Apple-1 execution target remains **VIRTUAL**, even when the host is a real
Pi. That does not make it a physical Replica result.

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
Pi closeout preserves both positive controls and rejected/negative outcomes.
[Historical Pilot 001](research/pilot-001/README.md) remains a separate,
incomplete pilot with its original thermal stop and parser failures.

## Find the right guide

- **Understand the design:** [system overview](architecture/system-overview.md),
  [research agenda](research/research-agenda.md),
  [data formats](data/schemas.md), and [portal interface](interface/portal.md).
- **Operate the commissioned Pi:** [current deployment and operator record](../STATUS.md#neural1-on-the-pi).
  The earlier [storage lifecycle](architecture/storage-lifecycle.md),
  [SSD layout](architecture/storage-layout.md),
  [Pi image baseline](operations/pi-image-baseline.md),
  [image archaeology](preservation/pi-image-archaeology-2026-08-30.md),
  [Pi recovery](operations/pi-recovery.md), and
  [SSD commissioning](operations/ssd-commissioning.md) retain their design and
  preservation context.
- **Run or review research:** [methodology](research/methodology.md),
  [controls](research/experimental-controls.md),
  [reproducibility](research/reproducibility.md),
  [threats to validity](research/threats-to-validity.md), and
  [initial technical report](publications/technical-report.md).
- **Develop and test:** [off-device validation commands](../../README.md#development-and-validation)
  and the [full project map](../PROJECT-MAP.md).

## Interpret the evidence

`[V]` means virtual Apple-1 execution. `[P]` is reserved for explicitly
commissioned physical qualification; running on Pi hardware alone does not earn
that label. `[M]` identifies a META result.

A model response is not execution evidence. Fake-provider demonstrations are
software tests, not LLM research findings. Synthetic fixtures are not historical
facts; the broad historical staging corpus and any reviewed console-corpus
claims retain their separate provenance gates. Unknown prices remain null.

NEURAL1 development and CI do not authorize serial opens, firmware/EEPROM/CFFA1
writes, GPIO, or physical Replica commissioning.
