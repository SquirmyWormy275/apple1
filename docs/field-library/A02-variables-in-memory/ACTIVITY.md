# A02 Activity: keep a value

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. Nothing is entered on the Replica 1 Plus.

## Part A: the before-and-after table (this is the first result)

Complete the first table on `assets/memory-before-after.txt`.

## Part B: the indexed version

Complete the second table on the same sheet. Confirm the two programs leave
memory in the same state.

## Part C: what does it write where

Given Y's value, name the address written.

| Instruction | Y | Address written |
|---|---:|---|
| `STA $0400,Y` | 0 | |
| `STA $0400,Y` | 1 | |
| `STA $0400,Y` | 16 | |
| `STA $0400,Y` | 255 | |
| `STA $0500,Y` | 3 | |

## Part D: label or address

| # | Item | Label or address |
|---|---|---|
| 1 | `$FF1F` | |
| 2 | `GETLINE` | |
| 3 | `$0400` | |
| 4 | `ECHO` | |
| 5 | `NOTCR` | |

Then: which of these appear in the bytes of a program, and which do not?

## Part E: read it back

Write a short program that stores `$5A` at `$0402`, then loads it back into X,
then returns to the Monitor. Use any addressing you like. Trace it.

## Part F: the collision

A program is entered at `$0300` and is 26 bytes long. A learner decides to use
`$0310` as their buffer.

1. What is the address range of the program?
2. What goes wrong?
3. What would the symptom look like to someone watching?
4. Give two different addresses that would be safe, and say why.

## Part G (optional): count the instructions saved

Write out what the indexed program on the worksheet would look like if it had to
store ten values instead of two, both with and without indexing. Count the
instructions in each.

## What this activity does not do

It traces programs on paper. It enters nothing on hardware and authorizes no
hardware action.
