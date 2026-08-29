# A03 Answer key

## Part A: Program A

| Pass | X before | X after | Branch? |
|---:|---|---|---|
| 1 | `$05` | `$04` | Yes |
| 2 | `$04` | `$03` | Yes |
| 3 | `$03` | `$02` | Yes |
| 4 | `$02` | `$01` | Yes |
| 5 | `$01` | `$00` | No |
| 6 | (does not happen) | | |

- **`DEX` ran 5 times.**
- **Branch taken 4 times.**
- **Final X = `$00`.**
- **`$0400` = `$00`.**

Observed during authoring: X = `$00`, `$0400` = `$00`, `DEX` executed 5 times,
13 instructions total.

## Part B: Program B

- **`DEX` ran 6 times.**
- **Final X = `$FF`.**

Observed during authoring: X = `$FF`, `$0400` = `$FF`, `DEX` executed 6 times,
15 instructions total.

**Why it is different:** `BPL` branches while the result is *plus*, meaning bit 7
is clear. When `DEX` produces `$00`, bit 7 is clear, so zero counts as positive
and the branch is taken one more time. That extra `DEX` turns `$00` into `$FF`,
which has bit 7 set, and only then does the loop end.

`BNE` stops *at* zero. `BPL` stops *one past* zero.

## Part C: offset arithmetic

| Branch at | Offset | Signed | Target |
|---|---|---|---|
| `$0303` | `$FD` | -3 | `$0302` |
| `$0310` | `$F0` | -16 | `$0302` |
| `$0305` | `$FB` | -5 | `$0302` |
| `$0320` | `$05` | +5 | `$0327` |
| `$0315` | `$FE` | -2 | `$0315` |

Working: target = address of branch + 2 + signed offset.

**The last one branches to itself.** A two-byte branch at `$0315` with offset -2
targets `$0315`, which is the branch. If the condition holds, the program spends
the rest of its life re-executing that one instruction. This is the "halted
machine" from C01: a loop that goes nowhere, and the usual way to write one
deliberately.

## Part D: how many times

| # | Passes | Why |
|---|---|---|
| 1 | 3 | Counts 3, 2, 1, stops at zero. |
| 2 | 1 | 1 becomes 0 on the first pass. |
| 3 | **256** | `$00` becomes `$FF`, which is not zero, so it keeps going all the way down through `$FE`, `$FD` ... to `$00` again. |
| 4 | **252** | `INY` from 4 counts up through `$FF` to `$00`, which is 252 passes. |

Rows 3 and 4 are the ones worth remembering. A count of zero does not mean "do
nothing"; it means "do it 256 times." This is the single most common 6502 loop
bug.

## Part E: predict the damage

1. **Stores `$FF` as a character.** `$FF` is not a printable ASCII value. Whatever
   the display does with it, it is not the character anyone intended.
2. **The second loop runs 256 times instead of 0.** See Part D row 3. The
   symptom appears in the second loop, which is not where the fault is.
3. **`LDA $0400,X` reads `$04FF`,** 255 bytes past the intended start, well
   outside a small buffer. It reads whatever happens to be there.

All three share a property: the damage shows up somewhere other than the
instruction that caused it. That is what makes off-by-one errors expensive.

## Part F: find the off-by-one

1. **Branch target:** `$030A` + 2 + (-8) = `$0304`. `$F8` is 248, and 248 minus
   256 is -8.
2. **It stores five characters,** at `$0400` through `$0404`.
3. **There is no bug.** The loop is correct.

   Trace it: Y starts 0, stores at `$0400`, `INY` makes Y 1, `CPY #$05` is not
   equal, branch back. This repeats for Y = 1, 2, 3, 4. After storing at `$0404`,
   `INY` makes Y 5, `CPY #$05` is equal, the zero flag is set, `BNE` does not
   branch, and control falls through.

   Five stores, at `$0400` to `$0404`. Exactly as specified.

**This item is a deliberate trap in the other direction.** Having spent the
lesson hunting off-by-one errors, most learners will find one here that is not
there. Being able to trace a loop and conclude "this is correct" is as important
as finding a fault, and a debugger who always finds something is not a good
debugger.

Note also that the branch targets `$0304`, not `$0302`. The `LDA #$41` sits
outside the loop, which is correct: the character never changes, so loading it
once is right.

## Part G: count up

One correct answer:

```text
0300  A2 00     LDX #$00
0302  E8        INX
0303  E0 05     CPX #$05
0305  D0 FB     BNE $0302
0307  8E 00 04  STX $0400
030A  4C 1F FF  JMP $FF1F
```

**Flag tested: the zero flag, via `BNE`,** because the stopping condition is "X
has reached 5," and `CPX #$05` sets the zero flag exactly when that is true.

`BPL` would be wrong here: X counting up from 0 stays positive until 128, so a
`BPL` loop would run 128 times.

Accept any version that ends with X = 5 and that names the flag its branch
tests.

## Try a variation: `LDX #$00`

**The body runs 256 times and X ends at `$00`.**

`DEX` on `$00` gives `$FF`, which is not zero, so the branch is taken. The count
runs down `$FE`, `$FD`, all the way to `$00`, at which point `BNE` finally falls
through. Two hundred and fifty-six passes.

The reason is the test at the bottom: the body runs before anything is checked,
so a loop can never run zero times, no matter what the count says.

## README: Check your understanding

1. **`DEX` runs 5 times; the branch is taken 4 times.**
2. **`$0302`.** `$0310` + 2 + (-16) = `$0302`.
3. **Because the offset is a single signed byte,** which reaches at most 127
   forwards and 128 backwards from the following instruction. 300 is outside
   that range, and a `JMP` with a full address is needed instead.
