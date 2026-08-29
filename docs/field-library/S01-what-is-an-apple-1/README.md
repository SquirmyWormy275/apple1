# S01 What is an Apple-1?

**Audience:** LOOK
**Time:** 10 minutes
**Status:** OFF-DEVICE
**Prerequisites:** none

## You will learn

By the end, you can look at three different things people all call "an Apple-1"
and say which one is a circuit board, which one is a program, and which one is a
modern reproduction.

## Why this matters

People use the name "Apple-1" for at least three different things, and they are
not interchangeable. One is a piece of 1976 hardware, one is a small piece of
software, and one is a machine built decades later. Keeping the three apart is
the difference between an accurate museum label and a wrong one, and it is the
habit that the rest of this library depends on.

## First result

A three-part diagram in which you have written the correct name on each part:
the board, the monitor, and the replica.

## What you need

- Paper and a pencil, or a plain-text editor.
- `assets/three-parts-blank.txt` (the worksheet).
- `assets/three-parts-labeled.txt` (the answer, kept closed until step 3).

Nothing here needs a powered machine, a cable, or a serial port.

## Activity

1. Open `assets/three-parts-blank.txt`. Read the three boxes without writing
   anything yet. Each box describes one thing.
2. Write a name on each blank line. Use exactly one of: **the board**, **the
   monitor**, **the replica**.
3. Open `assets/three-parts-labeled.txt` and compare. That is your first result.

`ACTIVITY.md` continues with two short sorting exercises. `ANSWERS.md` has every
answer.

## Explain what happened

**The board.** A *circuit board* is a flat piece of insulating material with
metal traces printed on it that connect the chips soldered to it. The Apple-1
was sold as one assembled board and nothing else. About two hundred were made,
and the retail price was $666.66. That price bought the board alone: the buyer
still had to find a keyboard, a power supply, and a video display before it
could do anything. What made it notable was that a keyboard and a display were
the normal way to use it. Competing hobby machines of the time, such as the
Altair, were operated with rows of switches and lights.

**The monitor.** This is the word that causes the most confusion, because
"monitor" also means a display screen. In this library, a *monitor program* is
a small program stored permanently in a chip that runs the moment you reset the
machine. Steve Wozniak named it that himself, describing a short program that
watched the keyboard and did the job the old front-panel switches used to do.
It is 256 bytes. Not 256 kilobytes, and not 256 megabytes: 256 individual bytes,
about the size of a short paragraph of text. It lives in *ROM*, read-only
memory, which is memory that keeps its contents when the power is off. The
monitor does three things and no more: it can show you what is stored at a
memory address, change what is stored there, and start running a program at an
address. It is a tiny toolset, not an operating system.

**The replica.** A *replica* is a newly manufactured object built to reproduce
an older design. The machine this repository documents is a Replica 1 Plus, a
modern reproduction board sold with its own user manual. It behaves similarly to
an original Apple-1 and includes a Woz Monitor in its ROM, along with BASIC and
an assembler that no 1976 Apple-1 shipped with. It is a replica. It is not an
original Apple-1, it is not worth what an original is worth, and a result you
get on it is a result about a replica.

The three parts are related but separate. The board is hardware. The monitor is
software that happens to live in a chip on that hardware. The replica is a
different, newer piece of hardware that runs a version of the same software.

## Try a variation

Write a one-sentence museum label for a Replica 1 Plus sitting on a table, in
under 25 words, that would not mislead a visitor into thinking it is an
original. Compare yours with the sample label in `ANSWERS.md`.

## Check your understanding

1. A friend says "I have an Apple-1 on my desk at home." Name two follow-up
   questions that would tell you whether they mean an original board or a
   replica.
2. The Woz Monitor is 256 bytes. Is that hardware or software, and how do you
   know from the sentence alone?
3. The Apple-1 sold for $666.66. What did the buyer still have to supply before
   the machine could display anything?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Full citations, with page numbers and the exact wording each claim rests on, are
in `SOURCE-NOTES.md`. In short:

- Board price, quantity, bare-board sale, and the keyboard-and-display point:
  Owad, *Apple I Replica Creation*, foreword and chapter 1.
- The name and size of the monitor program: Wozniak's foreword in the same book;
  the `$FF00` to `$FFFF` range in its chapter 7.
- Replica 1 Plus ROM contents and monitor behavior: Briel Computers,
  *Replica 1 Plus User Manual*, June 2014.

What this lesson does **not** establish:

- It does not show that this project's Replica 1 Plus powers on, displays text,
  or communicates over its serial port. Nothing here was run on hardware.
- It does not identify which firmware image is currently installed on this
  machine. A manual, a vendor source archive, or a published listing is
  candidate evidence about a design, not proof of an installed EEPROM image.
- It does not authorize any hardware action: no firmware load, no EEPROM write,
  no CFFA1 write, no serial-port open, and no physical modification.
