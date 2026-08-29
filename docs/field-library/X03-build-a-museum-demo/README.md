# X03 Build a museum demo

**Audience:** BUILD
**Time:** 60 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S01, S04, H02, H04

## You will learn

By the end, you can write a three-minute demonstration for a stranger, built so
that it works whether or not any hardware is available.

## Why this matters

Explaining something to a visitor is a real test of whether you understand it.
Three minutes with someone who did not come looking for this is much harder than
an hour with someone who did.

The constraint that matters most here is the fallback. A demonstration that
depends on a machine working is a demonstration that will fail in public, and in
this project the machine has an unresolved fault and a standing block on part of
it. A demo that cannot run without it is not finished.

## First result

A filled three-minute script with the fallback section completed.

## What you need

Paper. `assets/demo-script.txt`. Anything you plan to show, which must not be a
powered machine.

## Activity

1. Read the six timed sections and the fallback box on
   `assets/demo-script.txt`.
2. Fill in the hook, the object, and the one idea.
3. Fill in the fallback box. That is your first result, and the script is not
   finished without it.

## Explain what happened

**Three minutes is about four hundred words.** That is less than it sounds. It is
room for one idea, explained once, with something to look at.

**The hook has to earn the next twenty seconds.** A stranger has no investment.
"This is an Apple-1 replica" is a label, not a hook. "This computer has 256 bytes
of software in it, and that was the entire operating system" is a hook, because it
contains something surprising.

**Name the object correctly, every time.** H02's whole lesson lands here. If it is
a Replica 1 Plus, say so. A visitor who later discovers they were shown a replica
described as an Apple-1 will remember that, and they will be right to.

Saying it accurately costs you nothing. "This is a modern replica of a 1976
design" is just as interesting as the false version, and it is true.

**One idea. Not two.** The commonest failure in a short demo is fitting in
everything you know. Pick one: that the monitor is 256 bytes; that a byte is only
what you treat it as; that the machine was sold as a bare board and you supplied
the rest. Any of those fills three minutes.

The others are still there for anyone who asks.

**The show is what they watch, and it does not have to be a machine.** A byte
list on paper being decoded into a word is a show. A card being sorted is a show.
A person tracing a loop on a whiteboard while the audience predicts the next value
is a show, and it is more engaging than a screen they cannot read from three feet
away.

**The question back is what makes it a demonstration rather than a lecture.** One
question the visitor answers. It does not need to be hard. "This byte is 200 in
decimal. What do you think the letter A is?" gets people participating, and
someone who answers something remembers it.

**The fallback, which is the required part.** Your demonstration must work with no
powered hardware.

This is not a hedge against bad luck. In this project it is the normal case: the
machine has a serial fault under investigation, an opened serial session is
blocked, and running any program on it is a separate operator-led decision that a
demonstration does not get to make.

So the off-device version is not the backup. It is the demonstration, and anything
involving hardware is a bonus that may never happen.

**Four things that will go wrong, and all of them are plannable.**

*No power at the venue.* Your fallback covers this.

*The machine is not available.* Same.

*A question you cannot answer.* "I do not know" is a complete answer, and it is
much better received than a guess. "I do not know, and here is how you would find
out" is better still.

*Someone asks what it is worth.* This one catches people. The honest answer is
that this library makes no claim about value, that a replica and an original are
very different objects, and that you are not the person to ask. Say that
pleasantly and move on.

## Try a variation

Cut your script to ninety seconds. Which section survives? The answer tells you
what you actually think the point is.

## Check your understanding

1. Why must the demonstration work with no powered hardware?
2. What is wrong with a hook that is just the object's name?
3. A visitor asks what the board is worth. What do you say?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The project's boundaries are quoted from its own documents. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- **It grants no authority to power on, connect to, or run anything on the
  Replica 1 Plus for a demonstration or for any other reason.**
- It makes no claim about the value of any object.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
