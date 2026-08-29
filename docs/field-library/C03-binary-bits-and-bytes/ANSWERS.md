# C03 Answer key

## Part A: build six bytes

| Number | Binary | Working |
|---:|---|---|
| 65 | `0100 0001` | 64 + 1 |
| 200 | `1100 1000` | 128 + 64 + 8 |
| 128 | `1000 0000` | 128 alone. Only bit 7. |
| 255 | `1111 1111` | Every bit set. |
| 13 | `0000 1101` | 8 + 4 + 1 |
| 141 | `1000 1101` | 128 + 8 + 4 + 1 |

**The difference between 13 and 141 is bit 7, and nothing else.** That is the
answer to the question at the bottom of the worksheet, and it is the single most
useful fact in this lesson.

## Part B: read three back

| Binary | Number | Hex |
|---|---:|---|
| `0010 0000` | 32 | `$20` (a space) |
| `0111 1111` | 127 | `$7F` (the largest seven-bit value) |
| `1000 0001` | 129 | `$81` |

## Part C: the nibble shortcut

| Binary | Hex |
|---|---|
| `0000 1111` | `$0F` |
| `1010 0101` | `$A5` |
| `1111 0000` | `$F0` |
| `1000 1101` | `$8D` |
| `1101 0000` | `$D0` |

`$D0` is worth noticing: it is the high byte of every PIA address in this
library, `$D010` through `$D013`.

## Part D: one bit at a time

| From | To | Bit changed | Worth |
|---|---|---|---|
| `$0D` | `$8D` | Bit 7 | 128 |
| `$41` | `$61` | Bit 5 | 32 |
| `$7F` | `$FF` | Bit 7 | 128 |

The middle row is the ASCII upper-to-lower-case shift: `A` is `$41`, `a` is
`$61`, and one bit separates them. This matters for C04, and it matters for a
machine that only understands upper case.

## Part E: is bit 7 set?

| Value | Bit 7 set? |
|---|---|
| `$0D` | No |
| `$8D` | Yes |
| `$41` | No |
| `$C8` | Yes |
| `$7F` | No |
| `$80` | Yes |
| `$FF` | Yes |
| `$00` | No |

**Why the rule works:** the first hex digit is the top four bits, and bit 7 is
worth 8 within that nibble. So the first digit is 8 or more exactly when bit 7
is set.

## Part F: the counting trap

**The error is the range, not the arithmetic.** 2 to the eighth is 256, and that
is the count of possible values. But the values run 0 through 255. If 256 were
included there would be 257 of them. Off-by-one errors of exactly this shape are
covered again in A03.

## Try a variation: checking one bit

Comparing the whole byte asks "is this value exactly equal to that value."
Checking one bit asks "is this particular flag on," and it does not care what
the other seven bits are doing.

If a program compared the whole display register against a number, it would only
match when every other bit happened to hold the expected value too. Those bits
belong to the character being sent and are not predictable, so the comparison
would fail almost always and succeed by coincidence occasionally. The program
would appear to work intermittently, which is the worst kind of broken.

## README: Check your understanding

1. **100 is `0110 0100`.** Split it: `0110` is 6, `0100` is 4, so `$64`.
2. **`0100 0001` is 65, `$41`, and the character `A`.**
3. **It sets bit 7 and leaves the other seven bits alone.** That is why `$0D`
   plus 128 is `$8D` and still recognizably a carriage return underneath.
