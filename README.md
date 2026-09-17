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

**[Current status](docs/STATUS.md)** explains what is working, what is on a
branch rather than `main`, and what still needs evidence. The
**[project map](docs/PROJECT-MAP.md)** is the full documentation directory.

| Your goal | Start with |
|---|---|
| Use or understand NEURAL1 | [NEURAL1 overview](docs/neural1/README.md) and [Pi deployment status](docs/STATUS.md#neural1-on-the-pi) |
| Learn Apple-1 programming | [Field Library](docs/field-library/README.md) and [emulator guide](docs/emulator-demo-guide.md) |
| Continue the Replica investigation | [Troubleshooting record](docs/troubleshooting.md) and [captured evidence](docs/captures/README.md) |
| Explore the collection and its history | [Preservation dossier](docs/preservation-dossier.md), [display research](docs/peripherals/displays/README.md), and [Sanyo accession](docs/collection/sanyo-vm-4209-1979/README.md) |
| Work with software or CF exports | [RAM-only software library](docs/apple1-software-library.md) and [CF source-control guide](cf-card/README.md) |
| Contribute or audit the repository | [Project map](docs/PROJECT-MAP.md) and [repository records](docs/repository/README.md) |

## What runs today

The `main` baseline contains the virtual runtime, deterministic demonstrations,
campaign tooling, five experiment families, META/1, and the Field Library.

The **September 10 native Pi closeout records a usable Pi-hosted NEURAL1
application**, including a post-boot model run with eight accepted commands.
At the September 16 review, that implementation and its evidence were on
`neural1/pi-completion-r3`, not yet merged into `main`. See
[current status](docs/STATUS.md) for the pinned closeout, deployed revision,
and review pull request. A fresh checkout of `main` is not the commissioned Pi
application.

On the already commissioned Pi, the normal entry point is:

```text
neural1
```

That is an operator command for the installed Pi release, not an instruction to
reinstall or recommission it. Its Apple-1 execution target remains **VIRTUAL**.
The physical Replica/FT232R connection is still unresolved.

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
software-test evidence, not a model research result or a physical-hardware result.
For campaign preparation, see [Pilot 001](docs/neural1/research/pilot-001/README.md)
and [reproducibility](docs/neural1/research/reproducibility.md). Template model
registries are deliberately unqualified; do not run a real campaign until the
required model identities, digests, quantization, and provenance are recorded.

## Evidence and preservation

Preserved originals, research staging, test fixtures, and generated output have
different roles. The [repository architecture](docs/repository/architecture.md)
defines those boundaries; normal reading does not require following every audit
record.

Historical Pilot 001 retains its incomplete matrix, thermal stop, and zero
strict-parser acceptances. Later Pi acceptance does not rewrite that result.
The broader 1976 MULTIVERSE research index remains staging; missing prices stay
null. Reviewed branch-specific console claims are not blanket historical authority.

Third-party artwork is not redistributed without established rights. The pinned
[Apple1-Slideshow reference](docs/reference/apple1-slideshow.md) is a heritage
reference, not vendored artwork.

**Repository work does not authorize live hardware actions.** Keep physical
serial, firmware/EEPROM/CFFA1 writes, GPIO, wiring, and physical qualification
outside development and CI. Read the [troubleshooting record](docs/troubleshooting.md)
before planning any further Replica test.
