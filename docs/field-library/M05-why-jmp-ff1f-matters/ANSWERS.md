# M05 Answer key

## Part A: find it

| Question | Answer |
|---|---|
| Address | `$0317` |
| Bytes | `4C 1F FF` |
| English | Jump to `$FF1F`. |
| Target | The Monitor's warm entry, the label `GETLINE` in the Monitor listing, where it begins collecting a new input line. |

## Part B: the two jumps

| Instruction | Comes back? | Why |
|---|---|---|
| `JSR $FFEF` | **Yes** | `JSR` pushed the address of the following instruction onto the stack before jumping. The echo routine ends in `RTS`, which pulls that address and returns. |
| `JMP $FF1F` | **No** | `JMP` pushes nothing. Control transfers permanently. That is the point: the program is finished. |

Same destination region, opposite intent, and the difference is one instruction
choice.

## Part C: stack bookkeeping

| Instruction | Pushes? | Pulls? |
|---|---|---|
| `JSR` | Yes, the return address | No |
| `RTS` | No | Yes, an address |
| `JMP` | No | No |
| The Monitor's `R` | No | No |

**If a program started with `R` ends with `RTS`, it jumps to whatever two bytes
happen to be on the stack.** Nothing was put there for it. Those bytes are
leftovers, and their value is not predictable from the program. Execution
continues at that address, interpreting whatever is there as instructions.

The honest answer to "what address" is: **unknowable from the program alone.**
A learner who says "a random address" has it; a learner who names a specific
address has over-claimed.

## Part D: does it exit?

| # | Exits? | Why |
|---|---|---|
| 1 | **Yes** | `JMP $FF1F`, the documented exit. |
| 2 | **No** | `JMP $0300`, back to its own start. |
| 3 | **No** | `RTS` with no matching `JSR`. It jumps somewhere undefined. |
| 4 | **No** | The `JMP` is unreachable. `10 FE` is a branch to itself, so control never gets past it. The exit is decoration. |
| 5 | **Yes** | `JSR $FFEF` returns, then the `JMP` runs. |

Item 4 is the one to dwell on. The exit instruction is present and correct and
the program still never leaves. Presence of the right bytes is not the same as
reachability.

## Part E: Program Two

1. **`4C 00 03`, which is `JMP $0300`:** jump back to the program's own first
   instruction.
2. **`returned_to_monitor: false`.** Recorded in `../EMULATOR-RUNS.md`.
3. **No.** Program One follows the rule. Program Two does not.
4. **Not necessarily wrong.** The repository's software library describes it as
   reading the buffer back "before starting over," which is a description of a
   loop. So the behavior may be exactly as intended and the general rule in the
   RAM-only README may simply not have been written with this program's
   restarting design in mind.

   **What would settle it:** a statement from whoever wrote or adopted the
   artifact about whether the restart is intentional. That is a question for the
   repository owner, not something a learner can resolve by reading bytes.

   This finding is recorded in `../EMULATOR-RUNS.md` and flagged there.
5. **That the session ends by pressing reset.** Program One returns you to a
   Monitor prompt; Program Two does not, so the operator needs a planned reset
   and recovery step, decided before the session rather than during it.

## Part F: annotate a listing

The full breakdown of `line-input-echo-0300.hex`:

```text
0300  A0 00      LDY #$00
0302  AD 11 D0   LDA $D011
0305  10 FB      BPL $0302     <- control
0307  AD 10 D0   LDA $D010
030A  99 00 04   STA $0400,Y
030D  20 EF FF   JSR $FFEF     <- control
0310  C9 8D      CMP #$8D
0312  F0 03      BEQ $0317     <- control
0314  C8         INY
0315  10 EB      BPL $0302     <- control
0317  A0 00      LDY #$00
0319  B9 00 04   LDA $0400,Y
031C  20 EF FF   JSR $FFEF     <- control
031F  C9 8D      CMP #$8D
0321  F0 03      BEQ $0326     <- control
0323  C8         INY
0324  10 F3      BPL $0319     <- control
0326  4C 00 03   JMP $0300     <- control
```

Last byte at `$0328`. Start `$0300` plus 41 minus 1 = `$0328`. The boundaries
land exactly, which is the check.

Eight transfers of control, and not one of them leaves the program.

## Try a variation

**`JSR $FFEF` comes back because it left a note saying where to return to.** It
pushed the address `$0310` onto the stack before jumping, and the echo routine's
`RTS` pulled that address back off and jumped to it.

**`JMP $FF1F` does not come back because it left no note.** Nothing was pushed,
so nothing can return. The Monitor at `$FF1F` does not know or care that a
program was running; it simply starts collecting a line of input.

Same ROM, and the difference is entirely whether an address was saved on the way
in.

## README: Check your understanding

1. **`4C 1F FF` at `$0317`.**
2. **Because `RTS` needs an address that a `JSR` put on the stack, and the
   Monitor's `R` command does not do a `JSR`.** It jumps. So `RTS` pulls
   leftover bytes and jumps to whatever address they spell.
3. **No.** If the branch always loops backwards, control never reaches the `JMP`.
   The exit is present but unreachable, which is the same as absent.
