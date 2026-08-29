# A06 Answer key

Design work does not have single correct answers. What follows is a worked
example, plus the acceptance criteria to judge a learner's card against.

## Worked card: purpose 1, fill memory with a character

**1. Purpose.** Fill `$0400` through `$040F` with the character `*`.

**2. Inputs.** None from the user. The character `$AA` (`*` with the high bit
set) and the length 16 are both fixed in the program.

**3. Outputs.** Sixteen bytes of memory change. Nothing appears on screen. A, X,
and Y are left holding working values that the program does not promise anything
about.

**4. Memory.**

| | |
|---|---|
| Program at | `$0300` to about `$030C` (estimate, 13 bytes) |
| Data at | `$0400` to `$040F` |
| Clearance | 243 bytes, a little under one page |

**5. Exit.** `JMP $FF1F`, returning to the Monitor. Reachable on every path:
**yes**, there is only one path, a single loop with one way out.

**6. Test cases.**

| Case | Input | Expected |
|---|---|---|
| Typical | run it | `$0400` to `$040F` all hold `$AA`; `$0410` unchanged |
| Empty | length of 0 | Would fill 256 bytes, not none. Not reachable here since the length is fixed, but worth writing down |
| Biggest | length of 16, the fixed value | Last byte written is `$040F`, not `$0410` |
| Wrong | none possible, no user input | |

**7. What it does not do.** No user-chosen character. No user-chosen length. No
check that the destination is writable RAM.

**8. Status.** OFF-DEVICE.

A program matching that card:

```text
0300  A0 0F     LDY #$0F
0302  A9 AA     LDA #$AA
0304  99 00 04  STA $0400,Y
0307  88        DEY
0308  10 FA     BPL $0304
030A  4C 1F FF  JMP $FF1F
```

Thirteen bytes, so the estimate in section 4 was right. Counting down with `DEY`
and `BPL` fills `$040F` down to `$0400` and stops correctly, because `DEY` on
`$00` gives `$FF`, which has bit 7 set.

Note the "empty" test case row. It could not happen in this program, and writing
it down anyway is what would have caught the problem in a version where the
length was a variable.

## Acceptance criteria for a learner's card

**Section 1.** One sentence, no "and" joining two purposes. A purpose containing
"and then" is two programs.

**Section 2.** Describes the range of possible values, not just the expected
ones. "A key" is weaker than "any key, including control characters."

**Section 3.** Names what has changed when the program stops. A card that lists
only screen output for a program that fills a buffer has missed an output.

**Section 4.** Ranges must not overlap. Check the arithmetic: start plus length
minus one. Zero clearance should be flagged, not failed.

**Section 5.** An exit is named. The reachability answer is honest. "Not sure" is
acceptable and better than a wrong "yes."

**Section 6.** Expected results are written and are specific. "It works" is not
an expected result. The "biggest" case must actually reach a boundary; a
"biggest" of 3 in a 16-byte buffer does not.

**Section 7.** Not blank. Three items. This is the most-skipped section and the
one that most reliably indicates whether the learner designed or just wrote.

**Section 8.** Filled in, and OFF-DEVICE unless there is a specific reason
otherwise. A learner who writes RAM-ONLY should be asked what authority they
think that carries. The answer is none that this lesson can give.

## Part G: review criteria

The five review questions in order of how often they find something: section 7
blank, "biggest" not hitting a boundary, purpose containing "and," exit
reachability unexamined, ranges overlapping.

## Try a variation and Part H: retrospective card for `line-input-0300.hex`

| Section | Content |
|---|---|
| Purpose | Read a line of typed characters into a buffer, echoing each. |
| Inputs | Keyboard, via `$D010` and `$D011`. Any byte with bit 7 set. |
| Outputs | The buffer at `$0400` onward, including the carriage return. Characters on screen. Y left holding the count. |
| Memory | Program `$0300` to `$0319`. Data `$0400` to `$047F` worst case. Clearance 230 bytes. |
| Exit | `JMP $FF1F`. **Reachable on every path: yes, but by two different routes**, carriage return and Y reaching `$80`. |
| Test cases | Typical `HI`; empty just Return; biggest 128 characters with no Return; wrong a control character |
| Does not do | Backspace, explicit length limit, case conversion, buffer terminator beyond the stored CR |
| Status | RAM-ONLY, no live-run authority |

**What the card makes you notice that reading did not:** the exit reachability
question forces you to find the second exit. In A05 that came from being told to
look at `BPL $0315`. Here it falls out of asking a routine question about every
path.

That is the argument for the card. It asks the questions that catch the things
you would not have thought to look for.
