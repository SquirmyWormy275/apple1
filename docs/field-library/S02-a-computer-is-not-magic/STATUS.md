# S02 Status

**Mode: OFF-DEVICE**

No runnable artifact. Nothing in this packet is entered, loaded, transmitted, or
executed anywhere.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Paper worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/key-to-screen.txt` | Plain-text diagram, 40 columns | No |
| `assets/trace-blank.txt` | Plain-text worksheet, 40 columns | No |

The assets contain no program bytes and no entry instructions. The three
addresses they discuss (`$D010`, `$D011`, `$D012`) appear as reading material
only, and the lesson gives no procedure for accessing them on hardware.

## Expected result

A learner fills five blanks in the correct order on paper. There is no machine
state and nothing to recover.

## Known limitations

- The trace describes the documented Apple-1 design. Replica video and keyboard
  handling is known to differ on Propeller-based boards, and this packet does
  not model that path.
- Page-number citations inherit the shared pool's unverified-pagination note.

## Stop condition

Not applicable. No device interaction occurs, so no reset, recovery, or `STOP`
entry can arise from this lesson.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine.
