# C02 Status

**Mode: OFF-DEVICE**

No runnable artifact. The map is read on paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/memory-map.txt` | Plain-text map, 40 columns | No |
| `assets/address-worksheet.txt` | Plain-text worksheet, 40 columns | No |

The map carries an on-diagram notice that it is a documented model rather than a
reading from a board.

## Expected result

A learner assigns six addresses to regions and answers a set of read/write and
byte-interpretation questions, all with determinate answers in `ANSWERS.md`.

## Known limitations

- **The map is a model of the original Apple-1 design.** It is not a survey of
  this project's board, and the Replica 1 Plus differs from both the original
  and from the Replica I that Owad documents.
- The `$0200` Monitor input-line label is an inference from the Monitor listing,
  recorded as verification item V-9 in `SOURCE-NOTES.md`.
- Unused regions are shown stock. Period owners did expand them.

## Stop condition

Not applicable. No device interaction. This packet contains no procedure for
examining memory on a machine, and a learner completing it has no reason to
approach the hardware.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine.
