# X01 Status

**Mode: OFF-DEVICE**

No runnable artifact. Two dumps read on paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Hunt questions | No |
| `ANSWERS.md` | Separate answer page, to stay closed until attempted | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/hunt-sheet.txt` | Two dumps and five hints, 40 columns | No |

**Neither dump is a reading from a machine.**

- **Dump One** reproduces `software/ram-only/line-input-0300.hex` unmodified,
  laid out eight bytes per line with addresses. The bytes are real; the display
  is a formatting of a file, not a memory capture.
- **Dump Two** is invented for this puzzle and carries a disclaimer on the sheet
  directly above it.

Hints are on the worksheet rather than in the answer key, so a stuck learner can
get help without ending the search. The answer key is a separate file, as the X01
brief requires.

## Expected result

Determinate throughout. Key values: byte `10` at `$0305`, byte `20` at `$030D`,
last byte at `$0319`, last instruction `4C 1F FF` at `$0317` jumping to `$FF1F`,
`JSR $FFEF` at `$030D`, 26 bytes total, 15 with bit 7 set, and Dump Two spelling
`WELL DONE` followed by a carriage return.

## Known limitations

- **V-32 superseded:** Part C now defines the count precisely and asks for five.
  Learners assess a separate claim of four instead of receiving an incorrect
  instruction. The high-bit count is corrected from 14 to 15 (C8 was omitted).
- Dump One's Monitor-style layout could be mistaken for a memory capture. Part F
  question 15 makes that an examinable point, and both the sheet and these notes
  state it plainly.

## Stop condition

Not applicable. No device interaction, and no address in this packet is offered
for inspection on hardware.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. **Neither dump may be cited as a reading from any
machine.**
