# A01 Answer key

## Part A: three instructions

| Instruction | English |
|---|---|
| `LDX #$03` | Load X with the number 3. |
| `STA $0400` | Store the accumulator into address `$0400`. |
| `JMP $FF1F` | Jump to `$FF1F`. |

## Part B: name the parts

| Instruction | Mnemonic | Operand | Mode |
|---|---|---|---|
| `LDA #$8D` | `LDA` | `#$8D` | Immediate |
| `LDA $D010` | `LDA` | `$D010` | Absolute |
| `STY $0401` | `STY` | `$0401` | Absolute |
| `JMP $0300` | `JMP` | `$0300` | Absolute |
| `INY` | `INY` | none | Neither. It has no operand. |

## Part C: direction drill

| Instruction | Direction |
|---|---|
| `LDA $0400` | Into a register |
| `STA $0400` | Out of a register |
| `LDX #$00` | Into a register |
| `STY $0402` | Out of a register |
| `LDY $D011` | Into a register |

Rule: `LD` is in, `ST` is out. Every time.

## Part D: legal or not

| # | Legal? | Note |
|---|---|---|
| 1 | **Legal** | Load the number 65. |
| 2 | **Illegal** | Store needs a place. They meant `LDA #$41` then `STA` somewhere. |
| 3 | **Legal** | |
| 4 | **Illegal** | You jump to a place, not to a number. They meant `JMP $0300`. |
| 5 | **Legal** | Load X from address `$0400`. |
| 6 | **Illegal** | Same error as 2. They probably meant `LDX #$00`, or `STX` to an address. |

The three illegal ones are all the same mistake: using `#` where a place is
required.

## Part E: from the real listing

| Instruction | English |
|---|---|
| `LDY #$00` | Load Y with zero. |
| `LDA $D011` | Load A from address `$D011`. |
| `LDA $D010` | Load A from address `$D010`. |
| `STA $0400,Y` | Store A into address `$0400` **plus whatever is in Y**. |
| `JMP $FF1F` | Jump to `$FF1F`. |

**The unfamiliar form is `STA $0400,Y`.** The `,Y` is a third addressing mode,
called *indexed*. From context you can work out a good deal: the program sets Y
to zero at the start, and something later must be increasing it, because
otherwise every character would land in the same place. So `,Y` almost certainly
means "step along by Y," making `$0400` the start of a run of locations rather
than a single one.

That is exactly right, and it is A02's subject.

A learner who says "I do not know this one" and stops has been honest but has
left value on the table. A learner who reasons from Y being initialized to zero
has done the thing this lesson is really teaching.

## Part F: mechanics and intent

| Instruction | Mechanics | Intent (guess) |
|---|---|---|
| `LDY #$00` | Y becomes 0 | Start the character counter at the beginning of the buffer |
| `LDA $D011` | A gets the contents of `$D011` | Check whether a key is waiting |
| `LDA $D010` | A gets the contents of `$D010` | Collect the character that arrived |
| `STA $0400,Y` | Write A to `$0400` plus Y | Put this character in the next free buffer slot |
| `JMP $FF1F` | Go to `$FF1F` | Finish, and hand control back to the Monitor |

The mechanics column is in the bytes. The intent column is not, and every entry
in it is an inference. Marking them as guesses is the correct behavior; a learner
who states intent as fact has made a small version of the S04 error.

## Try a variation

**`LDA #$D0`** loads the number 208 into A. It does the same thing every time,
forever, because the value is written into the instruction.

**`LDA $D011`** reads the keyboard control register and loads whatever is there
right now. **This one can produce a different result each time it runs**, because
`$D011` is a hardware register whose contents change when a key is pressed.

That difference is the reason the program in Part E loops on it: reading it
repeatedly is only useful if the answer can change.

## README: Check your understanding

1. **`LDY $0400`** loads Y from address `$0400`. **`LDY #$04`** loads Y with the
   number 4.
2. **Because store writes a value into a place, and `#$41` is a value, not a
   place.** There is nowhere to write to.
3. **Three: `$0300`, A, and `$0400`.** Both instructions copy; neither removes
   anything from where it came from.
