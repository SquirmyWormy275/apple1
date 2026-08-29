# M04 Debugging as observation

**Audience:** LEARN
**Time:** 40 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S04, M03

## You will learn

By the end, you can turn "it does not work" into a written expectation, an
observation, and one hypothesis you could actually test.

## Why this matters

Most debugging goes wrong before any testing starts. Someone says "it is
broken," changes three things, and it starts working, and now nobody knows why.
Six months later it breaks again and there is nothing to go back to.

The alternative is slower for about ten minutes and faster forever afterwards.
Write what you expect. Look. Write what happened. The gap between those two
sentences is the only new information you have.

## First result

One filled two-column sheet with a single testable hypothesis under it.

## What you need

Paper. `assets/observation-sheet.txt`. Optionally the emulator from M03, which
is where any actual testing in this lesson happens.

## Activity

1. Take this situation: you run `line-input-0300.hex` in the emulator with the
   input `HI` and a carriage return, and the buffer comes back empty.
2. On `assets/observation-sheet.txt`, fill the expected column from M03's
   recorded results, fill the observed column from the situation, then write one
   hypothesis in the form given.
3. Compare with `ANSWERS.md`. That is your first result.

## Explain what happened

**"Expected" has to come first, in writing.** Once you have seen a result, your
memory of what you expected quietly reshapes itself to be closer to it. This is
not a character flaw, it is how memory works. Writing first is the only defense.

If you cannot state what you expect, that is itself the finding: you do not yet
understand the thing well enough to test it, and the next step is reading, not
testing.

**The difference is the information.** Two matching columns tell you your model
was right about this one case. Two differing columns tell you exactly where your
model is wrong, and *how* it is wrong, which is far more useful than "broken."

Be specific in both columns. "It did not work" is not an observation. "The
buffer field came back empty while the screen field showed `HI` and a carriage
return" is an observation, and it already rules things out: something ran,
characters were echoed, and only the storing part misbehaved.

**One hypothesis, stated so it could be wrong.** A useful hypothesis names a
cause and predicts a specific change. "Something is wrong with the buffer" is not
one. "The store target address is wrong, so if I check the bytes at the `STA`
instruction I will find something other than `99 00 04`" is one, because if you
look and find `99 00 04`, the hypothesis is dead and you have made progress.

**Change one thing.** If you change two and the problem goes away, you know the
problem was in one of two places, which is barely better than where you started.
Worse, you may have introduced a second fault that the first change happens to
mask. One change, one observation, write it down, then decide.

This applies to the change itself and to everything around it: the same input,
the same file, the same command, the same machine. A test where three things
moved is not a test.

**When to stop instead of continuing.** Some observations are not data points to
follow up. They are signals to stop the session.

This repository's rule, which applies to any work on the machine, is: if the
display changes unexpectedly, a reset occurs, identities drift, or bytes
mismatch, record `STOP`, recover to the known monitor state, and do not start
another test.

**A worked STOP from this project.** Earlier in this work, opening the FT232R
serial device from the host produced a garbled display. That is the STOP rule's
first condition exactly. What happened next is the model: it was recorded, the
session ended, and a further opened serial session and transmit test remain
blocked until a measurement test card exists and an operator explicitly starts
that single step.

Notice what was not done. Nobody opened it again to see if it happened twice.
Nobody changed a cable and retried. The observation was preserved intact, which
is why it is still usable as evidence now.

**Why stopping is a result.** A `STOP` records that a specific action produced a
specific unexpected outcome. That is a fact in the S04 sense and it is worth
more than a vague memory of things going oddly. The instinct to keep poking until
it works again is the instinct that destroys the evidence.

## Try a variation

Take the hypothesis you wrote and design the smallest possible test for it. Then
ask what result would make you abandon it. A hypothesis you cannot imagine
abandoning is not a hypothesis.

## Check your understanding

1. Why must the expected column be written before looking?
2. What is wrong with "it does not work" as an entry in the observed column?
3. You change one byte and the symptom disappears. What exactly have you
   established?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The STOP rule and the recorded FT232R result come from this repository's
preservation dossier and software library. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- The FT232R result is described as a recorded past event. **It is not a
  procedure and must not be repeated.** An opened serial session remains blocked.
- Any testing a learner does in this lesson happens in the emulator, off-device.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
