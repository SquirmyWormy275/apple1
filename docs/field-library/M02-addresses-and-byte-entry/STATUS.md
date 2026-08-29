# M02 Status

**Mode: OFF-DEVICE**

No runnable artifact. This packet is reading practice on an existing listing.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/listing-anatomy.txt` | Plain-text diagram, 40 columns. Invented example, labeled as such on its face | No |
| `assets/marking-worksheet.txt` | Plain-text worksheet, 40 columns. Quotes an existing repository artifact | No |

**This packet creates no new program artifact.** It quotes
`software/ram-only/line-input-0300.hex` for reading and adds nothing to
`software/ram-only/`.

**It contains no entry procedure.** The lesson teaches how to work out which
address a byte belongs to. It gives no instruction to enter a byte, and
`ACTIVITY.md` states at the top that nothing in it is to be typed on a machine.

## Expected result

Determinate throughout: load address `$0300`, 26 bytes, last byte at `$0319`,
instruction split after `EB`, and a fixed byte-at-address table. All keyed in
`ANSWERS.md` with working shown.

## Known limitations

- Relative-offset arithmetic is used in Part D but not derived. A03 covers it.
- The relocatability finding in Part D applies to this listing only and is stated
  that way. It is not a general property of repository artifacts.

## Stop condition

Not applicable. No device interaction, and no step of this lesson brings a
learner near the hardware.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No byte entry on hardware of any kind.
