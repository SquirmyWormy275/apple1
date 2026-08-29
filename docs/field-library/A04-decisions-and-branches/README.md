# A04 Decisions and branches

**Audience:** BUILD
**Time:** 50 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A03, C04

## You will learn

By the end, you can compare a value against a target, send the program down one
of two paths depending on the answer, and bring both paths back together.

## Why this matters

A03's loops repeat. This lesson is about choosing. Together they are the whole of
control flow: a program that can repeat and choose can express anything you can
describe, on any machine ever built.

## First result

A three-key trace showing which path the program took and what it echoed.

## What you need

Paper. `assets/choose-the-message.txt` and `assets/flag-card.txt`. Optionally the
M03 emulator.

## Activity

1. Read the program on `assets/choose-the-message.txt` and the flag rules on
   `assets/flag-card.txt`.
2. Trace it for the keys `Y`, `N`, and `Q`, filling in the path and what gets
   echoed.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**Compare, then branch, is one idea in two instructions.** `CMP #$D9` does a
subtraction and throws the answer away, keeping only the flags. If A held `$D9`,
the subtraction gives zero and the zero flag is set. If A held anything else, the
result is not zero and the flag is clear.

Then `BEQ` reads that flag. `BEQ` is "branch if equal," which is really "branch
if the zero flag is set," which after a compare means the same thing.

**`CMP` does not change A.** This is the property that makes it useful. You can
compare the same value against several targets in a row, and A is still there
afterwards to be used. If `CMP` overwrote A, every comparison would destroy the
thing being compared.

**Two paths, and the rejoin.** The program's shape is: compare, jump to path A if
equal, otherwise fall through into path B. Path B loads `$CE`, then must jump
over path A to reach the common ending. Path A loads `$D9` and then simply falls
into the ending, because it is already adjacent to it.

That asymmetry is worth staring at. Path B needs a `JMP` and path A does not,
purely because of where they sit in memory. If you rearranged the two paths, the
`JMP` would move to the other one. The structure is symmetric; the code is not,
because memory is a line and a decision is a fork.

Forgetting that `JMP` is one of the most common bugs in hand-written branching
code. Without it, path B runs and then falls straight into path A, and both
happen.

**Falling through is the default.** A branch not taken does nothing at all;
execution continues to the next instruction. So the "otherwise" case costs no
instructions, which is why programs are usually arranged so the common case falls
through and the exception branches away.

**The comparison value carries the high bit.** `CMP #$D9`, not `CMP #$59`,
because the byte arriving from `$D010` has bit 7 set. Comparing against plain
ASCII `$59` would never match anything. This is C04's convention doing real work,
and getting it wrong produces a program that compiles fine, runs fine, and simply
never takes the branch.

**Only two flags, deliberately.** The processor keeps several. This lesson needs
the zero flag and, from A03, the negative flag. `CMP` also sets the carry flag,
which is how you test greater-than and less-than, and that is not needed here.
Learn flags when a lesson needs them, not before.

## Try a variation

Change `CMP #$D9` to `CMP #$59`, plain ASCII `Y` with no high bit. Predict what
the program does for every possible key, then say why.

## Check your understanding

1. After `CMP #$D9`, what is in A?
2. Why does path B need a `JMP` when path A does not?
3. A programmer writes `CMP #$D9` then `BNE` to the "yes" path. What have they
   built?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction meanings from Owad's reference; the high-bit convention from the
Monitor listing; the observed results were produced in this repository's emulator
during authoring. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine.
The program is a teaching example, is not supplied as an artifact, and has no
entry procedure. It authorizes no firmware load, EEPROM write, CFFA1 write,
serial-port open, or physical modification.
