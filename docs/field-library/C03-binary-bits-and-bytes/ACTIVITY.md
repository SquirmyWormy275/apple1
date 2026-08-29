# C03 Activity: build the byte

**Status:** OFF-DEVICE. Paper and pencil.

## Part A: build six bytes (this is the first result)

Complete the top half of `assets/bit-drill.txt`: 65, 200, 128, 255, 13, 141.

## Part B: read three back

Complete the bottom half: `0010 0000`, `0111 1111`, `1000 0001`.

## Part C: the nibble shortcut

Convert straight to hex by splitting down the middle. No adding.

| Binary | Hex |
|---|---|
| `0000 1111` | |
| `1010 0101` | |
| `1111 0000` | |
| `1000 1101` | |
| `1101 0000` | |

## Part D: one bit at a time

For each, say which single bit changed and what its value is.

| From | To | Bit changed | Worth |
|---|---|---|---|
| `$0D` | `$8D` | | |
| `$41` | `$61` | | |
| `$7F` | `$FF` | | |

## Part E: is bit 7 set?

The fastest way to ask "is the top bit on" is to look at the first hex digit. If
it is 8 or higher, bit 7 is set. Test that rule on these, answering yes or no
without converting to binary.

`$0D` &nbsp; `$8D` &nbsp; `$41` &nbsp; `$C8` &nbsp; `$7F` &nbsp; `$80` &nbsp;
`$FF` &nbsp; `$00`

Then explain in one sentence why the rule works.

## Part F: the counting trap

A learner writes: "A byte holds 0 to 256, because 2 to the eighth is 256."

Find the error and state it precisely.

## Part G (optional): eight coins

Lay out eight coins, heads for 1 and tails for 0. Have someone else set a number
under 256 and see how fast you can read it. Then swap. Nothing to hand in; this
is the drill that makes the rest automatic.

## What this activity does not do

It is number representation practice. It measures nothing and authorizes no
hardware action.
