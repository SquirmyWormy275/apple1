# A05 Keyboard to screen

**Audience:** BUILD
**Time:** 55 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A01, A02, A03, A04, M05

## You will learn

By the end, you can read this repository's `line-input-0300.hex` end to end,
name what every instruction contributes, and explain the whole program in six
sentences.

## Why this matters

Everything in the A-series has been building to this. Twenty-six bytes, and they
contain a setup, a polling loop, an indexed store, a subroutine call, a
comparison, a counted loop, and a clean exit. If you can read this program, you
can read most small 6502 programs.

It is also a real artifact from this project rather than an exercise, which means
reading it correctly has value beyond the lesson.

## First result

The program divided into its stages, with a one-line English summary of each.

## What you need

Paper. `assets/four-stages.txt`. Optionally the M03 emulator.

## Activity

1. Read `assets/four-stages.txt` once, ignoring the bytes and looking only at
   the stage labels down the right-hand side.
2. Cover the English summary at the bottom and write your own one-line summary
   for each stage.
3. Uncover and compare. That is your first result.

## Explain what happened

**Setup: `LDY #$00`.** Y is the position in the buffer, and it starts at zero.
One instruction, and it has to be outside the loop, because running it again
would send every character back to the start.

**Input: three instructions that wait.** `LDA $D011` reads the keyboard control
register. `BPL $0302` branches back to that same read while the result is
positive, that is, while bit 7 is clear. So the loop spins until bit 7 of `$D011`
becomes 1, which is the hardware saying a key is waiting. Then `LDA $D010` takes
the character.

Two things are worth noticing. The flag test is a *bit* test, done with a branch
rather than a comparison, exactly as C03 predicted. And the byte that arrives has
bit 7 set, which is why every comparison later in the program uses a high-bit
value.

**Store: one instruction.** `STA $0400,Y` puts the character at `$0400` plus Y.
This is A02's indexed addressing doing the job it exists for.

**Echo: one instruction.** `JSR $FFEF` calls the Monitor's `ECHO` routine, which
displays the character in A. `JSR` because we want to come back; the routine ends
in `RTS` and returns to `$0310`. This is the M05 distinction in practice: `JSR`
here, `JMP` at the end.

Calling into the Monitor's ROM like this is the closest thing the machine has to
a library. You do not write display code; you jump to the display code that is
already there.

**Test and repeat: four instructions.** `CMP #$8D` compares against carriage
return with the high bit set. `BEQ $0317` leaves the loop if it matched. `INY`
advances the buffer position. `BPL $0302` goes back for another character.

That last branch is the interesting one. It is `BPL`, not an unconditional jump,
and it tests the flags left by `INY`. So the loop also ends if Y ever reaches
`$80`, that is, after 128 characters. It is a length limit, implemented for free
by choosing a conditional branch where an unconditional one would have done.

Whether that was deliberate is not something the bytes can tell you.

**Return: one instruction.** `JMP $FF1F`, the Monitor warm entry, as M05
covered.

**The whole program in six sentences.** Start at the beginning of the buffer.
Wait for a key and take it. Store it at the current position. Show it. If it was
Return, stop; otherwise move along one and wait for the next key. Then give
control back to the Monitor.

**What it does not do.** No backspace. No bounds check beyond the accidental
128-character limit. No handling of the case where the buffer wraps. No lower-case
conversion. Twenty-six bytes buys a great deal, and it does not buy those.

## Try a variation

The loop ends on carriage return **or** when Y reaches `$80`. Work out what
happens to the 129th character typed if no Return has been pressed, and say
whether the program's behavior in that case is well defined.

## Check your understanding

1. Why is `LDY #$00` outside the loop?
2. Why `JSR $FFEF` but `JMP $FF1F`?
3. The program compares against `$8D` rather than `$0D`. Why?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The artifact is this repository's; instruction meanings from Owad; the Monitor
entry points from the Briel manual's Appendix C; the observed behavior from
recorded emulator runs. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- **The artifact is classified RAM-ONLY with no live-run authority** in
  `docs/apple1-software-library.md`. This lesson does not change that and does
  not grant it.
- **This lesson is OFF-DEVICE.** It reads the program and optionally rehearses it
  in the emulator. It contains no entry procedure and nothing here is a step
  toward running it on hardware.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
