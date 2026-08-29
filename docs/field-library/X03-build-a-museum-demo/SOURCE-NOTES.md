# X03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Facts used in the worked script

| Claim | Key |
|---|---|
| The Monitor is 256 bytes | WOZ-FWD p. 17; M-ROM |
| Wozniak designed the Apple-1; it dates from 1976 | H-FOUNDED, H-MADE |
| About two hundred originals were made | H-MADE |
| The buyer supplied keyboard, power supply, and display | H-SUPPLY, H-BARE |
| `C8 C9 A0 D4 C8 C5 D2 C5` decodes to `HI THERE` with the high bit stripped | A-CHART, P-HIGHBIT; the same byte list used in C04 |
| `$41` is `A`, 65 in decimal | A-CHART |
| `C8` is the opcode `INY` | OWAD Appendix D p. 251 |
| The Replica 1 Plus is a modern reproduction documented by its June 2014 manual | BRIEL; H02 |

**The worked script's hook is checkable:** "256 bytes is about the length of this
sentence repeated four times" is an approximation offered as one, not a claim.

## Why the fallback is mandatory

The X03 brief requires an off-device fallback so the demo never depends on live
hardware. In this project the requirement is stronger than a general precaution:

| Constraint | Source |
|---|---|
| An opened serial session or transmit test is blocked until a measurement test card is ready and an operator explicitly starts that single step | REPO `docs/preservation-dossier.md`, "Current boundaries" |
| Hand entry or loading a program on a live Apple-1 is a separate, operator-led step | REPO `docs/apple1-software-library.md` |
| The RAM-only artifacts carry no live-run authority | REPO `docs/apple1-software-library.md` |
| Firmware loading, EEPROM writing, CFFA1 modification, serial-port opening, and automated device control must not appear in a lesson | REPO `docs/apple1-learning-library-curriculum.md`, rule 6 |

So the worked script uses no machine at all, and the answer key states that the
off-device version is not a backup but the demonstration itself. A learner whose
demo needs the machine has designed something this project cannot let them run.

## The value question

The answer key's response to "what is it worth" reflects this library's standing
position: no lesson makes any claim about value or rarity, stated in H02's
`STATUS.md` and repeated here. The advice to decline pleasantly is judgement, not
a cited claim.

## The inaccurate-statements list

Part G's second list is assembled from constraints elsewhere in this library:

| Item | Where it comes from |
|---|---|
| Calling the replica an Apple-1 | H02; S01 |
| Value or rarity claims | H02 `STATUS.md` |
| "What an original would do" | V-4, V-8 |
| Claiming the machine works | V-8; S04 statement (b) |
| Timing claims | V-22, R02's `STATUS.md` |
| Claiming the ROM contains particular firmware | E-110REV03; S04 |

Every one is a boundary this library already holds. The exercise gathers them so a
presenter carries them into a room where nobody will check.

## Deliberate simplifications

1. **No advice on presenting to children specifically**, though the Part E test
   mentions a twelve-year-old.
2. **Nothing about physical display, cases, or handling**, which is a museum
   practice question outside this library.
3. **Three minutes is treated as fixed.** Real demonstrations vary; the constraint
   is what forces the one-idea discipline.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-8 applies.** Nothing here establishes anything about the machine, and the
  worked script is written so that it does not need to.
- No new verification items.

## What this lesson does not establish or authorize

**It grants no authority to power on, connect to, or run anything on the Replica 1
Plus**, for a demonstration or otherwise. It makes no claim about the value of any
object. It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port
open, or physical modification.
