# A06 Design a tiny utility

**Audience:** BUILD
**Time:** 60 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A05

## You will learn

By the end, you can plan a small program on one page before writing any bytes,
including what it does not do and how you will know it worked.

## Why this matters

Writing bytes is the easy part. The expensive mistakes are decided before that:
picking an address that collides with something, discovering halfway through that
you needed a second buffer, or building something with no way out. All of those
are cheap to fix on paper and dear to fix in hex.

The design card also produces the thing this library keeps asking for: a written
expectation, recorded before the result, against which the result can be checked.

## First result

A completed design card for one small utility.

## What you need

Paper. `assets/design-card.txt`. A05's reading of `line-input-0300.hex` as a
worked reference.

## Activity

1. Pick one purpose from the list in `ACTIVITY.md`, or invent one that fits in a
   single sentence.
2. Fill in sections 1 through 4 of `assets/design-card.txt`.
3. Fill in section 6, the test cases, writing the expected result for each before
   you write any instructions. That is your first result.

## Explain what happened

**Purpose in one sentence, and mean it.** "Read a line and store it" is one
purpose. "Read a line, store it, and display it in reverse" is two, joined by an
"and." Two purposes in 26 bytes is how programs become unreadable. Split them, or
choose one.

**Inputs means the full range, not the expected case.** If input comes from the
keyboard, the possible values include every key, not just the ones you had in
mind. Most bugs live in the values you did not consider, so the design card asks
what is *possible* rather than what is *typical*.

**Outputs means what has changed when it stops.** A program that leaves a
character on screen has one output. A program that fills a buffer has another. A
program whose only output is a value left in a register has one too, and it is
worth writing down, because a value in a register vanishes the moment the Monitor
starts using it.

**Memory is where the accidents happen.** Write down the program's address range
and the data's address range, and check they do not overlap. A02's collision
exercise was this mistake made concrete: a 26-byte program at `$0300` runs to
`$0319`, so a buffer at `$0310` is inside it.

The clearance line asks how much room is between them. Zero clearance is legal
and fragile: it breaks the moment the program grows by one instruction. A page of
clearance, as `$0300` and `$0400` have, survives ordinary editing.

**Exit is the one people forget.** M05 exists because of this. Write down how the
program finishes and what takes control. Then ask the harder question: is the
exit reachable on *every* path? A program with three branches and one exit needs
all three branches to arrive there. A05's program has two exits, one of which
nobody documented.

"Not sure" is an allowed answer on the card, and it is more useful than a
confident wrong one.

**Test cases, with expectations written first.** Four kinds, and they are chosen
to catch different failures:

*Typical* is the case you had in mind. It almost always passes and it proves
almost nothing.

*Empty* is the zero case: no characters typed, an empty buffer, a count of zero.
A03 showed why: a loop with a count of zero runs 256 times, not none.

*Biggest* is the boundary: the full buffer, the last address, the largest value.
A05's 128-character limit lives here.

*Wrong* is the input you did not design for: a key you were not expecting, a
control character, a value out of range.

**"What it does not do" is a feature of the design, not an apology.** A05's
program has no backspace, and that is a legitimate choice for 26 bytes. Writing
the omission down means it was decided rather than overlooked, and it tells the
next person reading the code that they have not found a bug.

**Section 8 is not optional.** Every program in this project carries a status
label. A design that has not decided whether it is off-device, RAM-only, or
awaiting approval is a design that has not thought about where it will run. The
default for anything you design in this library is OFF-DEVICE, and moving beyond
that is a separate, operator-led decision governed by
`docs/apple1-software-library.md`, not something a design card grants.

## Try a variation

Take `line-input-0300.hex` and fill in a design card for it retrospectively, as
if you were about to write it. Compare what the card makes you notice against
what you noticed reading it in A05.

## Check your understanding

1. Why does the card ask for possible inputs rather than typical inputs?
2. What is wrong with a design whose program and data ranges touch exactly, with
   no clearance?
3. Why write expected results before writing the program?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The status labels and the acceptance requirements are this repository's; the
worked example is its artifact. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- **A completed design card grants nothing.** It is a plan on paper. It does not
  make a program safe to run, and it does not create RAM-only or live-run
  authority.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
