# A01 Read an instruction

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C01, C02, S03

## You will learn

By the end, you can take any load, store, or jump instruction, name its parts,
and translate it into a plain English sentence without hesitating.

## Why this matters

C01 introduced the idea of reading an instruction. This lesson turns it into a
reliable habit across a whole family of instructions, so that a listing becomes
something you skim rather than something you decode. Everything in A02 through
A06 assumes you can do this without effort.

## First result

Three instructions translated into English.

## What you need

Paper. `assets/instruction-shape.txt`. Nothing powered on.

## Activity

1. Read `assets/instruction-shape.txt`, especially the two ways of writing an
   operand.
2. Translate these three, using the pattern verb, what, with or into:

   - `LDX #$03`
   - `STA $0400`
   - `JMP $FF1F`

3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**Every instruction has at most two parts.** A *mnemonic*, three letters naming
the action, and an *operand*, saying what to act on. Some instructions have no
operand at all: `INY` just increments Y and there is nothing more to say.

**The mnemonics are abbreviated English.** `LDA` is LoaD Accumulator. `STA` is
STore Accumulator. `LDX` and `LDY` load the index registers, `STX` and `STY`
store them. Once you see the pattern, most of the instruction set reads itself.

**Load and store are opposites, and the direction matters.** `LDA $0400` reads
from memory into the register. `STA $0400` writes from the register into memory.
The register is always the *A* in the mnemonic, and the operand is always the
other end. Beginners reverse these constantly. The fix is to say the direction
out loud every time: "load A **from**," "store A **into**."

**Neither one moves anything.** Both copy. After `STA $0400`, the value is in
both A and `$0400`. After `LDA $0400`, likewise. Nothing is emptied.

**Immediate versus absolute.** This is the whole of the lesson's difficulty.

`#` means *immediate*: the operand is the value. `LDA #$41` puts 65 into A.

No `#` means *absolute*: the operand is an address. `LDA $41` goes to location
`$0041`, reads whatever is there, and puts that into A.

A useful test: if you can imagine the operand changing while the program runs, it
is an address. If it is fixed forever by the listing, it is immediate.

**Store has no immediate form, and the reason is worth a moment.** `STA #$41`
does not exist and cannot exist. Store writes a value somewhere, so its operand
must name a place. `#$41` names a number, and you cannot write into the number
65. If you find yourself wanting to write `STA #`, what you actually want is
`LDA #` followed by `STA` to an address.

**Jumps take an address, always.** `JMP $FF1F` goes to `$FF1F`. There is no
immediate jump, for the same reason: you jump *to* somewhere, and a bare number
is not somewhere.

**Reading intent, not just mechanics.** The last step is saying what an
instruction is *for*. `LDY #$00` is mechanically "load Y with zero." Its intent,
in the programs in this repository, is "start the counter at the beginning."
Mechanics tell you what happens; intent tells you why the programmer wrote it.
Both matter, and only the first is in the bytes.

## Try a variation

`LDA $D011` and `LDA #$D0` look similar and do completely unrelated things.
Explain both, and say which one could produce a different result each time it
runs.

## Check your understanding

1. Translate `LDY $0400` and `LDY #$04`.
2. Why can there be no `STA #$41`?
3. After `LDA $0300` followed by `STA $0400`, how many places hold the value?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction names and meanings from Owad's instruction reference; the example
instructions from this repository's listings. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
