# S03 Activity: hex drill

**Status:** OFF-DEVICE. Paper and pencil. Nothing is powered on.

## Part A: the table (this is the first result)

Fill in `assets/hex-table-blank.txt` for 0 through 15, then check against
`assets/hex-table-filled.txt`.

## Part B: decimal to hex

| Decimal | Hex |
|---:|---|
| 8 | |
| 15 | |
| 16 | |
| 17 | |
| 32 | |
| 64 | |
| 100 | |
| 128 | |
| 200 | |
| 255 | |

## Part C: hex to decimal

| Hex | Decimal |
|---|---:|
| `$05` | |
| `$0D` | |
| `$10` | |
| `$1F` | |
| `$41` | |
| `$7F` | |
| `$80` | |
| `$8D` | |
| `$C8` | |
| `$FF` | |

## Part D: the landmark trick

Some hex values show up constantly. Learn these five and most addresses become
readable at a glance.

| Hex | Decimal | Why it matters |
|---|---:|---|
| `$0D` | 13 | Carriage return, the Enter key |
| `$20` | 32 | Space, and the first printable character |
| `$41` | 65 | Capital A |
| `$80` | 128 | The top bit of a byte on its own |
| `$FF` | 255 | Every bit set, the largest byte |

Cover the decimal column and recite it. Then cover the hex column and go the
other way.

## Part E: the odd one out

Three of these four are the same number written differently. Which one is not,
and what is it instead?

`$1F` &nbsp;&nbsp; 31 &nbsp;&nbsp; `$F1` &nbsp;&nbsp; 16 + 15

## Part F (optional): why not base 10

In two or three sentences, explain to someone who has never programmed why the
Apple-1's manuals use hex instead of ordinary decimal. Do not use the word
"binary." `ANSWERS.md` has one version to compare against.

## What this activity does not do

It is number conversion practice. It measures nothing and authorizes no hardware
action.
