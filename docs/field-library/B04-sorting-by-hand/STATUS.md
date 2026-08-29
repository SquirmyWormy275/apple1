# B04 Status

**Mode: OFF-DEVICE**

No runnable artifact. The sorting is done with physical cards on a table.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/sort-trace.txt` | Plain-text worksheet, 40 columns | No |

**No sorting program exists in this packet.** Part G asks for a description in
English and explicitly instructs the learner not to write any bytes.

## Expected result

Fully determinate and hand-checkable:

| Starting order | Passes | Comparisons | Swaps |
|---|---:|---:|---:|
| `5 3 1 4 2` | 4 | 16 | 7 |
| `1 2 3 4 5` | 1 | 4 | 0 |
| `5 4 3 2 1` | 5 | 20 | 10 |

Selection-sort comparison count for five cards: 10.

Growth prediction table: 5 cards up to 20 comparisons, 10 up to 90, 20 up to 380,
100 up to 9,900.

`ANSWERS.md` includes a pass-by-pass walk-through of Part A so an educator can
check a learner's counts rather than only the totals.

## Known limitations

- No asymptotic notation, per the curriculum brief.
- Only two sorting rules; stability and memory use are not discussed.
- The README's "visible wait" remark is qualitative reasoning with no timing
  figure attached, and none should be added without a source (V-22).

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.
