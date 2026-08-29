# R05 Activity: encode a rhythm

**Status:** OFF-DEVICE. Paper, pencil, and hands. **Nothing is played by any
machine at any point.**

## Part A: clap and encode (this is the first result)

Complete `assets/rhythm-grid.txt`: clap all three rows, then encode rows 2 and 3
as bits and as hex.

## Part B: decode

| Byte | Bits | Slots that sound |
|---|---|---|
| `$88` | | |
| `$A4` | | |
| `$FF` | | |
| `$00` | | |
| `$C0` | | |
| `$81` | | |

Clap each one.

## Part C: what the byte does not say

| Property | Captured by the byte? |
|---|---|
| Which slots have an event | |
| How fast the slots go by | |
| How loud each event is | |
| How long each event lasts | |
| What sound is made | |
| How many times to repeat | |

## Part D: the handover test

1. Write a rhythm of your own as a byte.
2. Give only the byte to someone else, with no other instruction.
3. Have them clap it.
4. Record every way their version differed from yours.

Then: for each difference, say whether the byte was wrong or whether it simply
did not carry that information.

## Part E: extending the encoding

For each addition, say what it costs.

| Addition | Extra storage | Per what |
|---|---|---|
| Tempo for the whole pattern | | |
| Loudness, four levels, per slot | | |
| Note length, sustained or not, per slot | | |
| Two instruments at once | | |
| Sixteen slots instead of eight | | |

## Part F: the honest limits

Mark each **supported**, **unsupported**, or **not addressed by any source
here**.

| # | Statement | Verdict |
|---|---|---|
| 1 | Eight slots fit in one byte. | |
| 2 | `$88` means slots 1 and 5. | |
| 3 | The Apple-1 can play this rhythm. | |
| 4 | The Replica 1 Plus has a speaker. | |
| 5 | A rhythm encoding discards tempo. | |

## Part G (optional, STUDY): design a better encoding

Design an encoding that captures tempo and note length as well as position, for
sixteen slots. State its total size in bytes and what it still discards.

Every encoding discards something. Naming what yours discards is the deliverable.

## What this activity does not do

It claps rhythms and writes bytes on paper. **Nothing is played by any machine**,
and no hardware action is authorized.
