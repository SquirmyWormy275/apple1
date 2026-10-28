# B01 Status

> **Current host evidence (October 28, 2026):** The original paper activity
> remains available. [The BASIC chapter](../../textbook/reference/basic.md)
> now runs the preserved interpreter on a modeled NMOS 6502. U01–U06 retain
> actual sessions; U02 checks conversion bounds and U04 checks one-based arrays.
> V-20 and V-21 are resolved for these identified host sessions. Older "not run"
> notes below describe the earlier edition; they do not describe current host
> capability. Physical installation and execution remain unverified.

**Mode: OFF-DEVICE**

No runnable artifact. The original packet is a paper exercise; the new host interpreter labs are linked below.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/same-job-two-ways.txt` | Plain-text comparison, 40 columns | No |

The BASIC lines are quoted from published examples. The assembly side is written
as pseudocode rather than a byte listing, deliberately, so that nothing in this
packet resembles an enterable program.

## Expected result

Five task-to-language matches with reasons, plus determinate answers for the
true/false and cost/benefit parts. `ANSWERS.md` supplies a model answer and
reasoning for the open-ended items.

## Known limitations

- The original paper examples were cited. Current U01–U06 execute the identified interpreter; see the notice above.
- How Apple-1 BASIC internally represents or executes a program is not described,
  because no project source documents it.
- Krusader is located in the landscape but not taught.
- ROM-contents claims come from manuals for the Replica I and the Replica 1 Plus,
  not from this board (V-4).

## Stop condition

Not applicable. No device interaction, and nothing in this packet is runnable.

If a learner has access to a machine with BASIC in ROM and wishes to try these
lines, that is outside this lesson entirely and is governed by
`docs/preservation-dossier.md` and `docs/apple1-software-library.md`. This packet
grants nothing toward it.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No typing of any BASIC line on hardware.
