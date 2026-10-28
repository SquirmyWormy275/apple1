# The flash-card reading edition

The host-built core edition contains **50 numbered books**, an NMOS 6502 RAM
reader, and **six real CFFA1 BASIC programs**. It includes every original lesson's
reading, activity, text worksheets and answer key, plus all 39 SP01 board plates.
Guides connect the card to the local-model, software-feature, CPU and native
evidence labs on the host.

**State:** generated and rehearsed on the host; physical Replica acceptance is
pending. The preserved card image is never edited in place. A host image build
does not write a physical card or establish installed firmware identity.

[Browse the core page sources](education/pages/) ·
[Reading-edition manifest](education/manifest.json) ·
[RAM reader source](../software/card-reader/README.md) ·
[BASIC programs](../software/basic/README.md) ·
[Textbook](../docs/textbook/README.md)

## Verified combined media edition

The combined edition was loaded onto the original Lexar CF card on October 28.
Its complete readback matches the checked image, with all six original files
and metadata unchanged. In addition to this 50-book core and six BASIC programs,
it includes 319 supplemental readers and an exact-source archive: **386 files**
and **3,374 displayed pages** in total.

[Read the combined library](../wiki/CF-Card-Library.md) ·
[Loading and rebuilding](DEPLOYMENT.md) ·
[Installation audit](AUDIT-2026-10-28.md) ·
[Next agent: physical acceptance](HARDWARE-HANDOFF.md) ·
[Download built files](releases/README.md) ·
[Original six programs](original/README.md)

The rest of this page documents the independently reproducible core component.
The media copy is verified; physical Replica display, keyboard and serial
acceptance remain distinct from storage and firmware-model checks.

## What belongs where

| Location in the candidate image | Contents | Purpose |
|---|---|---|
| `EDUCATION/READFIRST` | Book index and navigation | Begin with book 00 |
| `EDUCATION/READER` | BIN `$06`, load/entry `$0800` | The paged reader |
| `EDUCATION/S01` through the other lesson IDs | All 42 complete packet readings, activities, text assets and answers | Work through the original lessons |
| `EDUCATION/MODELS`, `FEATURES`, `CPULABS`, `NATIVE` | Guides to the L/F/T/N host labs | Explain what runs on the Pi and what runs on the 6502 |
| `EDUCATION/BASICGUIDE`, `CARDGUIDE` | U01–U06 and K01–K04 | Interpreter, files, reader and build exercises |
| `EDUCATION/BOARDATLAS` | All 39 original SP01 plates in a display-safe reading copy | Compare the documented boards |
| `BASICLABS` | HELLO, CONVERT, SUM, SORT, QUIZ, PATTERN | Actual tokenized BA1 files, type `$F1` |
| `UTILITIES` and `GAMES` | Original card files | Preserved unchanged, including metadata |

The core image contains the complete **original packet text** and **guided
summaries** of the later labs. Full textbook chapters, exact Python sources,
images, transcripts, teacher/visitor material and annotation archives are host
resources; a combined card package can add those as clearly indexed supplements.
This core build does not claim that short lab guides contain every host artifact.

## Begin without a card

With the ordinary repository Python environment active:

```bash
python -m tools.textbook run U01
python -m tools.textbook run K01
python -m tools.card_image rehearse
python -m tools.card_book --out out/my-card-books
```

Use a new output directory. The compiler emits 40x24 page sources, binary books,
the reader and a manifest. `rehearse` executes the actual reader and CFFA1 ROM
against a small virtual card, including missing-prefix handling and answer jumps.

The compiler preserves exact source on the host. This is an uppercase reading
copy: case-sensitive Python, shell commands and exact JSON output must be copied
from their host sources. Lowercase character examples are spelled out, such as
`LOWERCASE A`, so `$61` does not get mislabeled as uppercase A.

## Build a new candidate image

The original image is stored with Git LFS. Hydrate that image in a normal checkout
with Git LFS available, or supply a separately downloaded, verified reference
copy. The builder requires the registered 128,974,848-byte SHA-256 identity:

```text
5c98a3bb8c77e4155167a1c8df353ae07697f57c939de9196b838ecf097ad836
```

```bash
python -m tools.card_image build \
  --baseline preservation/cf-card/2026-08-28/apple1-cf-card-lexar-disk2-128974848.img \
  --out out/my-card-image
python -m tools.card_image inspect out/my-card-image/education-candidate.img
python -m tools.card_preview --build out/my-card-image --out out/my-card-preview
```

The preview needs `python -m pip install -e '.[textbook]'`. Open
`out/my-card-preview/index.html` locally to browse the retained reader output.
Its buttons select recorded pages; they do not control hardware. PNGs and a
short GIF are labeled as modeled-display evidence.

The build checks the following before returning success:

- The baseline's length and SHA-256 match the preservation registry.
- The **identified CFFA1 firmware** creates ProDOS directories and files against
  modeled ATA; a second read-only parser independently validates the allocation.
- All original file bytes and type/aux metadata remain unchanged.
- Original allocated data blocks and the bytes after the first volume remain
  unchanged; root entries and allocation bitmap necessarily gain new data.
- Every book loads correctly; every page is displayed by the actual RAM reader.
  First/last page limits, answer jumps, book selection, errors and exit have
  separate fixture checks.
- Every BA1 is generated by `SaveBASICFile`, restored into cleared RAM by
  `LoadBASICFile`, and executed. Its result matches the cold source run.
- The reader makes **zero card writes**. The report records image, source and
  capture identities.

Outputs are a new image, `build.json`, and all recorded reader screens.
The current build receipt belongs in the textbook validation records.
The image is a candidate for later acceptance, not a physical-board success.

## Navigation on the intended machine

The following is the intended sequence **after the finished hardware and its
installed firmware have been accepted**. It is documentation for that session,
not evidence that it occurred.

| Stage | Intended action | Expected observation |
|---|---|---|
| Enter CFFA1 from Monitor | `9000R` | CFFA1 menu |
| Select the book directory | `P`, then `EDUCATION` and Return | Prefix becomes EDUCATION |
| Load the reader | `L`, then `READER` and Return | Loads at `$0800` |
| Return to Monitor | `Q` | Monitor prompt |
| Start the reader | `800R` | Book 00 / READFIRST |
| Read | `N` next, `P` back, `A` answers, `M` then 00–49 to select | Another recorded page or book |
| Leave | `Q` | Defined Monitor entry `$FF1F` |

The CFFA1 manual does not establish an automatic boot launcher. Load READER,
not an individual binary book. Its filename table and books occupy RAM, and
starting it replaces any BASIC program in that region.

For BASIC, first cold-initialize the identified Integer BASIC, then return to
Monitor using the qualified physical reset path. Enter the CFFA1 menu through
`9003R`, choose prefix `BASICLABS`, load a program such as `HELLO` with `L`,
and `Q` back to warm BASIC. `RUN` executes the restored program. A cold
`E000R` **after** loading would clear it; warm entry is `$E2B3`.
The host verifies the saved state and execution; the physical transition still
needs its own capture.

## Why the layout looks this way

CFFA1 uses **ProDOS**, not FAT. The edition uses filenames of at most 15
characters and only one subdirectory level. The root retains the original
UTILITIES/GAMES and gains EDUCATION/BASICLABS, well below its 51-entry limit.
The baseline's first volume contains 62,720 blocks; later bytes are preserved.

The reader uses a conservative **SPACE through `$5F`** character set. Atlas
vertical borders use `!` instead of `|`. Prose leaves a margin; complete
40-column plates use automatic wrap without a redundant CR. A full bottom-right
cell that would scroll away the first line is rejected during compilation.

Books are a documented `A1BK` binary format, not a claim that CFFA1 renders
Markdown or TXT. The reader, book buffer, firmware workspace and ROM have
separate memory regions. See the [reader contract](../software/card-reader/README.md)
and [identified firmware records](../preservation/software/apple1-reference/README.md).

## Source staging and preservation

`tools.export_cf_card_sources` still exports approved host sources according to
[the registry](manifests/current.json). It now refuses an existing output,
checks the full plan before creating it, rejects escaping paths and symlinks,
and records file hashes. It never recursively deletes a selected directory.

[Original-card preservation](original/README.md) ·
[Field Library review](../docs/field-library/review/README.md) ·
[Physical chapter and build storyboard](../docs/textbook/reference/physical-session.md)
