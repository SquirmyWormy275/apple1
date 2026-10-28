# 4. Write assembly as controlled state changes

By the end of this chapter you will copy a table, trace flags through arithmetic,
follow a subroutine through the stack, and explain a loop's boundary. Work one
section at a time. Predict the result, run the linked lab, then make its variation.
The complete sources, stdout, images and answers are in each worked lab.

## 4.1 Start with a routine contract

A routine needs more than a name. State its inputs, outputs, memory ranges,
clobbered registers, arithmetic mode, exit and maximum work. For our first copy:

| Property | Contract |
|---|---|
| Input | Five source bytes, `HELLO`, embedded after the code |
| Output | Exactly five bytes at `$0400` through `$0404` |
| Bounds | `$03FF` and `$0405` remain `$A5` |
| Registers | A and Y may change; X is unused |
| Exit | Transfer to Monitor warm entry `$FF1F` |
| Environment | Host Py65 world; no physical device |

The sentinels make an otherwise invisible extra store observable. The source
and destination do not overlap. That is a requirement of this forward-copy
example, not a promise about every possible copy routine.

## 4.2 A value is different from its address

Run [T01: values and addresses](../features/T01.md). Compare:

```asm
LDA #$20       ; A becomes the value $20
LDA $20        ; A becomes the byte at zero-page address $0020
LDA $0420      ; A becomes the byte at absolute address $0420
```

The `#` changes the meaning. The two memory forms read different locations.
A load changes A and the N/Z flags; it does not move, consume or erase its source
byte. A store copies a register into memory and preserves the arithmetic flags.

The [instruction reference](../reference/6502.md) groups all 56 documented NMOS
mnemonics. Read the CPU variant before copying code from another tutorial:
65C02 instructions such as `STZ`, `BRA`, `PHX` and `PLY` are outside these NMOS
lessons. A virtual experiment can impose narrower memory permissions than the
instruction set itself.

## 4.3 Labels describe addresses; they occupy no bytes

Our host assembler accepts labels, instructions, semicolon comments and `.BYTE`.
It does not supply the complete syntax of Krusader or another macro assembler.
The origin is supplied by the caller, normally `$0300` in these teaching labs.

```asm
LDY #$00
COPY: LDA DATA,Y
STA $0400,Y
INY
CPY #$05
BNE COPY
JMP $FF1F
DATA: .BYTE $48,$45,$4C,$4C,$4F
```

`COPY` and `DATA` are assembly-time names. They do not become runtime strings.
The assembler calculates final label positions after instruction sizes stabilize.
An absolute load takes three bytes; a mistaken two-byte size would make `DATA`
point into another instruction. [T09](../features/T09.md) includes that regression.

## 4.4 Walk the indexed copy before running it

In [T02](../features/T02.md), a short prelude first sets the sentinels. The copy
then follows this pattern:

| Pass | Y before | Source | Destination | Y after | Repeat? |
|---|---:|---|---|---:|---|
| 1 | 0 | DATA+0: H | `$0400` | 1 | yes |
| 2 | 1 | DATA+1: E | `$0401` | 2 | yes |
| 3 | 2 | DATA+2: L | `$0402` | 3 | yes |
| 4 | 3 | DATA+3: L | `$0403` | 4 | yes |
| 5 | 4 | DATA+4: O | `$0404` | 5 | no |

`CPY #$05` sets Z when Y equals five. `BNE` tests that result. The fifth store
has already happened when the comparison ends the loop. Changing five to six
still produces a clean exit but corrupts the upper sentinel. Run that variation
in a scratch source and explain which check catches it.

A zero-length copy needs a precheck. A bottom-tested loop executes its body at
least once. Do not turn this fixed five-byte example into a general function by
replacing one constant and assuming all 0–255 lengths now work.

## 4.5 Calculate a branch from the following PC

Run [T09](../features/T09.md). The countdown has `BNE` at `$0303`; the following
PC is `$0305`, and its target is `$0302`. Therefore the displacement is -3, or
`$FD`. The complete branch is `D0 FD`.

A relative branch reaches -128 through +127 from the following instruction.
At `$0300`, a branch can reach `$0381` (+127) but cannot reach `$0382` (+128).
The assembler rejects the latter. For a distant conditional path, invert the
condition over a three-byte `JMP` whose operand names the distant address.

Always identify the last instruction that sets the tested flag. Inserting an
`LDA` between `CPY` and `BNE` makes BNE test the load's Z result. Source order
alone does not preserve the comparison.

## 4.6 Carry and overflow answer different questions

Run [T03](../features/T03.md) and predict C, Z, N and V:

| Binary operation, incoming C=0 | Byte result | C | Z | N | V |
|---|---|---:|---:|---:|---:|
| `$FF + $01` | `$00` | 1 | 1 | 0 | 0 |
| `$7F + $01` | `$80` | 0 | 0 | 1 | 1 |
| `$80 + $80` | `$00` | 1 | 1 | 0 | 1 |

Unsigned 255+1 needs a ninth bit. Signed 127+1 cannot fit in -128..127. Those
are different failures of representation. N is the result's high bit, not a
universal signed comparison result. Decimal mode is another input: `CLD`
establishes binary arithmetic before these examples.

`ADC` includes incoming carry. [T04](../features/T04.md) uses that fact to add
two-byte numbers: add the low bytes, store the result, load the high byte, then
ADC the high operand without clearing the carry. `$00FF + $0001` produces the
memory pair `$00 $01`, representing `$0100`. Insert an extra CLC before the high
addition and explain why the answer becomes wrong.

## 4.7 Subtraction starts with no borrow

For binary subtraction, SBC computes `A - operand - (1-C)`. Use SEC for a fresh
subtraction with no incoming borrow. [T05](../features/T05.md) compares:

- 5-3 with SEC: 2, C=1.
- 3-5 with SEC: `$FE`, C=0; interpreted as an unsigned result it wrapped.
- 5-3 with CLC: 1, because the incoming borrow subtracts another one.

CMP preserves A and sets comparison flags. C=1 means unsigned A is greater than
or equal to the operand; Z=1 means equality. A signed less-than decision needs
signed-overflow-aware reasoning or a transformation of the ordering. `BMI`
after CMP is insufficient for arbitrary signed values. State the interpretation
before selecting the branch.

## 4.8 Use masks and rotates to operate on bits

[T06](../features/T06.md) removes a character's high bit with `AND #$7F`, restores
it with `ORA #$80`, and flips selected bits with EOR. These operations describe
bit patterns; they do not themselves know that a value represents a character.

ASL shifts bit 7 into C and shifts zero into bit 0. ROL rotates through C. Thus
ASL on `$81` gives `$02`, C=1; ROL then gives `$05`. A store between them preserves
carry. CLC between them changes the second result to `$04`.

## 4.9 Follow the stack through a call

Run [T07](../features/T07.md). Its contract says SUB preserves A and writes Z to
`$0401`. The caller later stores its preserved A at `$0400`.

| Moment | SP in this fixture | Meaning |
|---|---|---|
| Before JSR | `$FF` | Initial empty-stack convention |
| At SUB | `$FD` | Two return bytes have been pushed |
| After PHA | `$FC` | One saved accumulator byte above them |
| After PLA | `$FD` | A restored; return bytes exposed |
| After RTS | `$FF` | Call frame consumed; caller continues |

The stack page has 256 addresses, `$0100`–`$01FF`. A push stores at `$0100+SP`
and decrements the eight-bit SP; a pull increments SP and reads. JSR saves the
address of its final operand byte. RTS pulls it and advances by one. PHA/PLA
must be balanced before RTS can see the correct return frame. PLA changes N/Z;
preserving A is different from preserving processor status.

The real Monitor's R dispatch at `$FF94` is an indirect JMP, not JSR. It creates
no matching call frame for your program. An arbitrary RTS is therefore not a
return-to-Monitor operation. Use the explicit warm-entry transfer in these
routines. See the [verified listing notes](../review.md#manual-checks).

## 4.10 Understand pointers before using them in a loop

[T08](../features/T08.md) builds a two-byte zero-page pointer. With `$20=$FF`
and `$21=$04`, the pointer value is `$04FF`:

- `LDA ($20),Y` reads the pointer first, then adds Y. Y=1 reads `$0500`.
- `LDA ($20,X)` adds X to the zero-page operand first. X=2 selects the separate
  pointer at `$22/$23`.

A zero-page indexed address wraps within zero page. A pointer target plus Y can
cross a page. These affect semantics and sometimes cycle counts; our captures
report instruction counts, not physical timing. The NMOS indirect JMP also has
a page-boundary quirk described in the reference. Avoid placing its pointer at
`$xxFF` unless deliberately studying that behavior.

## 4.11 Test the original programs, including their surprises

[A03](../../field-library/A03-counting-and-looping/WORKED.md) contrasts BNE and
BPL countdowns: five decrements versus six from X=5. BPL includes zero.

[T10](../features/T10.md) executes the exact original thirteen-byte A06 fill.
Y=$0F fills 16 bytes. Changing its starting index to `$FF` as a supposed
zero-length case performs **one** store at `$04FF`, then exits with Y=$FE.
An earlier answer incorrectly claimed 256 stores; the corrected answer records
this measured distinction. A different ascending BNE loop can wrap through 256
iterations. Loop shape decides the result.

[T11](../features/T11.md) tests the line-input program at 127 and 128 ordinary
characters. At the first boundary Return is consumed; at the second, the index
exit occurs before Return. Chapter 5 derives the counts.

[T12](../features/T12.md) steps BRK and RTI in Py65 directly. The NEURAL1 world
instead intercepts BRK as a stop marker. A world BRK report does not mean an
interrupt handler ran. Distinguish reset, warm entry, subroutine return and
interrupt return; they have different state contracts.

## Practice and readiness

Complete T01–T12, then the original A01–A06 activities and X02. You are ready for
a capstone when you can explain a branch operand, preserve carry across two
bytes, balance a subroutine's stack, and detect an extra store despite a clean
exit. Keep one failing variation alongside your corrected program.

[Textbook home](../README.md) · [Previous chapter](03-monitor-and-first-program.md) · [Next chapter](05-input-output-and-debugging.md)
