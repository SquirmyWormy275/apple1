# Apple-1 / Replica 1 Plus / NEURAL1

A working collection of Apple-1 preservation records, source-grounded lessons,
and constrained-computing experiments. **NEURAL1** runs small local language
models against virtual Apple-1 worlds: models propose commands, deterministic
execution checks them, and META/1 records the resulting claims and evidence.

```text
APPLE-1
  +-- COMPUTER       ORDINARY APPLE-1 COMPUTING
  +-- FIELD LIBRARY  SOURCE-GROUNDED LEARNING
  +-- NEURAL1        EXPERIMENTAL COMPUTING LAB
        +-- META/1   CLAIMS / EVIDENCE / TESTS
```

Ordinary COMPUTER mode does not depend on a Pi or hidden AI. The physical
Apple-1/CFFA1 launcher remains a separate, unfinished integration.

## Start here

**[Current status](docs/STATUS.md)** explains what works and what remains open.
The **[project map](docs/PROJECT-MAP.md)** is the full documentation directory.

| Your goal | Start with |
|---|---|
| Use NEURAL1 on the commissioned Pi | [Operator guide](docs/neural1/operations/terminal-application.md) and [native Pi closeout](docs/neural1/operations/pi-closeout-2026-09-10.md) |
| Understand the five experiments | [NEURAL1 overview](docs/neural1/README.md) |
| Learn Apple-1 programming | [Field Library](docs/field-library/README.md) and [emulator guide](docs/emulator-demo-guide.md) |
| Continue the Replica investigation | [Troubleshooting record](docs/troubleshooting.md) and [captured evidence](docs/captures/README.md) |
| Explore the collection and its history | [Preservation dossier](docs/preservation-dossier.md), [display research](docs/peripherals/displays/README.md), and [Sanyo accession](docs/collection/sanyo-vm-4209-1979/README.md) |
| Work with software or CF exports | [RAM-only software library](docs/apple1-software-library.md) and [CF source-control guide](cf-card/README.md) |
| Contribute or audit the repository | [Project map](docs/PROJECT-MAP.md) and [repository records](docs/repository/README.md) |

## What runs today

The repository includes the virtual runtime, native Pi terminal application,
campaign tooling, five experiment families, META/1, and the Field Library.
On the already commissioned Pi, launch from any directory with:

```text
neural1
```

The [September 10 closeout](docs/neural1/operations/pi-closeout-2026-09-10.md)
records native local inference, persistent SSD state, automatic provider startup
after SSD arrival, and a post-boot model run with eight accepted commands. It
also preserves rejected and negative experiment outcomes.

The Apple-1 execution target remains **VIRTUAL**. A real Pi host does not make
these physical Replica results, and the FT232R connection remains unresolved.
Publishing source to `main` does not update the installed Pi release. A fresh
development checkout does not contain the Pi's private deployment configuration,
model weights, or SSD state; do not repeat commissioning just to use updated docs.

## Development and validation

Run these commands from a fresh development checkout. They mirror the
[off-device CI workflow](.github/workflows/ci.yml):

```bash
python -m pip install -e '.[dev]'
ruff check neural1 tools/neural1_validate.py tests/test_neural1*.py tests/test_storage.py
mypy neural1
python -m pytest -q
python tools/neural1_validate.py .
python -m neural1.demos --out out/neural1-demo
python -c "import json; from pathlib import Path; data=json.loads(Path('out/neural1-demo/summary.json').read_text(encoding='ascii')); assert data['serial_opened'] is False"
git diff --exit-code
```

The demo needs no model or physical serial connection. Fake-provider output is
software-test evidence, not a model research finding or physical-hardware result.
For campaign preparation, see [Pilot 001](docs/neural1/research/pilot-001/README.md)
and [reproducibility](docs/neural1/research/reproducibility.md). Template model
registries are deliberately unqualified; a real campaign needs recorded model
identities, digests, quantization, and provenance.

For host diagnostics without a benchmark workload:

```bash
python -m neural1.benchmark --hardware-report --output /tmp/neural1-native-hardware.json
```

Use a new output filename; existing reports are not overwritten. Workload and
provider benchmarks require the additional storage and model prerequisites in
the [benchmark guide](docs/neural1/benchmarks/pi-commissioning.md).

## Evidence and preservation

Preserved originals, research staging, test fixtures, and generated output have
different roles. The [repository architecture](docs/repository/architecture.md)
defines those boundaries; ordinary reading does not require following every
audit record.

Historical Pilot 001 retains its incomplete matrix, thermal stop, and zero
strict-parser acceptances. Later Pi acceptance does not rewrite that result.
The broad March-1976 research index remains staging. The console's two reviewed
year-end-1976 component records have a separate, bounded
[source review](docs/neural1/history/console-corpus-review.md); they do not
promote the broader corpus. Unknown prices remain null.

Third-party artwork is not redistributed without established rights. The pinned
[Apple1-Slideshow reference](docs/reference/apple1-slideshow.md) is a heritage
reference, not vendored artwork.

**Repository maintenance is not a live hardware procedure.** Keep physical
serial, firmware/EEPROM/CFFA1 writes, GPIO, wiring, and physical qualification
outside development and CI. Read the [troubleshooting record](docs/troubleshooting.md)
before planning any further Replica test.
