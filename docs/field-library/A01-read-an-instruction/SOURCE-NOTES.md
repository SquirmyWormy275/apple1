# A01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Instruction | Full name | Source |
|---|---|---|
| `LDA` | Load Accumulator with Memory | OWAD Appendix D p. 247 |
| `LDX` | Load Index X with Memory | OWAD Appendix D p. 247 |
| `LDY` | Load Index Y with Memory | OWAD Appendix D p. 248 |
| `STA` | Store Accumulator in Memory | OWAD Appendix D p. 248 |
| `STX` | Store Index X in Memory | OWAD Appendix D p. 248 |
| `STY` | Store Index Y in Memory | OWAD Appendix D p. 249 |
| `JMP` | Jump to New Location | OWAD Appendix D p. 261 |
| `INY` | Increment Index Y by One | OWAD Appendix D p. 251 |

| Claim | Key |
|---|---|
| `$D010` is the keyboard register; `$D011` its control register, whose contents change when a key arrives | P-KBD |
| `$FF1F` is the Monitor warm entry | W-FF1F |
| `$41` is `A`, `$8D` is a carriage return with bit 7 set | A-CHART, W-CR |
| The instructions quoted in Part E | REPO `software/ram-only/line-input-0300.hex` |
| Hexadecimal is written with `$`; immediate values with `#` in 6502 assembly | A-HEX; OWAD's listings and BRIEL Appendix C both use these conventions throughout |

## The addressing-mode restriction

The curriculum brief for A01 asks for immediate and absolute addressing only.
This packet observes that, with one deliberate exception: Part E quotes a real
repository instruction, `STA $0400,Y`, which is indexed.

It is quoted rather than taught. The exercise asks the learner to identify it as
unfamiliar and reason about it from context, and the answer key confirms the
reasoning and defers the explanation to A02. Removing it would have meant
misquoting the artifact, which is worse.

## Notes on correctness

The claim that `STA` has no immediate form and `JMP` has no immediate form
follows from the addressing modes listed for those instructions in OWAD Appendix
D, where neither is given an immediate form. The lesson explains *why* in terms
of what the operand has to name, which is reasoning about the instruction's
purpose rather than a cited claim.

## Deliberate simplifications

1. **Zero-page addressing is not distinguished from absolute.** `LDA $41`
   is described as reading location `$0041`, which is correct, without naming
   zero-page addressing as a separate mode.
2. **Indexed addressing is quoted but not taught** (see above).
3. **The full instruction set is not surveyed.** Seven mnemonics are enough for
   this lesson and for A02.

## Claims needing verification

- Page numbers inherit **V-1**.
- No claim here is specific to this project's board, so **V-8** is satisfied
  trivially.

## What this lesson does not establish

It teaches notation. It says nothing about any physical machine and authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
