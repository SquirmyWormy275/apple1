# X01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Dump One

The 26 bytes are `software/ram-only/line-input-0300.hex`, reproduced unmodified
and laid out eight per line with addresses, matching the Monitor's own block
display format (R-MON-8).

| Claim | Key |
|---|---|
| The artifact and its load address | E-RAMONLY; REPO `software/ram-only/line-input-0300.hex` |
| Eight locations per line is the Monitor's display format | R-MON-8 |
| `$FF1F` is the Monitor warm entry; `$FFEF` is `ECHO` | W-FF1F, W-FFEF |
| `$D010` and `$D011` are the keyboard registers | P-KBD |
| Little-endian operand ordering | C02, derived |
| Instruction identities (`4C` jump, `20` call, `AD`, `99`) | OWAD Appendix D pp. 247 to 261 |

**Dump One is a file laid out to resemble a memory display.** It is not a
reading taken from any machine's memory, and Part F question 15 makes that an
examinable point rather than a footnote. The distinction is recorded here because
a Monitor-format dump is exactly the kind of artifact that gets mistaken for a
capture later.

## Dump Two

Invented for this puzzle. The bytes encode `WELL DONE` followed by a carriage
return, each character with bit 7 set per C04, padded with `00` to complete the
eight-byte line.

| Claim | Key |
|---|---|
| Characters carry bit 7 set in Monitor terms | P-HIGHBIT, W-CR |
| ASCII values for the letters and space | A-CHART |
| ASCII assigns nothing above 127 | A-ASCII |

`assets/hunt-sheet.txt` states directly above Dump Two that it is invented for the
puzzle and is not a reading from any machine. This follows the M02 brief's
requirement for clearly fictional examples and is repeated in `STATUS.md`.

## The deliberate error in Part C

Part C asks for four referenced addresses and there are five. This is intentional
and the answer key says so, along with which two are most often missed.

A worksheet that quietly contained a wrong count would be a defect. One that
contains a wrong count *and* rewards the learner for catching it is an exercise in
not trusting the question, which is the S04 habit applied to an instruction sheet.

Recorded as **V-32** so no future editor "corrects" it: the Part C count of four
is deliberately wrong and the answer key depends on it.

## The Part D question 10 point

The observation that `D0` is also the `BNE` opcode, but cannot be one here, is
derived: both occurrences fall in the operand position of three-byte instructions,
which is knowable only after establishing instruction boundaries. `D0` as `BNE` is
from OWAD Appendix D p. 258.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-32 (new).** Part C's count of four is a deliberate error.
- **V-8 applies.** Neither dump was read from this board, and Dump One's bytes,
  though real, come from a file rather than from memory.

## What this lesson does not establish

Neither dump is a reading from any machine. No address in this packet is offered
for inspection on hardware, and no entry procedure appears. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
