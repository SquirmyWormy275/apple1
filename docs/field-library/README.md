# Apple-1 Field Library

Forty lesson packets written against the brief in
`../apple1-learning-library-curriculum.md`. Every packet follows that
document's authoring template and contains `README.md`, `ACTIVITY.md`,
`ANSWERS.md`, `SOURCE-NOTES.md`, `STATUS.md`, and an `assets/` directory.

## Status of the whole library

**Every lesson is OFF-DEVICE.** No packet contains an entry procedure, a
firmware or EEPROM step, a CFFA1 step, a serial-port step, a wiring step, or
any instruction to power on, connect to, or run anything on the Replica 1
Plus. Nothing in this library grants, implies, or advances any authority to
do so.

The two RAM-only artifacts in `../../software/ram-only/` are read and
discussed in several lessons. They remain RAM-only candidates with **no
live-run authority**, exactly as `../apple1-software-library.md` classifies
them. No lesson changes that.

**No packet has been through the review gate** at the end of the curriculum
document. That is verification item V-36 and it is outstanding.

## Shared files

| File | What it is |
|---|---|
| `SOURCES.md` | The citation pool. Every packet's `SOURCE-NOTES.md` cites into it by key, so each quoted passage is written down once. |
| `EMULATOR-RUNS.md` | Every emulator run performed while authoring, with inputs and outputs, so lessons state observed results rather than predicted ones. |

## Lessons

### 1. Start here

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [S01](S01-what-is-an-apple-1/README.md) | What is an Apple-1? | LOOK | 10 minutes | none |
| [S02](S02-a-computer-is-not-magic/README.md) | A computer is not magic | LOOK | 10 minutes | none |
| [S03](S03-your-first-hex-number/README.md) | Your first hex number | LEARN | 25 minutes | none |
| [S04](S04-facts-models-and-evidence/README.md) | Facts, models, and evidence | STUDY | 40 minutes | S01 |

### 2. Inside a computer

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [C01](C01-the-6502-at-work/README.md) | The 6502 at work | LEARN | 30 minutes | S02, S03 |
| [C02](C02-memory-is-a-map/README.md) | Memory is a map | LEARN | 35 minutes | S03, C01 |
| [C03](C03-binary-bits-and-bytes/README.md) | Binary, bits, and bytes | LEARN | 30 minutes | S03 |
| [C04](C04-characters-become-numbers/README.md) | Characters become numbers | LEARN | 35 minutes | C03 |
| [C05](C05-instructions-change-state/README.md) | Instructions change state | BUILD | 50 minutes | C01, C02, C03 |

### 3. The Woz Monitor and debugging

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [M01](M01-meet-the-monitor/README.md) | Meet the Monitor | LOOK | 15 minutes | S01, S03 |
| [M02](M02-addresses-and-byte-entry/README.md) | Addresses and byte entry | LEARN | 30 minutes | S03, C02 |
| [M03](M03-a-safe-rehearsal-loop/README.md) | A safe rehearsal loop | BUILD | 45 minutes | C05, M02 |
| [M04](M04-debugging-as-observation/README.md) | Debugging as observation | LEARN | 40 minutes | S04, M03 |
| [M05](M05-why-jmp-ff1f-matters/README.md) | Why `JMP $FF1F` matters | BUILD | 45 minutes | C05, M01, M02 |

### 4. Learn 6502 programming

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [A01](A01-read-an-instruction/README.md) | Read an instruction | LEARN | 30 minutes | C01, C02, S03 |
| [A02](A02-variables-in-memory/README.md) | Variables in memory | BUILD | 45 minutes | A01, C05 |
| [A03](A03-counting-and-looping/README.md) | Counting and looping | BUILD | 50 minutes | A02, C03, C05 |
| [A04](A04-decisions-and-branches/README.md) | Decisions and branches | BUILD | 50 minutes | A03, C04 |
| [A05](A05-keyboard-to-screen/README.md) | Keyboard to screen | BUILD | 55 minutes | A01, A02, A03, A04, M05 |
| [A06](A06-design-a-tiny-utility/README.md) | Design a tiny utility | BUILD | 60 minutes | A05 |

### 5. BASIC, algorithms, and data

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [B01](B01-from-instructions-to-basic/README.md) | From instructions to BASIC | LEARN | 30 minutes | A01 |
| [B02](B02-variables-input-and-output/README.md) | Variables, input, and output | LEARN | 35 minutes | B01 |
| [B03](B03-algorithms-recipes-for-information/README.md) | Algorithms: recipes for information | LEARN | 35 minutes | none |
| [B04](B04-sorting-by-hand/README.md) | Sorting by hand | LEARN | 40 minutes | B03 |
| [B05](B05-data-files-and-the-cf-card/README.md) | Data, files, and the CF card | STUDY | 40 minutes | S04, A06 |

### 6. Creative computing

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [R01](R01-pictures-made-of-letters/README.md) | Pictures made of letters | LOOK | 25 minutes | none |
| [R02](R02-motion-is-many-pictures/README.md) | Motion is many pictures | LEARN | 35 minutes | R01 |
| [R03](R03-generative-patterns/README.md) | Generative patterns | BUILD | 45 minutes | R01, S03 |
| [R04](R04-interactive-fiction/README.md) | Interactive fiction | BUILD | 60 minutes | B02, R02 |
| [R05](R05-sound-rhythm-and-code/README.md) | Sound, rhythm, and code | STUDY | 40 minutes | C03, R02 |

### 7. History, preservation, and responsible computing

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [H01](H01-the-1976-personal-computing-moment/README.md) | The 1976 personal-computing moment | LOOK | 20 minutes | S01 |
| [H02](H02-original-replica-and-reproduction/README.md) | Original, replica, and reproduction | STUDY | 40 minutes | S01, S04 |
| [H03](H03-why-provenance-matters/README.md) | Why provenance matters | STUDY | 45 minutes | S04, H02 |
| [H04](H04-safe-experimentation/README.md) | Safe experimentation | LEARN | 30 minutes | S04, M04 |
| [H05](H05-the-future-history-you-are-making/README.md) | The future history you are making | LOOK | 20 minutes | H03 |

### 8. Challenges and capstones

| ID | Title | Level | Time | Prerequisites |
|---|---|---|---|---|
| [X01](X01-hex-scavenger-hunt/README.md) | Hex scavenger hunt | LEARN | 45 minutes | S03, C02, C04, M02 |
| [X02](X02-fix-the-loop/README.md) | Fix the loop | BUILD | 50 minutes | A03, M04 |
| [X03](X03-build-a-museum-demo/README.md) | Build a museum demo | BUILD | 60 minutes | S01, S04, H02, H04 |
| [X04](X04-curate-a-mini-software-exhibit/README.md) | Curate a mini software exhibit | STUDY | 60 minutes | S04, H02, H03 |
| [X05](X05-invent-the-next-lesson/README.md) | Invent the next lesson | BUILD | 75 minutes | A06, H04, and at least four lessons completed |

## Open verification items

Claims that are cited but unconfirmed, inferences presented as inferences,
and questions this library could not close. Each is referenced from the
packet that raised it. **This list is the honest state of the library's
evidence and should be worked through before anything goes on the card.**

| Item | Raised in | What is open |
|---|---|---|
| **V-1** | `SOURCES.md` | Page numbers. Taken from indexed PDF text, not a page-by-page read of the local collection copies. Confirm before any packet goes on the card. |
| **V-2** | `SOURCES.md` | Made versus sold. H-MADE, H-SOLD, and H-BYTESHOP are three different counts of three different things. Lessons must not merge them into one number. |
| **V-3** | `SOURCES.md` | Reset vector typo. OWAD p. 216 states `$FFFE` and `$FFFF` correctly in one sentence and then writes "$FFEF and $FFFF" in the next. The first is correct for the 6502. Lessons cite the concept, not the typo. |
| **V-4** | `SOURCES.md` | Which replica. OWAD describes the Replica I and the Replica I TE. BRIEL documents the Replica 1 Plus. These are different products. A claim sourced to OWAD must not be stated as a fact about the Plus. |
| **V-5** | `SOURCES.md` | BASIC in ROM on the original. H-BASIC-TAPE and M-BASIC-RAM together support "a 1976 Apple-1 did not have BASIC in ROM," but the inference is the author's. A citation from the Apple-1 Operation Manual would settle it. |
| **V-6** | `SOURCES.md` | Manual identity. The knowledge base indexes `Replica_One_Plus_Manual__June_2014.pdf`; the collection folder holds `Replica_One_Plus_Manual_-_June_2014.pdf`. Presumed the same June 2014 edition. No SHA-256 comparison has been run, which... |
| **V-7** | `SOURCES.md` | Display geometry. The 40-column width used throughout this library comes from the repository's own rule and tooling, not from a cited Apple-1 display specification. A line count per screen is nowhere cited and is not claimed by any lesson. |
| **V-8** | `SOURCES.md` | This machine. Nothing in this pool describes the state of this project's board, its installed EEPROM, or its serial path. |
| **V-9** | `C02-memory-is-a-map` | The `$0200` Monitor input-line label is inferred from the Monitor listing's `STA IN,Y` assembling as `99 00 02`, not from a stated memory-map entry. Confirm against a primary Apple-1 memory map before this packet goes on the card. |
| **V-10** | `C04-characters-become-numbers` | The exact mechanism by which the harness applies the high bit was read from the tool's argument documentation and its keyboard-read helper, not from a line-by-line audit of the function. The recorded runs are consistent with it. A reviewer confirming C04... |
| **V-11** | `C05-instructions-change-state` | The claim that the harness begins with the carry clear was inferred from the observed result (`$42` rather than `$43`) plus a direct py65 reproduction, not from a stated guarantee in the tool. If a future harness change altered initial processor state,... |
| **V-12** | `M03-a-safe-rehearsal-loop` | The instruction-count rule is empirical over four inputs, not derived. Do not promote it to a stated property of the program without deriving it. |
| **V-13** | `M04-debugging-as-observation` | The FT232R account is summarized from the preservation dossier's "Current boundaries" section. The primary record of that event, with its date, operator, and exact observation, lives in the project's chain-of-custody and evidence ledger rather than in this... |
| **V-14** | `M05-why-jmp-ff1f-matters` | The lesson states that the Monitor's `R` command performs a jump rather than a `JSR`. This is taken from the repository's own statement in `software/ram-only/README.md` and is consistent with `RTS` being unsafe after `R`. It has **not** been confirmed... |
| **V-15** | `M05-why-jmp-ff1f-matters` | Whether `line-input-echo-0300.hex`'s restart loop is intended is an open question for the repository owner. This lesson presents it as observed behavior and explicitly declines to call it a defect. Do not edit the lesson to assert either answer before it... |
| **V-16** | `A03-counting-and-looping` | The recorded results for Programs A and B come from a direct `py65` reproduction performed during authoring, not from a run of `tools/apple1_emulator.py`, and are not listed in `../EMULATOR-RUNS.md` as harness runs. A reviewer wanting harness-level... |
| **V-17** | `A04-decisions-and-branches` | The A04 program's runs are recorded here and in `../EMULATOR-RUNS.md`, but the program is a teaching artifact written for this lesson and is not part of `software/ram-only/`. It carries no hardware authority of any kind and should not be promoted into the... |
| **V-18** | `A05-keyboard-to-screen` | The 128-character second exit and whether it is deliberate. |
| **V-19** | `A06-design-a-tiny-utility` | The A06 worked example is hand-traced, not executed. |
| **V-20** | `B01-from-instructions-to-basic` | No BASIC in this library has been executed. All behavior is cited from OWAD chapter 5. |
| **V-21** | `B02-variables-input-and-output` | The double-question-mark consequence in Part E is reasoned from B-INPUT-Q, not observed in a transcript. |
| **V-22** | `B04-sorting-by-hand` | The "visible wait" claim is qualitative reasoning. No timing figure is given anywhere and none should be added without a source. |
| **V-23** | `B05-data-files-and-the-cf-card` | Manifest self-integrity is unaddressed in project documentation. |
| **V-24** | `R01-pictures-made-of-letters` | The set of characters the Apple-1 video ROM can display is not established by any source in this project. This lesson restricts itself to printable ASCII on the repository's rule and does not claim all of it would render. |
| **V-25** | `R02-motion-is-many-pictures` | The write-once display constraint is sourced for the original Apple-1; its applicability to the Replica 1 Plus is unverified, and the learner text's phrasing is looser than the source supports. |
| **V-26** | `R03-generative-patterns` | The absence of a 6502 divide instruction is inferred from OWAD's instruction categories rather than positively stated. |
| **V-27** | `R05-sound-rhythm-and-code` | Whether the Apple-1 or the Replica 1 Plus has any sound capability is not established by any source in this project, in either direction. |
| **V-28** | `H01-the-1976-personal-computing-moment` | These sources date only these five events. |
| **V-29** | `H02-original-replica-and-reproduction` | The four definitions are a working scheme, uncited, and usage varies among collectors. |
| **V-30** | `H03-why-provenance-matters` | Evidence-card fields 9 and 10 are this library's addition, not documented project practice. |
| **V-31** | `H05-the-future-history-you-are-making` | The uncertainty field is this library's addition. |
| **V-32** | `X01-hex-scavenger-hunt` | Part C's count of four is a deliberate error. |
| **V-33** | `X02-fix-the-loop` | Both programs in this packet are teaching artifacts written for this lesson. Neither is in `software/ram-only/`, neither has been through that library's acceptance process, and neither carries any hardware authority. |
| **V-34** | `X04-curate-a-mini-software-exhibit` | Rights and permission status is unrecorded for several artifacts. |
| **V-35** | `X05-invent-the-next-lesson` | Two card sections extend the curriculum's stated requirements. |
| **V-36** | `X05-invent-the-next-lesson` | The review gate has not been applied to any existing packet. |

## What this library does not establish

Nothing in it is a measurement of this project's Replica 1 Plus. No lesson
shows that the board powers on, displays text, reads a keypress, or moves a
byte across its serial port, and no combination of lessons does either. A
manual describes a design, a book describes history, and an emulator result
describes a byte sequence. None of the three is a measurement of this
machine.
