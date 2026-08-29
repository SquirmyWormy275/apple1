# A06 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Repository requirements the card reflects

| Card section | Source |
|---|---|
| Section 8, status labels OFF-DEVICE / RAM-ONLY / LIVE BY SEPARATE APPROVAL | REPO `docs/apple1-learning-library-curriculum.md`, library design rule 5 |
| Section 6, expected result recorded before the observation | REPO `docs/emulator-demo-guide.md`; M04 |
| Section 5, exit and reachability | E-EXIT; M05 |
| Section 7, what it does not do | REPO curriculum review gate, "The lesson says what it does not establish" |
| The prompts purpose, inputs, outputs, memory, exit, test cases | REPO `docs/apple1-learning-library-curriculum.md`, the A06 writing brief, which names exactly these |

The card's structure is taken from the curriculum's own brief for this lesson
rather than invented.

## The worked example

The thirteen-byte fill program in `ANSWERS.md` was written for this lesson. Its
instructions are:

| Instruction | Source |
|---|---|
| `LDY`, `LDA`, `STA`, `JMP` | OWAD Appendix D pp. 247 to 261 |
| `DEY` | Decrement Index Y by One, OWAD Appendix D p. 252 |
| `BPL` | Branch on Result Plus, OWAD Appendix D p. 258 |

`$AA` is `*` (`$2A`) with bit 7 set, per A-CHART and C04.

**This program has not been executed.** Unlike the C05, A03, and A04 examples, no
run of it is recorded in `../EMULATOR-RUNS.md`. Its behavior in the answer key is
derived by hand-tracing: `DEY` from `$0F` down to `$00` keeps bit 7 clear so
`BPL` branches, and `DEY` on `$00` gives `$FF` with bit 7 set so the loop ends
after writing `$0400`.

Recorded as **V-19**: the A06 worked example is hand-traced, not observed. A
reviewer or learner running it would strengthen this packet.

## The retrospective card

Every entry in the `line-input-0300.hex` card is drawn from A05 and from the
recorded runs, except the "Y left holding the count" output, which is derived by
inspection: nothing in the program clears Y before exiting, so its value at exit
is the number of characters stored before the carriage return.

The two-route exit is V-18 from A05, carried forward unchanged, including the
open question of whether the 128-character route was intended.

## Deliberate simplifications

1. **The card has no space for cycle counts or timing.** Consistent with the rest
   of the library, which makes no timing claims.
2. **Section 4 asks for ranges, not a full memory map.** Sufficient for programs
   of this size.
3. **No review or sign-off field.** The repository's acceptance card in
   `docs/apple1-software-library.md` is the mechanism for that, and duplicating
   it here would create a second, weaker gate.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-19 (new).** The A06 worked example is hand-traced, not executed.
- **V-18 carried forward** in the retrospective card.
- **V-8 applies.** Nothing designed or discussed here has run on this board.

## What this lesson does not establish or authorize

**A completed design card carries no authority.** It does not make a program safe
to run, does not create RAM-only status, and does not advance anything toward a
live session. Section 8 records an intention, not a permission; permission for
anything beyond off-device work comes from
`docs/apple1-software-library.md` and an operator, not from a worksheet.

This packet authorizes no firmware load, EEPROM write, CFFA1 write, serial-port
open, or physical modification.
