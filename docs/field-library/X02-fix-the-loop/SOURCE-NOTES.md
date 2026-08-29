# X02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Instruction | Source |
|---|---|
| `LDY`, `LDA`, `STA`, `JMP` | OWAD Appendix D pp. 247 to 261 |
| `INY` | OWAD Appendix D p. 251 |
| `CPY` | Compare Memory and Index Y, OWAD Appendix D p. 256 |
| `BNE` | Branch on Result not Zero, OWAD Appendix D p. 258 |

| Claim | Key |
|---|---|
| `$41` is the character `A` | A-CHART |
| `$FF1F` is the Monitor warm entry; exit via `JMP $FF1F` | W-FF1F, E-EXIT |
| `$0400` is the buffer address used by this repository's programs | E-RAMONLY |
| Change one thing at a time | REPO `docs/preservation-dossier.md` evidence rules; M04 |
| A discrepancy in an emulator run is retained as a software issue | REPO `docs/emulator-demo-guide.md` |

## Recorded observations

Both versions were executed in `tools/apple1_emulator.py` during authoring.

| Version | Bytes | Buffer | Instructions | Returned |
|---|---|---|---:|---|
| As written | `A0 00 A9 41 99 00 04 C8 C0 06 D0 F8 4C 1F FF` | `AAAAAA` | 27 | true |
| Corrected | `A0 00 A9 41 99 00 04 C8 C0 05 D0 F8 4C 1F FF` | `AAAAA` | 23 | true |

Fifteen bytes each, differing in one. Recorded in `../EMULATOR-RUNS.md`.

The harness requires an input string ending in a carriage return, so one was
supplied. Neither program reads the keyboard and the input is never consumed.

This is off-device software evidence about fifteen bytes. Per E-EMU-SCOPE it is
not evidence about hardware.

## Exactly one bug, deliberately

The X02 brief requires exactly one intentional bug. There is one: `06` where `05`
belongs, at `$0308`.

The corrected program was verified to do precisely what the stated intention
says, so a learner who fixes it correctly gets a clean result rather than
discovering a second fault. This was checked by running it, not assumed.

The three wrong fixes in Part G were each traced by hand. Item 1's outcome, five
stores at `$0401` to `$0405`, is stated in the answer key with the trace that
produces it, and the answer key corrects its own first sentence mid-item rather
than presenting a tidy wrong summary. That is deliberate: the point of item 1 is
that a plausible fix can pass the obvious check.

## Part G item 3

The observation that changing the specification is not automatically wrong, but
is wrong when done silently, is reasoning rather than a cited claim. It follows
from the repository's own habit of recording intention separately from
observation (evidence rule 1) and from A06's design card, where the intention is
written before the program.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-33 (new).** Both programs in this packet are teaching artifacts written for
  this lesson. Neither is in `software/ram-only/`, neither has been through that
  library's acceptance process, and neither carries any hardware authority.
- **V-8 applies.** Neither version has run on this board.

## What this lesson does not establish

Neither program has run on this project's machine, neither is supplied as a
`.hex` artifact, and no entry procedure appears. It authorizes no firmware load,
EEPROM write, CFFA1 write, serial-port open, or physical modification.
