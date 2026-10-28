# Read the CF-card library

The original Lexar card now holds the reviewed lesson library, saved BASIC
programs, full teaching supplements and the six programs supplied with it.
The October 28 edition contains **386 files**. Its complete readback matches
the checked build. [Inventory and evidence](../cf-card/AUDIT-2026-10-28.md).

## Start with the main books

On a working Replica 1 Plus/CFFA1, using its keyboard:

1. From Monitor, enter `9000R` for the CFFA1 menu.
2. Use `P` with an empty name for the root, then `P` with `EDUCATION`.
3. Use `L` to load `READER`; accept its `$0800` address.
4. Use `Q` to return to Monitor, then enter `0800R`.
5. Begin with book **00**. Use **N** next, **P** back, **A** answers,
   **M** then a number **00–49** to choose, or **Q** to exit.

The main reader loads each selected book. The 50 books include all 42 lesson
readings, activities, text worksheets and answers, six lab guides, the index
and the 39-plate board atlas. The [core page sources](../cf-card/education/pages/)
and [reader contract](../software/card-reader/README.md) explain what was built.

## Find the full supporting material

| You want to read | Card folder | Online route |
|---|---|---|
| All 15 textbook chapters and course guides | `TEXTBOOK` | [Textbook](../docs/textbook/README.md) |
| All 42 worked companions | `WORKED` | [Lesson index](../docs/field-library/README.md) |
| Complete additional labs and their captured outputs | `FEATURES`, `RUNS` | [All 110 examples](../docs/textbook/coverage.md) |
| Teacher guide, worksheets, visitor tours and annotations | `TEACHERS` | [Teacher material](../docs/field-library/teacher-materials/README.md) |
| Full source/status notes, shared citations and glossary | `NOTES`, `REFERENCE` | [Review and source records](../docs/field-library/review/README.md) |
| Text art and portal | `ART` | [Artwork](../art/README.md) |
| Existing line-input RAM demonstrations | `RAMDEMOS` | [Program guide](../software/ram-only/README.md) |
| Exact code, text, figures, tools and tests | `HOSTSRC` | [Download the built package](../cf-card/releases/README.md) |

For a supplemental reader, enter `9000R`, select the root with an empty `P`,
then choose its folder with `P`. Load `INDEX` with `L`, accept **`$1000`**,
leave the CFFA menu with `Q`, and enter **`1000R`**. The index lists the files
to load next. These readers use **Space** next, **B** back and **Q** exit.
The root `START.HERE` overview uses this same `$1000` sequence.

`SOURCE.ZIP` and `BUILD.JSON` are **offboard data**, not loadable books or
programs. Extract them on a modern computer with CiderPress. The ZIP preserves
exact spelling, case-sensitive code, links and PNG/GIF figures. Display copies
use uppercase glyphs and `!` borders. Python and local-model inference run on
the host. Model weights and the large scanned-manual collection remain host
resources. [Full loading and reconstruction guide](../cf-card/DEPLOYMENT.md).

## Run the saved BASIC lessons

`BASICLABS` contains **HELLO, CONVERT, SUM, SORT, QUIZ and PATTERN** as genuine
CFFA1 BA1 files. Follow **BASICGUIDE** in the main reader and the
[Integer BASIC reference](../docs/textbook/reference/basic.md) for startup and
saved-program loading. These files restore BASIC state; cold-starting BASIC
after loading would clear the program. Save your work before starting the
book reader, which replaces the same RAM region.

## The six original programs

`UTILITIES` retains BASIC and the CFFA ROM/flasher/updater artifacts. `GAMES`
retains Lunar and Star Trek. All six are unchanged and
[individually downloadable with hashes and ProDOS metadata](../cf-card/original/README.md).
Maintenance files are preserved legacy objects, not lesson launchers. The
original full card image remains separately preserved in Git LFS.

## What is verified

- All **3,374 pages**: 1,468 main-library pages and 1,906 supplemental pages.
- The actual CFFA1 ROM loaded all 321 supplemental binaries, including the two
  RAM demonstrations, on the virtual card. All six BASIC programs restored and
  ran after their saved state was cleared. The readers made zero card writes.
- The source archive extracted correctly and reproduced all **110 examples**.
  The combined repository passed **498 tests**.
- The physical CF card was backed up, updated, flushed, reopened and read in
  full. Both independent filesystem checks passed; original bytes, metadata,
  allocated data blocks and the area beyond the first volume remain unchanged.

These storage and firmware-model results do not establish display, keyboard,
timing, electrical or serial operation on the physical Replica. That acceptance
remains open, alongside the [physical integration record](../docs/STATUS.md#physical-replica-and-propeller).
The [next-agent handoff](../cf-card/HARDWARE-HANDOFF.md) gives the exact remaining
reader/BASIC trials, photo/video checklist and publication steps for the finished
setup. The card installation is complete; the serial fault remains separate in
[repair issue #17](https://github.com/SquirmyWormy275/apple1/issues/17) and the
[bounded repair plan](../docs/hardware/replica-repair-plan.md).

[Wiki home](Home.md) · [Builder guide](For-Builders.md) ·
[Installation audit](../cf-card/AUDIT-2026-10-28.md)
