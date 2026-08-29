# A05 Answer key

## Part A: stage summaries

Compare against the block on the worksheet. Accept any wording that keeps the six
stages in order and gets the conditional right in the test stage.

## Part B: instruction by instruction

| Address | Instruction | Contribution |
|---|---|---|
| `$0300` | `LDY #$00` | Set the buffer position to the start. Runs once. |
| `$0302` | `LDA $D011` | Read the keyboard control register to see if a key is waiting. |
| `$0305` | `BPL $0302` | Go back and read again while bit 7 is clear, that is, while no key is ready. |
| `$0307` | `LDA $D010` | Take the character that arrived. |
| `$030A` | `STA $0400,Y` | Write it into the buffer at the current position. |
| `$030D` | `JSR $FFEF` | Call the Monitor's echo routine to display it, and come back. |
| `$0310` | `CMP #$8D` | Was that a carriage return? |
| `$0312` | `BEQ $0317` | If so, leave the loop. |
| `$0314` | `INY` | Advance the buffer position. |
| `$0315` | `BPL $0302` | Go back for another character, while Y is still under `$80`. |
| `$0317` | `JMP $FF1F` | Hand control back to the Monitor. |

## Part C: the two exits

1. **The intended exit is a carriage return**, detected by `CMP #$8D` and
   `BEQ $0317`.
2. **The second is Y reaching `$80`**, which makes `BPL $0302` fall through
   instead of branching.
3. **128 characters.** Y counts 0 through 127 while branching; when `INY` makes
   it `$80`, bit 7 is set and `BPL` is not taken.
4. **`BPL $0302` at `$0315` implements it.** Whether it is deliberate cannot be
   determined from the bytes.

   The argument that it is deliberate: an unconditional `JMP` would have cost one
   more byte and given no limit at all, so choosing a branch here buys a bound
   for free. The argument that it is incidental: `BPL` is the natural thing to
   write after `INY` if you are not thinking about the limit, and 128 is not an
   obviously chosen number.

   **The correct answer is that it is a claim needing evidence**, in the S04
   sense. A learner who says "deliberate" or "incidental" without hedging has
   over-read the bytes.

## Part D: trace three characters

| Pass | Char | A | Y after `INY` | `$0400` | `$0401` | Exit? |
|---|---|---|---|---|---|---|
| 1 | `H` | `$C8` | `$01` | `$C8` | `?` | No |
| 2 | `I` | `$C9` | `$02` | `$C8` | `$C9` | No |
| 3 | CR | `$8D` | not reached | `$C8` | `$C9` | **Yes** |

**The buffer contains `$C8 $C9 $8D` at `$0400`, `$0401`, `$0402`.**

The carriage return **is** stored. The store happens before the comparison, so
the CR goes into the buffer and only then does the program notice it and leave.
Y is not incremented on that pass, because `BEQ` jumps past `INY`.

This is why the recorded `buffer_text` for input `HI` is `HI` followed by a
carriage return, not just `HI`.

## Part E: predict, then check

| Field | Recorded |
|---|---|
| `screen_text` | `A` followed by CR |
| `buffer_text` | `A` followed by CR |
| `returned_to_monitor` | true |
| `instructions` | 20 |

From `../EMULATOR-RUNS.md`.

## Part F: what it does not do

Any five, with rough costs:

| Missing | Rough cost | Worth it? |
|---|---|---|
| Backspace handling | 5 to 8 instructions: compare against the backspace code, decrement Y, branch | The Monitor itself does this, so arguably yes for a standalone editor |
| A real length limit | 2 to 3: `CPY #n` and a branch | Cheap, and it would make the 128 limit explicit instead of accidental |
| Lower-case conversion | 3 to 5: test the case bit and clear it | The repository's firmware behavior model rejects this until measured |
| Buffer-full behavior | A few, plus a decision about what to do | The decision is the hard part, not the code |
| Rejecting non-printable characters | 4 or more: a range check | Probably not, at this size |
| A terminating marker in the buffer | 2 to 3 | Depends who reads the buffer afterwards |

The honest overall answer is that most of these cost only a few instructions
each, and adding all of them would roughly double the program. Twenty-six bytes
is not a limit anyone was forced into; it is the size of a program that does one
thing.

## Part G: the echo variant

The fifteen extra bytes are:

```text
0317  A0 00      LDY #$00
0319  B9 00 04   LDA $0400,Y
031C  20 EF FF   JSR $FFEF
031F  C9 8D      CMP #$8D
0321  F0 03      BEQ $0326
0323  C8         INY
0324  10 F3      BPL $0319
0326  4C 00 03   JMP $0300
```

**It is a playback stage.** It resets the position to zero and walks the buffer,
echoing each byte until it hits the stored carriage return. Structurally it is
the same loop as the input stage with the input step removed: read from memory
rather than from the keyboard.

**Where it fits:** it replaces the RETURN stage rather than adding to it. Instead
of handing control back, the program plays the buffer back and then jumps to its
own start. So the six-stage scheme becomes setup, input, store, echo, test,
playback, restart, with no return stage at all.

That is the M05 finding arriving from the program's own structure: there is
nowhere in this listing that returns to the Monitor.

## Try a variation: the 129th character

**Y becomes `$80`, `BPL` is not taken, and the program falls through to
`JMP $FF1F` and returns to the Monitor.**

So the behavior is well defined and reasonably graceful: the program stops
accepting input and exits cleanly. What it does *not* do is tell anyone why. From
the outside it looks as though the program ended for no reason, with no Return
pressed and no message.

The 128 characters typed are all in the buffer, at `$0400` through `$047F`, and
the last one has no carriage return after it. Anything reading that buffer
expecting a terminator will keep reading past the end.

## README: Check your understanding

1. **Because running it again would reset the position to zero every time
   round**, so every character would overwrite the first.
2. **`JSR` because the program wants to come back**, and the echo routine ends in
   `RTS` which returns to the instruction after the `JSR`. **`JMP` at the end
   because the program is finished** and wants to transfer control permanently.
   An `RTS` there would be wrong, because the Monitor's `R` command left no
   return address.
3. **Because the byte arriving from `$D010` has bit 7 set.** A carriage return
   from the keyboard is `$0D` plus `$80`, which is `$8D`. Comparing against `$0D`
   would never match.
