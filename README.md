# Apple-1 / Replica 1 Plus / NEURAL1

This repository preserves an Apple-1 / Replica 1 Plus collection, teaches the
machine through a source-grounded Field Library, and develops **NEURAL1**: a
virtual-first research environment in which small local language models must
work through Apple-1 constraints. It is not "ChatGPT on an Apple-1." Models
propose; deterministic execution verifies; recorded evidence supports claims.

```text
APPLE-1
  +-- COMPUTER       ORDINARY APPLE-1 COMPUTING
  +-- FIELD LIBRARY  SOURCE-GROUNDED LEARNING
  +-- NEURAL1        EXPERIMENTAL COMPUTING LAB
        +-- META/1   CLAIMS / EVIDENCE / TESTS
```

`COMPUTER` is sovereign: no hidden AI, no required Pi, and physical Reset
remains the ultimate recovery route to the ordinary Monitor. The portal and
all NEURAL1 results are currently virtual prototypes. The exact CFFA1/physical
launcher remains deliberately unresolved.

This repository preserves evidence and off-device tooling for a Replica 1 Plus
serial investigation. It does not authorize a firmware load, EEPROM write,
temporary wiring, soldering, or other physical modification.

## Start here

- [Preservation dossier](docs/preservation-dossier.md): collection inventory,
  chain of custody, and hard safety boundaries.
- [Firmware baseline](docs/firmware-baseline.md) and
  [recovery evidence ledger](docs/recovery-evidence-ledger.md): candidate-source
  provenance and the gates that still block any persistent firmware action.
- [Serial troubleshooting](docs/troubleshooting.md) and
  [capture protocol](docs/serial-test-protocol.md): the current live STOP
  result and the next evidence gate.
- [Read-only support bundle](docs/host-support-bundle.md): portable, explicit
  evidence collection with hashes and no serial-device access.
- [Firmware behavior model](docs/firmware-behavior-model.md): executable
  pre-change contract for a future single-writer candidate.
- [Virtual LLM bridge](docs/virtual-llm-bridge.md): full software rehearsal
  using the local 6502 harness and an optional local Ollama model, with no
  serial-device path.
- [Firmware static audit](docs/firmware-static-audit.md),
  [collection archive](docs/collection-archive.md), and
  [logic-trace validation](docs/logic-trace-validation.md): off-device
  source, provenance, and evidence-packet preparation.
- [RAM-only software library](docs/apple1-software-library.md) and
  [emulator/demo guide](docs/emulator-demo-guide.md): safe software rehearsal
  and deterministic terminal formatting.
- [Apple-1 Field Library curriculum scaffold](docs/apple1-learning-library-curriculum.md):
  structured, content-ready lessons for the CF-card educational catalog, with
  off-device and preservation boundaries.
- [NEURAL1 overview](docs/neural1/README.md): architecture, five flagship
  experiments, META/1, methods, maturity, and reproducible demonstrations.
- [Initial technical report](docs/neural1/publications/technical-report.md) and
  [visual system](docs/visual-system/design-language.md).
- [Next-eight implementation status](docs/neural1/phase-2-status.md).

## NEURAL1 foundation

The Python package provides a shared virtual Apple-1 world, modeled WozMon-only
agent surface, deterministic fake/replay model providers, stable run manifests,
content-addressed artifacts, snapshots, forks, replay metadata, lineage, five
experiment prototypes, META/1 claim graphs and proof capsules, Field Library
grounding, and state-driven ASCII visualizations. Tests require no model and
never open serial hardware.

```bash
python -m neural1.demos --out out/neural1-demo
python -m neural1.benchmark
python -m pytest tests/test_neural1_runtime.py tests/test_neural1_experiments.py \
  tests/test_neural1_meta_visual_field.py -q
```

Demo output is labeled prototype evidence, not a research finding or physical
result. There are no cameras, firmware loaders, EEPROM writers, CFFA1 writers,
or enabled physical adapters in NEURAL1.

The off-device campaign layer adds a versioned model registry, matched
experiment matrices, atomic checkpoints, interruption-safe resume, exact model
recordings, bounded local providers, evaluation, and hash-verifiable research
bundles. The committed Pilot 001 specification retains TinyLlama deliberately
as a lower-capability baseline alongside Qwen2.5-Coder 1.5B and SmolLM2 1.7B.
Registry records—not experiment definitions—carry backend and model-size
details, so later 3B–4B models require no experiment rewrite.

```bash
python -m pip install -e '.[dev]'
neural1 validate-campaign configs/neural1/pilot-001/campaign.json \
  configs/neural1/pilot-001/model-registry.template.json
python tools/neural1_validate.py .
```

The template registry is intentionally unqualified and cannot execute a real
campaign. Qualification must replace every pending digest, quantization, and
license field with locally observed metadata.

## Heritage visual reference

David Schmenk's [Apple1-Slideshow](docs/reference/apple1-slideshow.md), pinned
at `d436e3b088f94919f135e48af6303295058b3d51`, is the quality and format
reference. Its redistribution license is not established; upstream artwork is
excluded from this repository and from releases.
- [Apple1-Slideshow heritage artwork provenance](docs/reference/apple1-slideshow.md):
  pinned source and mandatory attribution record for the classic Apple-1
  Jobs/Woz and Apple-logo visual reference. Redistribution remains blocked
  until upstream license or permission terms are established.

## Verification

```powershell
python -m pytest tests -q
```
