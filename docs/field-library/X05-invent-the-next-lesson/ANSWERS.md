# X05 Answer key

## Part A: sections 1 to 6

Acceptance criteria:

- **Objective** contains a verb you could watch. Reject "understands,"
  "appreciates," "is aware of," "learns about."
- **First result** is a thing that exists when the learner is done: a filled
  table, a sorted list, a drawn diagram, a decoded word. Not a feeling.
- **Three actions or fewer**, counted honestly. Reading a sheet is one action.
- **Audience** matches the objective's ambition. A BUILD objective with a LOOK
  time budget will not work.

## Part B: fix the objective

| # | Rewritten |
|---|---|
| 1 | Converts a number under 256 to hexadecimal and back. |
| 2 | Names two design decisions the Apple-1 made to save cost, and says what each cost the user. |
| 3 | Labels three hypothetical artifacts as original, replica, or restored, with a reason for each. |
| 4 | Reads a load, store, or jump instruction and states its meaning in English. |

The pattern: every rewrite names a **product**. Something exists afterwards that
did not before, and you can look at it.

## Part C: count the actions

| # | First result | Actions | Note |
|---|---|---|---|
| 1 | Hex table | 3 | Read the rule, fill 0 to 9, fill A to F. This is S03. |
| 2 | A program entered and running | **Not permitted** | See below. |
| 3 | Three statements sorted | 3 | Read the bins, sort, check. This is S04. |
| 4 | A byte list decoded | 3 | Read the rule, strip the high bit, look up. |
| 5 | Four-room map | 3 | Read the example, draw, trace a path. This is R04. |

**Item 2 could not be a first result in this library**, and not because of the
action count. Entering and running a program on the machine is amber at best:
the RAM-only artifacts carry no live-run authority, hand entry is a separate
operator-led step, and a lesson cannot grant what an operator has not.

A learner who answers "too many actions" has missed the more important objection.

## Part D: sources

Acceptance: every Apple-1-specific or historical claim has either a source or an
entry in the "no source yet" column. An empty second column is a warning sign, not
an achievement.

Every packet in this library has open items. Examples a learner can look at: the
128-character second exit in A05, whose intent is unknown; the absence of a
divide instruction in R03, argued from absence; the sound question in R05, where
no source addresses it either way.

## Part E: the status label

Acceptance: **OFF-DEVICE**, in almost every case. If a learner proposes RAM-ONLY,
ask what authority they think it carries. The answer is none they can give.

If a learner cannot answer "could a learner finish without going near the
machine" with yes, the lesson needs redesigning. Relabelling it does not help.

## Part F: the answer key plan

Acceptance: a number, a split between determinate and open-ended, and a stated
method for judging the open-ended ones.

What this library does, and what a learner can copy: supply a fully worked
example plus explicit acceptance criteria, so two educators judging two learners
reach the same verdict. See A06, R04, X03, and X04, all of which are open-ended
and all of which are keyed that way.

"I would use my judgement" is not an answer key.

## Part G: the safety gate

**Any yes means the lesson does not go in the library.** Not "needs review." Does
not go in.

The follow-up question, whether the lesson *describes* any of these without
instructing them, is the one that catches people. H04's Part B item 5 covers it: a
lesson explaining how firmware loading works would violate the curriculum's rule 6
even if nobody ever acted on it.

The line this library draws: naming a category so a reader recognises it is
permitted. Describing how to perform it is not.

## Part H: the review gate

Acceptance: honest answers, including "no."

Note that **no lesson currently in this library has formally been through this
gate.** Each carries its own source notes with open verification items, and page
numbers throughout are unverified against the local collection copies. A learner
who notices that their proposal is being held to a standard the existing lessons
have not formally met has noticed something true, and the right response is that
the gate applies to all of them.

## Part I: retrospective card

Common findings when learners card an existing lesson:

- The "no source yet" section is longer than the lesson's own summary suggests.
- Section 12's describe-versus-instruct question is sharper than any check the
  lesson applied to itself.
- Section 5's action count sometimes needs generous interpretation.

All three are useful. The card is stricter than the lessons, which is the correct
direction for a gate to point.

## Try a variation

Same as Part I.

## README: Check your understanding

1. **You cannot watch understanding.** An objective has to name something the
   learner produces or does, so that a second person could tell whether it
   happened. "Converts a number to binary and back" is checkable; "understands
   binary" is a hope.
2. **Because the sourced list records work you have done and the unsourced list
   records risk you are carrying.** A lesson's failure mode is a claim that
   sounded right and was never checked. Writing it down is what stops it becoming
   a fact by repetition, and every packet in this library has such a list.
3. **It does not go in the library.** The gate is not a flag for extra scrutiny;
   it is a boundary on what this library is permitted to contain, and it applies
   to describing those actions as well as to instructing them.
