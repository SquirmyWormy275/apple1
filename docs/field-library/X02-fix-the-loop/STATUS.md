# X02 Status

**Mode: OFF-DEVICE**

No new artifact in `software/ram-only/`. Two fifteen-byte teaching programs
appear as listings and were executed off-device during authoring.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/broken-loop.txt` | Program listing and trace table, 40 columns | Traced on paper; optionally rehearsed off-device |

**Neither program has hardware authority.** Both were written for this lesson,
neither is added to `software/ram-only/`, neither has been through that library's
acceptance card, and this packet contains no entry procedure. Part E instructs the
learner to use scratch copies and not to add either program to the software
library.

## Expected result

Exact, and observed during authoring:

| Version | Bytes at `$0308` | Buffer | Instructions | Returned |
|---|---|---|---:|---|
| As written | `C0 06` | `AAAAAA`, six | 27 | true |
| Corrected | `C0 05` | `AAAAA`, five | 23 | true |

Paper trace: six stores at `$0400` to `$0405` before the fix, five at `$0400` to
`$0404` after.

**The bug is one byte: `06` at `$0309` should be `05`.**

## Known limitations

- **Exactly one bug is planted**, per the X02 brief. The corrected version was
  run to confirm it does what the stated intention says, so a correct fix
  produces a clean result.
- Part G item 3 raises a case where the specification rather than the code may be
  wrong. The answer key deliberately does not resolve it, because resolving it
  requires knowing what was intended.
- Both programs are teaching artifacts with no hardware authority (V-33).

## Stop condition

Not applicable to the paper work. For optional off-device rehearsal, M03's stop
condition applies: a result differing from the table above is a software finding
to record per `docs/emulator-demo-guide.md`, not a reason to approach hardware.
No machine state exists.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No entry of either program on hardware, and no addition of
either to `software/ram-only/` without that library's own acceptance process.
