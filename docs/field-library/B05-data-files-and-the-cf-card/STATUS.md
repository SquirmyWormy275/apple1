# B05 Status

**Mode: OFF-DEVICE**

No runnable artifact. **No card is inserted, read, or written at any point.**

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/three-kinds.txt` | Plain-text reference card, 40 columns | No |

## Expected result

Six files sorted with reasons, plus determinate answers for the hash table and
the proximity exercise. `ANSWERS.md` supplies worked answers throughout,
including for the two open-ended parts.

The intended insight in Part A is that a SHA-256 manifest cannot establish its
own integrity.

## Known limitations

- **No card mechanism is assumed or described.** The curriculum states that the
  boot and menu mechanism is intentionally undecided, and this packet does not
  decide it. Part F makes that absence the exercise.
- The three-kind scheme is coarser than real archival practice.
- Manifest self-integrity is not addressed anywhere in this project's
  documentation and is raised as an open question (V-23).
- The sample retention note contains genuine "not recorded" gaps, including the
  Briel manual's retrieval date and route, and carries forward the unresolved
  manual filename discrepancy (V-6).

## Stop condition

Not applicable. No device interaction and no card handling.

## What this status does not authorize

No firmware load. No EEPROM write. **No CFFA1 write.** No serial-port open. No
physical modification. No insertion, reading, or writing of any card, and no
assumption that a card workflow exists.
