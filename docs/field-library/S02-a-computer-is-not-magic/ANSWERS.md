# S02 Answer key

## Part A: the trace

1 input, 2 a mailbox, 3 processing, 4 memory, 5 output.

Accept "the mailbox" answered as "input" and step 1 as "the keyboard" if the
learner keeps the *order* right. The order is the point.

## Part B: name the slot

| Address | What is kept here |
|---|---|
| `$D010` | The character that came from the keyboard. |
| `$D011` | The flag that says a keyboard character is waiting. |
| `$D012` | The character on its way out to the display. |

## Part C: true, false, or not stated

| # | Answer | Why |
|---|---|---|
| 1 | **F** | The CPU writes to a slot. Separate circuitry drives the screen. |
| 2 | **T** | Stated in the lesson and sourced. |
| 3 | **T** | It checks the top bit of `$D012` and waits for it to go low. |
| 4 | **NS** | Nothing in this lesson was measured on that machine. This is the important one. |
| 5 | **F** | The hardware sets it when a key arrives. The program only reads it. |
| 6 | **F** | Once a character is on the display it cannot be modified. It leaves by scrolling off or by clearing the whole display. |

If a learner marks #4 true, stop and go back to it. Every other answer in this
library depends on not making that move.

## Part D: the waiting question

One line of reasoning: the CPU has nothing else to do. There is no second
program waiting for a turn, so time spent checking a flag costs nothing that
could have been spent elsewhere. Polling is only wasteful when something else
wanted the time.

Accept any answer that recognizes there is no competing work. A learner who says
"it wastes electricity" is not wrong, just answering a different question.

## Try a variation: a letter nobody typed

Steps 1, 2, and 3 drop out. There is no keypress, no keyboard slot, and no flag
to check. The program already has the character. It goes straight to the output
step: wait for the display slot to be free, then write.

## README: Check your understanding

1. **Steps 1 and 2, the input and the mailbox.** The addresses `$D010` and
   `$D011` are fixed by the circuit. The program cannot choose them. Step 4 uses
   an address the *program* picked.
2. **Because the slot always contains something.** Without the flag the CPU
   cannot tell a new keypress from the last one it already read, and would
   either miss keys or read the same one repeatedly.
3. **The previous character would be overwritten before the video section had
   taken it,** and it would never appear. The check is what makes the handoff
   reliable when one side is much slower than the other.
