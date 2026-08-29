# C04 Status

**Mode: OFF-DEVICE**

No runnable artifact. Characters are converted with pencil and paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/char-journey.txt` | Plain-text diagram, 40 columns | No |
| `assets/encoding-worksheet.txt` | Plain-text worksheet, 40 columns | No |

The byte lists in Parts B and C are text encoded as an exercise. They are not
programs, they are not intended for entry at any address, and they would not do
anything if entered.

## Expected result

A learner completes a six-row character table, decodes `HI THERE` from a
high-bit byte list, and encodes `APPLE`. All determinate, all keyed.

## Known limitations

- The high-bit convention is documented behavior from the Monitor listing and
  Owad's keyboard section. It has not been measured on this project's board.
- The emulator's handling of `--input` was read from the tool's own
  documentation and helper, not from a full audit. Recorded as V-10.
- Lower case is discussed but the library takes no position on whether a machine
  should convert it, following the repository's firmware behavior model.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.
