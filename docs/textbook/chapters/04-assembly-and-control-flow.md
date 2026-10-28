# 4. Write assembly as controlled state changes

Assembly is a readable notation for machine instructions. The host lesson
assembler translates it to bytes in two passes. Labels name addresses during
translation; they are not extra CPU operations and are not runtime strings.

## Choose an addressing mode

| Form | Read it as | Typical example |
|---|---|---|
| Immediate | Use this value | `LDA #$41` |
| Zero page | Access a byte in the first 256 addresses | `LDA $20` |
| Absolute | Access the specified address | `LDA $0400` |
| Indexed | Add X or Y to a base address | `STA $0400,Y` |
| Relative | Select a signed displacement after the branch | `BNE LOOP` |
| Indirect | Obtain an address through memory | `JMP ($0400)` |
| Indexed indirect / indirect indexed | Use zero-page pointers with an index | `LDA ($20,X)` / `LDA ($20),Y` |
| Implied / accumulator | The operand is implicit | `DEX` / `ASL A` |

These describe 6502 instruction forms, not blanket permissions in NEURAL1.
The experimental RAM policy can disallow addresses a physical CPU could access.
NMOS and CMOS variants differ; do not introduce later 65C02-only instructions
into an NMOS lesson. See the original MOS programming manual linked in chapter 1.

## Follow flags through branches

`CMP` compares without replacing A. `BEQ` tests zero set; `BNE` tests zero clear.
`BPL` tests negative clear; it includes zero. `BCC` and `BCS` inspect carry.
`BVC` and `BVS` inspect overflow. Identify which instruction last set the flag
you are branching on. A nearby instruction may overwrite it.

[A03](../../field-library/A03-counting-and-looping/WORKED.md) compares BNE and
BPL countdowns. Starting X at 5, the BNE version reaches zero and stops; the BPL
version decrements through zero to `$FF`. The captured instruction counts are
13 and 15 for these complete routines, not physical execution times.

## Indexed loops and boundary checks

To fill five bytes, initialize Y to zero, store at `$0400,Y`, increment, compare
against five, and repeat while unequal. Test both the last intended destination
and the byte immediately after it. A routine can return cleanly while writing
one extra byte. [X02](../../field-library/X02-fix-the-loop/WORKED.md) demonstrates
exactly that failure; the broken comparison writes at `$0405` as well.

## Subroutines and the stack

`JSR` records a return address on the hardware stack and transfers control;
`RTS` reconstructs the matching return. `PHA`/`PLA` and `PHP`/`PLP` save and
restore data/status with their specified effects. Balance pushes and pops and
decide which registers a subroutine preserves. A useful routine contract states
inputs, outputs, clobbered registers, memory writes, and exit behavior.

The world implements only the Monitor stubs its tests need. It does not supply
a real Monitor ROM, an operating system, or a complete physical interrupt path.
For full instruction semantics, consult the primary manual and Py65 code; for
the allowed experimental interface, consult `world.py` and its tests.

## Debug systematically

1. Predict the path for each input class, including empty and boundary cases.
2. Read before-instruction trace rows correctly; compare the next row for effects.
3. Check writes, final registers, and stop reason, not just screen output.
4. Change one instruction or operand and preserve both results.
5. Use a negative control that must fail the intended criterion.

Run A01–A06 in order, then X02. A06's fill utility is a small capstone: explain
its code/data separation and prove from the checks that it writes exactly five
bytes. Instruction counts are one metric; readability and a well-defined
contract are additional engineering goals.

[Textbook home](../README.md) · [Previous chapter](03-monitor-and-first-program.md) · [Next chapter](05-input-output-and-debugging.md)
