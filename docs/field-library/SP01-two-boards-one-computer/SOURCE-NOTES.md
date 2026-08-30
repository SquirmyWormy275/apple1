# SP01 Source notes

SP01 is self-contained so the card-facing atlas can be reviewed without
changing the existing shared source pool.

## Original Apple-1

### Apple Computer Company, *Apple-1 Operation Manual* (1976)

Primary source for the original architecture, schematics, keyboard/display I/O,
and display geometry. The manual specifies a 40-character by 24-line display
and describes dynamic shift-register display memory.

Computer History Museum scan:
`https://archive.computerhistory.org/resources/text/Apple/Apple.AppleI.1976.102646518.pdf`

### Mike Willegal, *Apple 1 Mimeo Computer Assembly and Bring Up Guide*, rev. 1.1

Primary physical-placement source for the ASCII atlas. The guide uses the
Apple-1 PCB A-D / 1-18 coordinate system and identifies, among other locations:

- A1/A2 — Monitor PROMs;
- A4 — 6820 PIA;
- A7 — 6502 CPU;
- A9/A10 — bus drivers;
- B4 — keyboard connector;
- B9 — address decoder;
- B11-B18 — DRAM bank X;
- A11-A18 — DRAM bank W;
- D2 — 2513 character generator;
- C3 — 2519;
- D4a/b, D5a/b, D14a/b, C11b — seven 2504 shift registers.

Source:
`https://www.willegal.net/appleii/A1-assembly-v1.1.pdf`

### SB-Projects, *Apple 1 — Terminal*

Supporting explanation of the recirculating 2504/2519/2513 terminal design.

Source:
`https://www.sbprojects.net/projects/apple1/terminal.php`

### Apple-1 Registry

Used only as a surviving-board visual/component cross-check, not to authenticate
any particular board.

Source:
`https://www.willegal.net/appleii/apple1-originals.htm`

## Replica 1 Plus

### Briel Computers, *Replica 1 Plus Setup and Users Manual*, June 2014,
Plus Edition Version 3.0

Primary source for the Replica atlas. Figure 3 is the labeled physical board
photograph used to orient the four tiles. Figure 4 is the logic block diagram.
The manual identifies the main ICs as 6502, 6821, 27C128, 62256,
P8X32A-D40 Propeller, 24LC256, 74LS00, and 74LS138, plus USB serial hardware.
It also states that the Propeller handles I/O including video, serial, PS/2, and
the master 1 MHz clock.

Project/reference scan:
`https://wiki.reactivemicro.com/images/7/73/Replica_One_Plus_Manual_-_June_2014.pdf`

## Project-unit evidence

`docs/hardware/plus-io-map.md` confirms the host-visible FTDI FT232R while
explicitly leaving several board-level signals unverified.

The project's 2026-08-27 no-transmit capture records a STOP result: opening the
FT232R disturbed the display and physical Reset restored the Monitor.

## Boundary

The Mimeo guide is used as a placement-reconstruction source; it is not
provenance for a surviving original Apple-1. The Replica manual describes the
manufacturer's design, not proof of the exact electrical behavior of this
project's live unit.

The ASCII layouts are educational identification maps, not service drawings.
They omit traces, voltages, test points, and pin-level probing instructions.
