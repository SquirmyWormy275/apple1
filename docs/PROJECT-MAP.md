# Apple-1 project map

Use this page to find the working guides, source code, and evidence. For what
has changed recently and what is still on a branch, read
[current status](STATUS.md) first.

```text
APPLE1
|
+-- COMPUTER      ordinary Apple-1 / Replica 1 Plus computing
+-- FIELD LIBRARY lessons, exercises, teacher and visitor material
+-- NEURAL1       constrained-computing experiments
|    +-- META/1   claims, evidence, tests, and replication
+-- PRESERVATION  original artifacts, captures, and provenance
+-- COLLECTION    physical-object history and accession records
```

## Use NEURAL1

[NEURAL1 overview](neural1/README.md) explains the shared runtime and its five
families. [Pi deployment status](STATUS.md#neural1-on-the-pi) distinguishes the
commissioned application from the source currently on `main` and links the
pinned operator closeout. Do not treat an old commissioning plan as a request
to repeat completed setup.

| Family | Question or constraint |
|---|---|
| [4K MIND](neural1/experiments/4k-mind.md) | What survives context resets through a small persistent RAM world? |
| [1976 MULTIVERSE](neural1/experiments/1976-multiverse.md) | Which machine designs satisfy explicitly sourced period constraints? |
| [SELFHOST/1](neural1/experiments/selfhost1.md) | Can an artifact retain ancestry and meet an exact rebuild criterion? |
| [256-BYTE UNIVERSE](neural1/experiments/256-byte-universe.md) | What can satisfy an exact 256-byte budget and deterministic tests? |
| [RAM REPUBLIC](neural1/experiments/ram-republic.md) | How do isolated participants interact through shared RAM rather than chat? |

[META/1 architecture](neural1/architecture/meta1-architecture.md) and the
[META/1 index](neural1/meta1/) cover claim graphs, falsification, research queues,
proof capsules, and replication. META/1 is the evidence layer, not a sixth
experiment family.

For implementation, use [system architecture](neural1/architecture/system-overview.md),
[data formats](neural1/data/schemas.md), and the
[portal interface](neural1/interface/portal.md). The
[COMPUTER-mode contract](neural1/interface/computer-mode.md) keeps ordinary
Apple-1 use independent of NEURAL1.

## Learn and rehearse Apple-1 computing

The [Field Library](field-library/README.md) is the lesson index and review
record. The [curriculum](apple1-learning-library-curriculum.md) supplies the
broader learning sequence.

- [Emulator/demo guide](emulator-demo-guide.md),
  [RAM-only software library](apple1-software-library.md), and
  [recorded lesson emulator runs](field-library/EMULATOR-RUNS.md).
- [Program annotations](field-library/program-annotations/README.md),
  [teacher material](field-library/teacher-materials/README.md), and
  [visitor mode](field-library/visitor-mode/README.md).
- [Virtual LLM bridge](virtual-llm-bridge.md) for an off-device 6502 rehearsal
  with an optional local model and no physical serial path.

Lesson presence, emulator success, and CF-card approval are different states.
The branch-specific lesson counts and remaining review work are summarized in
[current status](STATUS.md).

## Continue the Replica investigation

Begin with the [troubleshooting record](troubleshooting.md), not an old repair
plan. It separates the observed display corruption from unproven causes and
links the current diagnostic-preparation work.

| Need | Record or guide |
|---|---|
| Read the recorded tests | [Capture index](captures/README.md) and [September 2 packet](captures/2026-09-02-ft232r-open-analyzer/README.md) |
| Understand the next evidence gate | [Serial protocol](serial-test-protocol.md) and [logic-analyzer test card](captures/logic-analyzer-open-event-test-card.md) |
| Inspect candidate-source provenance | [Firmware baseline](firmware-baseline.md) and [recovery ledger](recovery-evidence-ledger.md) |
| Rehearse behavior without hardware | [Firmware behavior model](firmware-behavior-model.md) and [static audit](firmware-static-audit.md) |
| Collect or check saved evidence | [Read-only host bundle](host-support-bundle.md) and [logic-trace validation](logic-trace-validation.md) |
| Understand earlier plans | [Plan index and supersession notes](plans/README.md) |

A prepared test card or software worker is not an executed test. No repository
maintenance command authorizes serial access, transmission, firmware/EEPROM/CFFA1
writes, GPIO, or changes to wiring.

## Read the research

[Pilot 001](neural1/research/pilot-001/README.md) is the first model-validated
pilot package. Its incomplete matrix, thermal stop, parser failures, bounded
resume evidence, and zero automatic findings are preserved. Later Pi acceptance
is a separate run with its own scope.

Start research design with the [agenda](neural1/research/research-agenda.md),
[methodology](neural1/research/methodology.md),
[experimental controls](neural1/research/experimental-controls.md),
[reproducibility](neural1/research/reproducibility.md), and
[threats to validity](neural1/research/threats-to-validity.md).
The [initial technical report](neural1/publications/technical-report.md) and
[phase-two record](neural1/phase-2-status.md) document earlier project stages;
use [current status](STATUS.md) for subsequent commissioning and integration.

For 1976 MULTIVERSE, read [source ingestion](neural1/history/source-ingestion.md),
the [research-tranche record](neural1/research/1976-multiverse-research-tranche-status-v1.md),
and the [source ledger](neural1/research/1976-multiverse-source-ledger.md).
The [structured research index](../data/neural1/history/1976-research-index.json)
is staging, not a license to populate missing historical prices or promote
unreviewed claims into runtime data.

## Explore the collection

The [display research index](peripherals/displays/README.md) leads to
[Apple-1 display history](peripherals/displays/apple1-display-history.md), the
[visual chronology](peripherals/displays/visual-chronology.md), and
[Sanyo VM-4209 research](peripherals/displays/sanyo/vm-4209.md).
The [acquired VM-4209 record](collection/sanyo-vm-4209-1979/README.md) keeps
collection-specific provenance separate from general model history.

The [display evidence ledger](peripherals/displays/evidence-ledger.md) and
[image-rights ledger](peripherals/displays/image-rights-ledger.md) contain the
supporting qualifications rather than scattering them through every entry page.

The [preservation dossier](preservation-dossier.md) and
[collection archive guide](collection-archive.md) explain custody and identity.
Original bytes live under [preservation](../preservation/); interpretations live
under `docs/`. Candidate [vendor firmware](../firmware/vendor/110REV03/) is not
proof of what is installed on the board.

## Storage, recovery, and CF exports

For the deployed Pi, use the operator closeout linked from
[current status](STATUS.md#neural1-on-the-pi). The following guides retain the
storage design and earlier preservation/commissioning context:

- [Storage lifecycle](neural1/architecture/storage-lifecycle.md) and
  [dedicated SSD layout](neural1/architecture/storage-layout.md).
- [Pi image baseline](neural1/operations/pi-image-baseline.md),
  [preserved-image archaeology](neural1/preservation/pi-image-archaeology-2026-08-30.md),
  [Pi recovery](neural1/operations/pi-recovery.md), and
  [SSD commissioning](neural1/operations/ssd-commissioning.md).

[CF-card source control](../cf-card/README.md) combines approved project sources
with a preserved baseline through a manifest-controlled host-side export. The
repository tree is not a card image, and the exporter does not write a physical
CF card.

## Art and visual references

[Project art](../art/), the [visual-system guide](visual-system/design-language.md),
and the [heritage-art boundary](visual-system/heritage-art.md) explain the visual
language and ownership. [Apple1-Slideshow](reference/apple1-slideshow.md) remains
a pinned external reference; its artwork is not vendored without established
redistribution rights.

## Work on the repository

| Directory | Role |
|---|---|
| `neural1/`, `tools/`, `tests/` | Runtime, host-side utilities, and deterministic tests |
| `configs/`, `schemas/`, `data/` | Configuration, data contracts, and explicitly classified research data |
| `docs/` | Guides, interpretations, research records, and committed evidence |
| `preservation/`, `firmware/vendor/` | Preserved artifacts and candidate-source provenance |
| `software/`, `cf-card/`, `art/` | Apple-1 software, host-side export control, and project visual sources |
| `wiki/` | Repository-held wiki navigation source; not a second technical authority |

Use the [development and validation commands](../README.md#development-and-validation)
from a fresh checkout. The [repository records](repository/README.md) hold the
architecture, audits, branch archaeology, and preservation rules. Existing
subtrees stay in place unless moving them solves a real problem.
