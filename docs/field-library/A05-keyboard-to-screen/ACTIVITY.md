# A05 Activity: read the whole program

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. **Nothing here is entered on the Replica 1 Plus.** The artifact is
classified RAM-ONLY with no live-run authority, and this activity does not change
that.

## Part A: stage summaries (this is the first result)

Cover the English block on `assets/four-stages.txt` and write your own one-line
summary for each of the six stages. Then compare.

## Part B: instruction by instruction

| Address | Instruction | What it contributes |
|---|---|---|
| `$0300` | `LDY #$00` | |
| `$0302` | `LDA $D011` | |
| `$0305` | `BPL $0302` | |
| `$0307` | `LDA $D010` | |
| `$030A` | `STA $0400,Y` | |
| `$030D` | `JSR $FFEF` | |
| `$0310` | `CMP #$8D` | |
| `$0312` | `BEQ $0317` | |
| `$0314` | `INY` | |
| `$0315` | `BPL $0302` | |
| `$0317` | `JMP $FF1F` | |

## Part C: the two exits

The loop can end in two different ways.

1. What is the intended exit condition?
2. What is the second one?
3. How many characters can be typed before the second one triggers?
4. Which instruction implements it, and does it look deliberate?

## Part D: trace three characters

Type `HI` then Return. Fill in the state at the end of each pass.

| Pass | Character | A | Y after `INY` | `$0400` | `$0401` | Exit? |
|---|---|---|---|---|---|---|
| 1 | `H` | | | | | |
| 2 | `I` | | | | | |
| 3 | CR | | | | | |

Then: what does the buffer contain at the end, including the carriage return?

## Part E: predict, then check

Predict the emulator's four output fields for input `A` + CR, then check against
`../EMULATOR-RUNS.md` or run it.

| Field | Prediction | Recorded |
|---|---|---|
| `screen_text` | | |
| `buffer_text` | | |
| `returned_to_monitor` | | |
| `instructions` | | |

## Part F: what it does not do

List five things this program does not handle. For each, say roughly how many
instructions handling it would cost, and whether you think it is worth it in a
26-byte program.

## Part G (optional, BUILD): the echo variant

Read `line-input-echo-0300.hex` and describe the fifteen bytes it adds. What
stage would you call them, and where does it fit in the six-stage scheme?

## What this activity does not do

It reads and optionally rehearses a program off-device. It enters nothing on
hardware, grants no live-run authority, and authorizes no hardware action.
