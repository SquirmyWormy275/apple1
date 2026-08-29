# Program annotations

Line-by-line readings of the two RAM-only programs this repository already
holds. Nothing here is a new program.

| File | Annotates | Bytes |
|---|---|---:|
| `line-input-0300.md` | `software/ram-only/line-input-0300.hex` | 26 |
| `line-input-echo-0300.md` | `software/ram-only/line-input-echo-0300.hex` | 41 |

## Status of both annotations

**Mode: OFF-DEVICE.** These are readings. They contain no entry procedure and no
instruction to type anything into a machine.

**The artifacts themselves: RAM-ONLY, no live-run authority.** That is how
`docs/apple1-software-library.md` classifies them, and annotating a program does
not change its classification or create permission to run it. If anything, a
careful reading makes the reasons for the classification easier to see.

Both programs may be rehearsed off-device in the repository emulator on an
ordinary computer, per `docs/emulator-demo-guide.md`. That guide also forbids
connecting the emulator to the physical serial device.

## How to read an annotation

Each file has the same shape:

1. **What it is for**, in one sentence.
2. **Load address and size**, and how you know.
3. **Input and output**, meaning what goes in and what has changed when it
   stops.
4. **Memory it uses**, listing every address it touches.
5. **The listing**, disassembled with addresses.
6. **Stage by stage**, in English.
7. **How it ends**, which is the part worth most attention.
8. **Expected emulator behavior**, with the recorded numbers.
9. **Limitations**, meaning what it does not handle.
10. **What this does not prove or authorize.**

## A note on the two programs together

They share their first 23 bytes exactly. The second program is the first one
with its ending replaced: instead of returning to the Monitor, it plays the
buffer back and starts over.

That difference is the single most instructive thing in this folder, and it is
the subject of open verification item **V-15**.

## Sources

Instruction meanings throughout come from OWAD Appendix D. Monitor entry points
come from the Woz Monitor listing reprinted in BRIEL Appendix C. Machine
addresses come from OWAD chapter 7. Recorded emulator results come from
`../EMULATOR-RUNS.md`. Keys resolve in `../SOURCES.md`.

## What this folder does not establish

Neither program has been observed running on this project's Replica 1 Plus.
Every behavioral statement in these annotations is either read from the bytes or
observed in a software harness that emulates no Propeller, no serial hardware,
and no ROM image.

No firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification is described or authorized anywhere in this folder.
