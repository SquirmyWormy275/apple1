# R02 Status

**Mode: OFF-DEVICE**

No runnable artifact. Frames are drawn on paper and have not been displayed.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/frame-sheet.txt` | Plain-text frame worksheet, 40 columns | No |

## Expected result

Frames 4, 5, and 6 at columns 13, 17, and a decision at the wall. The rule is
"move four columns right." State is two numbers: position and direction.

Part D's ball-and-paddle answer is three numbers, not four, which is the intended
insight.

## Known limitations

- **No timing claim is made anywhere in this packet**, for any machine. No frame
  rate, no character speed, no smoothness. Nobody in this project has measured
  any of it, and Part F trains learners to reject such claims including one that
  carries a plausible-looking number.
- **The write-once display constraint is sourced for the original Apple-1 only.**
  Whether it holds on the Propeller-based Replica 1 Plus is unverified, and the
  learner text is phrased more loosely than the source supports (V-25).
- The 20-column frame field is a worksheet convenience and implies no display
  dimension.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. Nothing here is displayed on or sent to the Replica 1
Plus, and no design in this packet should be treated as implementable until the
display behavior it would depend on has been measured.
