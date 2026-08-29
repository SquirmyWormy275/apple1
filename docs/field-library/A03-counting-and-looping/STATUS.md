# A03 Status

**Mode: OFF-DEVICE**

No new runnable artifact. Two eleven-byte programs appear as listings in a
worksheet and were executed off-device during authoring.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/countdown-trace.txt` | Plain-text worksheet, 40 columns | Traced on paper |
| `assets/offset-card.txt` | Plain-text reference card, 40 columns | No |

Neither program is supplied as a `.hex` file, neither is added to
`software/ram-only/`, and this packet contains no entry procedure.

## Expected result

Determinate, and observed during authoring:

| Program | `DEX` passes | Final X | `$0400` | Instructions |
|---|---:|---|---|---:|
| A (`BNE`) | 5 | `$00` | `$00` | 13 |
| B (`BPL`) | 6 | `$FF` | `$FF` | 15 |

Part F's answer is that the loop shown is **correct**. That item is a deliberate
inverse trap and should not be edited into containing a real bug.

## Known limitations

- Only the zero and negative flags are covered.
- Only bottom-tested loops are covered.
- The recorded results come from a direct `py65` reproduction rather than a run
  of the repository harness (V-16), because neither program reads the keyboard.

## Stop condition

Not applicable to the paper work. If a learner reproduces these programs in a
simulator and gets different values, that is a software discrepancy to record per
`docs/emulator-demo-guide.md`. It is not a reason to approach hardware, and no
machine state exists to recover.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No entry of either program on hardware.
