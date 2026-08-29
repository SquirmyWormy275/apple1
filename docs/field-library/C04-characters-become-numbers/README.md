# C04 Characters become numbers

**Audience:** LEARN
**Time:** 35 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C03

## You will learn

By the end, you can turn a typed character into the byte a program would see,
strip a high bit to read a byte list back as text, and say which parts of that
are ASCII, which are Apple-1 convention, and which are an emulator's choice.

## Why this matters

A computer stores no letters. It stores numbers, and everyone agrees which
number means which letter. Understanding that agreement is what lets you look at
`C8 C9 A0` and see words instead of noise. It is also where a specific,
sourced Apple-1 quirk lives, and knowing exactly how far that quirk extends is
the difference between reading a byte list correctly and guessing.

## First result

A completed character table for six characters, with plain and high-bit values.

## What you need

Paper. `assets/char-journey.txt` and `assets/encoding-worksheet.txt`. The ASCII
chart in Owad's Appendix A if you have the book to hand, though the worksheet
gives you enough.

## Activity

1. Read `assets/char-journey.txt`, following `A` from keypress to byte.
2. Fill in Part 1 of `assets/encoding-worksheet.txt` for B, Z, 0, space, and
   carriage return.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**ASCII is an agreement.** The American Standard Code for Information
Interchange assigns a number to each character: `A` is 65, `B` is 66, space is
32, carriage return is 13. It assigns decimal 0 through 127 only, which is half
of what a byte can hold. Everything above 127 is unassigned by the standard.

Two consequences follow, and both matter here.

**First, letters are consecutive.** `A` is 65 and `B` is 66, so you can get from
a letter to the next one by adding 1. The digits are consecutive too: `0` is 48,
`1` is 49. That is not an accident, it is what makes character arithmetic
possible.

**Second, seven bits is enough.** 127 fits in seven bits, so bit 7 is spare. The
Apple-1's keyboard puts a seven-bit ASCII value on its data lines when you press
a key. And the Woz Monitor's own listing carries the note that when it loads a
keyboard character, bit 7 should be 1.

So in Monitor terms, `A` typed at the keyboard is not `$41`. It is `$C1`:
`$41` with the top bit set. Carriage return is not `$0D` but `$8D`.

**This is a convention, not a law of nature.** The letter did not change. Nothing
about ASCII changed. A particular machine's input path sets a spare bit, and
programs written for that machine expect it. Read a byte list from this
repository and you will see `$8D` where you expected `$0D`, and the reason is
this and only this.

**Reading a byte list back as text.** Strip the top bit, then look up the
result. `C8` minus `$80` is `$48`, which is `H`. Do it across a list and words
appear. Doing it in the other order, looking up `$C8` in an ASCII table, gets
you nothing, because ASCII does not assign anything to 200.

**Where the convention stops.** Three different things are easy to blur here.

- **ASCII** is a published standard. `A` is 65 everywhere, on every machine
  built since 1963.
- **The Apple-1 keyboard high bit** is a property of that machine's input path,
  documented in the Monitor listing.
- **This repository's emulator** takes ordinary seven-bit text on its command
  line, `--input "HI"` followed by a carriage return, and applies the high-bit
  convention itself before the program sees it. That is the harness being
  convenient. It is not a third fact about the Apple-1, and a byte value you see
  in an emulator transcript may have been shaped by the harness rather than by
  anything historical.

Keeping those three apart is the C04 version of the S04 sorting habit.

**One more wrinkle: case.** In ASCII, `A` is `$41` and `a` is `$61`. They differ
by bit 5, worth 32. The Replica 1 Plus manual states that the machine
understands upper case only, and that a PS/2 keyboard is set with caps lock on
by default. So the lower-case half of the table is real ASCII that this family
of machines is documented not to use.

## Try a variation

Work out what `$D4` decodes to, then explain why someone reading a byte list
without knowing about the high bit might reasonably conclude the machine was
using some other character set entirely.

## Check your understanding

1. Convert `HI` into the bytes a Monitor keyboard read would produce.
2. Why can a program convert a digit character into the number it represents by
   subtracting `$30`?
3. An emulator transcript shows a byte as `$C8`. Name two different things that
   could be responsible for the top bit being set.

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

ASCII values from Owad's chart; the seven-bit keyboard path and the Monitor's
bit-7 expectation from Owad's keyboard section and the Monitor listing in the
Briel manual; the emulator's input handling from the tool itself. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish:

- It does not show what byte this project's board would actually produce for a
  keypress. Nothing was measured. The high-bit convention is documented
  behavior, not an observation of this machine.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open,
  or physical modification.
