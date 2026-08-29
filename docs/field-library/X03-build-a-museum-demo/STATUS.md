# X03 Status

**Mode: OFF-DEVICE**

No runnable artifact. A script written on paper, for a demonstration that must
itself be off-device.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Script brief | No |
| `ANSWERS.md` | Worked script and acceptance criteria | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/demo-script.txt` | Timed script template with mandatory fallback box, 40 columns | No |

## Expected result

A completed three-minute script whose fallback box is filled in. The worked
example in `ANSWERS.md` uses no machine at any point, which is the standard the
learner's script is judged against.

Part B's hook 3 has two distinct faults, a value claim and an inaccuracy, and
identifying both is the intended insight.

## Known limitations

- **The demonstration designed here must not require the Replica 1 Plus.** In
  this project that is not a precaution against bad luck: an opened serial
  session is blocked, running a program is a separate operator-led step, and the
  RAM-only artifacts carry no live-run authority.
- Three minutes is treated as a fixed constraint, which is what forces the
  one-idea discipline.
- Museum practice questions such as physical display, handling, and case design
  are outside this lesson.

## Stop condition

Not applicable. No device interaction at any point, in the lesson or in the
demonstration it produces.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.

**This lesson grants no authority to power on, connect to, or run anything on the
Replica 1 Plus.** A learner who has written a demo script has written a script.
If a demonstration involving the machine is ever wanted, that is an operator's
decision under `docs/preservation-dossier.md` and
`docs/apple1-software-library.md`, and completing this lesson advances it not at
all.

**No claim about the value or rarity of any object may be made from this
lesson**, and the answer key trains a presenter to decline that question.
