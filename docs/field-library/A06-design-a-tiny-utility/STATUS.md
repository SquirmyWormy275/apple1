# A06 Status

**Mode: OFF-DEVICE**

No runnable artifact is supplied. Learners design programs on paper and may
optionally rehearse their own designs in the M03 emulator on an ordinary
computer.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Design brief and review checklist | No |
| `ANSWERS.md` | Worked example and acceptance criteria | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/design-card.txt` | Blank design card, 40 columns | No |

The thirteen-byte worked example in `ANSWERS.md` is a listing inside an answer
key. It is not supplied as a `.hex` file, is not added to `software/ram-only/`,
and has not been executed (V-19).

## Expected result

A completed design card. Design work has no single correct answer, so
`ANSWERS.md` supplies a fully worked example plus explicit acceptance criteria
for each of the eight sections, so an educator can judge a card consistently.

The retrospective card for `line-input-0300.hex` in Part H has determinate
content and is fully worked.

## Known limitations

- The worked example is hand-traced rather than observed (V-19).
- The card records no timing, and the library makes no timing claims.
- Section 8 records an intention only. It is not a gate and does not interact
  with the acceptance card in `docs/apple1-software-library.md`.

## Stop condition

Not applicable to the paper work. If a learner rehearses their own design in the
emulator, M03's stop condition applies: a mismatch between expected and observed
is a finding to record, not a reason to approach hardware.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.

**Specifically: completing a design card, including writing RAM-ONLY in section
8, grants no authority of any kind.** Any program a learner designs here is
off-device. Moving anything beyond that is a separate, operator-led decision
under `docs/apple1-software-library.md`.
