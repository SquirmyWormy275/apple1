# M01 Meet the Monitor

**Audience:** LOOK
**Time:** 15 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S01, S03

## You will learn

By the end, you can say what a monitor program is for, name its three jobs, and
explain why it is not an operating system.

## Why this matters

Modern computers hand you a desktop, a file manager, and a thousand programs.
The Apple-1 hands you a prompt and three verbs. Understanding those three verbs
is understanding what a computer minimally needs to be usable at all, which is a
better answer to "what does an operating system do" than most explanations of
operating systems.

## First result

The three jobs named, with an example of each.

## What you need

Paper. `assets/three-jobs.txt`. Nothing powered on.

## Activity

1. Read `assets/three-jobs.txt`.
2. Cover it and write down the three jobs in your own words.
3. Uncover and check. That is your first result.

## Explain what happened

**What a monitor program is.** A *monitor* here is a small program that gives you
direct access to memory. Steve Wozniak coined the usage for this machine: he
wrote a short program that watched the keyboard and did the job the front-panel
switches on earlier computers had done. It occupies 256 bytes.

Before machines like this, using a computer meant setting rows of physical
switches to enter each byte and reading lights to see the result. The Altair
worked that way. The monitor replaced the switches with typing.

**The three jobs.**

*Inspect.* Type an address and press Return. It prints what is there. Type
`300` and it answers `0300: E1`. Type a range with a dot between, like
`300.32F`, and it prints the block, up to eight values per line.

*Change.* Type an address, a colon, and a value. `300: FF` writes `$FF` at
`$0300`. The machine responds by printing the address and the value that was
there before. That response is easy to misread as a refusal; it is not. It is
the old contents, shown once, before the change took effect.

*Run.* Type an address followed by `R`. The Monitor jumps to that address and
starts executing. From that moment the Monitor is no longer in charge, and
whatever you jumped to is.

**Why it is not an operating system.** An operating system manages resources for
programs: memory, files, devices, time. The Monitor does none of that. It cannot
list anything, because there is nothing to list. It has no concept of a file. It
does not track what is running, cannot stop a program, and offers no way to
undo a change. It is closer to a pair of tweezers than to Windows.

That is not a criticism. Three verbs and 256 bytes is a remarkable amount of
capability for the size, and everything else you might want can be built on top
because "run" lets you hand control to anything.

**One consequence worth absorbing now.** Because "run" gives away control
permanently, a program you start has to bring you back deliberately. There is no
supervisor waiting to catch it. That is why the programs in this repository end
by jumping back to the Monitor, and it is the subject of M05.

## Try a variation

The Monitor prints the *old* value when you change a location. Suggest one
reason a designer might choose that over printing the new value, or over
printing nothing at all.

## Check your understanding

1. Name the Monitor's three jobs.
2. Why can the Monitor not stop a running program?
3. A friend calls the Woz Monitor "the Apple-1's operating system." Give one
   specific reason that is misleading.

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The three functions and the command syntax come from the Replica 1 Plus manual's
chapter on programming; the origin of the term and the 256-byte size from
Wozniak's foreword to Owad. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- The command examples are quoted from a manual. They are not a transcript from
  this project's machine, and nothing here shows that this board's Monitor
  responds as documented.
- Nothing in this lesson is an instruction to type anything on hardware. It
  authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
