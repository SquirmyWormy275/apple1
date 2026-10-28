# Prepare the physical Replica chapter

Use this chapter to connect the software model to the documented hardware and
to plan a measured session when the physical setup is available. The current
book includes no newly completed physical Replica run. The enclosure/setup is
still being prepared, and the recorded serial-open fault has not been closed.

## Identify the layers you will observe

| Layer | Useful observation | What it can tell you |
|---|---|---|
| 6502 and memory | Identified ROM/RAM map, documented program and readback | Whether the intended bytes and state are present |
| Keyboard/display interface | A known key, register convention and visible character | Whether that particular input/output path behaves as expected |
| Propeller implementation | Identified source candidate versus measured installed image | Which behavior is documented and which firmware identity is established |
| FT232R/USB serial | Device identity, open event, control-line capture, received/transmitted bytes | Which transport event coincides with a disturbance |
| Pi application | Provider request, proposal, verifier result and run record | What the modern host did; this alone says nothing about the physical transport |

Read the [SP01 board atlas](../../field-library/SP01-two-boards-one-computer/README.md)
with [chapter 1](../chapters/01-the-machine.md). The original Apple-1,
Replica I/TE and Replica 1 Plus have related interfaces but different physical
implementations. A source archive with a plausible filename does not identify
this unit's installed EEPROM.

## Rehearse the whole program first

Run M03, A05 and T11 on the host. Predict input bytes, stored bytes, emitted
characters, both exit paths and the expected memory range. Keep the exact
program hash and its independent host result. This supplies an expectation for
a future comparison; it does not measure the board.

An eventual physical session should answer one question at a time. A video of
text appearing can establish a visible result. A byte log can establish a
recorded transport exchange. A control-line trace can help distinguish an open
side effect from a transmitted payload. Pair the observations rather than
asking one photograph to prove every layer.

## Use the existing fault record to choose the next question

On August 27, a host open with no payload disturbed the display. The
[September 2 instrumented packet](../../captures/2026-09-02-ft232r-open-analyzer/README.md)
retains a later observation: TX/RX stayed high in the sampled interval, while
reset and analog rails were not measured. This narrows that observation; it
does not establish which unmeasured line or rail caused the disturbance.

The next session therefore begins with the
[open-event test card](../../captures/logic-analyzer-open-event-test-card.md),
not a faster text-transfer experiment. Use its verified board points and
measurement requirements. This book supplies no guessed wiring or pinout.

## Prepare a reviewable capture card

Record the board/revision, installed-image evidence if available, power source,
USB topology, by-id **and** by-path identities, software revision, time basis,
video and instrument settings, the exact intended event and the stop/recovery
procedure. State which lines and rails remain unobserved. Use the existing
[capture metadata template](../../captures/README.md) and
[serial characterization protocol](../../serial-test-protocol.md).

The first software discovery operation is the existing read-only probe:

```bash
python3 tools/serial_owner.py probe
```

It resolves identities without importing a serial driver or opening the port.
An absent or changed identity is a result to record, not a reason to guess a
`/dev/ttyUSB` number. A session/open is a distinct measured operation. Follow
the test card after the physical measurement setup is ready.

Only after a repeatable, non-disturbing open does the protocol introduce its
initial paced `TEST` plus CR payload. Later program entry and readback need
their own acceptance record. The vendor manual's generic 9600 8N1 setup is a
reference; its generic pacing example does not override this unit's measured
failure and the project's slower characterization sequence.

## What completes the missing physical illustration

A publishable record should include the exact question, setup photograph,
identified program or payload, raw serial log where applicable, video/trace
files, timestamp relationship, expected versus actual result and interpretation.
A failure belongs in the chapter too. A visible reset, mismatch or unexpected
output ends that trial; preserve the observation before proposing a change.

Keep firmware changes, EEPROM writes, CFFA1 writes and wiring changes as
separate operations with preserved originals and their own reviewable plans.
They are not prerequisites for learning from the host book, and none is needed
merely to produce a successful-looking capture.

[Textbook home](../README.md) · [Current investigation](../../troubleshooting.md) · [Review record](../review.md)


## Ready for the arrival

The [build storyboard kit](../../hardware/build-storyboard/README.md) has stable
shot IDs, empty credited-asset slots, a caption template and unmeasured
as-built fields. The [card guide](../../../cf-card/README.md) and
[BASIC chapter](basic.md) now supply host-rehearsed counterparts for later
physical reader and interpreter trials. Add genuine physical evidence beside
those captures when the finished setup arrives.

For the installed October 28 edition, the
[next-agent handoff](../../../cf-card/HARDWARE-HANDOFF.md) lists the exact local
reader/BASIC trials, evidence to retain and documentation closeout. Keep that
acceptance separate from the instrumented serial-fault investigation above.
