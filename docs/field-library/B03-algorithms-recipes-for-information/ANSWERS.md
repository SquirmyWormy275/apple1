# B03 Answer key

## Part A: the sandwich

Ambiguities, at minimum:

| Step | Ambiguous |
|---|---|
| 1 | "Some" (how much), "bread" (a loaf? slices? how many?) |
| 2 | "Spread" (how thickly), "butter" (how much), "it" (which slice, which face) |
| 3 | "Add" (where), "filling" (what, how much) |
| 4 | "Cut" (where, how many times, which direction), "it", "serve" (to whom, on what) |

A rewritten step 2:

> Take one slice. Identify its two large flat faces. Choose one of them. Using a
> knife, transfer butter from the packet to that face and move the knife across
> the face until the butter covers it in an even layer roughly one millimetre
> thick, stopping at the edges. Repeat for the second slice.

That is about 55 words replacing 5. **A tenfold expansion is normal**, and
learners should be told so, because most assume they have done it badly.

## Part B: which property fails

| # | Property failed | Why |
|---|---|---|
| 1 | **Finite** | It never ends. |
| 2 | **Definite** | "To taste" leaves the amount to judgement. |
| 3 | **Effective** | Pi has no last digit, so the step cannot be carried out. |
| 4 | **General** | It works for one specific list and nothing else. |
| 5 | **Effective** | Division by zero cannot be performed. Accept **definite** if the learner argues the procedure fails to say what to do in that case; that is a good answer for a different reason. |

Item 5 is deliberately arguable. The point is to notice the empty-list case at
all, which is the "empty" test case from A06 in a different setting.

## Part C: order matters

Correct order:

1. Take two slices of bread from the loaf.
2. Spread butter on one face of each slice.
3. Place the filling on the buttered face of the first slice.
4. Put the second slice on top, buttered side down.
5. Cut the sandwich once, corner to corner.

**Two swaps that read fine and are wrong:**

- Swapping 4 and 5: cutting before assembling reads perfectly well and produces
  two half-sandwiches with no top.
- Swapping 2 and 3: buttering after adding the filling reads fine and butters the
  filling.

Both produce a readable procedure and the wrong object, which is exactly the
failure mode of an out-of-order program.

## Part D: rewrite the ambiguous step

| Original | Rewrite | What it assumed |
|---|---|---|
| "Add water until it looks right" | "Add water until the surface of the liquid reaches the 200 ml mark on the side of the jug." | That the follower has seen the correct result before. |
| "Repeat as necessary" | "Repeat steps 3 to 5 until no grains remain visible on the surface." | That the follower knows the stopping condition. |
| "Enter the value" | "Type the four digits of the year, then press Return." | Which value, in what format, and how to finish. |
| "Wait a moment, then continue" | "Wait 30 seconds, then continue." | How long a moment is. |

Every one of the four assumed something the follower would have to already know.
That is what ambiguity is: an unstated dependency on shared knowledge.

## Part E: check an algorithm

| Property | Holds? | Why |
|---|---|---|
| Finite | **Yes** | It stops on a carriage return, and also when Y reaches `$80` after 128 characters. Both routes terminate. |
| Definite | **Yes** | Each instruction has exactly one meaning to the processor. There is nothing to interpret. |
| Effective | **Yes** | Every instruction is one the 6502 performs. |
| General | **Yes** | It works for any sequence of typed characters, not one specific input. The recorded runs used four different inputs and all behaved the same way. |

Note the finiteness argument depends on the second exit, which A05 flagged as an
open question about intent. The program is finite either way; whether the author
knew it is a separate matter.

## Part F: the ambiguity you cannot remove

No single answer. Common ones: "using a knife" assumes the follower can hold and
move a knife; "an even layer" assumes they can judge evenness; "the packet"
assumes they can identify it.

**The good arguments for relying on it:** the follower is a person with hands and
ordinary experience, and specifying how to hold a knife would never end. The good
argument against: if the follower is genuinely a machine, every one of those is a
real gap.

This is the correct answer to the whole lesson. Precision is relative to who is
following. Machine code is definite because the processor's vocabulary is fixed
and small; English is not, because a person's vocabulary is neither.

## Try a variation: the shoelace

Everyone stops somewhere. Common stopping points: describing what a loop is,
describing which direction to pass one lace under another, or describing the
final tightening.

The interesting observation is that the hard parts are the *spatial* ones.
Sequences are easy to write down and shapes are not, which is why knitting
patterns and origami diagrams use pictures rather than sentences.

## README: Check your understanding

1. **Finite.** It never ends.
2. **Because each instruction has exactly one defined meaning to the
   processor.** The ambiguity moves up a level, into the gap between what the
   programmer intended and what they actually wrote. The machine does precisely
   what the bytes say, which is not always what anyone meant.
3. **General.** It works for one case rather than all valid inputs.
