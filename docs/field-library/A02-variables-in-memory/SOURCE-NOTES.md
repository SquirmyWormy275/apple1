# A02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Instruction | Full name | Source |
|---|---|---|
| `LDA`, `LDX`, `LDY` | Load Accumulator / Index X / Index Y with Memory | OWAD Appendix D pp. 247 to 248 |
| `STA`, `STX`, `STY` | Store Accumulator / Index X / Index Y in Memory | OWAD Appendix D pp. 248 to 249 |
| `INY` | Increment Index Y by One | OWAD Appendix D p. 251 |
| `JMP` | Jump to New Location | OWAD Appendix D p. 261 |

| Claim | Key |
|---|---|
| The Monitor listing carries labels such as `GETLINE`, `ECHO`, and `NOTCR` beside addresses and bytes | BRIEL Appendix C p. 30; W-FF1F, W-FFEF |
| `$FF1F` is `GETLINE`, `$FFEF` is `ECHO` | W-FF1F, W-FFEF |
| `line-input-0300.hex` uses `LDY #$00`, `STA $0400,Y`, and `INY` | REPO `software/ram-only/line-input-0300.hex` |
| `line-input-echo-0300.hex` reads the buffer back with `LDA $0400,Y` | REPO `software/ram-only/line-input-echo-0300.hex` |
| The program occupies `$0300` to `$0319` (26 bytes) | Arithmetic on the artifact; M02 |
| `$48` is `H`, `$49` is `I`, `$5A` is `Z` | A-CHART |
| A full queue is a recorded stop, not a silent discard | REPO `docs/firmware-behavior-model.md` |

## Indexed addressing

Indexed addressing is described here operationally: base address plus index
register. The absolute-indexed forms of `LDA` and `STA` are those listed in OWAD
Appendix D for those instructions.

The claim that Y wraps from 255 to 0 follows from Y being a single byte
(C03) and from `INY` being an increment. It is arithmetic, not a cited claim.

## The Part G finding

The answer key's conclusion that straight-line indexing costs *more* instructions
than straight-line hard-coding was arrived at by counting, and it is stated
plainly rather than smoothed over. It is correct and it is pedagogically useful:
it forces the loop, which is A03.

This is worth preserving if the packet is edited. A version of Part G that
concluded indexing is always cheaper would be wrong.

## Deliberate simplifications

1. **Only Y-indexed absolute addressing is taught.** X-indexed exists and behaves
   the same way; indirect and indirect-indexed modes are not mentioned at all.
2. **"Variable" is used loosely** to mean an address a programmer has reserved by
   convention. There is no declaration mechanism to contrast it with at this
   level.
3. **The buffer-overrun discussion stops at "nothing warns you."** Bounds
   checking is an A06 design concern.

## Claims needing verification

- Page numbers inherit **V-1**.
- No claim here is specific to this project's board (**V-8** trivially
  satisfied).

## What this lesson does not establish

Nothing about any physical machine. Both example programs are paper exercises,
neither is supplied as an artifact, and this packet contains no entry procedure.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
