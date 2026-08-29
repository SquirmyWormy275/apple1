# B03 Activity: hunt the ambiguity

**Status:** OFF-DEVICE. Paper only.

## Part A: the sandwich (this is the first result)

Complete `assets/ambiguity-hunt.txt`: mark the ambiguous words in all four steps,
rewrite step 2 exactly, and count your words.

## Part B: which property fails

| # | Procedure | Property failed |
|---|---|---|
| 1 | "Keep adding one to the total forever." | |
| 2 | "Season to taste." | |
| 3 | "Write down the last digit of pi." | |
| 4 | "To sort: put 3 first, then 1, then 2." | |
| 5 | "Divide by the number of items." (the list may be empty) | |

## Part C: order matters

Here are the steps of a working procedure, shuffled. Put them in order, then say
which two swaps would still produce a readable but wrong procedure.

- Put the second slice on top, buttered side down.
- Take two slices of bread from the loaf.
- Cut the sandwich once, corner to corner.
- Spread butter on one face of each slice.
- Place the filling on the buttered face of the first slice.

## Part D: rewrite the ambiguous step

Each of these appears in real instructions. Rewrite each so a literal follower
cannot go wrong.

1. "Add water until it looks right."
2. "Repeat as necessary."
3. "Enter the value."
4. "Wait a moment, then continue."

For each, say what information the original assumed the follower already had.

## Part E: check an algorithm

Take `line-input-0300.hex` as described in A05. For each of the four properties,
say whether it holds and why.

| Property | Holds? | Why |
|---|---|---|
| Finite | | |
| Definite | | |
| Effective | | |
| General | | |

## Part F (optional): the ambiguity you cannot remove

Find one step in your rewritten sandwich recipe that still relies on the follower
knowing something. State what it is, and argue either that it is safe to rely on
or that it is not.

## What this activity does not do

It analyses instructions on paper. It runs nothing and authorizes no hardware
action.
