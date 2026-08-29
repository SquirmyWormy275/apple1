# S02 A computer is not magic

**Audience:** LOOK
**Time:** 10 minutes
**Status:** OFF-DEVICE
**Prerequisites:** none

## You will learn

By the end, you can trace one keypress from your finger to a letter on the
screen, naming input, memory, processing, and output at the right points.

## Why this matters

"The computer did it" is where most explanations stop. On a machine this small
you can go further, because there is no operating system, no driver stack, and
no window manager in the way. A key goes into a numbered slot, a program checks
that slot, and a letter comes out. That is the whole story, and it is small
enough to hold in your head at once.

## First result

A completed five-step trace, in order, from your finger to the letter on screen.

## What you need

Paper and a pencil. `assets/key-to-screen.txt` and `assets/trace-blank.txt`.

## Activity

1. Read `assets/key-to-screen.txt` once, top to bottom.
2. Cover it. On `assets/trace-blank.txt`, write the five step names in order:
   input, mailbox, processing, memory, output.
3. Uncover and check. That is your first result.

## Explain what happened

Start with the friendly version. Imagine a mail room with a wall of numbered
pigeonholes. Two of them have jobs. One is "things the keyboard left for you."
The other is a little flag that goes up when something new has been left. A
clerk walks past, sees the flag up, takes the item out, copies it into a
pigeonhole of their own choosing, then carries it to a third slot marked
"outgoing," but only when the outgoing slot is empty.

Now the real terms, in the same order.

- **Input** is anything that brings information in from outside. Pressing a key
  puts that character's seven-bit ASCII value on the keyboard's data wires and
  sends a pulse on a separate wire called the strobe, meaning "the value is
  ready now."
- The numbered slots are **memory addresses**. An address is just a number that
  names one storage location. On the Apple-1 the keyboard character lands at
  address `$D010` and the flag lives at `$D011`. The `$` means the number is
  written in hexadecimal, which lesson S03 covers.
- **Processing** is the CPU, the *central processing unit*, the chip that reads
  instructions and acts on them. It checks the flag at `$D011` repeatedly, and
  when the flag is set it reads the character out of `$D010`. Checking the same
  place over and over until something changes is called **polling**.
- **Memory** is storage the program can use freely. The CPU copies the character
  somewhere it picked, so it still has it after the keyboard slot is reused.
- **Output** sends information back out. The display has its own slot at
  `$D012`. Before writing, the CPU checks the top bit of `$D012` and waits until
  it goes low, meaning the video section has finished with the previous
  character. Then it writes, and the video section turns the number into the
  shape of a letter.

Two things are worth noticing. The CPU never talks to the keyboard or the screen
directly. It only reads and writes numbered slots, and separate circuitry deals
with the physical devices. And the CPU spends most of its time waiting, checking
a flag that has not changed yet. That is normal.

## Try a variation

Trace what has to be different when the machine *prints* a letter that nobody
typed, as it does when a program writes to the screen on its own. Which of the
five steps drop out? Answer in `ANSWERS.md`.

## Check your understanding

1. Which two of the five steps involve a numbered slot that the hardware, not
   the program, decided on?
2. Why does the CPU check a flag before reading the keyboard character, instead
   of just reading it whenever it wants?
3. The CPU checks the display slot *before* writing to it. What would go wrong
   if it did not?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Cited in `SOURCE-NOTES.md` against the shared pool in `../SOURCES.md`. The
address numbers and the flag-then-read sequence come from Owad's description of
the 6821 in the Apple-1; the keyboard strobe and seven-bit value come from the
same chapter.

What this lesson does **not** establish:

- The trace is how the design is documented to work. Nothing here was measured
  on this project's Replica 1 Plus, and no step of it has been observed on that
  machine.
- It does not authorize a firmware load, an EEPROM write, a CFFA1 write, a
  serial-port open, or any physical change. Reading a trace on paper is the
  whole of this lesson.
