# A05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## The artifact

`software/ram-only/line-input-0300.hex`, 26 bytes, load address `$0300`, quoted
in full. Its classification and intended behavior are the repository's:

| Claim | Source |
|---|---|
| Reads a key when `$D011` indicates ready, stores it at `$0400,Y`, echoes through `$FFEF`, stops after CR, returns to the Monitor | REPO `software/ram-only/README.md`, "Expected behavior" |
| Address-free byte list for entry at the address in its filename | E-RAMONLY |
| RAM-only candidate with **no live-run authority** | REPO `docs/apple1-software-library.md`, contents table |
| Exit via `JMP $FF1F`, not `RTS` | E-EXIT |

## Instructions

| Instruction | Source |
|---|---|
| `LDY`, `LDA`, `STA` | OWAD Appendix D pp. 247 to 249 |
| `INY` | OWAD Appendix D p. 251 |
| `CMP` | OWAD Appendix D p. 255 |
| `BEQ`, `BPL` | OWAD Appendix D pp. 257 to 258 |
| `JSR`, `JMP` | OWAD Appendix D p. 261 |

## Machine facts

| Claim | Key |
|---|---|
| `$D010` holds the keyboard character; `$D011` the ready flag; the processor checks the flag then reads the character | P-KBD |
| The keyboard byte has bit 7 set | P-HIGHBIT |
| `$8D` is a carriage return in Monitor terms | W-CR |
| `$FFEF` is `ECHO`; `$FF1F` is `GETLINE`, the warm entry | W-FFEF, W-FF1F |
| `$C8` is `H`, `$C9` is `I` with the high bit set | A-CHART, C04 |
| Lower-case conversion is rejected until measured | REPO `docs/firmware-behavior-model.md` |

## Observed behavior

All four recorded runs of this artifact are in `../EMULATOR-RUNS.md`. The Part D
trace conclusion that the carriage return is stored in the buffer is confirmed by
those runs: `buffer_text` for input `HI` is `HI` followed by a carriage return,
which could only happen if the store precedes the comparison.

## The 128-character limit

The lesson states that `BPL $0302` at `$0315` gives the loop a second exit at
Y = `$80`, and explicitly declines to say whether that was intended.

This is derived by reading the instruction, not cited. It is arithmetic on the
branch condition plus the fact that Y is a single byte. No source in this project
comments on the author's intent, and `docs/apple1-software-library.md` describes
the program's behavior without mentioning a length limit.

Recorded as **V-18**: the 128-character second exit is a property of the bytes,
observed by inspection. Whether it is a designed bound or an incidental
consequence of instruction choice is unknown and is presented that way.

## Deliberate simplifications

1. **Cycle timing is not discussed** anywhere, in keeping with the rest of the
   library.
2. **The polling loop is described as spinning on bit 7 of `$D011`** without
   detailing the 6821 control-register semantics that set that bit. C02 and S02
   go as far as this library needs.
3. **Part F's instruction costs are rough estimates** and are labeled as such.
   They are for weighing trade-offs, not for planning an implementation.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-18 (new).** The 128-character second exit and whether it is deliberate.
- **V-8 applies.** The artifact has not been observed running on this board, and
  this lesson does not move it any closer to doing so.

## What this lesson does not establish or authorize

The artifact remains RAM-ONLY with no live-run authority. This lesson is
OFF-DEVICE, contains no entry procedure, and grants nothing. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
