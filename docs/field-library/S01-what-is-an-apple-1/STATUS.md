# S01 Status

**Mode: OFF-DEVICE**

This lesson has no runnable artifact. Nothing in this packet is entered on a
machine, loaded, transmitted, or executed, on the Replica 1 Plus or anywhere
else.

## Artifacts in this packet

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Paper worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/three-parts-blank.txt` | Plain-text worksheet, 40 columns | No |
| `assets/three-parts-labeled.txt` | Plain-text answer diagram, 40 columns | No |

The two `assets/` files contain no bytes for entry, no addresses, and no
program. They are diagrams made of ASCII characters.

## Expected result

A learner writes three words on a worksheet and compares them against a labeled
copy. The result is on their paper. There is no machine state to check and
nothing to recover from.

## Known limitations

- The display text is formatted to 40 columns of upper-case printable ASCII so
  it could be read on an Apple-1-sized display, but it has never been shown on
  one. Formatting for a display is not evidence that a display works.
- Page-number citations in `SOURCE-NOTES.md` are taken from indexed PDF text and
  have not been checked page by page against the local collection copies.

## Stop condition

Not applicable. There is no device interaction, so there is no failure mode that
requires a reset, a recovery, or a `STOP` entry in the chain-of-custody record.

If a learner or operator wants to try anything on the physical machine after
reading this lesson, that is a separate decision governed by
`docs/preservation-dossier.md` and `software/ram-only/README.md`. It requires an
explicit, operator-led approval that this lesson does not grant and cannot
grant.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine. Reading, completing,
or teaching this lesson changes none of that.
