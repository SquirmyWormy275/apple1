# M02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The `.hex` files are address-free, space-separated byte lists for entry at the address in their filename | E-RAMONLY |
| The Monitor displays up to eight locations per line | R-MON-8 |
| `4C 1F FF` is `JMP $FF1F`; `$FF1F` is the Monitor warm entry | W-FF1F, E-EXIT |
| `10 FB` is `BPL` with a relative offset | OWAD Appendix D p. 258 |
| `99 00 04` is `STA $0400,Y` | OWAD Appendix D p. 248; little-endian ordering per C02 |
| The listing used throughout | REPO `software/ram-only/line-input-0300.hex` |
| A non-hex byte is rejected by the repository loader | REPO `tools/apple1_emulator.py`, `load_hex_program`, which raises `ProgramFormatError` on a non-hex token and on an invalid byte width |

## The invented example

`assets/listing-anatomy.txt` uses `A9 01 8D 00 04 4C 1F FF`, an eight-byte
sequence written for this lesson. The asset states on its face that it is
invented for teaching and is not a real program. This follows the curriculum
brief for M02, which asks for a clearly fictional or emulator-only example unless
a cited program is used.

The worksheet then uses a cited repository program, which the same brief permits.

## Byte counts and disassembly

The byte count (26), the last address (`$0319`), the instruction split after
`EB`, and the byte-at-address table were derived by hand from the artifact and
are arithmetic, not claims requiring a source. They are consistent with the
recorded emulator runs in `../EMULATOR-RUNS.md`, which execute the same 26 bytes
and report a return to the Monitor, which could only happen if the final
instruction is the jump at `$0317`.

The relocatability conclusion in Part D was derived by inspection: the listing's
only absolute addresses are `$D010`, `$D011`, `$0400`, `$FFEF`, and `$FF1F`, all
of which lie outside the program body. It is stated as a property of this
listing, not as a general property of repository artifacts.

## Deliberate simplifications

1. **Relative addressing is used but not fully explained.** Part D relies on
   "computes its target from its own position." The signed-offset arithmetic is
   A03's job.
2. **Checksums are raised only in the optional part** and no scheme is
   recommended, because recommending one would create a second format the
   repository does not use.
3. **Indexed addressing (`,Y`) appears in the answer key** for Part E without
   explanation, because the point there is the changed address, not the mode.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-8 applies.** Nothing in this lesson has been observed on this board, and
  the lesson contains no procedure that would involve it.
- No new verification items.

## What this lesson does not establish or authorize

It contains **no entry procedure**. Identifying which address a byte belongs to
is reading, not entry. This packet authorizes no firmware load, EEPROM write,
CFFA1 write, serial-port open, or physical modification, and does not instruct
anyone to type a byte into a machine.
