# S04 Facts, models, and evidence

**Audience:** STUDY
**Time:** 40 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S01

## You will learn

By the end, you can take a statement about a machine or a collectible and place
it in one of three bins: a fact someone observed, a model of how something
should behave, or a claim that nothing has established yet.

## Why this matters

This is the lesson the rest of the library rests on, and it is the one that
carries outside computing entirely.

A manual tells you what a machine was designed to do. A source-code archive
tells you what someone wrote. A photograph tells you what something looked like
on one day. None of the three tells you what the object on your bench is doing
right now. Collectors learn this the expensive way, when a "working, all
original" board turns out to be neither. Careful hobbyists learn it the cheap
way, by writing down which is which before they need to know.

## First result

Three statements sorted into the three bins, with a one-line reason each.

## What you need

Paper. `assets/sorting-card.txt` for the bin definitions. Nothing powered on.

## Activity

1. Read `assets/sorting-card.txt`, which defines the three bins and the question
   to ask for each.
2. Sort these three statements. Write F, M, or C beside each, plus one line of
   reasoning.

   - **(a)** "The Woz Monitor occupies 256 bytes from `$FF00` to `$FFFF`."
   - **(b)** "This board's EEPROM contains the `110REV03` firmware."
   - **(c)** "Opening the FT232R from the host garbled the display."

3. Compare with `ANSWERS.md`. That is your first result.

## Explain what happened

**(a) is a model.** It comes from published documentation of the Apple-1 design.
It is almost certainly true of the design. It is still a statement about how the
machine is *specified*, not a reading taken from this board's ROM. To move it
into the fact bin, someone would have to dump this machine's memory and look.

**(b) is a claim needing evidence.** A copy of the `110REV03` source exists in
this project. That establishes that the source exists. It does not establish
that this source is what was compiled, that what was compiled is what was
written, or that what was written is still there. Three separate gaps, none of
them closed by having the file. The repository's own preservation dossier says
exactly this: the vendor source is candidate evidence, not the installed image.

**(c) is a fact.** Somebody did the thing and recorded what happened. It has a
who, a when, and an observed result. Notice how much less it claims than the
other two. It does not say why the display garbled or what is broken. A fact is
often narrow, and its narrowness is the point.

**The asymmetry worth carrying away.** Facts are expensive and specific. Models
are cheap and general. A model can cover a thousand machines; a fact covers one
machine on one day. When someone offers you a model where you asked for a fact,
they are usually not lying. They are answering an easier question.

**The preservation connection.** In a collection, the words are different but
the bins are the same. "Manufactured in 1976" is a claim until a serial number,
a photograph, or a provenance record backs it. "All original parts" is a claim.
"Working" is a claim, and a specific one: working *how*, tested *when*, by
*whom*. A hash of a file establishes that this file is that file. It does not
establish that the file describes this object. That distinction is the whole
reason this repository hashes its sources and keeps a chain-of-custody table.

**Why this protects you.** The failure mode is not usually a lie. It is a model
that got repeated until it sounded like a fact, and then got acted on. Writing
`M` next to a sentence costs nothing. Discovering you soldered something on the
strength of an `M` costs a great deal more.

## Try a variation

Take a statement you believe about a machine, an object, or a purchase you are
considering. Write down what would have to be true for it to move from `C` to
`F`, and whether anyone has done that. If the answer is "I would have to ask the
seller," that is a useful thing to have discovered on paper.

## Check your understanding

1. A vendor manual states a machine's serial port runs at 9600 baud. Which bin,
   and what would move it?
2. A program runs correctly in an emulator. What does that establish, stated as
   narrowly as you can manage?
3. Why does hashing a manual with SHA-256 not tell you anything about the board
   sitting next to it?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The three worked statements are drawn from this repository's own records. Their
sources are listed in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- It does not resolve statement (b). This lesson uses the open question as a
  teaching example and leaves it open, which is where the repository leaves it.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open,
  or physical modification. Statement (c) describes something that already
  happened and is recorded as a `STOP`. It is not a procedure to repeat.
