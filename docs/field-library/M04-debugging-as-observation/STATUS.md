# M04 Status

**Mode: OFF-DEVICE**

No runnable artifact of its own. Any testing a learner chooses to do happens in
the M03 emulator on an ordinary computer.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/observation-sheet.txt` | Plain-text worksheet, 40 columns | No |

## Expected result

A learner produces a filled two-column sheet and one falsifiable hypothesis.
Parts B through E have determinate answers; Parts A and F are keyed with a model
answer and an acceptance criterion rather than a single string.

## Known limitations

- **The Part A scenario is hypothetical.** The empty-buffer failure did not
  occur. It is constructed because it is what the M02 transcription error would
  produce. All recorded runs passed.
- The FT232R account is summarized from the preservation dossier. The primary
  record with date, operator, and exact observation is elsewhere in the project.
  Recorded as V-13.
- "Change one thing" is taught without its exceptions.

## Stop condition

The lesson's subject *is* the stop condition. The rule it teaches, unchanged from
`docs/preservation-dossier.md`: if the display changes, a reset occurs,
identities drift, or bytes mismatch, record `STOP`, recover to the known monitor
state, and do not continue a test sequence.

For this packet itself there is nothing to recover, because no machine is
involved at any point.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine.

**Specifically: the FT232R incident described in this lesson must not be
reproduced.** It is recounted as a recorded past observation. An opened serial
session or transmit test remains blocked until a measurement test card is ready
and an operator explicitly starts that single step, per
`docs/preservation-dossier.md`.
