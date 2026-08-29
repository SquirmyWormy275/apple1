# R04 Status

**Mode: OFF-DEVICE**

No runnable artifact. The lesson stops at design; nothing is implemented.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Design brief | No |
| `ANSWERS.md` | Worked example and acceptance criteria | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/story-map.txt` | Plain-text map worksheet, 40 columns | No |

## Expected result

A four-room map in which every room is reachable, every dead end is an ending,
and a reachable ending exists. `ANSWERS.md` supplies a fully worked map with its
exit table and state count, plus acceptance criteria for each part.

The intended insight in Part D is that a small world's entire memory is one byte
of flags plus a position.

## Known limitations

- **Parsing is not covered.** How a program would interpret what the player typed
  is outside this lesson.
- **No implementation is discussed**, in any language.
- Room description lengths are not constrained in the exercise, though a
  40-column display would constrain them in practice.
- Faults 5 and 6 in Part F cannot be found from the map alone and need a separate
  flag list, which the answer key describes.

## Stop condition

Not applicable. No device interaction and nothing runnable.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.
