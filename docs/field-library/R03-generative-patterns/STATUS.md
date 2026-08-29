# R03 Status

**Mode: OFF-DEVICE**

No runnable artifact is supplied. The optional extension asks the learner to
write a short program **on an ordinary computer**, in any language, and states
explicitly that it must not be attempted on the Replica 1 Plus.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/pattern-rules.txt` | Generated patterns, 40 columns | No |
| `assets/rule-worksheet.txt` | Plain-text worksheet, 40 columns | No |

`assets/pattern-rules.txt` was produced by mechanically applying the three stated
rules during authoring, not by drawing, and passes
`tools/apple1_text.format_for_apple1` unchanged.

## Expected result

Fully determinate and hand-checkable:

- Row rule, columns 1 to 12: row 1 solid, row 2 `.#.#.#.#.#.#`, row 3
  `..#..#..#..#`, row 4 `...#...#...#`. Row 3 contains four `#`.
- Triangle rule over six rows produces the nested triangular shape shown in
  `ANSWERS.md`.
- Part C line 4 has more than one valid answer, deliberately.

## Known limitations

- The "no divide instruction" claim rests on absence from OWAD's instruction
  categories rather than a positive statement (V-26).
- Nothing here has been generated on or displayed by any Apple-1 or replica.
- No timing claim is made about generating any of these patterns.
- The 40-column canvas is this repository's convention (V-7).

## Stop condition

Not applicable to the paper work.

For the optional extension on an ordinary computer: if the program's output
differs from the three rows computed by hand, the hand computation is the
reference and the discrepancy is a software finding. There is no machine state
and nothing to recover.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. **The optional programming extension is for an ordinary
computer only** and grants no authority to run anything on the Replica 1 Plus.
