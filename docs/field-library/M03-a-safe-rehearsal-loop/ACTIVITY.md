# M03 Activity: rehearse and record

**Status:** OFF-DEVICE. This activity runs software on an ordinary computer.
**It does not involve the Replica 1 Plus, and the emulator must not be connected
to any serial device.**

## Part A: predict, then run (this is the first result)

1. Fill in the **prediction** half of `assets/rehearsal-card.txt` for
   `line-input-0300.hex` with input `HI` + CR. Do not run anything yet.
2. Set up and run per `docs/emulator-demo-guide.md`.
3. Fill in the observed half. Compare.

Hand in the card with both halves filled, including a wrong prediction if that
is what happened. A wrong prediction honestly recorded is worth more than a
right one written afterwards.

## Part B: three more runs

Predict each before running. Record all four fields.

| Input | Predicted instructions | Observed |
|---|---:|---:|
| `A` + CR | | |
| `HELLO` + CR | | |
| `APPLE-1` + CR | | |

## Part C: find the pattern

From your four data points, write a rule for the instruction count as a function
of the number of characters typed. Then predict a run you have not done and
check it.

## Part D: the second program

Run `line-input-echo-0300.hex` with input `HI` + CR.

1. What is different about the screen text?
2. What is different about `returned_to_monitor`?
3. Look at the last three bytes of that listing. Explain the difference you
   observed.
4. `software/ram-only/README.md` states the general rule "Exit via `JMP $FF1F`."
   Does this program follow it? Answer carefully.

## Part E: what a pass does not buy

You have four green runs. For each statement, say whether your runs support it.

| # | Statement | Supported? |
|---|---|---|
| 1 | These 26 bytes implement a keyboard read-and-echo loop. | |
| 2 | The program returns control to the Monitor. | |
| 3 | The Replica 1 Plus can read a keypress. | |
| 4 | The Replica 1 Plus display works. | |
| 5 | The byte list contains no transcription error. | |
| 6 | The serial fault in this project is a hardware problem, not a software one. | |

## Part F (optional): break it on purpose

Copy the byte list to a scratch file, change exactly one byte, predict what will
change, and run it. Do not modify anything in `software/ram-only/`.

## What this activity does not do

It runs a software model on an ordinary computer. It does not power on, connect
to, or measure the Replica 1 Plus, and it authorizes no hardware action.
