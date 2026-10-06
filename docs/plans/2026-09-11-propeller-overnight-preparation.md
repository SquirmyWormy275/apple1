# Propeller preparation — executed 2026-09-11

Status: PREPARATION COMPLETE. The user directed execution immediately; the
scheduled duplicate was disabled. No live experiment has been executed.
Authority class: DERIVED DOCUMENTATION.
Repository: SquirmyWormy275/apple1.
Starting main commit: 2c40f1c5c63a083184eb724df4500cd1427bd3d2.

Completed deliverables and validation are in the
[execution report](../hardware/propeller-overnight-report-2026-09-11.md).
The work order below is retained to show scope. References to overnight/morning
describe its original scheduling, not deferred or still-running work.

## Objective

Prepare the next attended diagnostic session so Alex only needs to identify and
attach the verified probes, observe the display, and perform physical recovery.
Complete all useful source research, saved-file analysis, and software rehearsal
without needing the Replica, Raspberry Pi, analyzer, or laptop online.

The immediate question is whether an FT232R open coincides with a Propeller
reset-net event or analog power/ground disturbance. An overnight preparation
result must not claim that it repaired the machine or established root cause.

## Read first

Read current versions and relevant changes before implementation:

- [Completed September 2 worksheet](../captures/2026-09-02-ft232r-open-analyzer/worksheet.md)
- [Capture metadata](../captures/2026-09-02-ft232r-open-analyzer/metadata.json)
- [Probe-point record](../captures/2026-09-02-ft232r-open-analyzer/probe-point-record.md)
- [Troubleshooting record](../troubleshooting.md)
- [Serial protocol](../serial-test-protocol.md)
- [Original test card](../captures/logic-analyzer-open-event-test-card.md)
- [Recovery ledger](../recovery-evidence-ledger.md)
- [Candidate firmware baseline](../firmware-baseline.md)
- [Firmware static audit](../firmware-static-audit.md)
- [Repository architecture](../repository/architecture.md)

Inspect tools/serial_owner.py, tools/trace_packet.py, tools/capture_manifest.py,
tools/firmware_static_audit.py, tools/propeller_preflight.py, their existing tests,
and pyproject.toml. Reuse these facilities where appropriate.

## Established starting point

| Item | Evidence |
|---|---|
| Analyzer | SparkFun TOL-18627, USB 0925:3881, fx2lafw; sigrok-cli previously worked on the Omarchy laptop strathex-P1 |
| Previous topology | Analyzer USB on P1 laptop; Replica FT232R connected to Pi 5 USB host; CFFA1 and Lexar 128 MB card installed |
| Previous channels | CH0 FT232R TX-O; CH1 FT232R RX-I; board ground at labelled USB INTERFACE GND |
| Baseline | Both channels high throughout 12 seconds at 4 MS/s |
| Open capture | Both channels high throughout 30 seconds at 4 MS/s: 120,000,000 samples, no recorded transitions |
| Serial action | One 202.5 ms open/drain/close; requested DTR=false and RTS=false; no transmit event; empty startup drain |
| Display | Corruption reproduced; physical Reset restored a live cursor; stale garbage remained |
| DTR/RTS | September 2 recorded an unrouted four-conductor connection; the newly retrieved drawing depicts DTR/C9/Q1, requiring physical reconciliation |
| Missing measurement | Propeller RESn; analog 3.3 V/5 V supply and ground behavior |
| Physical access gap | No verified RESn point, no multimeter, and no IC grabbers were available during that session |
| Board identity | replica I plus; revision not independently verified from board markings |
| Media | Two videos externally held and hash-identified; do not claim to inspect unavailable bytes |

Do not substitute older, unexecuted test-card assumptions for the completed
September 2 record. The name P1 in the workstation topology means the laptop;
the Propeller P1 chip is a separate component.

## Overnight deliverables

### 1. Independent analysis of the existing files

Verify packet hashes and existing validators. Read the native .sr archives and
their embedded metadata before choosing a parser. Confirm channel packing,
enabled-channel mapping, sample rate, number of samples, duration, initial/final
states, per-channel high/low counts, and transition counts. Count transitions at
chunk boundaries as well as within chunks. Preserve raw files byte-for-byte.

Retain a reproducible command and a compact derived report outside the completed
capture packet. Do not infer no reset or healthy supply rails from UART traces.
Respect the coarse timing correlation between the P1 capture and Pi owner log.
Do not manufacture exact timestamp alignment.

If a new offline helper is necessary, restrict it to explicitly supplied regular
files. It must not scan devices, open serial ports, invoke an uploader, or have
a live-capture mode. Test constant levels, transitions crossing data chunks,
disabled channel bits, and corrupt/inconsistent metadata. A fixture is synthetic
evidence, clearly separated from the September capture.

### 2. Primary-source reset and power reference

Consult manufacturer material from Parallax, Briel/ReActiveMicro, FTDI, and
SparkFun. Start with retained manuals and provenance in the repository, then
verify current primary-source URLs. Record exact document title/revision, relevant
page/section, supported claim, board applicability, and unresolved differences.
Do not redistribute third-party diagrams unless rights permit it.

Distinguish:
- Propeller RESn from the 6502 reset net, board RESET button, and CLEAR input;
- chip package pinout from a verified accessible point on Alex's board;
- candidate 110REV03 source behavior from the installed EEPROM image;
- FT232R switch setting from an actually measured voltage;
- an external reset-net transition from an internal reset or analog failure.

Check whether the candidate Propeller clock output affects the 6502 clock.
Treat any connection to the observed corruption as a hypothesis until measured.

Produce a source-backed probe-location guide. Any location requiring a current
board photograph or power-off continuity check remains explicitly UNVERIFIED.
Never invent a completed physical pin map.

### 3. Next-session card and software rehearsal

Refine the [prepared session card](../captures/propeller-reset-power-next-session.md).
Use continuous streamed capture with pre-event coverage for this analyzer;
do not promise a hardware trigger or onboard pre-trigger memory.

Build/reuse a file-only or fake-transport rehearsal for:
capture readiness, timestamp logging, one simulated owner action, bounded
completion, missing/reset-channel detection, capture failure, and output
preservation. Rehearsal must never resolve a real device by accident.
Any stop must end the simulated sequence, without an automatic retry.

Generate a human-reviewed live plan only; no overnight command may execute it.
Keep the existing serial-owner CLI intact. A missing RESn point is a physical
dependency, not something software should silently waive.

### 4. Morning report and repository handoff

Create docs/hardware/propeller-overnight-report-2026-09-11.md with:
- work actually completed and exact commit;
- original evidence versus new derived results;
- test commands/results and any retrieval/runtime limitations;
- verified source findings and still-unverified physical points;
- exactly what Alex needs to supply next;
- one first-action instruction for local Codex on strathex-P1.

Keep the report concise and link detailed evidence. If no accessible reset point
can be verified remotely, finish the other deliverables and name that remaining
dependency. Do not turn it into a request to rerun the old two-channel test.

## Execution and persistence

Re-read the work branch and main head. Preserve local changes and use an isolated
checkout/worktree where needed. Commit only this task's documents, helpers,
meaningful tests, and small derived reports to the existing preparation branch
and draft PR. Do not merge automatically or rewrite prior evidence.

If shell network access cannot clone the public repository, use the connected
GitHub file/blob APIs. For binary captures, request base64 and decode locally;
never mistake an API response or Git LFS pointer for capture bytes. If bytes
remain inaccessible, state that independent raw reanalysis was not completed
and continue the research and document preparation.

Checkpoint completed work before a runtime limit. Do not pad the job to occupy
the night or repeatedly rerun successful tests.

## Overnight execution boundary

This job is off-device. The Replica can remain powered off. No serial open,
serial transmit, programming, EEPROM access, GPIO, wiring/power change, service
reconfiguration, or camera operation is part of this overnight job. Access to
GitHub or this scheduled job does not grant access to Alex's P1 or Pi.
