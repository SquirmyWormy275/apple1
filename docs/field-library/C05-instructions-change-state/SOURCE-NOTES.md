# C05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Instruction semantics

| Instruction | Meaning | Source |
|---|---|---|
| `LDA` | Load Accumulator with Memory | OWAD Appendix D p. 247 |
| `STA` | Store Accumulator in Memory | OWAD Appendix D p. 248 |
| `ADC` | Add Memory to Accumulator **with Carry** | OWAD Appendix D p. 249 |
| `DEX` | Decrement Index X by One | OWAD Appendix D p. 251 |
| `BNE` | Branch on Result not Zero | OWAD Appendix D p. 258 |
| `JMP` | Jump to New Location | OWAD Appendix D p. 261 |

The name of `ADC` in the reference is itself the citation for the carry
behavior: it is "Add Memory to Accumulator **with Carry**", not "add."

| Claim | Key |
|---|---|
| The processor status register holds a carry flag and a zero flag | OWAD ch. 7 p. 215, the status register diagram |
| `$41` is `A`, `$42` is `B`, `$5A` is `Z` | A-CHART |
| `$FF1F` is the Monitor warm entry, label `GETLINE` | W-FF1F |
| Exit via `JMP $FF1F` rather than `RTS` | E-EXIT |
| Power-on shows a screen of garbage (Part E reasoning) | R-RESET |

## The recorded run

The ten bytes `A9 41 69 01 8D 00 04 4C 1F FF` were executed in this
repository's `tools/apple1_emulator.py` during authoring. Result: `A = $42`,
`$0400 = $42`, `returned_to_monitor: true`, 4 instructions. A variant with a
leading `CLC` (`18`) gave the same values in 5 instructions.

Recorded in `../EMULATOR-RUNS.md`. Per E-EMU-SCOPE and
`docs/emulator-demo-guide.md`, this is software evidence about a byte sequence
and is not evidence about hardware.

**The run is cited for what it shows and for what it hides.** It confirms the
arithmetic. It also demonstrates the failure mode the lesson teaches: because
the harness starts with the carry clear, the missing `CLC` produces a correct
answer, and the defect is invisible in the transcript.

## Deliberate simplifications

1. **Only the carry and zero flags are discussed,** and only as far as `ADC` and
   `BNE` require. The full status register waits for A04.
2. **The overflow flag is not mentioned** in the `$FF` plus `$01` discussion.
   Unsigned wrap and the carry are enough at this level; signed overflow is a
   separate flag and a separate lesson.
3. **Decimal mode is not mentioned.** The Monitor clears it at reset (W-FF00),
   so a program reaching this point runs in binary mode, and raising it here
   would cost more than it teaches.
4. **`ADC` is written as immediate only.** Addressing modes stay at immediate
   and absolute, matching C01 and the A01 brief.

## Claims needing verification

- Page numbers inherit **V-1**.
- The recorded run is off-device software evidence only (**V-8** unaffected:
  the lesson makes no hardware claim).
- **V-11 (new).** The claim that the harness begins with the carry clear was
  inferred from the observed result (`$42` rather than `$43`) plus a direct
  py65 reproduction, not from a stated guarantee in the tool. If a future harness
  change altered initial processor state, this lesson's "what the emulator
  produced" note would need rechecking.

## What this lesson does not establish

It does not establish that either program has ever run on this project's
machine, and neither is offered for entry there. It authorizes no firmware load,
EEPROM write, CFFA1 write, serial-port open, or physical modification.
