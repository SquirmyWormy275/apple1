# B03 Algorithms: recipes for information

**Audience:** LEARN
**Time:** 35 minutes
**Status:** OFF-DEVICE
**Prerequisites:** none

## You will learn

By the end, you can say what makes a procedure an algorithm, find the ambiguous
step in an everyday set of instructions, and rewrite it so a literal follower
cannot go wrong.

## Why this matters

Every program you will ever write is a set of instructions for something that
takes them completely literally and never asks a clarifying question. Most
programming bugs are not mistakes in logic; they are places where the programmer
knew what they meant and the machine did not.

Finding ambiguity in a sandwich recipe is the same skill as finding it in code,
and it is much easier to practise on the sandwich.

## First result

One ambiguous step rewritten so it cannot be misread.

## What you need

Paper. `assets/ambiguity-hunt.txt`. Nothing powered on.

## Activity

1. Read the four properties at the top of `assets/ambiguity-hunt.txt`.
2. Mark the ambiguous words in the four-step recipe.
3. Rewrite step 2 so a follower who knows nothing about sandwiches cannot get it
   wrong, and count your words. That is your first result.

## Explain what happened

**An algorithm is a procedure with four properties.**

*Finite:* it ends. A procedure that can run forever is not an algorithm, however
useful it might be.

*Definite:* every step is exact. No step leaves a choice to the follower's
judgement.

*Effective:* every step can actually be carried out. "Find the largest prime
number" is exact and never done.

*General:* it works for any valid input, not just the one you had in mind. A
procedure that only sorts the list `3, 1, 2` is not an algorithm for sorting.

**Ambiguity hides in ordinary words.** "Some bread" does not say how much, or
that it should be two slices, or that they should be separate. "Spread butter on
it" does not say on which surface, how much, or that only one side of each slice
is involved. "Add filling" does not say what, or where, or that the second slice
then goes on top. "Cut it" does not say where, how many times, or in what
direction.

A human reader supplies all of that from experience without noticing. That
supplying is exactly what a computer cannot do.

**Being exact is expensive, and that is the real lesson.** Rewriting "spread
butter on it" precisely takes many more words than the original, and most people
are surprised how many. This is not a sign that you are bad at it. It is the true
cost of precision, and it is why programs are long.

**Where to stop.** You cannot specify everything. At some point you rely on the
follower knowing what "spread" means, just as a program relies on the machine
knowing what `LDA` means. The skill is choosing the right level: exact about
everything that could reasonably differ, and relying on shared ground for the
rest.

The question to ask is not "is this fully specified" but "could a reasonable
follower do something other than what I meant."

**Order is part of the specification.** "Cut it and serve" happens to be in the
right order. Swap two steps in a recipe and it often still reads fine while
producing something quite different. Programs are the same, and an out-of-order
program is harder to spot than a missing one because nothing looks wrong.

**Connecting back to the machine.** `line-input-0300.hex` is an algorithm.
Finite, because carriage return or a full buffer ends it. Definite, because every
instruction has exactly one meaning. Effective, because each instruction is one
the processor can perform. General, because it works for any sequence of typed
characters and not just one.

Notice that "definite" is free in machine code. An instruction cannot be
ambiguous. All the ambiguity lives one level up, in what the programmer thought
they were asking for.

## Try a variation

Write instructions for tying a shoelace, exactly, for someone who has never seen
a shoe. Stop when you give up, and note where you stopped. Everyone gives up
somewhere; the interesting part is where.

## Check your understanding

1. Which of the four properties does "keep adding one forever" fail?
2. Why can machine code never be ambiguous, and where does the ambiguity go
   instead?
3. A recipe works for a cheese sandwich but not for any other filling. Which
   property does it fail?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The four properties are standard computing-science definitions and are not
Apple-1-specific. The machine-code example is this repository's artifact.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine. It
authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
