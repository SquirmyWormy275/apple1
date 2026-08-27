# Apple-1 RAM-only software library

This library preserves known monitor programs and their test intent without
pretending that they may be run automatically. Each program is a **RAM-only**
candidate: hand entry or loading it on a live Apple-1 is a separate,
operator-led step with a known monitor prompt, video recording, and reset
recovery prepared.

## Contents

| Artifact | Address | Purpose | Hardware authority |
|---|---:|---|---|
| `software/ram-only/line-input-0300.hex` | `$0300` | Read/echo one keyboard line into `$0400`, return to Monitor | No live-run authority |
| `software/ram-only/line-input-echo-0300.hex` | `$0300` | Read/echo a line, then echo the buffer again | No live-run authority |
| `software/ram-only/README.md` | — | Entry, expected behavior, stop conditions, and recovery | Documentation only |

## Acceptance card for a future single program run

1. Photograph the initial monitor prompt and record power/USB topology.
2. Confirm no host serial process has the FT232R open.
3. Enter or load exactly one program while preserving the byte record.
4. Exercise only its documented keyboard/display behavior.
5. On unexpected output, reset to the monitor prompt, record `STOP`, and do
   not start another program.
6. Do not infer serial behavior from screen echo. The documented transmit
   experiment showed local display echo does not establish Pi-side receipt.

These are learning and regression artifacts; they do not change ROM, CFFA1,
Propeller RAM, or EEPROM.
