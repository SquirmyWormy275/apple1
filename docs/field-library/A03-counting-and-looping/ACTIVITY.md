# A03 Activity: trace the loop

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. Nothing is entered on the Replica 1 Plus.

## Part A: Program A (this is the first result)

Complete the pass table and the four totals on `assets/countdown-trace.txt`.

## Part B: Program B

Complete the two totals for Program B and answer the "why is it different" line.

## Part C: offset arithmetic

| Branch at | Offset byte | Signed value | Target |
|---|---|---|---|
| `$0303` | `$FD` | | |
| `$0310` | `$F0` | | |
| `$0305` | `$FB` | | |
| `$0320` | `$05` | | |
| `$0315` | `$FE` | | |

The last one is worth a second look. Say what a program does when it executes it.

## Part D: how many times

For each loop shape, say how many times the body runs.

| # | Setup | Body | Test | Passes |
|---|---|---|---|---|
| 1 | `LDX #$03` | `DEX` | `BNE` back to body | |
| 2 | `LDX #$01` | `DEX` | `BNE` back to body | |
| 3 | `LDX #$00` | `DEX` | `BNE` back to body | |
| 4 | `LDY #$04` | `INY` | `BNE` back to body | |

## Part E: predict the damage

Program B leaves X at `$FF`. For each later use of X, say what goes wrong.

1. `STX $0400` stores it as a character.
2. X is used as a loop count for a second loop.
3. X is used as an index: `LDA $0400,X`.

## Part F: find the off-by-one

This loop is meant to store five characters at `$0400` through `$0404`.

```text
0300  A0 00     LDY #$00
0302  A9 41     LDA #$41
0304  99 00 04  STA $0400,Y
0307  C8        INY
0308  C0 05     CPY #$05
030A  D0 F8     BNE $0304
030C  4C 1F FF  JMP $FF1F
```

1. Work out the branch target from the offset.
2. How many characters does it actually store?
3. Is there a bug? If so, what is it? If not, say why not.

`CPY #$05` compares Y against 5 and sets the zero flag if they are equal.

## Part G (optional): rewrite Program A to count up

Write a version that counts from 0 up to 5 and ends with X holding 5. State which
flag your branch tests and why.

## What this activity does not do

It traces loops on paper. It enters nothing on hardware and authorizes no
hardware action.
