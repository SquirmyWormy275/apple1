# M03 Answer key

## Part A and Part B: the recorded results

| Input | Screen | Buffer | Returned | Instructions |
|---|---|---|---|---:|
| `A` + CR | `A` CR | `A` CR | true | 20 |
| `HI` + CR | `HI` CR | `HI` CR | true | 30 |
| `HELLO` + CR | `HELLO` CR | `HELLO` CR | true | 60 |
| `APPLE-1` + CR | `APPLE-1` CR | `APPLE-1` CR | true | 80 |

These are the values recorded in `../EMULATOR-RUNS.md`. A learner's run should
match exactly. If it does not, the discrepancy is the finding, and per
`docs/emulator-demo-guide.md` it should be retained as a software issue.

## Part C: the pattern

**Instructions = 10 x (characters + 1).**

Check: 1 character gives 20, 2 gives 30, 5 gives 60, 7 gives 80. All four fit.

The "+1" is the carriage return, which goes round the same loop as a typed
character before the comparison ends it. The 10 is the number of instructions in
one pass of the loop.

A learner who predicts 110 for a nine-character input and gets 110 has done the
strongest thing available in this lesson: predicted an unseen number from a
model and been right.

## Part D: the second program

1. **The screen shows the text twice:** `HI` CR `HI` CR. The buffer still holds
   `HI` CR once. The program reads the line, then reads the buffer back out
   through the same display call.
2. **`returned_to_monitor` is `false`.**
3. **The last three bytes are `4C 00 03`, which is `JMP $0300`:** a jump back to
   the program's own start, not to the Monitor. So it loops forever rather than
   exiting. The harness runs out of input and stops; on a real machine it would
   keep going until reset.
4. **No, it does not follow the rule.** `line-input-0300.hex` ends with
   `4C 1F FF`, `JMP $FF1F`, and does follow it. `line-input-echo-0300.hex` ends
   with `JMP $0300` and has no self-directed exit at all.

   This is worth stating carefully rather than calling it a bug. The software
   library describes the program as reading the buffer back "before starting
   over," so the loop may well be intended. But the consequence is real: a
   future operator-led session involving this program would end by reset, not by
   the program returning. That finding is recorded in `../EMULATOR-RUNS.md` and
   flagged for the repository owner.

   A learner who notices this unprompted has done genuinely good work.

## Part E: what a pass does not buy

| # | Supported? | Why |
|---|---|---|
| 1 | **Yes** | Directly demonstrated by the screen and buffer output. |
| 2 | **Yes**, for `line-input-0300.hex` | `returned_to_monitor: true`. Not for the echo variant. |
| 3 | **No** | The harness supplies keystrokes itself. No physical keyboard was involved. |
| 4 | **No** | There is no display in this harness. "Screen text" is a string the harness accumulated. |
| 5 | **No**, and this one is subtle | The runs show these bytes behave sensibly. A transcription error that produced a *different but still sensible* program would pass. See M02 Part E, where `04` became `40`. |
| 6 | **No** | Nothing here touches serial at all. The harness emulates no serial hardware. |

Item 5 is the one worth discussing. A green run is consistent with correctness.
It is not the same as correctness.

Item 6 is the one that matters for this project. It is precisely the inference
the repository's evidence rules exist to block.

## Part F: break it on purpose

No single answer. Common informative results:

- Changing `8D` (the CR comparison) to another value: the loop no longer stops on
  Enter, and the run consumes all input or hits the instruction ceiling.
- Changing `04` in `99 00 04` to `40`: the program still runs and still returns,
  but the buffer field comes back empty, because characters went to `$4000`
  instead. This reproduces M02's dangerous-error case and is the best single
  experiment in this lesson.
- Changing `1F` in `4C 1F FF`: `returned_to_monitor` becomes false.

Confirm the learner worked in a scratch copy. `software/ram-only/` must be
unchanged afterwards.

## Try a variation: predicting `APPLE-1`

Seven characters, so 10 x 8 = **80 instructions**. The recorded run gives 80.

## README: Check your understanding

1. **Because a prediction written afterwards is not a prediction.** Any output
   looks reasonable once you have seen it. Writing first is what makes a
   mismatch visible, and a mismatch is the only thing in the exercise that
   teaches you something you did not already know.
2. **Because a program can produce correct-looking output and still not come
   back.** The echo variant does exactly that: the screen text is fine and the
   exit is missing. Separating the two fields is what makes that visible.
3. **Any three of:** whether the board powers on; whether the display shows
   anything; whether a keypress reaches `$D010`; what firmware is on the
   Propeller; whether the EEPROM holds the image anyone believes it holds;
   whether a byte crosses the serial port. All exactly as unknown as before the
   run.
