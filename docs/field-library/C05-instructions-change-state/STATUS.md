# C05 Status

**Mode: OFF-DEVICE**

The programs in this packet are paper exercises. One of them was additionally
executed in the repository emulator during authoring, which is off-device
software rehearsal, not a hardware run.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/state-trace.txt` | Plain-text worksheet, 40 columns | Traced on paper |
| `assets/branch-trace.txt` | Plain-text worksheet, 40 columns | Traced on paper |

**Neither program is supplied as a `.hex` artifact and neither is offered for
entry on hardware.** They appear as listings inside worksheets. This packet adds
nothing to `software/ram-only/`.

## Expected result

Deterministic, and recorded:

- Paper trace of `A9 41 69 01 8D 00 04 4C 1F FF`: A ends at `$42` **if the carry
  was clear**, `$43` if it was set. `$0400` receives whichever value A holds.
- The same bytes in `tools/apple1_emulator.py`: `A = $42`, `$0400 = $42`,
  `returned_to_monitor: true`, 4 instructions.
- Branch worksheet: `DEX` runs 3 times, the branch is taken 2 times.

## Known limitations

- **The traced program omits `CLC` before `ADC`, deliberately.** This is a
  teaching defect, not an oversight, and the answer key and `SOURCE-NOTES.md`
  both say so. Do not "fix" the listing without rewriting the lesson around it.
- The emulator's initial carry state is inferred from observed behavior rather
  than a documented guarantee. Recorded as V-11.
- Only the carry and zero flags are covered.

## Stop condition

Not applicable to the paper work.

For the optional emulator rehearsal: if a run produces a value other than the
one recorded above, that is a discrepancy against this packet and should be
retained as a software issue per `docs/emulator-demo-guide.md`. It is not a
reason to approach the hardware, and no recovery procedure is needed because no
machine state exists.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine. A successful
emulator run does not waive any hardware evidence gate.
