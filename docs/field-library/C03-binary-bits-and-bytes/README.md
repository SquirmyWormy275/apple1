# C03 Binary, bits, and bytes

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S03

## You will learn

By the end, you can build any number from 0 to 255 out of eight ones and zeros,
read one back, and convert between binary and hex without arithmetic.

## Why this matters

Hex told you how to write a byte down. Binary tells you what a byte *is*. Some
things only make sense at the bit level: the top bit that separates `$0D` from
`$8D`, the flag the keyboard sets, the "Data Available" line that is a single
bit of the display register. Those are not numbers being compared. They are
individual bits being looked at.

## First result

A byte built out of ones and zeros on the bit strip.

## What you need

Paper, a pencil, and scissors if you want to cut the strip out.
`assets/bit-strip.txt` and `assets/bit-drill.txt`.

## Activity

1. Look at `assets/bit-strip.txt`. Note the value written under each of the
   eight columns: 128, 64, 32, 16, 8, 4, 2, 1.
2. Build 65: put a 1 under 64 and a 1 under 1, zeros everywhere else. Add them
   up to check.
3. Do the same for 200 on `assets/bit-drill.txt`. That is your first result.

## Explain what happened

**A bit is one yes or no.** It has two states, written 1 and 0. That is the
smallest thing a computer stores. Everything else is bits in a row.

**Eight bits is a byte.** With eight of them you can make 2 x 2 x 2 x 2 x 2 x 2
x 2 x 2 = 256 different patterns, which is why a byte holds 0 through 255.

**Each column is worth double the one to its right.** Rightmost is 1, then 2, 4,
8, 16, 32, 64, and leftmost 128. To read a byte, add up the columns that have a
1. To write one, work from the left: take the biggest column that fits, subtract
it, repeat.

Building 200: does 128 fit? Yes, 72 left. Does 64 fit? Yes, 8 left. 32? No. 16?
No. 8? Yes, 0 left. So 1100 1000.

**The numbering runs right to left.** The rightmost is bit 0, the leftmost is bit
7. This trips people up constantly, because we read text left to right but
number bits right to left. Bit 7 is the leftmost and the biggest, worth 128, and
it gets called the *high bit* or *top bit*.

**Binary to hex is free.** This is the payoff. Split the eight bits down the
middle into two groups of four. Each group of four is worth 0 to 15, which is
exactly one hex digit. No arithmetic needed:

```text
1100 1000
 C    8      $C8
```

Four bits is called a *nibble*, which is a joke that stuck.

**Why the top bit gets special treatment here.** ASCII only uses 0 through 127,
which fits in seven bits. That leaves bit 7 spare. The Apple-1 keyboard sends
seven-bit ASCII, and the Monitor expects the byte it reads to arrive with bit 7
set. So `$0D`, a carriage return, becomes `$8D` once the top bit is on. Same
character, one extra bit.

In binary that is obvious at a glance:

```text
0000 1101   $0D   13
1000 1101   $8D   141
```

One bit different. In decimal, 13 and 141 look unrelated, which is exactly why
nobody writes bytes in decimal.

## Try a variation

The display register at `$D012` uses its top bit as a "busy" signal, and a
program checks that one bit before writing. Explain why checking a single bit is
different from comparing the whole byte to a number, and what would go wrong if
a program compared the whole byte instead.

## Check your understanding

1. Write 100 in binary, then convert your answer straight to hex.
2. `0100 0001` is which number, which hex value, and which ASCII character?
3. Adding 128 to a byte under 128 does what to its bits?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Number-system equivalences come from Owad's appendix; the keyboard high-bit
convention from the Monitor listing and Owad's keyboard description. Citations
in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's hardware.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
