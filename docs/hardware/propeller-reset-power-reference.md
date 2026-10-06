# Propeller reset and power reference

Reviewed 2026-09-11. Authority: DERIVED DOCUMENTATION. Drawing-based locations
below are candidates until checked on Alex's actual board. No live measurement
was performed for this report.

## New finding: a relevant schematic is available

An original Vince Briel drawing, titled **replica I plus**, revision **0**, dated
**3/29/2014**, was retrieved from a third-party archive and visually inspected.
It depicts an 18-position USB interface. The September 2 record instead describes
a four-conductor installed connection. Resolve this mismatch physically; neither
source silently supersedes the other.

The drawing separates two nets:

| Schematic net | Connected components in the drawing | Meaning |
|---|---|---|
| RST | U7 pin 11 and Q1 collector | Propeller reset |
| RESET | RESET switch, U1 pin 40, U2 pin 34, expansion and ASCII reset contacts | 6502/6821 reset |
| PHI0 | U7 pin 20, U1 pin 37, expansion PHI0 | Propeller-generated CPU clock |

It also depicts **USB-interface DTR -> C9 -> Q1 base**, with R10 to ground and
Q1 collector on RST. This is a candidate reset-on-open path, not proof that the
installed breakout connects DTR. Q1 lead order must be established from the
actual transistor/package or continuity, not inferred from its drawing symbol.

Drawing evidence: [Briel schematic, revision 0](http://retro.hansotten.nl/uploads/apple1/r1plus%20schematics.pdf).
Downloaded PDF SHA-256:
`dbd707582e00d98be685e69e6c7640ae28edc1e32074778976de98f496860dbe`.
The source PDF was used for research and is not redistributed by this change.

## Chip reference and candidate probe points

Parallax's D40 drawing confirms the following pin assignments. Apply them only
after checking the installed chip marking, DIP orientation, and board routing.

| Target | P8X32A-D40 physical pin | Candidate access |
|---|---:|---|
| RESn | 11 | U7 lead/socket pad, or a verified point on its RST net |
| Ground / VSS | 9, 29 | Verified ground header or pad |
| VDD | 12, 32 | Verified supply point, for meter/scope |
| P15 / candidate PHI0 | 20 | Verified U7/clock-net point |
| P30 / TX to host | 39 | Verified UART net |
| P31 / RX from host | 40 | Verified UART net |
| BOEn | 10 | Establish its connection from drawing/continuity; no setting change |

RESn is active low; reset disables cogs and floats I/O. BOEn controls brownout
monitoring and RESn behavior. The operating supply range is 2.7-3.6 V. These
chip facts do not identify a safe clip location or prove installed firmware.
Reference: [Parallax P8X32A datasheet, rev 1.4, 6/14/2011](https://www.parallax.com/package/p8x32a-propeller-datasheet/),
pages 4, 6, 25. PDF SHA-256:
`c160519a8012990485803a4af8f2be8dde8c155725478f152f7e658121638550`.

## Power-selector discrepancy to resolve first

The completed capture records a **3.3V** switch setting. ReActiveMicro's
Programming And Source Code section calls for **5V**. This is a documentation
discrepancy, not authorization to move the switch. The manufacturer's Versions
section describes its 2017 production as a reproduction of the earlier board,
but that does not settle which breakout is installed today.

The separate screen-noise guidance concerns intermittent slash/linefeed noise.
It is not a demonstrated diagnosis of this open-associated failure. Its prose
also calls Propeller physical pin 39 a transmit line; direction must be stated
from the correct device perspective and checked against the datasheet/source.
Reference: [ReActiveMicro Replica 1 documentation](https://wiki.reactivemicro.com/Replica_1),
Programming And Source Code, Screen Noise Issue, and Versions; page revision
5708, last edited 2021-04-11, checked 2026-09-11.

FTDI distinguishes VCC (core supply), VCCIO (UART output-level supply), and
3V3OUT (regulated output, up to 50 mA external load in the cited revision).
The selector could affect output supply, VCCIO, or both depending on the module.
No module behavior can be deduced from the switch label alone. Check its actual
part number and connections before assessing loading or voltage compatibility.
Reference: FTDI-authored **FT_000053, version 2.07**, pages
[7](https://www.alldatasheet.com/html-pdf/394106/FTDI/FT232R/701/7/FT232R.html) and
[8](https://www.alldatasheet.com/html-pdf/394106/FTDI/FT232R/802/8/FT232R.html),
read through an identified mirror. The official FTDI PDF endpoint returned 403;
this mirror has not been asserted to be the latest revision.

## Why clock observation matters

The retained **Replica 1 Plus Users Manual, version 3.0 / June 2014**, page 9,
identifies the Propeller as the master 1 MHz clock source. Page 12 lists the
D40 package; page 19 distinguishes 5 V and 3.3 V power checks. The manual's
block diagram is not a pin-level schematic, and some legacy wording remains.
Manual SHA-256:
`fdd7c0e471d9ed2a8417dfbcefdb3987f29202d2cdf7405f5d653cad7d3cd79e`.
See the [retained manual register](../../preservation/manuals/2026-08-28/manuals-manifest.json).

The unchanged 110REV03 candidate confirms P15/CLK0 driving the 6502 in its
declaration and startup routine. It also deliberately fills the display during
startup. Thus restarting that candidate could disturb CPU clocking and produce
a startup display. This is a testable hypothesis; it does not identify the
installed EEPROM image or prove that the September screen was a reboot.
All nine files match their retained [vendor hashes](../../firmware/vendor/110REV03/provenance.json).

## Physical identification procedure for the next session

1. Obtain a sharp top-down board photo plus close-ups of U7, Q1/C9/R10, and
   both sides of the USB breakout/interconnect. Keep the board unpowered when
   repositioning it. Confirm the actual chip and module markings.
2. With all board power disconnected, use continuity to identify ground,
   U7 pin 11/RST, and whether any installed DTR connection reaches C9. Distinguish
   DTR from RTS. Inspect underside connections before accepting a four-wire
   count. Check the RESET-button net separately.
3. Establish whether the breakout exposes distinct board supply and UART-level
   supplies. Photograph the selector's current position. Trace first; do not
   experiment by moving it. Have Alex measure static rails at verified points
   during the attended power-on setup.
4. Select insulated grabber points that can be held without slipping between
   adjacent pins. Prefer an accessible verified net pad to a crowded IC lead.
   A missing secure point is a remaining physical dependency.
5. Record a new channel map. RESn is required for the proposed next capture;
   DTR is added only if its actual circuit is accessible and established.
   Consider PHI0 if a secure point is available.

The useful equipment is the existing analyzer, a continuity/DC-voltage
multimeter, and insulated IC grabbers. An oscilloscope is needed to resolve
short supply/ground disturbances; no new instrument purchase is assumed here.

## Analyzer capabilities and measurement limits

SparkFun specifies TOL-18627 at up to 24 MHz, 5.25 V maximum input, 2.0 V
minimum logic high, and 0.8 V maximum logic low. Its warning identifies the
CH6-adjacent apparent ground as unreliable on some units; the earlier session
used the CH7-side ground. Confirm actual ground before attachment.
[SparkFun product specifications](https://www.sparkfun.com/usb-logic-analyzer-24mhz-8-channel.html).

At 4 MS/s, samples are 250 ns apart. A flat trace cannot exclude every shorter
or sub-threshold disturbance. It cannot measure analog rail amplitude. Add
scope coverage if digital traces remain unexplained. At 12 MS/s, a 30-second
one-byte capture is approximately 360 MB before compression; verify streaming
capacity before including the 1 MHz clock in detailed timing analysis.

The old files use sigrok v2: INI metadata, one-byte samples, numbered logic
chunks. Only probe1/probe2 are enabled; remaining bits are not six extra observed
signals. The new analyzer reads chunks numerically and carries edge state across
boundaries. Reference: [sigrok v2 specification](https://sigrok.org/wiki/File_format:Sigrok/v2).

## Remaining uncertainty

No remotely examined source verifies the present solder connections, secure
probe point, rail voltages, selector wiring, or installed EEPROM image. The
schematic resolves what to inspect; it does not replace that inspection.
