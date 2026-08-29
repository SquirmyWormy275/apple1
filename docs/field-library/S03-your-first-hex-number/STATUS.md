# S03 Status

**Mode: OFF-DEVICE**

No runnable artifact. This lesson is arithmetic practice on paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Drill worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/hex-table-blank.txt` | Plain-text worksheet, 40 columns | No |
| `assets/hex-table-filled.txt` | Plain-text answer, 40 columns | No |

## Expected result

A learner completes a sixteen-row conversion table and two conversion drills.
Every item has a single correct answer, listed in `ANSWERS.md` with working
shown.

## Known limitations

- The lesson covers 0 to 255 and four-digit addresses. It does not cover
  negative numbers, two's complement, or signed byte interpretation. Those
  matter for the branch instructions in A03 and A04 and are introduced there.
- Binary is mentioned only in passing. C03 covers it properly.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.
