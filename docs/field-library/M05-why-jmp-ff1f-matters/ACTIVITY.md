# M05 Activity: find the exit

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. **Neither program here is to be entered on any machine.**

## Part A: find it (this is the first result)

In Program One on `assets/exit-annotation.txt`:

| Question | Answer |
|---|---|
| Address of the last instruction | |
| Its three bytes | |
| What it means in English | |
| What is at the target address | |

## Part B: the two jumps

Program One contains two transfers into the Monitor ROM.

| Instruction | Address | Comes back? | Why |
|---|---|---|---|
| `JSR $FFEF` | `$030D` | | |
| `JMP $FF1F` | `$0317` | | |

## Part C: stack bookkeeping

Say what each does to the stack.

| Instruction | Pushes? | Pulls? |
|---|---|---|
| `JSR` | | |
| `RTS` | | |
| `JMP` | | |
| The Monitor's `R` command | | |

Then: if a program started with `R` ends with `RTS`, what address does it jump
to?

## Part D: does it exit?

For each ending, say whether the program has a working self-directed exit.

| # | Last instructions | Exits? |
|---|---|---|
| 1 | `... 4C 1F FF` | |
| 2 | `... 4C 00 03` | |
| 3 | `... 60` (an `RTS`) after a program started with `R` | |
| 4 | `... 10 FE` (a branch to itself) then `4C 1F FF` | |
| 5 | `... 20 EF FF` then `4C 1F FF` | |

## Part E: Program Two

1. What are its last three bytes and what do they mean?
2. What does the emulator report for `returned_to_monitor`?
3. `software/ram-only/README.md` gives the rule "Exit via `JMP $FF1F`." Does
   Program Two follow it?
4. Is Program Two wrong? Answer carefully and say what evidence would settle it.
5. If someone planned a session using Program Two, what would they need to know
   in advance that Program One's user would not?

## Part F (optional, BUILD): annotate a listing

Take `line-input-echo-0300.hex`, split all 41 bytes into instructions with
addresses, and mark every transfer of control. Check your instruction boundaries
by confirming they land exactly on byte 41.

## What this activity does not do

It reads listings on paper and optionally runs software off-device. It enters
nothing on hardware and authorizes no hardware action.
