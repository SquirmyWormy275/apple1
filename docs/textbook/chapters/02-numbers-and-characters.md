# 2. Numbers, bits, and characters

The same pattern of bits can be interpreted in several ways. First learn the
representation; then state which interpretation the program uses.

## Hexadecimal without guessing

A byte has eight bits and 256 possible patterns. A hex digit represents four
bits, so two hex digits represent a byte exactly. Decimal 42 is `2*16+10`, or
`$2A`. A 16-bit address normally needs four hex digits. Prefix `$` here means
hexadecimal, not a currency amount or a shell variable.

Work [S03](../../field-library/S03-your-first-hex-number/WORKED.md), then
[C03](../../field-library/C03-binary-bits-and-bytes/WORKED.md). For each conversion,
explain the high and low nibble instead of relying solely on Python's formatter.

## Unsigned and signed interpretations

As an unsigned byte, `$FF` is 255. As an eight-bit two's-complement value it
represents -1. The bits have not changed. A relative branch's offset uses that
signed interpretation: `$FD` is -3. Address arithmetic uses the PC after the
two-byte branch instruction as its base.

An eight-bit addition can wrap. `$FF + $01` leaves `$00` in the byte result,
with carry describing the extra unsigned bit. The overflow flag answers a
different question about signed arithmetic. Never treat carry and overflow as
interchangeable.

## Flags are inputs as well as outputs

`ADC` computes A plus the operand plus carry. If a routine requires binary
addition with no incoming carry, establish it with `CLD` and `CLC`. `LDA` does
not clear carry. A simulator's initial state is not a portable program contract.
Run the two explicit carry cases in
[C05](../../field-library/C05-instructions-change-state/WORKED.md).

## Bytes that represent characters

ASCII assigns numeric codes to characters. `$41` is uppercase A and `$0D` is
carriage return. The repository RAM harness sets the top bit for keyboard input,
so A becomes `$C1` and carriage return becomes `$8D`. AND with `$7F` recovers
the seven-bit value. These are documented harness operations, not measurements
of today's physical keyboard.

[C04](../../field-library/C04-characters-become-numbers/WORKED.md) encodes and
decodes `HI` plus Return. Explain why comparing `$8D` to `$0D` would fail unless
the high bit had first been removed.

## Addresses are also encoded as bytes

A 6502 absolute operand stores the low byte first. `STA $0400` encodes as
`8D 00 04`; `JMP $FF1F` encodes as `4C 1F FF`. The opcode determines how many
bytes to consume and how to interpret the next bytes. The value `D0` inside an
address operand is not automatically a branch instruction.

## Practice and checks

1. Convert decimal 200 to hex and binary. Answer: `$C8`, `11001000`.
2. Interpret `$FE` as an unsigned byte and a signed offset. Answer: 254 and -2.
3. A branch at `$0303` has operand `$FD`. Its base is `$0305`; its target is `$0302`.
4. Explain why a screen character, a branch offset, and a stored integer can
   share the same byte pattern while having different meanings.

Use [X01](../../field-library/X01-hex-scavenger-hunt/WORKED.md) to practice
reading a known artifact listing with addresses and instruction boundaries.

[Textbook home](../README.md) · [Previous chapter](01-the-machine.md) · [Next chapter](03-monitor-and-first-program.md)
