# X03 Answer key

Design work has no single right answer. Below is a worked script and the criteria
to judge a learner's against.

## Worked three-minute script

**0:00 The hook.** "The whole operating system on this machine is 256 bytes.
That is about the length of this sentence, repeated four times."

**0:20 The object.** "This is a Replica 1 Plus, a modern reproduction of the
Apple-1 that Steve Wozniak designed in 1976. It is not one of the originals;
about two hundred of those were made."

**0:45 The one idea.** "A computer does not know what a byte means. The same
number can be a letter, an instruction, or just a number, and the only thing that
decides is what the program does with it."

**1:15 The show.** Hold up a card reading `C8 C9 A0 D4 C8 C5 D2 C5`. "Every one
of these is a number. Watch what happens if I treat them as letters." Subtract
`$80` from each on a second card and reveal `HI THERE`. Then: "and if the machine
had jumped to this instead of reading it, `C8` would have meant add one to a
counter."

**2:15 The question back.** "This byte is `$41`, which is 65. If A is 65, what do
you think B is?"

**2:45 Where to go next.** "There is a whole library of these written out. If you
want the one that starts from nothing, ask for S01."

**The fallback:** there isn't one, because nothing above uses the machine. The
cards work on a table, in a corridor, in a power cut. If the machine happens to be
available it sits there being looked at, which is all a visitor needs from it.

That is the model. Not "a demo with a backup," but a demo that never needed the
machine.

## Part B: rate your hook

| # | Verdict |
|---|---|
| 1 | **Weak.** A label. Nothing surprising, nothing to stay for. |
| 2 | **Good.** Contains a surprise, and the surprise is true. |
| 3 | **Bad, twice over.** |
| 4 | **Good.** Surprising and accurate, and it leads somewhere. |
| 5 | **Weak.** Announces a lecture. "Let me tell you about" is a warning to the listener. |

**Hook 3's two problems:** it makes a **value claim**, which this library does not
make and which you are not the person to make; and if the object is a replica,
"very rare" is **inaccurate**, because replicas are manufactured products. It is
the H02 error and the value error in one sentence.

## Part C: one idea

Acceptance: exactly one circled, two visibly crossed out. A learner who keeps two
has not done the exercise, and their demo will run long.

## Part D: the show, without hardware

Acceptance criteria:

- **Uses no powered machine at all.** If the show needs the machine, it fails.
- The audience watches something change, rather than listening to a description.
- It fits inside about a minute.
- It connects to the one idea from Part C rather than being a separate trick.

Strong options: decoding a byte list into words; sorting cards while the audience
predicts; tracing a loop on a whiteboard with the audience calling the next
value; the C03 bit strip with a volunteer building a number.

## Part E: the question back

Acceptance: answerable in under ten seconds, needs no prior knowledge, connects to
the one idea, and has a definite answer so the visitor knows they got it.

"If A is 65, what is B?" passes all four. "What do you think of the 6502
architecture?" passes none.

## Part F: the four failures

| Failure | A good plan |
|---|---|
| No power | Nothing changes. The demo never used it. |
| Machine unavailable | Same. Show the cards, describe the object, and say it is not here today. |
| A question you cannot answer | "I do not know." Then, if you can: "here is how you would find out." Never guess in public; a guess repeated by a visitor becomes a rumour with your name on it. |
| What is it worth | "I genuinely do not know, and I am not the person to ask. Replicas and originals are very different objects and the difference matters a lot to collectors." Pleasant, honest, and it moves on. |

The last two share a principle: **the honest answer is short and the dishonest one
is long.** If you find yourself explaining at length, check whether you are
covering for not knowing.

## Part G: what you will not say

Acceptance for the first list: three real cuts, each with a reason. "There was no
time" is a valid reason.

For the second list, the inaccurate things, any three of:

- Calling the replica an Apple-1 without qualification.
- Any statement about its value or rarity.
- "This is what an original would do," about anything not measured.
- Any claim that the machine works, or that any part of it works.
- A timing claim, such as how fast anything runs.
- Stating that the ROM contains any particular firmware.

The last two are the ones learners miss, because they do not feel like claims.

## Part H: run it

The test is whether the listener can state your one idea afterwards. If they
describe the object instead, the demo was about the object and the idea did not
land.

## Try a variation: ninety seconds

The hook and the show survive. The object naming survives, shortened, because it
must. What goes is the question back and where-to-go-next.

**What that tells you:** the demo is the hook and the show. Everything else is
scaffolding. If your ninety-second version keeps a different pair, that is worth
knowing about your own priorities.

## README: Check your understanding

1. **Because in this project the machine is not available for it.** There is an
   unresolved serial fault, an opened serial session is blocked pending a
   measurement test card and an explicit operator start, and running any program
   is a separate operator-led decision that a demonstration does not get to make.
   Beyond this project: a demo that depends on hardware fails in public.
2. **It contains nothing surprising and gives a stranger no reason to stay.** A
   name is what a label is for. A hook has to offer something the visitor did not
   already have.
3. **That you do not know and are not the person to ask**, and that replicas and
   originals are very different objects. This library makes no claim about the
   value of anything, and neither should you while standing next to it.
