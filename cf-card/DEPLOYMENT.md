# Reading the combined CF-card edition

The combined edition joins the reviewed 50-book CFFA1 library and six saved
Integer BASIC programs with the full textbook, worked examples, source/status
notes, teacher and visitor material, captures, ASCII art and exact-source ZIP.
All six original card files remain in `UTILITIES` and `GAMES`.

The main library uses `EDUCATION/READER` at **`$0800`**. Supplemental readers
load individually at **`$1000`**. `START.HERE` is the combined entry guide.
Installation receipts distinguish a checked storage copy from physical
Replica display/keyboard acceptance; see [dated deployments](deployments/).

## Begin with the main library

On a working Replica 1 Plus/CFFA1, using its keyboard:

1. At Monitor, enter `9000R` for the CFFA1 menu.
2. Use `P`, then an empty directory name, to select the root. Use `P` again
   with `EDUCATION` to enter the main book directory.
3. Use `L` to load `READER`; accept the displayed `$0800` address.
4. Use `Q` to return to Monitor, then enter `0800R`.
5. Use **N** next, **P** back, **A** answers, **M** then **00–49** to choose
   a book, or **Q** to return to Monitor. Book 00 is the index.

Load `READER`, not an individual `A1BK` book container. The reader loads its
selected books through CFFA1. Starting it replaces BASIC program RAM; save a
program before switching. The [core guide](README.md) and
[reader contract](../software/card-reader/README.md) describe the format and
the independently checked firmware model.

## Read a supplement

Use `9000R`, `P` with an empty name, then `P` with the desired folder. Load
`INDEX` with `L`, accept `$1000`, leave the menu with `Q`, and enter `1000R`.
The index lists the files to load using the same sequence.

These standalone readers use **Space** next, **B** back and **Q** for Monitor;
next on the last page also exits. Their source is [`reader.s`](reader.s).
The root `START.HERE` file uses this same `$1000` sequence and explains both
interfaces.

| Folder | Contents |
|---|---|
| `EDUCATION` | 42 complete packet readings/activities/text assets/answers, six lab guides, index and all 39 atlas plates |
| `BASICLABS` | Six genuine BA1 programs: HELLO, CONVERT, SUM, SORT, QUIZ and PATTERN |
| `TEXTBOOK` | All 15 teaching chapters, course guide, references and native evidence guide |
| `WORKED` | Full worked companions for all 42 lesson packets |
| `FEATURES`, `RUNS` | Complete additional-lab text and the actual outputs of all 110 catalog examples |
| `TEACHERS` | Teacher guide, worksheets, visitor tours and program annotations |
| `NOTES`, `REFERENCE` | Every packet's source/status notes, shared sources, glossary and curriculum |
| `ART` | Text art and portal |
| `RAMDEMOS` | The two existing line-input binaries at `$0300`, plus their guide |
| `HOSTSRC` | `SOURCE.ZIP`, its component `BUILD.JSON`, and a display index |
| `UTILITIES`, `GAMES` | All six original card files, unchanged |

Use `BASICGUIDE` in the main reader and the [Integer BASIC reference](../docs/textbook/reference/basic.md)
for the saved-program sequence. The BA1 programs restore BASIC state; they are
not ordinary binaries to run at an auxiliary address. A cold BASIC start after
loading a saved program would clear it.

## Exact source and reading copies

The display edition uses the original conservative SPACE–`$5F` alphabet.
Vertical borders use `!`; lowercase character examples are labeled explicitly.
Prose is reflowed, while code/worksheet layout and full-width atlas coordinates
are preserved within the display limit. A 40-column row relies on automatic
wrap and does not receive a second carriage return. `.V1`, `.V2`, etc. are
separately loadable volumes of a large document.

`HOSTSRC/SOURCE.ZIP` retains the exact original text, case-sensitive code,
links, PNG/GIF captures, tools, BASIC sources, reference interpreter/firmware
bytes and tests at its recorded source revision. Extract it with CiderPress on
a modern computer, or download the [ready-built package](releases/README.md).
Python, NEURAL1 and model inference remain modern-host activities. The 6502
reader displays their material; it does not execute Python or provide a serial
AI bridge. Model weights and the large scanned-manual collection remain host
resources. Review limitations remain in the source/status records.

## Rebuild the two components

Build the core from a hydrated or separately verified original image:

```bash
python -m tools.card_image build --baseline /absolute/path/original.img --out out/core-new
python -m tools.build_cf_library --supplements --output out/supplements-new
```

Both outputs must be new directories. The baseline is the immutable
128,974,848-byte image with SHA-256
`5c98a3bb8c77e4155167a1c8df353ae07697f57c939de9196b838ecf097ad836`.
The core builder exercises the identified CFFA1 firmware against virtual ATA,
checks all main-reader pages and all six BASIC restores, and preserves the
original files and bytes beyond the first volume.

The supplemental build produces `payload/` with CiderPress NAPS names retaining
ProDOS types/load addresses, exact `screens/`, `SOURCE.ZIP` and `build.json`.
It excludes the retained ZIP releases from the source archive, avoiding nested
copies of older packages. Its `HOSTSRC/BUILD.JSON` describes the other component
payloads and is checked against the external copy.

Use [CiderPress II](https://github.com/fadden/CiderPress2) to append the payload
to a **copy** of the checked core image. From the supplemental payload directory:

```bash
cp2 add --no-overwrite --no-interactive /absolute/path/combined.img:1 *
```

The files remain in one directory level of the first ProDOS volume. The image
builder, supplemental builder and auditors open ordinary host files; they do
not open physical block devices. The source-staging exporter remains a separate
workflow and does not replace this image build.

## Verify before and after a physical copy

```bash
python -m pytest -q
python -m tools.textbook verify docs/textbook/captures --rerun
python -m tools.card_image inspect combined.img
python -m tools.cf_card_audit combined.img --before original.img --build combined-manifest.json
```

A combined manifest lists every added core and supplemental file with byte hash,
type and auxiliary address, including the component manifest explicitly. The
independent auditor rejects changed original entries/contents, wrong or missing
payloads, unexpected files, changed boot blocks and changes beyond the original
volume. The stricter ProDOS inspector also checks allocation ownership and
directory links. Compare original allocated blocks separately; only the root
and allocation bitmap should gain changes.

Execute every core and supplemental page from the combined image, check answer
jumps and exit, and restore/run the six BA1 programs. Preserve a verified
whole-card backup and recheck the target identity and full pre-write hash before
copying. Flush and close the write handle, reopen the card, read it in full,
and run the same byte/hash and filesystem checks on that readback.

The dated receipt records what was actually installed and checked. Emulator,
firmware-model and storage checks do not establish display, keyboard, timing,
electrical or serial operation on the physical board.
