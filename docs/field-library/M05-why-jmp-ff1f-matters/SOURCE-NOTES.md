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

## The central claim is the repository's own

The reason `RTS` is wrong here is stated directly in
`software/ram-only/README.md` and is quoted rather than reconstructed. The
lesson then explains the mechanism, which follows from the documented behavior of
`JSR` and `RTS`.

The curriculum brief for M05 requires that the explanation be based on the
existing RAM-only README and that `RTS` not be substituted. Both are observed.

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
- **V-14 (new).** The lesson states that the Monitor's `R` command performs a
  jump rather than a `JSR`. This is taken from the repository's own statement in
  `software/ram-only/README.md` and is consistent with `RTS` being unsafe after
  `R`. It has **not** been confirmed against the `RUN` routine's actual bytes in
  the Monitor listing (BRIEL Appendix C). A reviewer should read the listing from
  the `RUN` label and confirm the instruction used, so that the mechanism in this
  lesson rests on the listing rather than only on the README's summary.
- **V-15 (new).** Whether `line-input-echo-0300.hex`'s restart loop is intended
  is an open question for the repository owner. This lesson presents it as
  observed behavior and explicitly declines to call it a defect. Do not edit the
  lesson to assert either answer before it is settled.
- **V-8 applies.** Neither program has been observed running on this board.

## What this lesson does not establish or authorize

It does not establish that either program has run on this project's machine. It
contains no entry procedure. It authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
