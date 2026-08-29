# C03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Decimal, binary, and hex equivalences, including 0 to 15, 127, 255 | A-TABLE |
| Two hex characters represent one byte | A-HEX |
| A byte is eight bits; nibble and word terminology | OWAD Appendix E p. 266, the word/byte/nibble/bit diagram |
| ASCII uses decimal 0 to 127, half the space in a byte, leaving bit 7 spare | A-ASCII |
| `A` is `$41`, space is `$20`, carriage return is `$0D` | A-CHART |
| The keyboard supplies a seven-bit ASCII value | P-KBD-7BIT |
| The Monitor expects a keyboard byte with bit 7 set | P-HIGHBIT |
| `$8D` is a carriage return in Monitor terms | W-CR |
| The display register's top bit is the Data Available line | P-DDR |
| A program checks bit 7 of `$D012` and waits for it to go low | P-DSP-BUSY |
| The PIA registers are `$D010` to `$D013` | P-KBD, P-DSP |
| The machine understands upper case only | R-UPPER |

## Not sourced, and not needing a source

Place value in base two, the doubling column values, the nibble-to-hex split,
and every worked conversion are general arithmetic. They carry no
Apple-1-specific claim.

The claim in Part D that `$41` and `$61` differ by bit 5 is a property of the
ASCII table (A-CHART), read directly.

## Deliberate simplifications

1. **Signed values are not mentioned.** A byte is presented as 0 to 255
   throughout. Two's complement and negative branch offsets arrive in A03, where
   the `BPL $0302` offset of `$FB` needs them.
2. **Bit operations are not taught.** `AND`, `ORA`, and `EOR` are the real way a
   program tests or sets a single bit. This lesson teaches what a bit *is*; the
   instructions that manipulate them belong in the A-series.
3. **The Data Available line is named but not developed.** P-DDR is cited so an
   educator can follow it up, but the lesson only needs "one bit means busy."

## Claims needing verification

- Page numbers inherit **V-1**.
- No claim in this lesson is specific to this project's machine.
- **V-4 note:** R-UPPER is cited from the Replica 1 Plus manual and is stated in
  the answer key as context for the case-shift bit, not as a claim about how
  this board behaves today.

## What this lesson does not establish

Nothing about hardware. It authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
