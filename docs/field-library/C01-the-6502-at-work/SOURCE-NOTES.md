# C01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key or basis |
|---|---|
| `LDA` is Load Accumulator with Memory; `STA` is Store Accumulator in Memory; `LDY` is Load Index Y with Memory | OWAD Appendix D, "Instructions by Category", pp. 247 to 249 |
| `BPL` is Branch on Result Plus | OWAD Appendix D, p. 258 |
| The 6502 has A, X, and Y registers and a processor status register | OWAD ch. 7 pp. 215 to 216 |
| The stack occupies `$0100`-`$01FF` (mentioned only in passing) | M-STACK |
| `$D011` is the keyboard control register holding the ready flag | P-KBD |
| The worked byte sequence `A0 00 / AD 11 D0 / 10 FB` | REPO `software/ram-only/line-input-0300.hex`, first seven bytes |
| `line-input-0300.hex` ends with `JMP $FF1F` and returns to the Monitor | E-EXIT; confirmed by run, `../EMULATOR-RUNS.md` |
| `$FF1F` is the Monitor label `GETLINE` | W-FF1F |

## Disassembly of the worked bytes

The instruction breakdown in Part D was produced by hand from the byte list and
checked against the recorded emulator runs in `../EMULATOR-RUNS.md`, which
execute the same bytes and report `returned_to_monitor: true`. The opcode
meanings are from OWAD Appendix D; the address arithmetic is arithmetic.

`A0` is `LDY` immediate. `AD` is `LDA` absolute. `10` is `BPL` relative with
offset `$FB`, which is minus five, giving a target of `$0307 - 5 = $0302`.

## Deliberate simplifications

1. **Only three registers are named.** The processor status register, the stack
   pointer, and the individual flags are deferred. A04 introduces flags when the
   lesson needs them.
2. **Addressing modes are limited to immediate and absolute,** per the
   curriculum brief for A01 and the same restraint here. Indexed addressing
   appears in the byte list but is not explained until A02.
3. **"Fetch, decide, act"** is a teaching name. The conventional term is the
   fetch-execute or instruction cycle. Nothing turns on the naming.
4. **Cycle counts and timing are not mentioned at all.** This library makes no
   timing claims about any machine.

## Claims needing verification

- Page numbers inherit **V-1**.
- The instruction semantics are properties of the 6502, not of this board, so
  **V-8** does not bite. The lesson makes no claim about this machine.

## What this lesson does not establish

It describes an instruction set. It does not show that any of these instructions
have ever executed on this project's Replica 1 Plus. It authorizes no firmware
load, EEPROM write, CFFA1 write, serial-port open, or physical modification.
