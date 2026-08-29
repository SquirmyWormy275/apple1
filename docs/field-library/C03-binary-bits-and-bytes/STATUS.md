# C03 Status

**Mode: OFF-DEVICE**

No runnable artifact. Bits are built with pencil, paper, and optionally coins.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Drill worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/bit-strip.txt` | Printable bit strip, 40 columns | No |
| `assets/bit-drill.txt` | Plain-text worksheet, 40 columns | No |

All assets observe the 40-column upper-case rule and pass `format_for_apple1`
40. An eight-column table with borders cannot fit an Apple-1-sized line, and
splitting it across two lines would destroy the one thing the strip is for.
It is a print-and-cut worksheet, not display material, and the curriculum's
40-column rule applies to material intended for the Apple-1-sized display.
`assets/bit-drill.txt` observes the 40-column rule.

## Expected result

A learner builds six bytes from column values and reads three back. Every item
has one correct answer, with working shown in `ANSWERS.md`.

## Known limitations

- Bytes are treated as unsigned, 0 to 255, throughout. Signed interpretation is
  deferred to A03.
- The lesson explains what bits are but teaches no instruction for testing or
  setting them.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.
