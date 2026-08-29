# S04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## The three worked statements

| Statement | Basis | Key |
|---|---|---|
| (a) Monitor occupies 256 bytes at `$FF00`-`$FFFF` | Published design documentation | M-ROM |
| (b) This board's EEPROM contains `110REV03` | Deliberately unresolved. The repository states the vendor source is candidate evidence only | E-110REV03 |
| (c) Opening the FT232R garbled the display | Recorded in the repository as a `STOP` result | E-FT232-STOP |

Statement (b) is used as a teaching example precisely because it is open. This
lesson does not resolve it and must not be edited to imply that it has been
resolved.

## Part B items

| # | Basis | Key |
|---|---|---|
| 1 | Retail price | H-PRICE |
| 3 | Serial parameters as documented | R-SERIAL |
| 4 | Recorded emulator run | `../EMULATOR-RUNS.md`, RUN |
| 6 | Keyboard register address | P-KBD |
| 7 | Dated host-side observation | REPO `docs/hardware/plus-io-map.md` |
| 8 | The USB serial value is non-unique | REPO `docs/hardware/plus-io-map.md` |
| 9 | Production count, and the three distinct counts | H-MADE, H-SOLD, H-BYTESHOP, V-2 |

Items 2, 5, and 10 rest on no source, which is the answer.

## Part D items

| # | Fact half | Model half | Key |
|---|---|---|---|
| 1 | Garbage screen on power-up is documented behavior | Health of the video circuitry is not established by it | R-RESET |
| 2 | Hashing establishes file identity at capture time | Not that the file describes the installed image | E-NOPROOF, REPO `docs/collection-archive.md` |
| 3 | RESET produces a backslash | Not that the ROM is any particular image | R-RESET, E-110REV03 |

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-2 applies directly** to Part B item 9 and is the reason the answer key
  spells out that "made," "sold," and "purchased by the Byte Shop" are three
  different numbers.
- **V-8 applies** to statements (b), and Part B items 2, 5, and 10. This lesson
  does not close any of them and is written so that a future editor cannot
  quietly close them either.

## What this lesson does not establish

It resolves no open question about this machine. It teaches a sorting habit.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification, and statement (c) is a record of something that already
happened, not a procedure to repeat.
