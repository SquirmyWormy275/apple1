# 1. Build a mental model of the machine

A computer is an arrangement of state and rules for changing it. The CPU reads
an instruction from memory, interprets its opcode and operands, changes
registers or memory, and selects the next instruction. Input supplies values;
output makes selected values visible. An attractive case or display is not
required to understand this sequence.

## Distinguish the objects

An original Apple-1 is a historical physical object. A Replica 1 Plus is a
modern implementation documented by its manufacturer. NEURAL1 is modern host
software with a virtual execution world. The Raspberry Pi runs the model and
application; the virtual Apple-1 receives proposed machine commands.

Read [S01](../../field-library/S01-what-is-an-apple-1/WORKED.md) and
[SP01's board atlas](../../field-library/SP01-two-boards-one-computer/README.md).
The atlas explains functional substitutions, not verified probing points on the
project's live board.

## Addresses, values, and available storage

A 16-bit address has 65,536 possible values: `$0000` through `$FFFF`. That is
an address space, not a promise that every address is writable RAM. A hardware
map assigns ranges to RAM, ROM, and I/O. The experiment world deliberately
exposes only a 1–4 KiB RAM window, normally starting at `$0200`. Its allocated
64 KiB image does not give an agent permission to use all 64 KiB.

Memory contains bytes. A byte at `$0300` might be an opcode, text, or a number;
the consumer determines the interpretation. A variable name exists in source
code. The running CPU uses numeric addresses. See
[C02](../../field-library/C02-memory-is-a-map/WORKED.md).

## The state you will trace

| Register | Role in these lessons |
|---|---|
| A | Accumulator for loads, stores, arithmetic, comparisons, and ECHO |
| X, Y | Index registers used for counters and indexed access |
| PC | Address of the next instruction |
| SP | Position in the CPU's stack page |
| P | Status bits, including zero, negative, carry, overflow, and decimal mode |

The stack occupies CPU addresses `$0100–$01FF`; push and pop operations follow
6502 stack conventions. A subroutine call uses it for a return address. A model's
conversation history is a different kind of state entirely.

## I/O as a contract

The documented keyboard/display interface uses the `$D010–$D013` region. A
program interacts with register semantics, while the circuitry implementing
those semantics differs between original and replica designs. The lesson RAM
harness models just the needed keyboard reads and Monitor ECHO/warm-entry calls.
The general virtual world does not emulate the whole Propeller or keyboard.

## Reset is not warm entry

The NMOS 6502 reset vector is the low/high address pair `$FFFC/$FFFD`.
NMI uses `$FFFA/$FFFB`; IRQ/BRK uses `$FFFE/$FFFF`. These are vector *locations*;
their bytes identify an entry address. `JMP $FF1F`, used in the lesson programs,
is a transfer to the documented Monitor warm entry, not a CPU reset.

This corrects an earlier shared-source note. See
[the explicit erratum](../../field-library/SOURCES.md#reset-vector-correction-october-27-2026)
and MOS Technology's [programming manual, section 9.12, p. 146](https://www.bitsavers.org/components/mosTechnology/6500-50A_MCS6500pgmManJan76.pdf).
The source quotation is retained and qualified; it is not silently treated as
correct. The installed ROM contents of the physical board remain a separate
verification question.

## Practice

Draw the path from a keypress to a stored buffer byte to a displayed letter.
Label which parts are represented in S02's harness run. Then mark which parts
would require physical observations before claiming they work on this unit.

[Textbook home](../README.md) · [Previous chapter](00-how-to-use-this-book.md) · [Next chapter](02-numbers-and-characters.md)
