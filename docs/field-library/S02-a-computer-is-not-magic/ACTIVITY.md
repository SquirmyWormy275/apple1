# S02 Activity: trace one keypress

**Status:** OFF-DEVICE. Paper only. Nothing is powered on or connected.

## Part A: the trace (this is the first result)

1. Read `assets/key-to-screen.txt` once.
2. Cover it. Fill in the five blanks on `assets/trace-blank.txt` from the word
   bank at the bottom.
3. Uncover and check.

## Part B: name the slot

Three memory addresses appear in this lesson. Write what each one holds.

| Address | What is kept here |
|---|---|
| `$D010` | |
| `$D011` | |
| `$D012` | |

## Part C: true, false, or not stated

Mark each T, F, or NS. "Not stated" means this lesson gives you no basis to
decide, which is a legitimate answer and not a cop-out.

1. The CPU sends the letter directly to the screen.
2. The keyboard puts a seven-bit value on its data wires when a key is pressed.
3. The CPU waits for the display slot to be free before writing to it.
4. This project's Replica 1 Plus performs this sequence correctly today.
5. The flag at `$D011` is set by the program.
6. A character that has been sent to the display can be erased by writing a
   space over it.

## Part D (optional): the waiting question

The CPU checks the keyboard flag thousands of times between two keystrokes and
finds nothing almost every time. Write two or three sentences on why that is not
wasteful in this design. There is no single right answer; `ANSWERS.md` gives one
line of reasoning to compare against.

## What this activity does not do

It builds a mental model from documentation. It measures nothing, and it
authorizes no hardware action of any kind.
