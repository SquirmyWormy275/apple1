# A04 Activity: choose the message

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. Nothing is entered on the Replica 1 Plus.

## Part A: the three-key trace (this is the first result)

Complete the table on `assets/choose-the-message.txt` for `Y`, `N`, and `Q`,
then answer the question underneath it.

## Part B: flag drill

For each, say whether the zero flag ends up set or clear.

| A holds | Instruction | Z set or clear |
|---|---|---|
| `$D9` | `CMP #$D9` | |
| `$CE` | `CMP #$D9` | |
| `$00` | `CMP #$00` | |
| `$D9` | `CMP #$59` | |
| `$05` | `DEX` (X holds 1) | |

The last row is a trap. Say what it is.

## Part C: which branch

You want to take a branch when the condition below is true. Name the branch.

| # | Condition after `CMP #$D9` | Branch |
|---|---|---|
| 1 | The key was `Y` | |
| 2 | The key was not `Y` | |
| 3 | (after `DEX`) X reached zero | |
| 4 | (after `DEX`) X has bit 7 set | |

## Part D: the missing jump

Someone deletes `4C 13 03` at `$030E` and shifts everything up.

1. Trace what happens when the key is not `Y`.
2. What gets echoed?
3. Would the program still return to the Monitor?
4. Would a casual test with the key `Y` reveal the bug?

Question 4 is the important one.

## Part E: add a third path

Extend the program: echo `Y` for `Y`, `N` for `N`, and `?` for anything else.
`$BF` is `?` with the high bit set. Write the instructions with addresses, and
say how many `JMP`s your version needs and why.

## Part F: predict the instruction counts

The recorded runs report an instruction count. Predict which of `Y` and `N`
takes more instructions, and by how many, before looking at `ANSWERS.md`.

## Part G (optional): rearrange to remove the jump

Rewrite the original program so the `JMP` at `$030E` is not needed, by changing
which condition branches. State what you changed.

## What this activity does not do

It traces a program on paper and optionally runs it off-device. It enters nothing
on hardware and authorizes no hardware action.
