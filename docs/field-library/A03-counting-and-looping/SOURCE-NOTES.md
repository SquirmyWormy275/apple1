# A03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Instruction | Full name | Source |
|---|---|---|
| `DEX` | Decrement Index X by One | OWAD Appendix D p. 251 |
| `INX` | Increment Index X by One | OWAD Appendix D p. 251 |
| `INY` | Increment Index Y by One | OWAD Appendix D p. 251 |
| `BNE` | Branch on Result not Zero | OWAD Appendix D p. 258 |
| `BPL` | Branch on Result Plus | OWAD Appendix D p. 258 |
| `CPX` | Compare Memory and Index X | OWAD Appendix D p. 256 |
| `CPY` | Compare Memory and Index Y | OWAD Appendix D p. 256 |
| `LDX`, `STX`, `JMP` | As A01 and A02 | OWAD Appendix D pp. 247, 248, 261 |

| Claim | Key |
|---|---|
| The processor status register carries a zero flag and a negative flag | OWAD ch. 7 p. 215, status register diagram: `N` and `Z` |
| Bit 7 set means negative in the status register's sense | Same diagram, `1 = NEG` |
| `$FF` is 255 and every bit is set | A-TABLE, C03 |
| The Monitor's `BPL NEXTCHAR` and `BMI GETLINE` show branches in real use | BRIEL Appendix C p. 30 |
| Relative branches survive relocation while absolute jumps carry their target | M02, derived |

## Recorded observations

Both programs were executed during authoring against the `py65` NMOS 6502 model,
the same processor model the repository's harness uses.

| Program | Result |
|---|---|
| A (`BNE`) | X = `$00`, `$0400` = `$00`, `DEX` executed 5 times, 13 instructions |
| B (`BPL`) | X = `$FF`, `$0400` = `$FF`, `DEX` executed 6 times, 15 instructions |

These were run directly against the processor model rather than through
`tools/apple1_emulator.py`, because neither program reads the keyboard and the
harness's command-line interface requires an input string. The bytes executed
are the bytes in the worksheet.

This is off-device software evidence about eleven bytes. Per E-EMU-SCOPE and
`docs/emulator-demo-guide.md`, it is not evidence about hardware.

## Signed offsets

The two's-complement reading of branch offsets (`$80` to `$FF` as -128 to -1,
read by subtracting 256) is standard 6502 behavior and is arithmetic. It is
introduced here because A03 is the first lesson that needs it; C03 deliberately
deferred it.

The branch range of -128 to +127 from the following instruction follows from the
offset being one signed byte.

## Deliberate simplifications

1. **Only the zero and negative flags are discussed.** Carry, overflow, decimal,
   and interrupt-disable are not, though `CPX` and `CPY` also affect the carry.
2. **Compare instructions are described only by their effect on the zero flag,**
   which is all Part F and Part G require. Their full flag behavior is not given.
3. **The "test at the bottom" structure is treated as the only loop shape.**
   Testing at the top exists and is not covered.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-16 (new).** The recorded results for Programs A and B come from a direct
  `py65` reproduction performed during authoring, not from a run of
  `tools/apple1_emulator.py`, and are not listed in `../EMULATOR-RUNS.md` as
  harness runs. A reviewer wanting harness-level confirmation would need to wrap
  these bytes in a form the harness accepts.
- **V-8 applies.** Neither program has run on this board.

## What this lesson does not establish

Nothing about this project's machine. Neither program is supplied as an artifact
and no entry procedure appears anywhere in the packet. It authorizes no firmware
load, EEPROM write, CFFA1 write, serial-port open, or physical modification.
