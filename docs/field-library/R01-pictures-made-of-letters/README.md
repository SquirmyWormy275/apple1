# R01 Pictures made of letters

**Audience:** LOOK
**Time:** 25 minutes
**Status:** OFF-DEVICE
**Prerequisites:** none

## You will learn

By the end, you can design a banner that fits a 40-column display, using only
upper-case printable characters, and say why it has to be planned before it is
drawn.

## Why this matters

The Apple-1's display shows characters, not pixels. It has no bitmapped graphics
at all: the video section stores a character's code and looks up its shape in a
small ROM, so only the characters in that ROM can appear on screen.

That sounds like a limitation, and it is, but it is also a constraint that
produced a genuine craft. Working inside it teaches something that unlimited
tools do not.

## First result

A 40-column banner, drawn on the grid, that fits.

## What you need

Paper and a pencil. `assets/grid-40.txt` and `assets/banner-examples.txt`.
Nothing powered on.

## Activity

1. Look at `assets/banner-examples.txt` and count the width of the second
   example against the ruler on `assets/grid-40.txt`.
2. Choose a word of five letters or fewer.
3. Draw it on the grid, counting columns as you go. That is your first result.

## Explain what happened

**The canvas is characters, not dots.** Each position on the display holds one
character. You cannot draw a diagonal line; you can place characters that
suggest one. The whole art is choosing characters whose shapes, at a glance,
read as something else.

**Forty columns is not many.** A readable block letter needs about five columns
and five rows. Five letters at five columns each, with two columns of gap
between, is 33 columns. Six letters is exactly 40. Seven does not fit.

So the first decision is the word, and it is a real constraint rather than a
formality. "APPLE" fits comfortably. "COMPUTER" does not, at that size, and you
either shrink the letters until they stop being readable or choose another word.

**Weight is the only shading you have.** `#` and `@` read as solid, `+` and `=`
as medium, `.` and `'` as light. Using three weights suggests depth. Using seven
different characters usually reads as noise, because the eye cannot rank them
quickly.

**Upper case only, and it is not arbitrary.** The Replica 1 Plus manual states
that the machine understands upper case only, and that a PS/2 keyboard has caps
lock on by default. This library follows the same rule for material intended for
the display, and the repository's formatting tool enforces it: text passed
through it comes back upper-cased, with anything unsupported replaced by a
visible `?` rather than silently dropped.

That visible `?` is worth noticing. It is the same principle as the M04 stop
rule: make the problem visible rather than quietly losing information.

**No going back.** On the original machine, once a character was sent to the
display it could not be modified. It stayed until it scrolled off the top or the
whole display was cleared. There is no erasing and no editing in place.

This is why the lesson insists on planning before drawing. On paper you can
rub out a mistake. On the machine the design has to be right before the first
character is sent, and a design that runs one column too wide has no recovery.

**Why plan on paper at all.** Because counting is easier than fixing. A banner
that overruns by one column is not a small error; it wraps, and everything after
it is displaced. The ruler at the top of the grid exists so you can count before
committing rather than discovering afterwards.

## Try a variation

Design a banner for a word that does not fit at five columns per letter. Solve it
in two different ways: by making the letters narrower, and by using two lines.
Say which reads better and why.

## Check your understanding

1. Why can the Apple-1 not display an arbitrary picture?
2. How many five-column letters fit in 40 columns with two-column gaps?
3. Why does a character on the display need to be right the first time?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The display's character-based operation and its write-once behavior are cited
from Owad; the upper-case rule from the Briel manual and this repository's own
formatting tool. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- No banner in this packet has been displayed on any machine. Nothing here was
  seen on a screen.
- Nothing about this project's board or its display.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
