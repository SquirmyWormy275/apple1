# S03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Two hex characters represent one byte | A-HEX |
| Hex is prefixed with `0x` or `$` | A-HEX |
| Decimal, binary, and hex equivalences for 0 to 15, 16, 31, 32, 63, 127, 255 | A-TABLE |
| `$0D` is carriage return; `$20` is space; `$41` is capital A | A-CHART |
| ASCII assigns decimal 0 to 127, one byte per character | A-ASCII |
| `$D010` is the keyboard slot, `$D012` the display slot (used in the variation) | P-KBD, P-DSP |
| `$8D` is a carriage return with bit 7 set | W-CR, P-HIGHBIT |

## Not sourced, and not needing a source

The arithmetic is arithmetic. Dividing by sixteen, the place-value explanation,
and the worked conversions are general mathematics and carry no Apple-1-specific
claim. They are not cited and do not need to be.

The claim that a byte holds 256 values follows from eight bits, which is
general computing background rather than an Apple-1 fact.

## Claims needing verification

- Page numbers inherit **V-1**.
- No claim in this lesson is specific to this project's machine, so **V-8** is
  satisfied trivially: the lesson makes no hardware claim to verify.

## What this lesson does not establish

Nothing about hardware at all. It authorizes no firmware load, EEPROM write,
CFFA1 write, serial-port open, or physical modification.
