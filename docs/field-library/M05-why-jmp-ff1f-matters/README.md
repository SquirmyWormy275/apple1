# M05 Why `JMP $FF1F` matters

**Audience:** BUILD
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C05, M01, M02

## You will learn

By the end, you can find the exit instruction in a byte listing, explain why it
is a jump and not a return, and tell whether a given program has a
self-directed exit at all.

## Why this matters

M01 established that the Monitor's `R` command gives away control and does not
get it back. That means every program has to bring you home itself. Getting the
exit wrong does not produce an error message. It produces a machine that has
stopped responding for reasons nobody can see, which then gets described as "it
crashed" and investigated as a hardware fault.

This is the single highest-value detail in the M-series, and it is one
instruction.

## First result

The exit instruction located in a real listing, with its address.

## What you need

Paper. `assets/exit-annotation.txt`. Optionally the M03 emulator.

## Activity

1. Open `assets/exit-annotation.txt` and look only at Program One.
2. Find the last instruction and write down its address and its three bytes.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**The exit is `4C 1F FF` at `$0317`, which is `JMP $FF1F`.**

`$FF1F` is inside the Monitor ROM. In the Monitor's own listing it is the label
`GETLINE`, the point where the Monitor starts collecting a fresh line of input
from you. Jumping there is the program saying "I am finished, you have the
keyboard back."

It is sometimes called the *warm entry*, to distinguish it from `$FF00`, which is
the full reset entry. Warm entry means "carry on from a known good state" rather
than "start over from nothing."

**Why not `RTS`?** This is the part worth understanding properly rather than
memorizing.

`JSR`, jump to subroutine, does two things: it pushes the address of the
instruction after it onto the stack, then jumps. `RTS`, return from subroutine,
does the reverse: it pulls an address off the stack and jumps to it. They are a
matched pair, and `RTS` only works because some earlier `JSR` left something for
it to find.

The Monitor's `R` command does not do a `JSR`. It jumps. Nothing was pushed. So
an `RTS` at the end of your program pulls two bytes off the stack that were never
put there for it, treats them as an address, and jumps there. Whatever was on the
stack, left over from something else, becomes the place your program goes next.

The result is not a crash in any orderly sense. It is execution continuing at an
arbitrary address, running whatever bytes are there as instructions.

**Notice this is a statement about the Monitor, not about `RTS`.** `RTS` is
correct and necessary in its proper place. The program in Program One uses
`JSR $FFEF` to call the Monitor's echo routine, and that routine ends with an
`RTS` which works perfectly, because the `JSR` put an address there for it. The
rule is not "avoid `RTS`." The rule is that `RTS` needs a matching `JSR`, and
starting a program with `R` does not provide one.

**Program Two does not exit at all.** This is the second half of the lesson and
it is a real finding about this repository's artifacts.

`line-input-echo-0300.hex` ends with `4C 00 03`, which is `JMP $0300`: a jump
back to its own first instruction. It reads a line, echoes the buffer back, and
then starts over. There is no instruction anywhere in it that returns to the
Monitor.

Run in the repository emulator, it reports `returned_to_monitor: false`, which
confirms by observation what the bytes say.

This is not necessarily wrong. The software library describes the program as
reading the buffer back "before starting over," so looping may be exactly what
was intended. But the consequence is definite: a session using this program would
end by pressing reset, not by the program handing control back. Anyone planning
such a session needs to know that in advance rather than discovering it while the
machine is running.

**How to check any listing for an exit.** Work out where the last instruction
starts, read it, and ask three questions. Is it a jump? Does it target the
Monitor rather than somewhere inside the program? And is it actually reachable,
or is it sitting after a loop that never falls through to it? A `JMP $FF1F`
placed after an infinite loop is decoration.

## Try a variation

Program One contains a `JSR $FFEF` at `$030D` and a `JMP $FF1F` at `$0317`. Both
transfer control into the Monitor ROM. Explain why one of them comes back and
the other does not, using only what you now know about the stack.

## Check your understanding

1. What are the three bytes of Program One's exit, and at what address?
2. Why would replacing that exit with `RTS` not simply return to the Monitor?
3. A listing ends with `JMP $FF1F`, but the instruction before it is a branch
   that always loops backwards. Does the program exit?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The exit rule and the reason for it are quoted from this repository's RAM-only
README; `$FF1F` and `$FFEF` are identified from the Monitor listing in the Briel
manual. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- Neither program is offered for entry on hardware, and this packet contains no
  entry procedure.
- Nothing here shows that either program has run on this project's machine.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
