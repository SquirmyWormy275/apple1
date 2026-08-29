# A04 Answer key

## Part A: the three-key trace

| Key | Path taken | Echoed |
|---|---|---|
| `Y` | Path A. `CMP` matched, `BEQ` taken to `$0311`. | `Y` |
| `N` | Path B. No match, fell through to `$030C`, loaded `$CE`, jumped over path A. | `N` |
| `Q` | Path B, same as `N`. | `N` |

Observed in the repository emulator during authoring: `Y` gives screen text `Y`
in 9 instructions; `N` and `Q` both give `N` in 10 instructions. All three
returned to the Monitor.

**Why path B needs a `JMP` and path A does not:** path A's code sits immediately
before the shared ending, so when it finishes it simply falls into it. Path B
sits before path A, so without a jump it would run on into path A's instructions
and load `$D9` over the `$CE` it just loaded. The `JMP` exists to skip past path
A, and it is needed only because of physical position in memory, not because of
anything about the logic.

## Part B: flag drill

| A holds | Instruction | Z |
|---|---|---|
| `$D9` | `CMP #$D9` | **Set.** Equal. |
| `$CE` | `CMP #$D9` | **Clear.** Not equal. |
| `$00` | `CMP #$00` | **Set.** Equal. |
| `$D9` | `CMP #$59` | **Clear.** `$D9` and `$59` differ by bit 7. |
| `$05` | `DEX` (X = 1) | **Set**, and A is irrelevant. |

**The trap in the last row:** `DEX` operates on X, not A. It sets the flags from
X's new value, which is 0, so the zero flag is set. The value in A has nothing to
do with it. Flags describe the result of the last instruction that sets them, not
the accumulator specifically.

## Part C: which branch

| # | Condition | Branch |
|---|---|---|
| 1 | Key was `Y` | `BEQ` |
| 2 | Key was not `Y` | `BNE` |
| 3 | X reached zero | `BEQ` |
| 4 | X has bit 7 set | `BMI` |

## Part D: the missing jump

1. **Path B loads `$CE` into A, then falls straight into `$0311`, which loads
   `$D9` into A.**
2. **`Y` gets echoed**, for every key.
3. **Yes.** The ending is unchanged, so `JSR $FFEF` and `JMP $FF1F` still run and
   the program still returns cleanly.
4. **No, and this is the point.** Testing with `Y` gives `Y`, which is correct.
   The program looks fine. The bug only appears for inputs the tester did not
   try, and it presents as "it always says yes" rather than as a crash.

   A test suite that only exercises the happy path passes this broken program.
   That is why M04 insists on stating expectations for cases you expect to fail
   as well as cases you expect to pass.

## Part E: add a third path

One correct answer:

```text
0300  AD 11 D0  LDA $D011
0303  10 FB     BPL $0300
0305  AD 10 D0  LDA $D010
0308  C9 D9     CMP #$D9      ; 'Y'?
030A  F0 0A     BEQ $0316
030C  C9 CE     CMP #$CE      ; 'N'?
030E  F0 04     BEQ $0314
0310  A9 BF     LDA #$BF      ; '?'
0312  D0 04     BNE $0318     ; always taken
0314  A9 CE     LDA #$CE
0316  A9 D9     LDA #$D9
0318  20 EF FF  JSR $FFEF
031B  4C 1F FF  JMP $FF1F
```

There is a deliberate flaw in that answer for discussion: `$0314` loads `$CE`
and then falls into `$0316`, which loads `$D9` over it. The `N` path needs its
own jump. A corrected version needs **two** jumps for three paths.

**The general rule: n paths rejoining need n minus 1 jumps,** because exactly one
path can be adjacent to the ending and fall through. Accept any working version;
the answer worth having is the rule.

Note also `D0 04` used as an always-taken branch at `$0312`: after `LDA #$BF` the
zero flag is clear because `$BF` is not zero, so `BNE` always branches. This is a
real technique and a good thing to notice, but it is fragile, and `JMP` says what
it means.

## Part F: predict the instruction counts

**`N` takes one more instruction than `Y`:** 10 against 9.

Path A is `BEQ` taken, then `LDA #$D9`. Path B is `BEQ` not taken, then
`LDA #$CE`, then `JMP`. The extra instruction is exactly the jump that path B
needs and path A does not, which is Part A's answer showing up as a number.

## Part G: rearrange to remove the jump

Swap which case branches:

```text
0308  C9 D9     CMP #$D9
030A  D0 04     BNE $0310     ; not Y: go to the N path
030C  A9 D9     LDA #$D9      ; Y path, falls through
030E  4C 12 03  JMP $0312
0310  A9 CE     LDA #$CE      ; N path, falls through
0312  20 EF FF  JSR $FFEF
```

**This does not remove the jump.** It moves it to the other path. With two paths
and one shared ending, one of them must jump, whichever way round you arrange it.

A learner who discovers that and states it has answered the question correctly.
A learner who produces a version with no jump at all has almost certainly written
the Part D bug.

## Try a variation: `CMP #$59`

**It echoes `N` for every possible key, including `Y`.**

The byte read from `$D010` always has bit 7 set, so its value is always `$80` or
higher. `$59` is below `$80`. No key can ever produce a byte equal to `$59`, so
the comparison never matches, `BEQ` is never taken, and path B runs every time.

The program does not crash, does not misbehave visibly, and gives a plausible
answer. It is simply always wrong in one direction, which is the worst kind of
bug to find by testing.

## README: Check your understanding

1. **`$D9`, unchanged.** `CMP` throws away its subtraction and keeps only the
   flags.
2. **Because path A is physically adjacent to the shared ending and falls into
   it, while path B sits before path A and would otherwise run through it.**
3. **They have built the opposite program.** `BNE` branches when the key was
   *not* `Y`, so the "yes" path would run for every key except `Y`. The
   comparison is right and the branch is inverted.
