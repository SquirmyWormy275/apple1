# A06 Activity: fill the card

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. **Nothing designed here is entered on the Replica 1 Plus, and a
completed card grants no authority to do so.**

## Part A: pick a purpose

Choose one, or write your own in a single sentence.

1. Fill a run of memory with one repeated character.
2. Copy a run of bytes from one address to another.
3. Read a key and store it only if it is a digit.
4. Count how many characters were typed before Return and leave the count in a
   register.
5. Echo every character typed, but stop after a fixed number.

## Part B: sections 1 to 4 (this is the first result, part one)

Fill in purpose, inputs, outputs, and memory on `assets/design-card.txt`.

For the memory section, state the address range of your program even though you
have not written it yet. An estimate is fine; say it is an estimate.

## Part C: section 6, the test cases (this is the first result, part two)

Write four test cases with their expected results **before writing any
instructions**. Typical, empty, biggest, wrong.

## Part D: sections 5 and 7

Exit and what it does not do. For the exit, answer the reachability question
honestly, including "not sure."

## Part E: now write it

Write your instructions with addresses. Then go back to section 4 and correct the
address range to the real one. Note whether your estimate was low.

## Part F: check against your own tests

Run your four test cases, on paper or in the M03 emulator. Record observed
against expected. Any mismatch is a finding, whichever side was wrong.

## Part G: review someone else's card

Swap cards. On the one you receive, look only for these five things:

1. Is the purpose really one sentence?
2. Do the program and data ranges overlap?
3. Is the exit reachable on every path?
4. Does the "biggest" test case actually hit a boundary?
5. Does section 7 contain anything, or is it blank?

Section 7 being blank is the most common defect and the most informative.

## Part H (optional): retrospective card

Fill in a card for `line-input-0300.hex` as though you were about to write it.
Compare against your A05 reading.

## What this activity does not do

It plans and optionally rehearses programs off-device. It enters nothing on
hardware, and a completed card creates no RAM-only or live-run authority.
