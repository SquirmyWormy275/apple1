# A04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Instruction | Full name | Source |
|---|---|---|
| `CMP` | Compare Memory and Accumulator | OWAD Appendix D p. 255 |
| `BEQ` | Branch on Result Zero | OWAD Appendix D p. 257 |
| `BNE` | Branch on Result not Zero | OWAD Appendix D p. 258 |
| `BMI` | Branch on Result Minus | OWAD Appendix D p. 257 |
| `BPL` | Branch on Result Plus | OWAD Appendix D p. 258 |
| `DEX` | Decrement Index X by One | OWAD Appendix D p. 251 |
| `LDA`, `JSR`, `JMP` | As A01 and M05 | OWAD Appendix D pp. 247, 261 |

| Claim | Key |
|---|---|
| The status register carries `Z` (zero) and `N` (negative) flags | OWAD ch. 7 p. 215, status register diagram |
| `$D010` holds the keyboard character; `$D011` the ready flag | P-KBD |
| A keyboard byte arrives with bit 7 set | P-HIGHBIT |
| `Y` is `$59`, `N` is `$4E`, `?` is `$3F`; with bit 7 set, `$D9`, `$CE`, `$BF` | A-CHART, C03, C04 |
| `$FFEF` is the Monitor `ECHO` routine, called with `JSR` | W-FFEF |
| `$FF1F` is the Monitor warm entry | W-FF1F |
| The Monitor listing itself uses `CMP` followed by `BEQ` in exactly this pattern | BRIEL Appendix C p. 30, e.g. `CMP #$DF` then `BEQ BACKSPACE` |

The last row is worth noting: the compare-then-branch shape taught here is the
shape the Woz Monitor itself is built out of, which a learner can verify by
reading Appendix C.

## Recorded observations

The 25-byte program in `assets/choose-the-message.txt` was executed in this
repository's `tools/apple1_emulator.py` during authoring.

| Input | `screen_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---:|
| `Y` + CR | `Y` | true | 9 |
| `N` + CR | `N` | true | 10 |
| `Q` + CR | `N` | true | 10 |

The trailing carriage return is required by the harness, which rejects input not
ending in CR. The program reads only the first key, so the CR is never consumed.

This is off-device software evidence about 25 bytes. Per E-EMU-SCOPE it is not
evidence about hardware.

## The Part E flaw is deliberate

The three-path answer in `ANSWERS.md` contains a fall-through bug, and the answer
key says so and uses it to derive the "n paths need n minus 1 jumps" rule. It
should not be silently corrected; the rule is the teaching content and the flaw
is how the lesson earns it.

## Deliberate simplifications

1. **Only the zero and negative flags are covered.** `CMP` also sets the carry
   flag, which is how greater-than and less-than are tested. The lesson says so
   and defers it.
2. **`CMP` is described as "a subtraction it throws away."** Accurate for the
   flags this lesson uses, and it omits the carry behavior.
3. **The always-taken `BNE` in Part E is shown and then discouraged.** It is a
   real technique; presenting it without the caveat would be worse than omitting
   it.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-17 (new).** The A04 program's runs are recorded here and in
  `../EMULATOR-RUNS.md`, but the program is a teaching artifact written for this
  lesson and is not part of `software/ram-only/`. It carries no hardware
  authority of any kind and should not be promoted into the software library
  without going through that library's own acceptance process.
- **V-8 applies.** The program has not run on this board.

## What this lesson does not establish

Nothing about this project's machine. The program is not supplied as a `.hex`
artifact and no entry procedure appears in this packet. It authorizes no firmware
load, EEPROM write, CFFA1 write, serial-port open, or physical modification.
