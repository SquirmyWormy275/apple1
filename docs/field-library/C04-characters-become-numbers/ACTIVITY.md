# C04 Activity: encode and decode

**Status:** OFF-DEVICE. Paper only. No key is pressed on any machine.

## Part A: the table (this is the first result)

Complete Part 1 of `assets/encoding-worksheet.txt`: B, Z, 0, space, carriage
return, in decimal, hex, and high-bit-set hex.

## Part B: decode the message

Part 2 of the worksheet. Strip the top bit from each byte, then read.

```text
C8  C9  A0  D4  C8  C5  D2  C5  8D
```

## Part C: encode a message

Write `APPLE` as Monitor keyboard bytes, ending with a carriage return.

## Part D: which layer is responsible

For each statement, say whether it is **ASCII**, **Apple-1 convention**, or
**emulator convention**.

| # | Statement | Layer |
|---|---|---|
| 1 | `A` is 65. | |
| 2 | A keyboard byte arrives with bit 7 set. | |
| 3 | Letters are consecutive, so `B` is `A` plus one. | |
| 4 | `--input "HI"` is written as plain text on a command line. | |
| 5 | Carriage return is 13. | |
| 6 | A program compares against `$8D` to detect Enter. | |

## Part E: spot the mistake

A learner decodes `C8 C5 CC CC CF` by looking each value up in an ASCII table
directly, finds nothing, and concludes the file is corrupted.

1. What did they actually have?
2. What one step did they skip?
3. What would the same mistake look like in reverse, encoding rather than
   decoding?

## Part F (optional): the case question

The Replica 1 Plus manual states the machine understands upper case only. In
ASCII, upper and lower case differ by one bit. Write two or three sentences on
what a program could do with a lower-case byte if it received one, and what it
would cost to handle versus reject it.

## What this activity does not do

It converts characters on paper. It presses no key on any machine, and it
authorizes no hardware action.
