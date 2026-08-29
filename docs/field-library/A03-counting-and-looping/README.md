# A03 Counting and looping

**Audience:** BUILD
**Time:** 50 minutes
**Status:** OFF-DEVICE
**Prerequisites:** A02, C03, C05

## You will learn

By the end, you can trace a loop, count how many times its body runs, work out
where a branch goes from its offset byte, and spot an off-by-one before it costs
you an afternoon.

## Why this matters

A02 ended on an awkward note: indexing did not save any instructions, because
everything was written out longhand. The loop is what makes it pay. Four
instructions that repeat are worth more than forty that do not.

Loops are also where the bugs are. Almost every loop bug is a counting error at
one end or the other, and the only reliable defense is being able to trace one by
hand.

## First result

A completed countdown trace with the final value of X.

## What you need

Paper. `assets/countdown-trace.txt` and `assets/offset-card.txt`. Optionally the
M03 emulator.

## Activity

1. Read Program A on `assets/countdown-trace.txt` and the two branch rules
   underneath.
2. Fill in the pass table and the four totals.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**A loop is a body plus a way back.** `DEX` is the body. `BNE $0302` is the way
back. The branch looks at what just happened and decides whether to go round
again.

**Branches test a flag, not a value.** `DEX` does not just change X; it also sets
flags describing the result. The zero flag is set when the result was zero. The
negative flag is set when bit 7 of the result was 1. `BNE` looks at the zero
flag, `BPL` looks at the negative flag. Neither one looks at X directly, which is
why a branch can follow an instruction that touched a different register
entirely.

**Counting the passes.** X starts at 5. `DEX` brings it to 4, and 4 is not zero,
so back we go. This continues until `DEX` produces 0, at which point `BNE` does
not branch and control falls through. The body ran five times and the branch was
taken four.

The body count matches the starting value here. That is not a general rule; it is
a property of counting down to zero with the test at the bottom.

**Where the branch actually goes.** The offset byte `$FD` is a *signed*
displacement counted from the address of the next instruction. `$FD` is 253 as
an unsigned byte, but as a signed byte it is 253 minus 256, which is minus 3. The
next instruction is at `$0305`, so the target is `$0305` minus 3, which is
`$0302`. That is the `DEX`.

Signed bytes are new here. Values `$00` to `$7F` are 0 to 127. Values `$80` to
`$FF` are minus 128 to minus 1. The trick to reading a negative one is to
subtract 256. Bit 7 set means negative, which is the same top bit you met in C03
doing an entirely different job. Context decides.

**A branch cannot go far.** Minus 128 to plus 127 from the following
instruction, and no further. That is a real constraint on how programs are laid
out, and it is why `JMP`, with its full two-byte address, exists alongside
branches.

It is also why branches survive relocation while jumps do not, which is the M02
finding arriving from the other direction: a branch describes a distance, and a
distance does not change when you move both ends.

**Program B and the off-by-one.** Program B changes one byte, `D0` to `10`, so
`BNE` becomes `BPL`: branch while the result is *positive* rather than while it
is *not zero*.

Trace it. X reaches 0, and 0 has bit 7 clear, so 0 counts as positive and the
branch is taken again. `DEX` on 0 gives `$FF`, which has bit 7 set, so now the
branch is not taken. The body ran six times instead of five and X ends at `$FF`,
which is 255 unsigned or minus 1 signed.

One byte, one extra pass, and a final value that is the largest possible byte
rather than the smallest. If that value were then used as a count or an index,
the damage would happen somewhere else entirely and look unrelated.

**The general shape of off-by-one.** The test is at the bottom of the loop, so
the body always runs at least once and always runs one more time than the branch
is taken. Whether the loop stops at zero or one past zero depends on which flag
you test. Neither is wrong in itself; being unclear about which you meant is.

## Try a variation

Change Program A's first instruction to `LDX #$00` and trace it. The answer
surprises most people, and the reason is the same "test at the bottom" property.

## Check your understanding

1. In Program A, how many times does `DEX` run and how many times is the branch
   taken?
2. A branch at `$0310` has offset `$F0`. Where does it go?
3. Why can a branch not reach an address 300 bytes away?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction meanings from Owad's reference; the observed results for both
programs were produced during authoring and are recorded. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish: nothing about this project's machine.
Both programs are paper exercises with no entry procedure. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
