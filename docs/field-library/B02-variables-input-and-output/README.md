# B02 Variables, input, and output

**Audience:** LEARN
**Time:** 35 minutes
**Status:** OFF-DEVICE
**Prerequisites:** B01

## You will learn

By the end, you can plan a small program as four boxes, ask, get, work, tell, and
name its variables correctly for Apple-1 BASIC.

## Why this matters

Almost every small useful program has this shape. A calculator, a quiz, a unit
converter, a lookup: all of them ask for something, receive it, do something to
it, and report back. Recognizing the shape means you can plan a program before
knowing any syntax.

## First result

A completed four-box flow diagram for one program of your own.

## What you need

Paper. `assets/flow-diagram.txt`. Nothing powered on.

## Activity

1. Read the four boxes on `assets/flow-diagram.txt`.
2. Pick one job from `ACTIVITY.md` Part A and fill in the four lines at the
   bottom of the sheet, plus the variable name and type.
3. Check your variable name against the naming rules in `ANSWERS.md`. That is
   your first result.

## Explain what happened

**A variable is a named box for one value.** In BASIC you do not choose an
address; you choose a name, and BASIC decides where it lives. That is the whole
difference from A02, where you picked `$0400` yourself.

**Apple-1 BASIC's names are short.** An integer variable is a letter, or a letter
and a digit: `A`, `N`, `A1`, `B8`. A string variable is a letter with a `$` on
the end: `A$`, `R$`, `N$`. That is all. `TOTAL` is not a legal integer name and
`NAME$` is not a legal string name, because both are too long.

This surprises people used to modern languages, and it changes how you write.
With one or two characters to work with, a comment or a note beside the program
carries the meaning that a long name would.

**Strings must be told their size first.** `DIM N$(20)` reserves twenty
characters for `N$`. Each character takes one byte, and the maximum is 255. If
you forget to dimension a string before using it, you have not told BASIC how much
room to set aside.

**Input always announces itself.** `INPUT "WHAT IS YOUR NAME", N$` prints the
prompt, and then prints a question mark whether you want one or not. There is no
way to switch it off. Write your prompts knowing a `?` is coming.

**Output is `PRINT`, and the punctuation matters.** A semicolon joins pieces
together on one line: `PRINT "YOUR NAME IS "; N$` puts the text and the variable
side by side. Quotation marks are the difference between a variable and its name:
`PRINT N$` prints what is in the variable, and `PRINT "N$"` prints the two
characters N and dollar sign.

**Keep the first program to one input and one result.** Two inputs double the
places a program can go wrong and do not teach anything the first one did not.
Once ask, get, work, tell runs correctly, adding a second input is a small change.

**Where the four boxes come from.** They are the same input, processing, output
from S02, with "ask" split out because a program that reads without prompting
looks broken to the person using it. The machine does not need the prompt. The
person does.

## Try a variation

The `WORK` box in a quiz is a comparison rather than a calculation: is the answer
right? Redraw the four boxes for a one-question quiz and say what changes in the
`TELL` box.

## Check your understanding

1. Which of these are legal Apple-1 BASIC variable names: `A`, `A1`, `SUM`,
   `N$`, `NAME$`, `Z9`?
2. Why must a string be dimensioned before use?
3. What is the difference between `PRINT N$` and `PRINT "N$"`?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Variable naming, dimensioning, `INPUT` behavior, and `PRINT` punctuation are all
cited from Owad's chapter on programming in BASIC. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish:

- No BASIC program in this packet has been run. There is no runnable BASIC
  environment in this repository.
- Nothing about this project's machine.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
