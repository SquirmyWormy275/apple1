# A01 Activity: translate

**Status:** OFF-DEVICE. Paper only. Nothing is entered or run on any machine.

## Part A: three instructions (this is the first result)

| Instruction | English |
|---|---|
| `LDX #$03` | |
| `STA $0400` | |
| `JMP $FF1F` | |

## Part B: name the parts

| Instruction | Mnemonic | Operand | Immediate or absolute |
|---|---|---|---|
| `LDA #$8D` | | | |
| `LDA $D010` | | | |
| `STY $0401` | | | |
| `JMP $0300` | | | |
| `INY` | | | |

## Part C: direction drill

Say whether each moves data **into** a register or **out of** one.

`LDA $0400` &nbsp; `STA $0400` &nbsp; `LDX #$00` &nbsp; `STY $0402` &nbsp;
`LDY $D011`

## Part D: legal or not

Mark each legal or illegal. For the illegal ones, say what the writer probably
meant.

| # | Instruction | Legal? |
|---|---|---|
| 1 | `LDA #$41` | |
| 2 | `STA #$41` | |
| 3 | `STA $0400` | |
| 4 | `JMP #$0300` | |
| 5 | `LDX $0400` | |
| 6 | `STX #$00` | |

## Part E: from the real listing

Translate every instruction in `line-input-0300.hex` that is a load, a store, or
a jump. Ignore the branches and the `JSR` for now.

```text
0300  A0 00      LDY #$00
0302  AD 11 D0   LDA $D011
0307  AD 10 D0   LDA $D010
030A  99 00 04   STA $0400,Y
0317  4C 1F FF   JMP $FF1F
```

One of these has an operand form you have not been taught. Identify it and say
what you can work out about it from context.

## Part F (optional): mechanics and intent

For each of the five instructions in Part E, write the mechanical meaning and
then a guess at the intent. Mark your intent guesses as guesses.

## What this activity does not do

It translates instructions on paper. It runs nothing and authorizes no hardware
action.
