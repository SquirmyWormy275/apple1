# C01 Activity: read the instruction

**Status:** OFF-DEVICE. Paper only.

## Part A: read three aloud (this is the first result)

Say each as "verb, what, where."

| Instruction | Your English |
|---|---|
| `LDA #$00` | |
| `LDA $D011` | |
| `STA $0400` | |

## Part B: hash or no hash

For each pair, say what is different.

| A | B | Difference |
|---|---|---|
| `LDA #$10` | `LDA $10` | |
| `LDY #$FF` | `LDY $FF` | |

## Part C: name the register

| Register | One-line job |
|---|---|
| A | |
| X | |
| Y | |
| Program counter | |

## Part D: the real program's first six bytes

These are the first bytes of `software/ram-only/line-input-0300.hex`, split into
instructions for you. Write the English for each.

```text
0300:  A0 00        LDY #$00
0302:  AD 11 D0     LDA $D011
0305:  10 FB        BPL $0302
```

1. What does the first line do?
2. What does the second line do, and what is at `$D011`?
3. The third line is a branch. Without knowing the rules yet, guess from the
   target address what this three-line sequence is doing as a whole.

## Part E: how many bytes

Instructions are not all the same length. Using the listing in Part D, fill in:

| Instruction | Bytes | How you know |
|---|---:|---|
| `LDY #$00` | | |
| `LDA $D011` | | |
| `BPL $0302` | | |

## Part F (optional): the fetch-decide-act trap

The diagram says the loop never stops. Yet a program can clearly "finish." Write
two sentences reconciling those.

## What this activity does not do

It reads instructions on paper. Nothing is entered on a machine and nothing is
executed.
