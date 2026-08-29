# R01 Status

**Mode: OFF-DEVICE**

No runnable artifact. Banners are drawn on paper and have not been displayed
anywhere.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/grid-40.txt` | Printable 40-column grid with column ruler | No |
| `assets/banner-examples.txt` | Three worked banners, 40 columns | No |

Both assets were checked against `tools/apple1_text.format_for_apple1` during
authoring and pass unchanged: upper case, printable seven-bit ASCII, no line over
40 columns, no `?` substitutions.

## Expected result

A banner within 40 columns using upper-case printable ASCII. Parts B, C, E, and F
have determinate answers. Parts A, D, and G are design work, keyed with
acceptance criteria plus a worked example that meets all of them.

## Known limitations

- **The 40-column canvas is this repository's convention**, from the curriculum
  rule and the formatter's default width, not a cited Apple-1 display
  specification (V-7).
- **No row count is claimed.** The grid's 12 rows are a working area, chosen for
  convenience, and no screen height should be inferred from it.
- Which characters the Apple-1 video ROM can actually render is not established
  by any project source (V-24). The lesson restricts itself to printable ASCII on
  the repository's rule.
- The craft advice about letter widths and weights is judgement, not sourced.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. Nothing in this packet is displayed on, sent to, or typed
into the Replica 1 Plus.
