# R05 Sound, rhythm, and code

**Audience:** STUDY
**Time:** 40 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C03, R02

## You will learn

By the end, you can encode a rhythm as a byte, decode someone else's, and say
precisely what such an encoding does and does not capture.

## Why this matters

Rhythm is the simplest interesting thing to encode. It is a row of yes-or-no
decisions, which is exactly what a byte is, so the representation almost writes
itself. That makes it a good place to study the gap between a thing and its
encoding, which is the real subject here.

It is also an honest lesson about limits. This one is conceptual throughout, for
a reason given below.

## First result

A rhythm clapped from a grid, then written as one byte.

## What you need

Paper, a pencil, and your hands. `assets/rhythm-grid.txt`. Nothing powered on.

## Activity

1. Read the first row of `assets/rhythm-grid.txt`, count 1 to 8 steadily, and
   clap on each `X`.
2. Do the same for the second and third rows.
3. Encode row 2 and row 3 as eight bits and then as a hex byte. That is your
   first result.

## Explain what happened

**A rhythm is a row of slots, each on or off.** Divide time into equal slots and
decide for each whether something happens. That structure is identical to a byte:
eight positions, each 1 or 0.

So `X . . . X . . .` is `1000 1000`, which is `$88`. An entire eight-slot rhythm
in one byte, using the C03 bit strip with no modification.

**The encoding is exact and enormously incomplete.** `$88` says something happens
at slots 1 and 5 and nowhere else. It says nothing about how fast the slots go by,
how loud each event is, how long each one lasts, or what sound is made.

Two people handed `$88` will clap the same *pattern* and it will not sound the
same. Neither of them is wrong, because the byte never claimed to specify those
things.

**That gap is the lesson.** An encoding captures what it was designed to capture
and silently discards everything else. The discarding is invisible: `$88` looks
complete. Nothing about it announces that tempo is missing.

This is the same shape as C02's "a byte is only what you treat it as," and as
S04's distinction between what a record establishes and what someone assumes it
establishes.

**Extending the encoding costs bits.** Want tempo? That is another number. Want
loudness per slot? That is no longer one bit per slot. Want note lengths? You need
a way to say "this event continues into the next slot," which means a second bit
per slot, doubling the size.

Every feature costs space, and choosing which to keep is the design. The 8-slot,
1-bit-per-slot encoding is not primitive; it is a choice that keeps exactly one
property and is very cheap.

**Reading a byte back as a rhythm.** Take `$A4`. That is `1010 0100`, so events at
slots 1, 3, and 6. Clap it. The round trip works, which is what makes it an
encoding rather than a summary.

**Why this lesson is conceptual, stated plainly.** No source in this project
documents a sound capability for the Apple-1 or the Replica 1 Plus. Owad's
chapter on the machine covers the processor, memory, keyboard, and video, and
this library has no material on sound hardware, no sound artifact, and no
measurement.

So this lesson makes **no claim that any of this could be played on the machine**.
It teaches encoding using rhythm as the subject, and the clapping is done by you.
The curriculum's own brief for R05 asks for exactly that: keep it conceptual
unless a verified, compatible sound artifact is added later. None has been.

If someone adds one, this lesson would need a source, a status label, and an
expected result before it could say anything about playing a rhythm.

## Try a variation

Encode a sixteen-slot rhythm. You need two bytes. Decide which slots go in which
byte and whether the order is obvious to someone else. Hand it over and see.

## Check your understanding

1. What does `$C0` clap as, over eight slots?
2. Name three things an eight-bit rhythm encoding does not capture.
3. Why does adding note lengths double the size of the encoding?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The bit encoding follows C03. The absence of sound material in this project is
recorded in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- **It makes no claim that the Apple-1 or the Replica 1 Plus can produce sound.**
  No source in this project documents such a capability, and none has been
  measured.
- No rhythm here has been played by any machine. All of it is clapped.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
