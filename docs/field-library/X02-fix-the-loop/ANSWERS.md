# X02 Answer key

## Part A: trace first

| Pass | Y before | Stored at | Y after |
|---:|---|---|---|
| 1 | `$00` | `$0400` | `$01` |
| 2 | `$01` | `$0401` | `$02` |
| 3 | `$02` | `$0402` | `$03` |
| 4 | `$03` | `$0403` | `$04` |
| 5 | `$04` | `$0404` | `$05` |
| 6 | `$05` | `$0405` | `$06` |

- **Stores: six.**
- **Highest address written: `$0405`.**
- **Was that the intention? No.** The intention was five stores, `$0400` to
  `$0404`.

## Part B: state the discrepancy

| | |
|---|---|
| Supposed to do | Store `$41` at `$0400` through `$0404`. Five copies. |
| Actually does | Stores `$41` at `$0400` through `$0405`. Six copies. |
| Difference | It writes one byte too many, at `$0405`. |

## Part C: find the bug

| | |
|---|---|
| Address | `$0308` |
| As written | `C0 06`, meaning `CPY #$06` |
| Should be | `C0 05`, meaning `CPY #$05` |
| How you know | The loop ends when Y equals the compare value. Y equals 6 only after six increments, and six increments means six stores. Comparing against 5 ends it after five. |

**One byte.** The `06` should be `05`.

## Part D: the after trace

| Pass | Y before | Stored at | Y after |
|---:|---|---|---|
| 1 | `$00` | `$0400` | `$01` |
| 2 | `$01` | `$0401` | `$02` |
| 3 | `$02` | `$0402` | `$03` |
| 4 | `$03` | `$0403` | `$04` |
| 5 | `$04` | `$0404` | `$05` |
| 6 | Does not happen | | |

- **Stores: five.**
- **Highest address written: `$0404`.**
- **Matches the intention: yes.**

## Part E: predict the emulator

Observed during authoring in `tools/apple1_emulator.py`:

| Version | Buffer | Instructions | Returned |
|---|---|---:|---|
| As written (`C0 06`) | `AAAAAA`, six characters | 27 | true |
| Corrected (`C0 05`) | `AAAAA`, five characters | 23 | true |

Both return to the Monitor. Both produce a buffer full of the letter `A`. The
only differences are one character and four instructions, and neither is visible
unless you were counting.

Recorded in `../EMULATOR-RUNS.md`.

## Part F: why it is dangerous

| # | Symptom | Present? |
|---|---|---|
| 1 | Crashes | **No** |
| 2 | Fails to return | **No** |
| 3 | Obviously wrong address | **No.** `$0405` is adjacent to the intended range and looks entirely normal. |
| 4 | No output | **No** |
| 5 | Visibly longer | **No.** Four extra instructions. |
| 6 | Does one thing more than intended | **Yes**, and it is the only one. |

**A casual test would catch none of the first five**, because none of them
happens. The only way to find this is to compare against a written statement of
what the program was supposed to do.

That is the argument for A06's design card in one line: without a recorded
intention, this bug is undetectable.

## Part G: three wrong fixes

1. **`A0 01` instead of `A0 00`.** Now Y starts at 1, so the loop stores at
   `$0401` through `$0405`: still six stores, wrong range. It does not even fix
   the count. It changes which addresses are wrong.

   Actually trace it: Y goes 1, 2, 3, 4, 5, and the compare against 6 stops it
   after the store at `$0405`. Five stores, at `$0401` to `$0405`. So the *count*
   becomes right and the *range* becomes wrong, and `$0400` is never written. A
   fix that makes the symptom you were watching go away while moving the fault
   somewhere else is the worst possible outcome, because now you believe it is
   fixed.

2. **`D0 FA` instead of `D0 F8`.** The branch target moves from `$0304` to
   `$0306`, which is the middle of the `STA $0400,Y` instruction. The program
   would resume executing at an operand byte, and the behavior from there is not
   what anyone intended. This does not fix anything; it breaks the program in a
   new and much less obvious way.

3. **Leave the program and change the intention to six.**

   **This is the interesting one, and it is not automatically wrong.** If the
   real requirement was six characters and the specification was written down
   incorrectly, then the program is right and the spec is the bug.

   The honest procedure is to find out which was intended, not to pick whichever
   is easier to change. What makes it a *wrong fix* is doing it silently, because
   changing the specification to match the code makes any code correct.

   The question to ask: does anything else depend on there being five? If the
   buffer is read by something expecting five, the spec is right and the code is
   wrong. If nothing does, somebody has to decide.

## Part H: plant your own

Acceptance: exactly one byte changed, the intention written at the top, and the
planter can produce a before-and-after trace of their own bug.

Confirm nothing was added to `software/ram-only/`.

## Try a variation: `A0 01`

Covered in Part G item 1. **Five stores at `$0401` through `$0405`.** `$0400` is
never written.

**Worse than the real bug**, for two reasons. The count is now correct, so the
most obvious check passes. And `$0400` is left holding whatever it held before,
which anything reading the buffer from the start will pick up as if it were data.

The real bug writes one byte too many. This one writes the right number of bytes
in the wrong place and leaves stale data at the start. The first is a
straightforward overrun; the second silently mixes new data with old.

## README: Check your understanding

1. **Because looking first produces a suspect and tracing produces a fact.** If
   you hunt before you trace, you will find something plausible and stop. The
   trace tells you the program does six stores, and only then do you know what to
   look for.
2. **Because returning correctly says nothing about what it did on the way.** The
   exit path is fine; the loop body ran once too often. Every observable behavior
   is normal except the one nobody was measuring.
3. **Because you can hold one change in your head and attribute the difference to
   it.** With three, a fix and a new bug can cancel out, and the before-and-after
   comparison stops proving anything.
