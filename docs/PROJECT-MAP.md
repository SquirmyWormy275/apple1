# Apple1 project map

## What this repository is

Apple1 is a long-term Apple-1 preservation, education, experimental-computing, and research repository centered on an Apple-1 / Replica 1 Plus environment.

It deliberately combines several related products while keeping their evidence and authority separate.

## The shortest route in

```text
APPLE1
|
+-- COMPUTER      ordinary Apple-1 / Replica-1 computing
+-- FIELD LIBRARY education, lessons, visitor/teacher material
+-- NEURAL1       constrained experimental-computing research
|    +-- META/1   claims/evidence/falsification/research layer
+-- PRESERVATION  source artifacts, captures, manifests, provenance
+-- COLLECTION    physical-object history and accession research
```

If you are unsure where something belongs, start with [repository architecture](repository/architecture.md).

## Current project state

### Physical Replica / serial investigation

**BLOCKED pending evidence.** A recorded no-transmit FT232R open disturbed the Replica display and required physical Reset. This repository architecture pass does not open serial hardware or advance physical qualification.

Read:

- [Preservation dossier](preservation-dossier.md)
- [Troubleshooting status](troubleshooting.md)
- [Serial test protocol](serial-test-protocol.md)
- [Captured evidence](captures/README.md)
- [Logic-analyzer test card](captures/logic-analyzer-open-event-test-card.md) — prepared procedure, not authorization/executed evidence

### COMPUTER mode

Ordinary Apple-1 / Replica-1 use is conceptually independent from NEURAL1. The portal contract is documented in [NEURAL1 interface documentation](neural1/interface/computer-mode.md).

### Field Library

The Field Library is the educational product:

- [Library index and lesson status](field-library/README.md)
- [Curriculum scaffold](apple1-learning-library-curriculum.md)
- [Emulator evidence](field-library/EMULATOR-RUNS.md)
- [Teacher material](field-library/teacher-materials/README.md)
- [Visitor mode](field-library/visitor-mode/README.md)
- [Program annotations](field-library/program-annotations/README.md)
- [RAM-only software library](apple1-software-library.md)

The library index currently records 41 lesson packets. H06 has passed its review gate; the older forty-packet corpus still carries an open set-level verification item. Existing lessons do not become CF-card-approved merely because they are committed.

### NEURAL1

Start with [NEURAL1 overview](neural1/README.md).

The five primary experiment families are:

1. [4K MIND](neural1/experiments/4k-mind.md)
2. [1976 MULTIVERSE](neural1/experiments/1976-multiverse.md)
3. [SELFHOST/1](neural1/experiments/selfhost1.md)
4. [256-BYTE UNIVERSE](neural1/experiments/256-byte-universe.md)
5. [RAM REPUBLIC](neural1/experiments/ram-republic.md)

NEURAL1 source code is under `../neural1/`; schemas under `../schemas/neural1/`; campaign configuration under `../configs/neural1/`.

### META/1

META/1 is the epistemic/scientific layer, not another experiment family. Read [META/1 architecture](neural1/architecture/meta1-architecture.md) and the [META/1 documentation index](neural1/meta1/).

It covers claim graphs, falsification, causal status, tribunals, invariants, research queues, phylogeny, proof capsules, and replication state.

### Pilot 001

[Pilot 001](neural1/research/pilot-001/README.md) is the first model-validated pilot package. Preserve its negative and incomplete results:

- 45 planned cells;
- 6 completed;
- cooperative stop at 102 C;
- 156 recorded turns;
- zero strict-parser acceptances;
- bounded resume evidence for one interrupted cell;
- zero automatic scientific findings;
- `physical_serial_opened: false`.

### 1976 MULTIVERSE historical research

The historical corpus is intentionally split between research staging and future authoritative runtime evidence.

Read:

- [Source ingestion rules](neural1/history/source-ingestion.md)
- [1976 research tranche status](neural1/research/1976-multiverse-research-tranche-status-v1.md)
- [Source ledger](neural1/research/1976-multiverse-source-ledger.md)
- `../data/neural1/history/1976-research-index.json`

Current status is `RESEARCH_STAGING` with zero authoritative runtime component records. Missing prices stay null. No LLM-generated price estimates.

### Display and Sanyo history

Start with [display research index](peripherals/displays/README.md).

Key routes:

- [Apple-1 display history](peripherals/displays/apple1-display-history.md)
- [Visual chronology](peripherals/displays/visual-chronology.md)
- [Evidence ledger](peripherals/displays/evidence-ledger.md)
- [Image-rights ledger](peripherals/displays/image-rights-ledger.md)
- [Sanyo VM-4209 research](peripherals/displays/sanyo/vm-4209.md)
- [Acquired VM-4209 collection record](collection/sanyo-vm-4209-1979/README.md)

### Preservation

Preserved byte artifacts live under `../preservation/`; interpretations and dossiers live under `docs/`.

Important routes:

- [Preservation dossier](preservation-dossier.md)
- [Collection archive rules](collection-archive.md)
- `../preservation/manuals/2026-08-28/`
- `../preservation/cf-card/2026-08-28/`
- `../firmware/vendor/110REV03/`

Do not infer installed firmware, current hardware behavior, or authenticity from a preserved manual/source file alone.

### CF-card work

The repository tree is not the card image/layout.

Read `../cf-card/README.md` for the host-side flow:

```text
preserved baseline
+ approved project sources
-> manifest-controlled export
-> out/cf-card-staging/
-> future separately validated deployment
```

The exporter does not write a physical CF card.

### Art / heritage references

- `../art/` — original project art and provenance
- [Visual-system docs](visual-system/design-language.md)
- [Heritage-art boundary](visual-system/heritage-art.md)
- [Apple1-Slideshow provenance record](reference/apple1-slideshow.md)

The external slideshow is pinned as a reference. No redistribution license was established, so its artwork is not vendored.

## Development workflow

From a fresh checkout:

```bash
python -m pip install -e '.[dev]'
ruff check neural1 tools/neural1_validate.py tests/test_neural1*.py
mypy neural1
python -m pytest -q
python tools/neural1_validate.py .
python -m neural1.demos --out out/neural1-demo
```

The deterministic demo is off-device and must report `serial_opened=false`.

CI is defined at `../.github/workflows/ci.yml`.

## Repository governance

For why the tree is organized this way, what is authoritative, branch archaeology, provenance gaps, and migration history, see [repository governance](repository/README.md).

## Non-negotiable safety boundary

Repository work does not itself authorize physical experimentation. Do not use a repository tool to open the Replica serial device, transmit bytes, load firmware, program EEPROM, write CFFA1, operate GPIO, change wiring/jumpers/solder, use cameras, or conduct physical qualification without a separate explicitly approved procedure.
