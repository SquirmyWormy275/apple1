# B04 Activity: sort five cards

**Status:** OFF-DEVICE. Cards and paper. Nothing runs on any machine.

## Part A: the sort (this is the first result)

Complete `assets/sort-trace.txt` for the starting order `5 3 1 4 2`. Record the
order, comparisons, and swaps after every pass, including the final pass that
makes no swaps.

## Part B: best and worst

Repeat for two more starting orders and fill in the totals.

| Starting order | Passes | Comparisons | Swaps |
|---|---:|---:|---:|
| `5 3 1 4 2` | | | |
| `1 2 3 4 5` | | | |
| `5 4 3 2 1` | | | |

## Part C: predict without counting

| Cards | Comparisons per pass | Passes at most | Comparisons at most |
|---:|---:|---:|---:|
| 5 | | | |
| 10 | | | |
| 20 | | | |
| 100 | | | |

Then: when the number of cards doubles, what happens to the last column?

## Part D: the wasted pass

1. Why does the procedure need a pass that makes no swaps?
2. Could you stop without it? What would you need to know instead?
3. Is the final pass wasted work or necessary work? Defend your answer.

## Part E: the free improvement

After the first pass, the largest card is definitely in the last position. After
the second, the two largest are.

1. How many comparisons could you skip on pass 2?
2. On pass 3?
3. Roughly what fraction of the total work does this save for 100 cards?
4. Does it change how the work grows when the list doubles?

Question 4 is the important one.

## Part F: a different rule

Try this instead: find the smallest card anywhere in the row, move it to the
front, then repeat with the rest.

1. Sort `5 3 1 4 2` this way and count comparisons.
2. Compare with your Part A total.
3. Does this rule have a best case and a worst case, or does it always cost the
   same?

## Part G (optional): what would it take on the machine

Sketch, in English rather than 6502, what a program would need in order to sort
bytes in the buffer at `$0400`. List what it needs to keep track of. Do not write
any bytes.

## What this activity does not do

It sorts cards on a table. It writes no program, runs nothing, and authorizes no
hardware action.
