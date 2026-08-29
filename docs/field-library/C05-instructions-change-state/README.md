# C05 Instructions change state

**Audience:** BUILD
**Time:** 50 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C01, C02, C03

## You will learn

By the end, you can take a short list of instructions and predict, line by line,
what every register and memory location holds afterwards, including when the
answer is "unknown."

## Why this matters

Reading an instruction and predicting a program are different skills. A program
is a sequence of small changes to a small amount of state, and the only way to
know what it does is to track that state. Tracing on paper is how every 6502
programmer debugs, and it is the skill that makes the rest of the A-series
possible.

The lesson also teaches something people get wrong for years: knowing when you
do **not** know a value.

## First result

A four-row state trace with the accumulator and one memory location filled in.

## What you need

Paper and a pencil. `assets/state-trace.txt` and `assets/branch-trace.txt`.

## Activity

1. Read the four-instruction program at the top of `assets/state-trace.txt` and
   the four rules underneath it.
2. Fill in the A column and the `$0400` column for steps 1 through 4.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**State is everything the machine currently holds.** For our purposes: the
accumulator A, the index registers X and Y, one carry bit, and whatever is in
memory. An instruction changes a small, specific part of it and leaves the rest
alone. Tracing means writing down the whole picture after each step.

**Walking the program.**

`LDA #$41` puts `$41` into A. `$0400` is untouched. This is the load.

`ADC #$01` adds. And here is the honest complication: `ADC` means *add with
carry*. It adds the number, plus the carry bit, which lives outside A and is left
over from whatever happened before. Nothing in this program set it. So the
correct trace entry for A after step 2 is either `$42` or `$43`, depending on a
bit the program never established.

That is not a trick question. It is the actual behavior, and it is why careful
6502 programs put a `CLC`, clear carry, immediately before an `ADC`. A program
that omits it works most of the time and fails when something upstream happened
to leave the carry set. This library's own emulator harness starts with the carry
clear, so a run there gives `$42` every time, which is exactly how a bug like
this hides.

`STA $0400` copies A into address `$0400`. A is unchanged; copying is not moving.
Now two places hold `$42`.

`JMP $FF1F` sets the next address to `$FF1F`, the Monitor's warm entry. No
register changes. Control leaves.

**Reading it as characters.** `$41` is `A` and `$42` is `B`. The program loads
the letter A, adds one, and stores the letter B. Adding one to a letter gets you
the next letter, because ASCII assigns consecutive numbers to consecutive
letters. That is C04 paying off.

**Branches are just a conditional change to "next."** The second worksheet
introduces `DEX`, subtract one from X, and `BNE`, branch if the last result was
not zero. A branch does not compute anything. It only decides which instruction
happens next, based on a flag that a previous instruction set.

Counting loop passes is where off-by-one errors live, which is why the worksheet
asks separately how many times the body ran and how many times the branch was
taken. Those two numbers are never the same.

**Writing "unknown" is a real answer.** In step 0 of the trace, A and `$0400` are
marked `?`. That is correct. Before the program runs, nothing has established
what is in them. A learner who writes `$00` has invented a fact, which is the
S04 failure wearing different clothes.

## Try a variation

Insert `CLC` as a new first instruction. Say what changes in the trace, what
stays the same, and why the program is better for it even though the emulator's
answer does not move.

## Check your understanding

1. After `STA $0400`, what is in A?
2. Why is the value of A after `ADC #$01` not fully determined by this program?
3. `JMP` changes no register at all. What does it change?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction semantics from Owad's instruction reference. The traced program was
executed in this repository's emulator during authoring and the result recorded;
see `SOURCE-NOTES.md` and `../EMULATOR-RUNS.md`.

What this lesson does **not** establish:

- The emulator result is software evidence about ten bytes. It says nothing
  about this project's Replica 1 Plus.
- The program in this lesson is a paper exercise. It is not offered for entry on
  hardware, and this packet gives no procedure for doing so.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open,
  or physical modification.
