# B04 Answer key

## Part A: the sort

Starting order `5 3 1 4 2`. Four comparisons per pass.

| Pass | Order at end | Comparisons | Swaps |
|---:|---|---:|---:|
| 1 | `3 1 4 2 5` | 4 | 4 |
| 2 | `1 3 2 4 5` | 4 | 2 |
| 3 | `1 2 3 4 5` | 4 | 1 |
| 4 | `1 2 3 4 5` | 4 | 0 |

**Total comparisons 16. Total swaps 7.**

Pass 1 walk-through, for checking a learner's work: compare 5 and 3, swap, giving
`3 5 1 4 2`; compare 5 and 1, swap, giving `3 1 5 4 2`; compare 5 and 4, swap,
giving `3 1 4 5 2`; compare 5 and 2, swap, giving `3 1 4 2 5`. The 5 travelled all
the way in one pass because once you pick it up you keep carrying it.

## Part B: best and worst

| Starting order | Passes | Comparisons | Swaps |
|---|---:|---:|---:|
| `5 3 1 4 2` | 4 | 16 | 7 |
| `1 2 3 4 5` | 1 | 4 | 0 |
| `5 4 3 2 1` | 5 | 20 | 10 |

**Already sorted is the cheapest case:** one pass, no swaps, and the procedure
stops. **Exactly backwards is the most expensive:** every comparison swaps, and
every card has to travel the full distance.

## Part C: predict without counting

| Cards | Comparisons per pass | Passes at most | Comparisons at most |
|---:|---:|---:|---:|
| 5 | 4 | 5 | 20 |
| 10 | 9 | 10 | 90 |
| 20 | 19 | 20 | 380 |
| 100 | 99 | 100 | 9,900 |

**When the number of cards doubles, the last column roughly quadruples.** 10 to
20 goes from 90 to 380, a little over four times. The reason is that both factors
grow: each pass gets longer *and* you need more passes.

## Part D: the wasted pass

1. **Because that is how it knows it is finished.** The procedure has no other
   way to tell. Nothing in the row announces that it is sorted.
2. **You could stop without it if you knew in advance how many passes were
   needed**, which for n cards is at most n minus 1. That trades a check for a
   count.
3. **Necessary.** It produces information: "no swaps happened, therefore
   everything is in order." A pass that changes nothing is not the same as a pass
   that does nothing. This is the same idea as M04's expected-versus-observed:
   confirming that nothing changed is a result.

## Part E: the free improvement

1. **One comparison** skipped on pass 2, because the last position is settled.
2. **Two** on pass 3.
3. **Roughly half.** Instead of 99 comparisons every pass you do 99, then 98,
   then 97, and so on, which totals about half of 99 times 99.
4. **No.** And this is the important answer.

   Halving the work is a real and worthwhile saving. But the work still roughly
   quadruples when the list doubles, because you have halved a quantity that is
   still growing with the square of the length. Twice as fast is not the same as
   growing more slowly.

   That distinction, between making something faster and changing how it scales,
   is the single most useful idea in this lesson.

## Part F: a different rule

1. **Ten comparisons.** Finding the smallest of 5 takes 4 comparisons, then of 4
   takes 3, then 2, then 1: 4 + 3 + 2 + 1 = 10.
2. **Better than Part A's 16** for this input.
3. **It always costs the same.** Finding the smallest of what remains takes the
   same number of comparisons regardless of the order, so there is no best or
   worst case for comparisons. Already-sorted input costs exactly as much as
   backwards input.

   That is a genuine trade. Bubble sort can finish in one pass if it gets lucky;
   this rule never gets lucky and never gets unlucky. Which you prefer depends on
   whether your input tends to be nearly sorted already.

   Note also that this rule still roughly quadruples when the list doubles. Both
   rules are in the same growth class; they differ in constants and in variance,
   not in scaling.

## Part G: what would it take on the machine

A sketch, in English. The program would need to keep track of:

- The start address of the run, `$0400`.
- How many bytes are in it, or where it ends.
- A position for the outer pass.
- A position for the inner comparison.
- Whether any swap happened this pass, so it knows when to stop.
- Somewhere to put a byte temporarily while two are exchanged, since swapping two
  memory locations needs a third holding place.

The last one catches people. You cannot exchange two values without somewhere to
put one of them, and on this machine that is either a register or a spare byte of
memory.

Accept any answer that lists a position, a bound, and a way to know when to stop.
A learner who spots the need for temporary storage during the swap has done well.

## Try a variation: sorted and reverse-sorted

From Part B: already sorted costs 4 comparisons and 0 swaps; exactly backwards
costs 20 comparisons and 10 swaps.

**What the difference tells you:** this algorithm is cheap when the input is
nearly in order and expensive when it is badly out of order. Its cost depends on
the input, not just its size. Any claim about how long it takes has to say what
the input looked like, which is why "how fast is it" is usually an incomplete
question.

## README: Check your understanding

1. **Because that pass is how it knows it is done.** Without a pass that produces
   no swaps, the procedure has no evidence that the row is in order.
2. **Four passes**, for five cards. A card moving left travels one position per
   pass, so a card at the far right of five needs four passes to reach the far
   left. This is the asymmetry that makes the algorithm expensive.
3. **About 400.** Doubling the list roughly quadruples the work.
