# M05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Exit via `JMP $FF1F`; do not replace it with `RTS`, because the Monitor's `R` command jumps to the address and leaves no return address on the stack | E-EXIT (quoted from `software/ram-only/README.md`) |
| `$FF1F` is the Monitor label `GETLINE` | W-FF1F |
| `$FFEF` is the Monitor label `ECHO`, reached by `JSR` | W-FFEF |
| `$FF00` is the Monitor's `RESET` entry | W-FF00 |
| `R` runs a user program | W-RUNCMD, R-MON-SYNTAX |
| `JSR` jumps saving a return address; `RTS` returns | OWAD Appendix D p. 261, "JSR - Jump to New Location Saving Return Address"; "RTS - Return" |
| `JMP` jumps to a new location | OWAD Appendix D p. 261 |
| The stack occupies `$0100`-`$01FF` | M-STACK |
| The expected exit path is Monitor warm entry at `$FF1F`, not `RTS` after the Monitor's `R` command | REPO `docs/emulator-demo-guide.md` |
| `line-input-echo-0300.hex` reads the buffer back "before starting over" | REPO `docs/apple1-software-library.md` |
| `returned_to_monitor: false` for the echo program | `../EMULATOR-RUNS.md` |
| Both listings, byte for byte | REPO `software/ram-only/*.hex` |

## The central claim is now checked against the listing

BRIEL Appendix C, printed/PDF p. 31, shows RUN at `$FF94` as bytes
`6C 24 00`: `JMP (XAML)`. The selected local scan was visually inspected.
This resolves V-14 and supports the no-call-frame explanation independently
of the repository README. It does not identify this unit's installed ROM.

## Disassembly

The instruction breakdowns in `assets/exit-annotation.txt` and in Part F were
produced by hand from the byte lists and cross-checked three ways: the
instruction boundaries land exactly on the final byte (`$0319` for 26 bytes,
`$0328` for 41); the branch offsets resolve to instruction boundaries rather than
mid-instruction; and the recorded emulator runs are consistent with both
programs' observed behavior, including the differing `returned_to_monitor`
values.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-14 resolved** by the exact RUN bytes above (W-RUNCMD).
- **V-15 (new).** Whether `line-input-echo-0300.hex`'s restart loop is intended
  is an open question for the repository owner. This lesson presents it as
  observed behavior and explicitly declines to call it a defect. Do not edit the
  lesson to assert either answer before it is settled.
- **V-8 applies.** Neither program has been observed running on this board.

## What this lesson does not establish or authorize

It does not establish that either program has run on this project's machine. It
contains no entry procedure. It authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
