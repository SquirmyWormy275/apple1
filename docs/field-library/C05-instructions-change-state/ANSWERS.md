# C05 Answer key

## Part A: the four-instruction trace

| Step | Instruction | A | `$0400` | Next |
|---|---|---|---|---|
| 0 | (start) | `?` | `?` | `0300` |
| 1 | `LDA #$41` | `$41` | `?` | `0302` |
| 2 | `ADC #$01` | `$42` **or** `$43` | `?` | `0304` |
| 3 | `STA $0400` | `$42` or `$43` (unchanged) | same as A | `0307` |
| 4 | `JMP $FF1F` | unchanged | unchanged | `FF1F` |

**Step 2 is the point of the exercise.** `ADC` adds the operand *and the carry
bit*. This program never cleared the carry, so A is `$42` if the carry was clear
and `$43` if it was set. A trace that writes only `$42` has assumed something the
program did not establish.

A learner who wrote `$42` with a note like "assuming carry clear" has done it
correctly. A learner who wrote `$42` with no note has made the mistake.

**What the emulator actually produced:** running these ten bytes in this
repository's harness gives `A = $42` and `$0400 = $42`, returning to the Monitor
after 4 instructions. That is because the harness begins with the carry clear.
It confirms the arithmetic; it does not make the omission safe.

## Part B: the branch trace

| Pass | X before | X after | Branch? |
|---:|---|---|---|
| 1 | `$03` | `$02` | Yes, not zero |
| 2 | `$02` | `$01` | Yes, not zero |
| 3 | `$01` | `$00` | No, result was zero |

- **`DEX` ran 3 times.**
- **The branch was taken 2 times.**
- **Why they differ:** the branch is tested *after* the body, so the last pass
  runs the body and then falls through instead of branching. A loop that runs n
  times branches n minus 1 times. This is the shape of nearly every off-by-one
  bug in loop code.

## Part C: predict before you check

| # | Final A | Note |
|---|---|---|
| 1 | `$20` | 16 + 16 = 32. |
| 2 | `$00` | 255 + 1 wraps. |
| 3 | `$00` | The store happened first; `$0400` holds `$41`, but A was then overwritten. |
| 4 | `$09` | The second load discards the first entirely. |

**Snippet 2, the ninth bit:** there isn't one. A holds eight bits, so the result
wraps to `$00` and the overflow is recorded in the carry bit, which is set. That
is what the carry is *for*, and it is why the carry left over from one operation
matters to the next one. Snippet 2 is the situation that makes Part A's warning
real.

## Part D: what changed, what did not

| Instruction | A | X | Memory | Next address | Carry |
|---|---|---|---|---|---|
| `LDA #$41` | yes | | | yes (advances) | |
| `STA $0400` | | | yes | yes (advances) | |
| `DEX` | | yes | | yes (advances) | |
| `BNE $0312` | | | | yes (conditionally) | |
| `JMP $FF1F` | | | | yes (always) | |

Every instruction changes the next address, because the program counter always
advances. `BNE` and `JMP` are the only two here that change it to something
other than "the following instruction."

`ADC` would tick both the A column and the carry column, which is worth adding
to the table if a learner asks.

## Part E: the unknown column

**Ben is right.** `?` in both cells.

- **Ana** invented two facts. Nothing in the program or the exercise establishes
  either value.
- **Cleo** is doing the more dangerous version, because the reasoning sounds
  informed. RAM does not reliably come up zeroed; the Replica 1 Plus manual
  describes a screen of garbage at power-on, which is what uninitialized memory
  looks like. Cleo has stated a model as a fact, which is the S04 error exactly.

The correct habit: a value is unknown until something in front of you
establishes it.

## Part F: write your own

One correct answer:

```text
0300:  A9 5A     LDA #$5A      ; 'Z'
0302:  8D 01 04  STA $0401
0305:  4C 1F FF  JMP $FF1F
```

That is three instructions, which is fine; four was a ceiling, not a quota. A
four-instruction version might add `CLC` or load and add.

**One thing it assumes but does not establish:** that `$0401` is writable RAM on
whatever machine runs it. The program has no way to check, and a store to ROM or
to an unmapped address would silently do nothing.

Accept any honest answer of that shape. Reject "it assumes nothing."

## Try a variation: inserting `CLC`

**What changes:** step 2's answer becomes determinate. A is `$42`, full stop, and
the `or $43` disappears from the trace.

**What stays the same:** the emulator's output, because the harness already began
with the carry clear.

**Why it is better anyway:** the program now establishes what it depends on
instead of inheriting it. The old version was correct by luck, and luck does not
survive being called from somewhere else. This is the whole argument for
initializing state, in miniature.

## README: Check your understanding

1. **The same value it had before.** `STA` copies A to memory and leaves A
   alone.
2. **Because `ADC` adds the carry bit as well, and the program never set it.**
   The answer depends on state that arrived from outside the program.
3. **It changes the next address**, that is, the program counter. That is the
   only thing it changes, and it is enough to change everything that happens
   afterwards.
