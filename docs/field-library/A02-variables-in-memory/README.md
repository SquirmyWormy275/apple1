# A02 Variables in memory

**Audience:** BUILD
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A01, C05

## You will learn

By the end, you can store a value at a chosen address, read it back, use an
index register to reach a run of addresses with one instruction, and explain why
a label in a listing is not the same thing as an address.

## Why this matters

A program that cannot keep anything is a program that can only do one thing.
Memory is where a program keeps what it needs, and the moment you have more than
one thing to keep, you need a way to talk about *the next one*. That is what
indexed addressing is for, and it is the last piece of notation you need to read
this repository's programs completely.

## First result

A filled memory-before-and-after table for a five-instruction program.

## What you need

Paper. `assets/memory-before-after.txt`. Optionally the M03 emulator.

## Activity

1. Read the first program on `assets/memory-before-after.txt`.
2. Fill in the A, `$0400`, and `$0401` columns after each instruction.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**A variable is an address you decided to use for something.** There is no
declaration and no name. You pick a location, you keep your value there, and you
remember what it is for. `$0400` in this repository's programs is a buffer
because the programmer decided it was, not because the machine knows.

**Storing and retrieving.** `STA $0400` writes A into that location.
`LDA $0400` reads it back. Between those, the value sits there and nothing
touches it unless another instruction does.

**Two values need two addresses.** The first program writes `$48` at `$0400` and
`$49` at `$0401`, using two separate store instructions with two hard-coded
addresses. That works, and it does not scale. Twenty characters would need
twenty store instructions.

**Indexed addressing solves that.** `STA $0400,Y` means: take the address
`$0400`, add whatever is currently in Y, and store there. With Y at 0 it writes
to `$0400`; with Y at 1 it writes to `$0401`; with Y at 17 it writes to `$0411`.

One instruction, and the destination is decided while the program runs. Combined
with `INY`, which adds one to Y, you can walk along a run of memory as long as
you like.

This is why `line-input-0300.hex` starts with `LDY #$00` and contains `INY`. The
Y register is the position in the buffer, and `STA $0400,Y` is "put this
character at the current position."

`$0400` is called the *base address* and Y is the *index*. The corresponding
load, `LDA $0400,Y`, reads back from the same place, which is exactly what the
echo program uses to read the buffer out again.

**Labels are not addresses.** In a listing you will see things like:

```text
FF1F: A9 8D GETLINE LDA #$8D
```

`GETLINE` is a *label*, a name a human wrote for the benefit of other humans. It
is not in the bytes. The instruction is `A9 8D` and the address is `$FF1F`;
`GETLINE` exists only in the listing.

This matters more than it sounds. A label can be renamed with no effect on the
program. An address cannot be changed without changing the bytes. When someone
says "jump to `GETLINE`," the machine is doing `JMP $FF1F` and the name is
scaffolding. If you are transcribing bytes, labels are the part you throw away.

**Choosing where to put things.** The programs here use `$0400`. Nothing makes
that address special. It needs to be RAM, it needs to be somewhere the program
itself is not, and it needs to be somewhere nothing else is using. `$0300` holds
the program, so the buffer goes a page further along, and 256 bytes of clearance
is a simple way to be sure they cannot collide.

## Try a variation

The buffer starts at `$0400` and Y starts at 0. Y is a single byte, so it can
reach 255. What is the highest address the program can write to, and what
happens on the next `INY` after that?

## Check your understanding

1. What does `STA $0400,Y` do when Y holds 5?
2. Why does `LDY #$00` have to happen before the loop rather than inside it?
3. A listing shows `LOOP` next to address `$0302`. What is in memory at `$0302`?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction meanings from Owad's reference; the labeled listing example from the
Monitor listing in the Briel manual; the buffer convention from this repository's
programs. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine.
The example programs are paper exercises with no entry procedure. It authorizes
no firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
