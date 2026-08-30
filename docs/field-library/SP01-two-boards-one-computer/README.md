# SP01 Two Boards, One Computer

**Audience:** STUDY / BUILD  
**Time:** 45–75 minutes  
**Status:** OFF-DEVICE  
**Prerequisites:** S01, C01, C02, M01, H02

## You will learn

By the end, you can locate the major physical subsystems of an original Apple-1
and a Replica 1 Plus, explain which software-visible ideas remain familiar, and
explain why the two boards can support related software while using very
different support hardware.

## Why this matters

A replica can preserve a programming model without reproducing every IC, trace,
power circuit, and peripheral implementation of the historical machine. The
Apple-1 and Replica 1 Plus make that distinction unusually visible: both center
on a 6502-family processor and PIA-style memory-mapped I/O, while the Replica
collapses much of the original terminal circuitry into modern components.

This packet is a special Field Library lesson built for the eventual CF-card
educational catalog. Its learner-facing material is under `card/` as fixed-size
ASCII screens rather than as a modern graphical poster.

## First result

1. Read `card/original/00-atlas-map.txt`.
2. Read `card/replica/00-atlas-map.txt`.
3. Find the 6502 and the display/video subsystem in each atlas.

**Visible result:** the CPU remains recognizable in both designs while the
surrounding memory, video, keyboard, power, and host-I/O hardware changes
substantially.

## What you need

A terminal or text viewer. The card-facing pages are printable seven-bit ASCII,
uppercase, no more than 40 columns, and no more than 24 lines per page.

No physical Apple-1, Replica 1 Plus, CF card, serial device, or emulator is
required.

## The atlas

The original Apple-1 map uses the documented A-D / 1-18 board-coordinate system
and is divided into six tiles:

```text
       +--------+--------+--------+
D / C  |  DC1   |  DC2   |  DC3   |
       +--------+--------+--------+
B / A  |  BA1   |  BA2   |  BA3   |
       +--------+--------+--------+
```

The Replica 1 Plus uses four photograph-oriented tiles based on the labeled
board view in the Briel Computers manual:

```text
       +-------------+-------------+
TOP    |     UL      |      UR     |
       +-------------+-------------+
BOTTOM |     LL      |      LR     |
       +-------------+-------------+
```

The atlas then adds dedicated pages for the original video subsystem, Replica
logic block, memory technologies, the common CPU/PIA model, Woz Monitor-style
interaction, and a keypress-to-screen path through each machine.

## Explain what changed

### Original Apple-1

The original board devotes a large fraction of its IC count to the terminal.
The atlas identifies the 2504 shift-register population, 2519 row-shift logic,
2513 character generator, TTL counters/gates, cursor timing, processor, 6820
PIA, Monitor PROM pair, two DRAM-bank positions, keyboard connector, address
decoder, power section, and expansion edge.

The useful visual lesson is that the **terminal is physically a major subsystem
of the computer**, not a small peripheral chip hanging off the processor.

### Replica 1 Plus

The Replica keeps a recognizable 6502 + PIA core while replacing the original
DRAM with SRAM, using modern ROM storage, and assigning many I/O duties to the
P8X32A-D40 Propeller. The manufacturer's manual describes the Propeller as
handling video, serial, PS/2, and master-clock functions. The board also adds
USB serial/power hardware and PS/2 while retaining an ASCII-keyboard path and an
Apple-1-style expansion connection.

### Software-visible continuity

The classic Apple-1 keyboard/display locations remain the important teaching
contract:

| Function | Address |
|---|---:|
| Keyboard data | `$D010` |
| Keyboard control | `$D011` |
| Display data | `$D012` |
| Display control | `$D013` |

A program can care about those software-visible locations and behaviors without
needing to know whether the display is implemented by 1976 shift-register logic
or a modern programmable controller.

That is the central distinction in this lesson:

> **Compatible does not mean physically identical.**

## Activity

Use the card atlas to locate the 6502, 6820 PIA, RAM banks, and video-dense rows
on the original board. Then identify the Replica component that absorbs many of
the original terminal/I/O jobs. Complete `ACTIVITY.md` and check `ANSWERS.md`.

## Try a variation

Pick one subsystem—memory, video, keyboard, Monitor storage, power, or expansion—
and write a two-column comparison:

```text
1976 IMPLEMENTATION | REPLICA IMPLEMENTATION
```

Describe which part of the **software contract** stays familiar and which part
of the **physical implementation** changes.

## Check your understanding

1. Why does the original Apple-1 have so many video-related IC packages?
2. What role does the PIA play in the programming model?
3. How does the Replica simplify main-memory hardware?
4. Name three I/O/clock jobs assigned to the Propeller by the Replica manual.
5. Why can related Apple-1 software run on hardware that is not a component-for-
   component reproduction?
6. What does this lesson establish—and not establish—about this project's live
   Replica 1 Plus?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

See `SOURCE-NOTES.md` for the original Apple-1 manual, Mike Willegal's Mimeo
assembly guide, Apple-1 Registry cross-check, SB-Projects terminal explanation,
Briel Computers Replica 1 Plus manual, and project-specific evidence.

The ASCII maps are **educational identification maps**, not service drawings.
They deliberately omit traces, pin numbers, voltages, test points, and probing
instructions.

This lesson authorizes no serial-port open, CF-card write, firmware load, EEPROM
write, jumper change, wiring change, or live program run.
