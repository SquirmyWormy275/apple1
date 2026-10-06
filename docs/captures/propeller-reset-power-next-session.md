# Prepared session: Propeller reset and power investigation

Status: PREPARATION COMPLETE / LIVE SESSION NOT EXECUTED.
Authority class: DERIVED DOCUMENTATION.
This card adds measurement coverage after the completed September 2 capture.
It does not change that packet's INCONCLUSIVE scientific result.
The [capture runner](../hardware/propeller-unattended-capture.md) implements this
initial attended cycle with the three required channels. A successful attended
checkout plus an observed stable display can qualify one subsequent unattended
cycle on the unchanged setup. No such qualification has been performed here.

## Question

Does the no-transmit FT232R open coincide with an observable Propeller RESn
transition? What additional analog measurements are needed to determine whether
the board's power or ground is disturbed?

## Topology to preserve for the first comparison

| Item | Intended connection |
|---|---|
| SparkFun TOL-18627 USB | strathex-P1 Omarchy laptop |
| Analyzer passive probes | Verified Replica signal points and ground |
| Replica FT232R USB | Existing Pi 5 USB host connection |
| Local Codex | Laptop; Pi coordination through verified existing SSH access |
| Board load | Record CFFA1/card and actual power arrangement; preserve baseline for this comparison |

The previous test's power arrangement was recorded but not independently
electrically verified. Check present wiring before power-on; do not introduce
a second supply. Do not silently relocate the Replica USB host to the laptop.

## Physical readiness

Alex's current board photographs and, where needed, power-off continuity
measurements must identify the chip package/orientation and accessible RESn
point. Record a specific point, voltage domain, and supporting evidence.
A package pin number alone does not verify a board test point.

The newly retrieved Briel Revision 0 drawing identifies **RST at U7 pin 11
and Q1 collector** as the Propeller reset net. Its **RESET** button net instead
resets the 6502/6821. It also shows DTR coupled through C9/Q1, whereas the old
session recorded only four connected conductors. Inspect the actual breakout's
top and underside and check routing before deciding whether DTR is connected.
See the [source and candidate-point guide](../hardware/propeller-reset-power-reference.md).

Resolve the power-selector discrepancy before the live comparison: the old
record says 3.3V, while generic manufacturer programming instructions say 5V.
Identify what the installed module actually switches and measure its rails;
the documentation difference alone is not a reason to move the selector.

Use secure insulated clips suitable for the point. Attach/reposition probes
with board power off. Ground goes first. The old session used analyzer ground
on the CH7 side: SparkFun warns against the GND position adjacent to CH6 on
some units. Verify ground rather than relying only on the connector's appearance.

A multimeter can establish continuity and static voltage. It cannot establish
the absence of a short supply transient. The logic analyzer likewise does not
measure supply amplitude. A scope measurement is the appropriate follow-on
for rail droop/ground disturbance; its grounding arrangement must also be
checked for this actual setup.

## Planned channels — not completed wiring instructions

| Channel | Logical target | Physical identification |
|---|---|---|
| GND | Board reference | Prior labelled USB INTERFACE GND; verify current setup |
| CH0 | FT232R TX-O | Prior labelled header point; verify current setup |
| CH1 | FT232R RX-I | Prior labelled header point; verify current setup |
| CH2 | Propeller RESn / RST | Candidate U7 pin 11 or Q1 collector net; actual access UNVERIFIED |
| Optional CH3 | Breakout DTR | Only if installed routing and secure access are verified |
| Optional CH4 | PHI0 / CPU clock | Candidate U7 P15, physical pin 20; actual access UNVERIFIED |

Do not attach a probe to an unverified IC leg. Do not treat the board RESET
button as proof that it is connected to Propeller RESn.

## Acquisition plan

Starting comparison settings: 4 MS/s, named channels, 12-second passive
baseline, then a separate 30-second continuous recording with at least
5 seconds before and after the event. Verify host throughput/sample counts.
At 4 MS/s the sample interval is 250 ns; a shorter disturbance may be missed.
If PHI0 timing is included, prefer a verified 12 MS/s acquisition (360 MB of
one-byte samples for 30 seconds before compression). Rehearsal does not establish
that either host can sustain this rate. Record any early stop as a partial trace.

Use streamed recording for the fx2lafw analyzer. An event-trigger assumption
must not eliminate pre-event samples. Record Pi and laptop clocks and their
uncertainty; owner log timestamps are not exact capture sample timestamps.

Record display state and recovery on an operator-controlled video. Retain
native files before making derived exports.

## Attended sequence

1. Local Codex reads this card, the current repository, and the September 2
   packet. Verify analyzer identity and existing Pi access. Read-only serial
   identity inspection is distinct from opening the port.
2. Establish and record the physical map with Alex. Capture readiness requires
   verified RESn coverage, correct ground, secure probes, and a stable display.
3. Save passive baseline. Unexplained behavior ends the sequence.
4. With Alex present and the measurement setup verified for the
   test, start fresh recording, retain pre-event coverage, then invoke the
   existing exclusive owner's no-transmit session once.
5. Save the raw trace and owner log. If the display changes or another stop
   condition occurs, Alex performs the known physical Reset recovery.
   No automatic repeat or transmit follows.
6. Write a new packet with observed facts, timing limits, native-file hashes,
   display evidence, physical-point evidence, and the actual outcome.

## Interpretation

| Observation | Supported conclusion and follow-on |
|---|---|
| RESn transition and display corruption | Measured association; inspect reset routing and power behavior before assigning a cause |
| No captured RESn transition and corruption | No observed external reset-net event within measurement limits; internal reset, short/sub-threshold events, and analog failures remain possible |
| UART and RESn digitally quiet | Digital channels do not explain the symptom; prepare scope coverage of relevant rails/ground |
| Stable open | This individual open remained stable; does not establish general repair or authorize transmission |
| Missing channel, bad mapping, lost samples, or unstable baseline | Incomplete measurement; preserve evidence and resolve that limitation |

## Preparation completion versus hardware completion

A source guide and successful software rehearsal mean PREPARATION COMPLETE.
They do not mean the board is repaired, firmware is qualified, or a live
experiment has run. Firmware changes and EEPROM programming are outside this
card.

References:
- [Completed preparation report](../hardware/propeller-overnight-report-2026-09-11.md)
- [Local Codex handoff](../hardware/propeller-codex-handoff.md)
- [Reset and power sources](../hardware/propeller-reset-power-reference.md)
- [Completed worksheet](2026-09-02-ft232r-open-analyzer/worksheet.md)
- [Serial protocol](../serial-test-protocol.md)
- [Overnight work order](../plans/2026-09-11-propeller-overnight-preparation.md)
- [SparkFun analyzer specifications and ground warning](https://www.sparkfun.com/usb-logic-analyzer-24mhz-8-channel.html)
- [sigrok-cli reference](https://sigrok.org/wiki/Sigrok-cli)
