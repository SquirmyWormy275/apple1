# A04 Status

**Mode: OFF-DEVICE**

No new runnable artifact in `software/ram-only/`. A 25-byte teaching program
appears as a listing in a worksheet and was executed off-device during authoring.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/choose-the-message.txt` | Plain-text worksheet, 40 columns | Traced on paper; optionally rehearsed off-device |
| `assets/flag-card.txt` | Plain-text reference card, 40 columns | No |

**The program has no hardware authority.** It is a teaching example written for
this lesson, not a repository artifact. It is not added to `software/ram-only/`,
it has not gone through that library's acceptance card, and this packet contains
no entry procedure.

## Expected result

Exact, and observed during authoring:

| Input | Screen | Returned | Instructions |
|---|---|---|---:|
| `Y` + CR | `Y` | true | 9 |
| `N` + CR | `N` | true | 10 |
| `Q` + CR | `N` | true | 10 |

The harness requires input ending in a carriage return. The program reads one key
and never consumes the CR.

## Known limitations

- Zero and negative flags only. `CMP` also sets the carry flag, used for
  greater-than and less-than comparisons, which this lesson does not cover.
- The Part E three-path answer contains a deliberate fall-through flaw, used to
  derive the jump-counting rule. Do not silently correct it.
- The program is a teaching artifact with no hardware authority (V-17).

## Stop condition

Not applicable to the paper work. For optional off-device rehearsal, M03's stop
condition applies: a result differing from the table above is a software finding
to record per `docs/emulator-demo-guide.md`, not a reason to approach hardware.
No machine state exists to recover.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No entry of this program on hardware, and no promotion of
it into `software/ram-only/` without that library's own acceptance process.
