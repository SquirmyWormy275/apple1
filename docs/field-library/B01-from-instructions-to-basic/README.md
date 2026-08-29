# B01 From instructions to BASIC

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A01

## You will learn

By the end, you can look at a task and say which of assembly or BASIC would suit
it better, and give a reason that is about the task rather than about which
language you prefer.

## Why this matters

The A-series taught you to think in single instructions. BASIC is a different
altitude: one line does what a dozen instructions would. Neither altitude is
correct. Knowing which one a job wants is a real skill, and it survives long
after these particular languages.

## First result

Five tasks matched to the more convenient language, with a reason each.

## What you need

Paper. `assets/same-job-two-ways.txt`. Nothing powered on.

## Activity

1. Read `assets/same-job-two-ways.txt`, comparing the two versions of the same
   job.
2. In `ACTIVITY.md` Part A, match five tasks to a language and write one reason
   for each.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**A high-level language does bookkeeping for you.** `PRINT "HELLO WORLD"` in
Apple-1 BASIC finds the text, walks through it, knows where it ends, calls the
display routine, and comes back. In assembly all of that is yours to write, and
you must also decide how the text is stored and how the end is marked.

**What you get in exchange for that bookkeeping.** Control and size. The
assembly version does exactly what you wrote, uses exactly the memory you chose,
and runs at the speed of the instructions. The BASIC version does whatever
BASIC's authors decided, which is usually reasonable and occasionally not what
you wanted.

**And BASIC has to be there.** On an original Apple-1, BASIC lived in RAM at
`$E000` and had to be loaded from cassette or typed in by hand every time the
machine was switched on. Later replicas put it in ROM so it is available
immediately. Assembly needs nothing but the machine.

**Apple-1 BASIC has real edges, and they are instructive.** It handles integers
only. Ask it for 38 divided by 9 and it answers 4, discarding the remainder;
`MOD` gives you the 2 separately. Variables are named with a letter or a letter
and a digit, and strings need a `$` on the end and must be told their maximum
length in advance. `INPUT` always prints a question mark and there is no way to
turn that off.

None of that is a defect. It is a small language on a small machine, and every
one of those limits bought space somewhere else.

**Choosing between them.** Some rough guidance, all of it defeasible:

*BASIC suits* arithmetic, prompting for input, anything where you would otherwise
write a lot of bookkeeping, and anything you will change often. Typing a new line
and running it is much faster than reassembling by hand.

*Assembly suits* anything that touches hardware registers directly, anything that
must fit in a fixed small space, anything where you need to know exactly what
happens, and anything BASIC cannot express. `line-input-0300.hex` reads `$D011`
and `$D010` and calls a ROM routine; you would not attempt that in BASIC.

*Neither is a general answer.* The question "which language is better" has no
content. "Which language suits this job" always does.

**A note on this library.** No runnable BASIC environment is packaged in this
repository. The BASIC lines in this lesson are drawn from published examples and
are read, not run. If you have access to a machine with BASIC in ROM, running
them is a separate matter governed by the project's own rules, not by this
lesson.

## Try a variation

`line-input-0300.hex` reads a line of text and stores it. BASIC's `INPUT`
statement also reads a line of text and stores it. List three things the assembly
version can do that `INPUT` cannot, and two things `INPUT` does that the assembly
version does not.

## Check your understanding

1. Name one thing BASIC does for you in `PRINT "HI"` that assembly would make
   you write.
2. Why is "which language is better" a question with no answer?
3. Apple-1 BASIC answers `PRINT 38/9` with 4. Is that a bug?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

BASIC's behavior is cited from Owad's chapter on programming in BASIC; the memory
arrangement from his chapter on the machine. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- No BASIC program here has been run. There is no runnable BASIC environment in
  this repository, and the examples are read from published sources.
- Nothing about this project's machine, including whether its ROM contains BASIC.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
