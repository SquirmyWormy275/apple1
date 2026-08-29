# C05 Activity: trace the state

**Status:** OFF-DEVICE. Paper only. Neither program in this packet is offered
for entry on any machine.

## Part A: the four-instruction trace (this is the first result)

Complete `assets/state-trace.txt`. Fill A and `$0400` for each of the four
steps. Use `?` for unknown and `-` for unchanged.

## Part B: the branch trace

Complete `assets/branch-trace.txt`. Then answer the two counting questions and
the "why are they different" line.

## Part C: predict before you check

For each snippet, write the final value of A **before** reading any answer.

| # | Snippet | Final A |
|---|---|---|
| 1 | `LDA #$10` then `ADC #$10` (carry clear) | |
| 2 | `LDA #$FF` then `ADC #$01` (carry clear) | |
| 3 | `LDA #$41` then `STA $0400` then `LDA #$00` | |
| 4 | `LDA #$05` then `LDA #$09` | |

Snippet 2 is the interesting one. Say what happens to the ninth bit.

## Part D: what changed, what did not

For each instruction, tick every part of state it can alter.

| Instruction | A | X | Memory | Next address | Carry |
|---|---|---|---|---|---|
| `LDA #$41` | | | | | |
| `STA $0400` | | | | | |
| `DEX` | | | | | |
| `BNE $0312` | | | | | |
| `JMP $FF1F` | | | | | |

## Part E: the unknown column

Three learners fill in step 0 of the state trace differently.

- Ana writes `$00` in both cells.
- Ben writes `?` in both cells.
- Cleo writes `$00` in `$0400` and `?` in A, and explains that memory is cleared
  at power-on.

Who is right, and what is wrong with each of the other two?

## Part F (optional, BUILD level): write your own

Write a four-instruction program that stores the character `Z` at `$0401` and
returns to the Monitor. Trace it. State one thing your program assumes that it
does not establish.

## What this activity does not do

It traces programs on paper. It runs nothing on hardware and authorizes no
hardware action.
