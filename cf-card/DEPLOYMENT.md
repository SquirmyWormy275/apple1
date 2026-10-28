# Reading the educational CF-card edition

The missing delivery layer is a set of RAM-only 6502 paged readers built from
the existing lesson and textbook sources. Files are added to the original
ProDOS volume alongside `UTILITIES` and `GAMES`. Every reader is a `BIN` file
with load address `$1000`, and fits below `$8000`, including a 512-byte-rounded
CFFA load. No firmware change is needed.

## Start with one lesson

On an otherwise working Replica 1 Plus/CFFA1, using its keyboard:

1. At Monitor, enter `9000R` for the CFFA1 menu.
2. Use `P`, then an empty directory name, to select the root.
3. Use `L` to load `START.HERE`; accept the displayed `$1000` address.
4. Use `Q` to return to Monitor, then enter `1000R` to read it.
5. In a reader, use **Space** for next, **B** for back, or **Q** for Monitor.

After leaving a reader, `9000R` returns to the CFFA1 menu. Select `START` with
`P`, load `S01.READ` with `L`, leave the menu with `Q`, then use `1000R`.
Use an empty `P` directory name to return to the root before selecting a sibling
folder. Each folder contains an `INDEX` reader listing its files and sources.

These instructions follow the manufacturer's [CFFA1 1.1 manual](https://dreher.net/projects/CFforApple1/downloads/CFFA1_Manual_1.1.pdf),
pp. 11–16 and 23–24: the first ProDOS volume, one directory level, `P`/`L`/`Q`,
and the saved binary load address. The CFFA menu has no separate `R` run command;
execution is through the Woz Monitor.

## What the card contains

| Folder | Contents |
|---|---|
| `START`, `COMPUTER`, `MONITOR`, `ASSEMBLY` | S, C, M, and A lesson packets |
| `BASIC`, `CREATIVE`, `HISTORY`, `PROJECTS` | B, R, H, and X lesson packets |
| `HARDWARE` | SP01 packet and all 39 original atlas screens |
| `TEACHERS` | Teacher guides, worksheets, visitor tours, program annotations |
| `TEXTBOOK` | 13 chapters, course guide, review, references, native evidence guide |
| `FEATURES` | 58 feature, local-model, CPU-extension and evidence labs |
| `RUNS` | The actual stdout of all 100 catalog examples |
| `REFERENCE`, `ART` | Glossary, source pool, curriculum, emulator records, ASCII art |
| `RAMDEMOS` | The two existing line-input binaries at `$0300`, plus their status guide |
| `HOSTSRC` | `SOURCE.ZIP`, `BUILD.JSON`, and a display index |
| `UTILITIES`, `GAMES` | All original card files, preserving bytes and directory metadata |

For each lesson, `.READ` is the lesson, `.TRY` the activity, `.KEY` the answer
key, `.WORKED` the worked example, `.SOURCES` the citations, `.STATUS` the
limitations, and `.ASSETS` any text worksheet/code assets. A large document can
span `.V1`, `.V2`, etc.; each volume is separately loadable. No pages are dropped.

The display edition converts prose to uppercase ASCII and wraps it to 40
columns. Each ordinary screen has 20 body rows and navigation within 24 rows.
Atlas source screens retain their original text, dimensions, and diagrams;
Space/B/Q still work on screens without a footer. Forty-column rows rely on
the terminal's automatic wrap and do not receive a second carriage return.

The ZIP keeps original UTF-8 text, case-sensitive code, links, PNG captures,
host tools, runtime source and tests byte for byte. Extract it with CiderPress
on a modern computer. Python exercises, NEURAL1 and local model inference
remain modern-host activities. The reader displays those materials; it does
not execute their Python or provide a physical AI bridge. Model weights are
not included. Existing source review items and evidence limits remain recorded;
loading their text onto storage does not resolve them.

## Rebuild and audit

From the repository environment:

```bash
python -m tools.build_cf_library --output out/cf-library-new
python -m pytest tests/test_cf_library_reader.py tests/test_cf_card_audit.py tests/test_cf_card_sources.py -q
python -m tools.textbook verify docs/textbook/captures --rerun
```

The builder requires a **new** output directory. It produces `payload/` with
CiderPress NAPS names retaining ProDOS types/load addresses, `screens/` with
the exact screen arrays, `SOURCE.ZIP`, and `build.json` with source and payload
hashes. `HOSTSRC/BUILD.JSON` describes the other payloads; its own identity is
checked against the external copy to avoid a self-referential hash.

Construct an image with [CiderPress II](https://github.com/fadden/CiderPress2)
using a copy of a freshly acquired card backup. From the payload directory,
use `cp2 add --no-overwrite --no-interactive /absolute/path/working.img:1 *`.
Neither Python builder nor auditor opens a physical device. The auditor checks
the first volume independently of CiderPress:

```bash
python -m tools.cf_card_audit working.img --before before.img --build out/cf-library-new/build.json
```

It rejects changed original files or directory entries, wrong new bytes,
wrong ProDOS types/load addresses, missing/unexpected files, changed boot
blocks, and changes beyond the original volume. Retain the original image
and verified backups before any physical installation. Recheck the device
identity and its complete pre-write hash, flush writes, then read the entire
card again and run the same audit against that readback.

The reader's machine-code tests cover next/back/quit, first/last-page behavior,
decimal-mode entry, screen wrapping and allowed memory writes. Full-edition
rehearsal compares each emitted screen to its build output. These are emulator
and storage checks; display and keyboard operation on the physical board remain
a separate observation.
