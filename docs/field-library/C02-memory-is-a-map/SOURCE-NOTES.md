# C02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| 64 KB addressable space; the address bus is 16 bits wide | M-64K |
| Monitor ROM is 256 bytes at `$FF00`-`$FFFF` | M-ROM |
| The 6502 finds its start address at the top of memory on reset | M-RESET-VEC |
| Original: 4 KB at `$0000`-`$0FFF`; 4 KB at `$E000`-`$EFFF` | M-RAM-ORIG |
| `$E000`-`$EFFF` was RAM on the original, so BASIC was reloaded every power-up | M-BASIC-RAM |
| The stack is `$0100`-`$01FF`, base `$01FF`, growing down | M-STACK |
| The PIA occupies `$D010`-`$D012` on the map | M-PIA-RANGE |
| `$D011` is the keyboard control register | P-KBD |
| `$D012` is the display register; writing hands a character to the video section | P-DSP, P-DSP-BUSY |
| Replica: 32 KB user space, Integer BASIC in ROM at `$E000`-`$EFFF` | M-REPLICA-MAP |
| `$FF1F` is the Monitor label `GETLINE` | W-FF1F |
| Repository programs are written for `$0300` and buffer at `$0400` | E-RAMONLY; `software/ram-only/README.md` |
| The byte sequences `99 00 04` and `4C 1F FF` | REPO `software/ram-only/line-input-0300.hex` |

## The map is a model

This is stated in the lesson body, in `STATUS.md`, and here, because the
curriculum brief for C02 requires it.

`assets/memory-map.txt` reproduces the documented layout of the **original
Apple-1**, from OWAD Figure 7.14 and the surrounding text. It is not a reading
taken from any board. Two labels on it come from this repository rather than
from OWAD, and are marked as such on the diagram: the `$0300` entry point and
the `$0400` buffer used by the RAM-only programs.

The `$0200` label for the Monitor's input line is inferred from the Monitor
listing, where the text buffer is indexed as `IN,Y` and assembled as
`99 00 02` at `FF31`, giving a base of `$0200`. That inference is recorded as
verification item **V-9** below rather than presented as documented fact.

## Deliberate simplifications

1. **Zero page is named but its addressing modes are not explained.** Zero-page
   addressing is faster and shorter; that belongs in the A-series.
2. **"Unused" regions are shown as empty.** OWAD notes a user could add RAM
   there, and that Joe Torzewski upgraded his Apple-1 to 16 KB. The map shows
   the stock design.
3. **Little-endian is introduced by example only,** without discussing why the
   6502 does it that way.
4. **The `$D013` boundary on the diagram** is drawn to include the display
   control register. OWAD's own figure labels the block `$D010 - $D012`. The
   fourth register at `$D013` is documented in Table 7.5. The diagram shows the
   register block; the figure caption shows the three most-used addresses.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-4 applies and is load-bearing here.** OWAD's replica map is the Replica I.
  This project's machine is a Replica 1 Plus. The lesson says "later replicas"
  and "the replica design documented by Owad", never "this machine".
- **V-9 (new).** The `$0200` Monitor input-line label is inferred from the
  Monitor listing's `STA IN,Y` assembling as `99 00 02`, not from a stated
  memory-map entry. Confirm against a primary Apple-1 memory map before this
  packet goes on the card.
- **V-8 applies.** Nothing here was read from this board.

## What this lesson does not establish

It does not establish what is at any address on this project's machine. It
authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification, and offers no procedure for inspecting memory on
hardware.
