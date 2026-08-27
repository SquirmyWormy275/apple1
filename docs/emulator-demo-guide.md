# Emulator and demo preparation

Use an Apple-1 emulator as an off-device rehearsal environment for Monitor
syntax, 6502 byte sequences, program flow, screenshots, and presentation
scripts. Emulator results are useful software evidence but never prove a
Replica 1 Plus electrical, Propeller, PS/2, FT232R, or timing behavior.

The repository now includes `tools/apple1_emulator.py`: a pinned Py65-backed,
ROM-free harness that executes the RAM-only `$0300` programs with Apple-1
keyboard high-bit input and a Monitor ECHO stub. It is deliberately narrower
than a complete Apple-1 machine emulator: it does not ship a Woz Monitor ROM,
emulate the Propeller, or open serial hardware.

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest tests\test_apple1_emulator.py -q
python .\tools\apple1_emulator.py .\software\ram-only\line-input-0300.hex --input "HI`r"
```

## Repeatable rehearsal packet

- Emulator name/version and ROM image provenance
- Exact program bytes and load address
- Input transcript and screen capture
- Expected exit path: Monitor warm entry at `$FF1F`, not `RTS` after the
  Monitor's `R` command
- Any discrepancy from the RAM-only library, retained as a software issue

For host-generated demonstrations, use `tools.apple1_text.format_for_apple1`.
It produces deterministic upper-case seven-bit printable text with visible `?`
substitution for unsupported characters and fixed-width wrapping. It has no
serial or model dependency, which keeps demo work separate from the blocked
hardware path.

Do not connect an emulator to the physical serial device, and do not use a
successful emulator run to waive a hardware evidence gate.
