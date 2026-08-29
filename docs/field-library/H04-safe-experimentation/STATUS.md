# H04 Status

**Mode: OFF-DEVICE**

No runnable artifact. Sorting on paper. Nothing is powered on, connected, or
changed at any point.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Sorting worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations, one row per boundary | No |
| `assets/decision-card.txt` | Green/amber/red reference card, 40 columns | No |

## Expected result

Six actions sorted, then ten more. All determinate and keyed. The intended
insights are that action 4, opening the FT232R "to see what happens," is red
rather than curious, and that Part B item 5 shows some actions are red as
*writing* and not only as doing.

## Known limitations

- **This lesson restates boundaries; it does not create or lift them.** If the
  project's documents change, this packet must be updated to match rather than
  becoming a second, divergent statement of the rules.
- The FT232R account is summarized from the preservation dossier's "Current
  boundaries." The primary record with date, operator, and exact observation is
  elsewhere in the project (V-13).
- The third row of Part C answers honestly that no current document provides a
  process for an EEPROM action, which is different from a process nobody has
  completed.

## Stop condition

Not applicable to this packet: no device interaction occurs at any point.

The stop rule this lesson restates, unchanged from
`docs/preservation-dossier.md`: if the display changes, a reset occurs,
identities drift, or bytes mismatch, record `STOP`, recover to the known monitor
state, and do not continue a test sequence.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine.

**No procedure for any amber or red action appears anywhere in this packet.**
Categories are named so a reader can recognise them; none is described. This
lesson grants no authority, lifts no block, and advances nothing toward a live
session. Completing it changes nothing about what anyone is permitted to do.
