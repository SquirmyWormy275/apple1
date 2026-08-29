# B04 Sorting by hand

**Audience:** LEARN
**Time:** 40 minutes
**Status:** OFF-DEVICE
**Prerequisites:** B03

## You will learn

By the end, you can sort five cards by a fixed rule, count the work it took, and
say what happens to that work when the list gets longer.

## Why this matters

Sorting is the classic first algorithm because it is obvious what "done" means
and not at all obvious how much work getting there costs. It is also where most
people first meet the idea that two correct procedures can differ enormously in
what they cost, which matters far more on a machine measured in kilobytes than
on a modern one.

## First result

Five cards in order, with the number of comparisons it took written down.

## What you need

Five cards or scraps of paper numbered 1 to 5. `assets/sort-trace.txt`. Nothing
powered on.

## Activity

1. Lay the cards out as `5 3 1 4 2`.
2. Apply the rule on the worksheet: compare neighbours left to right, swap when
   the left one is bigger, repeat passes until a pass makes no swaps.
3. Record the order, comparisons, and swaps for each pass. That is your first
   result.

## Explain what happened

**The rule is the whole algorithm.** Compare two neighbours, swap if they are out
of order, keep going. It is called a bubble sort, because on each pass the
largest remaining value rises to the end like a bubble.

It is not a good sorting algorithm. It is an excellent first one, because you can
hold the entire rule in your head and still be surprised by how much work it
does.

**Why one pass is not enough.** A single pass moves the largest value all the way
to the right, because once you pick it up you keep swapping it along. But smaller
values only move one place left per pass. If the smallest card starts at the far
right, it needs one pass for every position it has to travel.

That asymmetry is the whole cost of the algorithm.

**Counting the work.** With five cards each pass makes four comparisons, and you
need several passes plus one final pass that makes no swaps to know you are done.
That last pass finds nothing and is not wasted: it is how the procedure knows to
stop. An algorithm needs a stopping condition it can actually check.

**What happens as the list grows.** Ten cards means nine comparisons per pass and
up to nine passes. A hundred cards means ninety-nine per pass and up to
ninety-nine passes. The work does not double when the list doubles; it roughly
quadruples, because both the length of each pass and the number of passes grow
together.

That is the intuition worth carrying away. Some procedures cost proportionally
more as the input grows. Others cost disproportionately more, and those are the
ones that work fine in testing and fall over in use.

**Why this matters on a small machine.** On an Apple-1 the difference is not
abstract. Sorting a hundred items with this rule is around ten thousand
comparisons, each of which is several instructions. On a machine of this era that
is a visible wait. Choosing a better rule is not premature optimization; it is the
difference between a program that finishes and one that appears to have hung.

**A better rule exists, and you have half of it already.** If after each pass you
know the last position is settled, the next pass does not need to check it. That
one observation removes a growing chunk of the work for free, and it is the sort
of thing you notice by counting rather than by thinking about it in the abstract.

## Try a variation

Sort `1 2 3 4 5`, already in order. Count the comparisons and the swaps. Then
sort `5 4 3 2 1`, exactly backwards. Compare the two totals and say what the
difference tells you about when this algorithm is cheap.

## Check your understanding

1. Why does the procedure need a final pass that changes nothing?
2. A card starts at the far right and belongs at the far left. How many passes
   does it need?
3. If ten cards take about 100 comparisons, roughly how many will twenty take?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

This lesson carries no Apple-1-specific claim except the instruction-count
observation, which is discussed in `SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine. No
sorting program has been written or run. It authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification.
