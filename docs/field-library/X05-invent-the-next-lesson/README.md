# X05 Invent the next lesson

**Audience:** BUILD
**Time:** 75 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A06, H04, and at least four lessons completed

## You will learn

By the end, you can propose a lesson for this library that is accurate, safe, and
buildable, using the same card its existing lessons were held to.

## Why this matters

This is the last lesson in the catalog, and it is the one that lets the catalog
grow. It is also the best test of whether the rest landed: proposing a lesson
requires you to state an objective, find your sources, pick a status label, and
say what your lesson will not establish, which is every discipline this library
has been teaching, applied at once.

## First result

Sections 1 to 6 of an author card, filled in: a lesson with an objective and a
first result reachable in three actions.

## What you need

Paper. `assets/author-card.txt`. The curriculum's own authoring template in
`docs/apple1-learning-library-curriculum.md`. The shared source pool in
`../SOURCES.md`.

## Activity

1. Pick something you understand well enough to teach.
2. Fill in sections 1 to 4 of `assets/author-card.txt`.
3. Fill in sections 5 and 6: the first visible result, and the three actions or
   fewer that reach it. That is your first result.

## Explain what happened

**An objective is something you could watch someone do.** "Understands
hexadecimal" is not one, because you cannot watch understanding. "Converts a
number under 256 to hexadecimal" is, because you can hand someone a number and
see.

If your objective contains "understands," "appreciates," or "is aware of", rewrite
it until it contains a verb you could film.

**Three actions to a visible result is the hardest constraint.** It is the
curriculum's rule and it is the one that forces the lesson to be about something
rather than around something. If your first result takes six steps, the lesson
starts too far back; find a smaller result and put the rest afterwards.

Three actions is not three minutes. It is three things the learner does. Reading
the sheet, writing three words, and checking the answer is three actions and can
take fifteen minutes.

**Sources before writing, and the honest column.** Section 7 asks for every
Apple-1 or historical claim and where it comes from, and then asks for the claims
you have no source for yet.

That second list is the important one. Every lesson in this library has one, and
each carries a numbered verification item recording what remains unchecked. A
lesson proposal with an empty "no source yet" list has usually not looked hard
enough.

**Pick the status label honestly, and expect it to be OFF-DEVICE.** Every lesson
in this library is off-device. If your proposal is not, ask what changed. The
RAM-only artifacts carry no live-run authority, and a lesson cannot grant it.

Writing OFF-DEVICE is not a formality. It is a statement that a learner can
complete your lesson without going near the machine, and if they cannot, the
lesson needs redesigning rather than relabelling.

**Every question needs an answer, including the open-ended ones.** Section 9 asks
how many questions and how the open-ended ones will be judged. "It depends" is not
an answer key. What the existing lessons do is supply a worked example plus
explicit acceptance criteria, so an educator can judge two different learners
consistently.

If you cannot say how you would judge an answer, the question needs rewriting.

**Section 10 is not optional.** What the lesson does not establish. Every lesson
here has one and they are specific: not "this is only an introduction" but "this
does not show that this board reads a keypress."

**Section 12 is a gate, not a checklist.** Any yes means the lesson does not go in
the library. Not "gets extra review." Does not go in. The curriculum's rule 6 lists
five of those categories and the preservation dossier adds the rest, and a lesson
containing one is outside what this library is allowed to be.

Note that this applies to *describing* them as much as to doing them. H04's Part B
covers that: some things are red as writing.

**Then look at the review gate.** The curriculum ends with a checklist to apply
before a lesson joins the catalog. Run your proposal against it. Nothing in this
library has formally been through it, which is itself an open item, and your
proposal has as much right to be checked as any of them.

## Try a variation

Fill in an author card retrospectively for a lesson that already exists here.
Compare what the card demands against what the lesson actually delivers, and note
anything the card would have caught.

## Check your understanding

1. What is wrong with "the learner understands binary" as an objective?
2. Why does the "no source yet" list matter more than the sourced list?
3. What happens to a proposal with one yes in section 12?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The card's structure comes from the curriculum's own authoring template and
review gate. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- **A completed author card is a proposal, not an approval.** It grants nothing
  and adds nothing to the catalog.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification, and no lesson proposed through it may either.
