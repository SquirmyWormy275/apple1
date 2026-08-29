# C04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## ASCII layer

| Claim | Key |
|---|---|
| ASCII assigns decimal 0 to 127 only; one byte per character | A-ASCII |
| `A` is 65 `$41`, space is 32 `$20`, carriage return is 13 `$0D` | A-CHART |
| Values above 127 are not assigned by the standard | A-ASCII |
| Hex, decimal, binary equivalences used in the tables | A-TABLE |

`B` = 66, `Z` = 90, `0` = 48, and the consecutive ordering of letters and digits
are read directly from the same chart (A-CHART).

## Apple-1 convention layer

| Claim | Key |
|---|---|
| A keypress puts a seven-bit ASCII value on the keyboard data lines | P-KBD-7BIT |
| The Monitor expects the keyboard byte to have bit 7 set | P-HIGHBIT |
| `$8D` is the Monitor's carriage return | W-CR |
| The keyboard character is read from `$D010` after a flag at `$D011` | P-KBD |
| The machine understands upper case only; PS/2 caps lock is on by default | R-UPPER |

## Emulator convention layer

| Claim | Basis |
|---|---|
| The harness takes seven-bit keyboard text on the command line and applies the high-bit convention before the program sees it | REPO `tools/apple1_emulator.py`, the `--input` argument documented as "seven-bit keyboard text ending with CR", and its keyboard-read preparation |
| The harness is ROM-free and models only the keyboard registers plus Monitor `ECHO` and warm entry | E-EMU-SCOPE |
| Recorded transcripts showing `HI\r` as both input and screen text | `../EMULATOR-RUNS.md` |

Separating this third layer explicitly is required by the curriculum brief for
C04, which asks that emulator conventions be distinguished from Apple-1-specific
behavior.

## Repository position on case conversion

The answer key to Part F cites the repository's own stance rather than inventing
one: `docs/firmware-behavior-model.md` records that lower-case conversion,
high-bit conversion, and LF handling are "rejected until measured rather than
guessed." The lesson does not tell a learner which choice is correct.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-8 applies.** The high-bit behavior is documented, not measured on this
  board. The lesson says so in the README and in `STATUS.md`.
- **V-10 (new).** The exact mechanism by which the harness applies the high bit
  was read from the tool's argument documentation and its keyboard-read helper,
  not from a line-by-line audit of the function. The recorded runs are
  consistent with it. A reviewer confirming C04 should read
  `tools/apple1_emulator.py` directly.

## What this lesson does not establish

It does not establish what byte this project's board produces for any keypress.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
