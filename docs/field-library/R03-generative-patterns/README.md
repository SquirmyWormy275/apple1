# R03 Generative patterns

**Audience:** BUILD
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** R01, S03

## You will learn

By the end, you can write a rule that produces a pattern, work the first few rows
out by hand, and recognise when a rule is producing more structure than you put
into it.

## Why this matters

R01 made you draw a picture. This lesson makes a picture appear without anyone
drawing it. That difference matters on a machine with very little memory: a
picture costs a byte per character, and a rule costs a few instructions and
produces as many rows as you like.

It is also the first place most people meet the surprise that a short rule can
produce something that looks designed.

## First result

Four rows of a pattern, worked out by hand from a rule.

## What you need

Paper and a pencil. `assets/rule-worksheet.txt` and
`assets/pattern-rules.txt`. Optionally a computer for the extension.

## Activity

1. Read the first rule on `assets/rule-worksheet.txt`.
2. Fill in rows 1 to 4, columns 1 to 12, one character at a time.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**A rule is a question asked at every position.** For each column, ask: does this
number divide exactly by the row number? Print one character if yes and another
if no. That is the whole design. There is no picture anywhere, only a question
and two answers.

**Small rules produce large output.** The first rule, one sentence, produces as
many rows and columns as you have patience for. Stored as a picture, forty
columns by twenty rows is 800 characters. Stored as a rule, it is one sentence.

That ratio is why this technique mattered so much on machines of this size. It is
also why a pattern generator makes a good demonstration: the surprise is the gap
between how little went in and how much came out.

**Some rules produce more than you expect.** The third rule on
`assets/pattern-rules.txt` is Pascal's triangle: each number is the sum of the
two above it. Mark the odd numbers and leave the even ones blank, and a nested
triangular pattern appears. Nobody put a triangle in the rule. It fell out of
addition and parity.

That is worth sitting with. The rule mentions no triangles, no symmetry, and no
nesting. Every one of those is a consequence, and none of them is visible in the
sentence that produced them.

**Working by hand first is not busywork.** Three rows by hand tells you whether
the rule does what you meant. If you generate a hundred rows first and they look
wrong, you have no idea whether the rule is wrong or your reading of the output
is. Three rows you computed yourself is a known-good answer to check against,
which is the M04 expectation habit in another setting.

**Choosing characters matters as much as the rule.** The same pattern in `#` and
`.` reads as texture; in `#` and space it reads as a shape. Dots fill the
background and make the eye see a grid; spaces let the eye see the form. Neither
is wrong, and the difference is dramatic. Try both before deciding.

**Where the arithmetic gets awkward on this machine.** "Divides exactly by" is
easy to say and is division, which the 6502 does not have as an instruction.
Repeated subtraction or a counter that resets is how you would actually do it.
Rules based on counting and resetting are much cheaper than rules based on
division, which is the kind of consideration that shapes what patterns are
practical rather than merely possible.

## Try a variation

Take the row rule and change "divides exactly" to "leaves a remainder of 1."
Predict what changes before working it out, then work out three rows.

## Check your understanding

1. Why does row 1 of the row rule have no dots in it?
2. A pattern is 40 columns by 20 rows. How much smaller is the rule than the
   picture?
3. The triangle rule mentions no triangles. Where does the shape come from?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The patterns on `assets/pattern-rules.txt` were generated during authoring by
applying the stated rules. Citations and method in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- No pattern here has been generated on, or displayed by, this project's machine.
- No claim is made about how fast any of this would run.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
