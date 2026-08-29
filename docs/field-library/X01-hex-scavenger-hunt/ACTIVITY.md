# X01 Activity: the hunt

**Status:** OFF-DEVICE. Paper only. **Neither dump was read from a machine**, and
no address in this activity is offered as one to inspect on hardware.

Use `assets/hunt-sheet.txt`. Hints H1 to H5 are on the sheet. Use them when
stuck.

## Part A: the first three (this is the first result)

| # | Question | Answer |
|---|---|---|
| 1 | What byte is at `$0305`? | |
| 2 | What byte is at `$030D`? | |
| 3 | What is the address of the last byte in Dump One? | |

## Part B: find the instructions

| # | Question | Answer |
|---|---|---|
| 4 | At what address does the last instruction start? | |
| 5 | How many bytes long is it? | |
| 6 | What address does it jump to? | |
| 7 | There is one `20` byte in Dump One. At what address, and what address does that instruction reference? | |

## Part C: find the addresses

Four different addresses are referenced by instructions in Dump One. Find all
four and give the address of the instruction that references each.

| Referenced address | Referenced from |
|---|---|
| | |
| | |
| | |

## Part D: count

| # | Question | Answer |
|---|---|---|
| 8 | How many bytes are in Dump One? | |
| 9 | How many bytes have bit 7 set? | |
| 10 | How many times does the byte `D0` appear, and does it mean the same thing each time? | |

Question 10 is the interesting one.

## Part E: read Dump Two

| # | Question | Answer |
|---|---|---|
| 11 | What does Dump Two spell? | |
| 12 | What is the byte at `$0409` and what does it represent? | |
| 13 | Why are the bytes from `$040A` onward `00`? | |

## Part F: the trap

| # | Question | Answer |
|---|---|---|
| 14 | Is Dump Two a reading from a machine? | |
| 15 | Is Dump One a reading from a machine? | |
| 16 | If you found this sheet in five years with no context, how would you tell? | |

## Part G (optional): make your own

Encode a short message with the high bit set, lay it out eight bytes per line
with addresses, add one hint, and give it to somebody who has done C04.

## What this activity does not do

It reads dumps on paper. Neither dump was taken from a machine, no address here
is offered for inspection on hardware, and no hardware action is authorized.
