# X02 Fix the loop

**Audience:** BUILD
**Time:** 50 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A03, M04

## You will learn

By the end, you can find a one-byte bug in a loop by tracing rather than
guessing, fix it, and explain what changed using a before-and-after trace.

## Why this matters

A03 taught you to trace loops. M04 taught you to write down what you expected
before you looked. This exercise puts them together against a program that is
wrong in exactly one place.

The bug is the kind that matters most: the program runs, returns cleanly, and
produces output that looks entirely reasonable. Nothing announces the fault.

## First result

A completed six-row trace showing how many stores actually happened.

## What you need

Paper. `assets/broken-loop.txt`. Optionally the M03 emulator.

## Activity

1. Read the intention at the top of `assets/broken-loop.txt` and the program
   underneath.
2. **Before looking for the bug**, fill in the trace table.
3. Answer the three questions under the table. That is your first result.

## Explain what happened

**Trace before you hunt.** If you go looking for the bug first, you will find
something that looks suspicious and convince yourself. If you trace first, the
discrepancy finds you: the table says six stores and the intention says five, and
now you know what you are looking for rather than guessing.

This is M04's order of operations, and it is the reason the worksheet puts the
trace above the question.

**The trace.** Y starts at 0. Store at `$0400`, `INY` makes Y 1, compare against
6, not equal, branch back. This repeats for Y = 1, 2, 3, 4, 5. After the store at
`$0405`, `INY` makes Y 6, the compare matches, the zero flag is set, `BNE` does
not branch, and control falls through to the jump.

Six stores, at `$0400` through `$0405`. The intention was five.

**The bug is `C0 06` at `$0308`. It should be `C0 05`.** One byte, one extra
pass, one address written that should not have been.

**Why this is the dangerous kind.** The program runs to completion. It returns to
the Monitor properly. It writes plausible-looking data to a plausible-looking
address. Every symptom you might look for is absent.

The only thing wrong is that it did one thing more than it was supposed to, and
you can only detect that by comparing against what it was supposed to do. Which
means the intention has to be written down somewhere, which is A06's design card
earning its keep.

**What the extra byte costs.** If nothing else uses `$0405`, nothing bad happens
and the bug sits there. If something else does use it, that something breaks, and
it breaks somewhere else entirely, at a time unconnected to this program running.
That is the shape of the worst bugs: the damage and the cause are separated.

**Fixing it, and proving the fix.** Change one byte and trace again. The
before-and-after pair is the deliverable, not the fixed program. A fix you cannot
demonstrate is a change you are hoping about.

**Change one thing.** M04's rule applies. One byte, one trace, one comparison. If
you also tidied the loop while you were there, you no longer know which change
fixed it.

## Try a variation

Suppose instead the bug were `A0 01` at `$0300`, starting Y at 1. Trace it. How
many stores, and at which addresses? Is this bug better or worse than the real
one?

## Check your understanding

1. Why trace before looking for the bug?
2. The program returns to the Monitor correctly. Why is that not reassuring?
3. What makes a one-byte change safer to reason about than a three-byte one?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The programs were executed off-device during authoring and the results recorded.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- Neither version has run on this project's machine, and neither is offered for
  entry there.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
