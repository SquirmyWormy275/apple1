# S03 Answer key

## Part A

See `assets/hex-table-filled.txt`. 0 to 9 unchanged; 10 to 15 become A to F.

## Part B: decimal to hex

| Decimal | Hex | Working |
|---:|---|---|
| 8 | `$08` | Under 16, so one digit, padded to two. |
| 15 | `$0F` | 15 is F. |
| 16 | `$10` | One group of sixteen, no ones. |
| 17 | `$11` | One sixteen and one. |
| 32 | `$20` | Two sixteens. |
| 64 | `$40` | Four sixteens. |
| 100 | `$64` | 100 / 16 = 6 remainder 4. |
| 128 | `$80` | 128 / 16 = 8 remainder 0. |
| 200 | `$C8` | 200 / 16 = 12 remainder 8; 12 is C. |
| 255 | `$FF` | 255 / 16 = 15 remainder 15. |

## Part C: hex to decimal

| Hex | Decimal | Working |
|---|---:|---|
| `$05` | 5 | |
| `$0D` | 13 | |
| `$10` | 16 | 1 x 16 + 0 |
| `$1F` | 31 | 1 x 16 + 15 |
| `$41` | 65 | 4 x 16 + 1 = 64 + 1 |
| `$7F` | 127 | 7 x 16 + 15 = 112 + 15 |
| `$80` | 128 | 8 x 16 + 0 |
| `$8D` | 141 | 8 x 16 + 13 = 128 + 13 |
| `$C8` | 200 | 12 x 16 + 8 = 192 + 8 |
| `$FF` | 255 | 15 x 16 + 15 |

`$8D` is worth pausing on. It is `$0D`, the carriage return, plus `$80`. You
will meet it again in the M-series, where it is exactly that: a carriage return
with the top bit set.

## Part E: the odd one out

**`$F1` is the odd one out.** `$1F`, 31, and 16 + 15 are all thirty-one. `$F1`
is 15 x 16 + 1 = **241**. Reversing two hex digits does not reverse the number,
it changes it completely, which is why transcription order matters when copying
a byte list.

## Part F: why not base 10

One version: computers store information in fixed-size chunks, and one chunk
holds exactly 256 different values. Sixteen times sixteen is 256, so two hex
characters describe one chunk exactly, always. Decimal does not divide evenly
into that, so numbers would sometimes be two characters and sometimes three, and
you could not tell where one chunk ended.

Accept any answer built on "hex lines up with the size of the storage." Do not
accept "hex is what computers use internally." It is not. It is a convenient way
for people to write down what computers use internally.

## Try a variation: `$D010` and `$D012`

They are **two apart**. Only the last digit differs, 0 against 2, and the last
digit is the ones column in both numbers, so the difference is 2 minus 0. No
conversion to decimal is needed, which is exactly the convenience hex buys.

## README: Check your understanding

1. 12 = `$0C`, 16 = `$10`, 31 = `$1F`, 100 = `$64`, 255 = `$FF`.
2. `$0A` = 10, `$20` = 32, `$7F` = 127, `$8D` = 141.
3. **Because the width never changes.** Every byte is two characters, so a list
   of bytes lines up in columns, a missing or extra digit is visible
   immediately, and you can count bytes by counting character pairs.
