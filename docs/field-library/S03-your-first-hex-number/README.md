# S03 Your first hex number

**Audience:** LEARN
**Time:** 25 minutes
**Status:** OFF-DEVICE
**Prerequisites:** none

## You will learn

By the end, you can convert any number from 0 to 255 into hexadecimal and back,
and say why the Apple-1's documentation is written that way.

## Why this matters

Every address and every byte in this library is written in hexadecimal:
`$D010`, `$FF00`, `$8D`. If you cannot read those, every other lesson is a wall
of noise. It takes about twenty minutes to stop being a wall.

You need no maths beyond counting and dividing by sixteen.

## First result

A completed decimal-to-hexadecimal table for 0 through 15.

## What you need

Paper and a pencil. `assets/hex-table-blank.txt`, and
`assets/hex-table-filled.txt` kept covered until step 3.

## Activity

1. On `assets/hex-table-blank.txt`, fill in the hex column for 0 through 9.
   They are the same digits you already know.
2. For 10 through 15, write A, B, C, D, E, F in order.
3. Uncover `assets/hex-table-filled.txt` and check. That is your first result.

## Explain what happened

**Counting in tens.** Ordinary numbers use ten symbols, 0 to 9. When you run out
you start a new column: after 9 comes 10, meaning "one group of ten, no ones."

**Counting in sixteens.** Hexadecimal, or *hex*, uses sixteen symbols. The first
ten are the familiar 0 to 9. Since there are no single digits for ten through
fifteen, letters do the job: A is 10, B is 11, C is 12, D is 13, E is 14, F is
15. After F comes `$10`, meaning "one group of sixteen, no ones," which is
decimal 16.

The `$` prefix means "this is hex." You will also see `0x` used for the same
purpose. Without a marker, `10` is ambiguous: sixteen or ten?

**Why sixteen and not ten?** Because computer memory is built out of bits, and
bits come in groups of eight. Eight bits is a *byte*. A byte can hold 256
different values, 0 through 255. Sixteen times sixteen is 256, so exactly two
hex digits describe exactly one byte, every time, with no leftovers. Ten does
not divide into that cleanly: 255 in decimal is three digits, 99 is two, and
there is no fixed width.

That is the whole reason. Hex is not more mathematical than decimal. It just
lines up with the hardware, so a byte is always two characters and an address is
always four.

**Converting by hand.** To turn a decimal number under 256 into hex, divide by
16. The whole part is the first digit, the remainder is the second.

- 200 divided by 16 is 12, remainder 8. Twelve is C, so 200 is `$C8`.
- 45 divided by 16 is 2, remainder 13. Thirteen is D, so 45 is `$2D`.

Going the other way, multiply the first digit by 16 and add the second.

- `$3F` is 3 times 16, which is 48, plus 15, which is 63.

## Try a variation

The Apple-1's keyboard character slot is at `$D010` and its display slot is at
`$D012`. Those are four hex digits, not two, because an address needs sixteen
bits rather than eight. Without converting them to decimal, say how far apart
the two addresses are, and explain how you know.

## Check your understanding

1. Convert to hex: 12, 16, 31, 100, 255.
2. Convert to decimal: `$0A`, `$20`, `$7F`, `$8D`.
3. Why is it useful that every byte is exactly two hex digits?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The decimal, binary, and hexadecimal equivalences and the `0x` and `$` prefix
convention come from Owad's appendix on number systems. Full citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's hardware.
It is arithmetic. It authorizes no firmware load, EEPROM write, CFFA1 write,
serial-port open, or physical modification.
