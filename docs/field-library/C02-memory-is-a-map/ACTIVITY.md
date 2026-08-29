# C02 Activity: where does it live?

**Status:** OFF-DEVICE. Paper only. No address here is offered as something to
inspect on a machine.

## Part A: place the addresses (this is the first result)

Complete `assets/address-worksheet.txt` for `$0300`, `$0400`, `$01FF`, `$D011`,
`$FF1F`, `$9000`.

## Part B: read or write

For each region, can a running program write to it? Answer yes, no, or
"something else happens."

| Region | Writable? |
|---|---|
| `$0300` user RAM | |
| `$0100`-`$01FF` stack | |
| `$D012` display register | |
| `$FF00`-`$FFFF` Monitor ROM | |
| `$9000` unused | |

## Part C: the same byte, three ways

The byte `$C1` appears in memory. For each context, say what it means.

1. Fetched by the CPU as an opcode.
2. Loaded into the accumulator and compared against a number.
3. Sent to the display register.

You do not need to know which instruction `$C1` is. Answer at the level of
"what kind of thing is it being treated as."

## Part D: little-endian drill

Write the bytes as they would appear in a listing.

| Address in an instruction | Bytes, low first |
|---|---|
| `$D011` | |
| `$0400` | |
| `$FF1F` | |
| `$0300` | |

Then go the other way: the bytes `00 04` in an instruction mean which address?

## Part E: the original and the replica

Two differences between the original Apple-1 map and the replica map are stated
in this lesson. Name them, and say for each whether the difference makes the
machine easier or harder to use.

## Part F (optional, STUDY extension): what the map does not tell you

The map shows what the design says lives where. List three things you would
still not know about a specific board after memorizing it.

## What this activity does not do

It reads a documented map on paper. It inspects no machine and authorizes no
hardware action.
