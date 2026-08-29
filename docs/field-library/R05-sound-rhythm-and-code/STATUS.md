# R05 Status

**Mode: OFF-DEVICE**

No runnable artifact. **No sound artifact exists in this repository**, and
nothing in this packet is played by any machine. The rhythms are clapped by the
learner.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/rhythm-grid.txt` | Plain-text worksheet, 40 columns | No |

The bytes in this packet encode rhythms for a person to read and clap. They are
not programs, are not intended for entry at any address, and would do nothing if
entered.

## Expected result

Determinate:

| Row | Bits | Hex |
|---|---|---|
| `X . . . X . . .` | `1000 1000` | `$88` |
| `X . X . X . X .` | `1010 1010` | `$AA` |
| `X . . X . . X .` | `1001 0010` | `$92` |

Decoding table in Part B is fully keyed. Parts D and G are open-ended with stated
acceptance criteria.

## Known limitations

- **This lesson is conceptual throughout, deliberately.** The curriculum brief
  asks for that unless a verified, compatible sound artifact is added, and none
  has been.
- **Whether either machine has any sound capability is unknown to this library**
  (V-27). No source here addresses it, and the lesson states "not addressed"
  rather than "no."
- Pitch is not encoded. Only equal-length slots are considered.
- The bit-order convention is stated by the worksheet and is not intrinsic to the
  encoding, which Part D demonstrates.

## Stop condition

Not applicable. No device interaction, nothing runnable, and no sound produced by
anything other than the learner's hands.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification.

**If a sound artifact is ever added to this project, this lesson does not cover
it.** Such an artifact would need its own source, exact file, expected result,
status label, and stop condition before any lesson could describe playing it.
