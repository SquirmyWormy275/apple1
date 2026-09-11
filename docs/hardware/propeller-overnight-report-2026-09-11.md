# Propeller preparation completed — 2026-09-11

**Preparation complete; hardware root cause remains inconclusive.** Executed
immediately at Alex's request. The previously scheduled duplicate was disabled.
No laptop/Pi connection, live serial session, or hardware change occurred.
Authority: DERIVED DOCUMENTATION, with separately labelled synthetic fixtures.

Repository: [Apple1 PR #6](https://github.com/SquirmyWormy275/apple1/pull/6).
Evidence baseline: `2c40f1c5c63a083184eb724df4500cd1427bd3d2`.
Preparation work order: `f4f257acaf14d03c10a15a506e015978e4f5261d`.
Completed implementation and validated helpers:
`8fb55d19a5a88d967e2abf9aa0de387c96afea42`.
The following documentation commit records that exact execution revision.

## Completed work

- Re-read both native September 2 sigrok captures with a new file-only analyzer.
  Verified the original packet's nine manifest hashes and both existing packet
  validators. Raw evidence and candidate firmware are unchanged.
- Retrieved and visually inspected Briel's Revision 0 schematic and Parallax's
  D40 pinout; reconciled them with the retained manual, candidate source,
  ReActiveMicro guidance, and FTDI/SparkFun specifications in the
  [reset and power reference](propeller-reset-power-reference.md).
- Implemented and executed all six fake-transport scenarios using the existing
  SerialOwner class. Added parser and rehearsal regression tests.
- Completed the [next-session card](../captures/propeller-reset-power-next-session.md)
  and [local Codex handoff](propeller-codex-handoff.md).

## Saved-capture results

Both enabled channels were high for every saved sample, at 4 MS/s:

| File | Samples | Duration | Data chunks | CH0 transitions | CH1 transitions |
|---|---:|---:|---:|---:|---:|
| passive-idle.sr | 48,000,000 | 12 s | 1,187 | 0 | 0 |
| host-open-no-transmit.sr | 120,000,000 | 30 s | 2,967 | 0 | 0 |

Embedded metadata enables D0/D1 only; the worksheet identifies these as FT232R
TX-O/RX-I. The owner log contains opened, empty startup drain, and closed,
with no transmit event. Logged session duration is 0.202514 seconds, with
DTR=false and RTS=false requested. This agrees with the previous result.

This does not establish that RESn, rails, or ground were stable. Those signals
were not measured. Contiguous saved chunks do not prove absence of upstream
sample loss, and host timestamps do not supply an exact shared timebase.
The two externally retained videos were not available for byte-level inspection.
See the [derived counts, hashes, and limits](../captures/2026-09-11-propeller-offline-analysis.json).

## What the research unblocks

The original Briel drawing has **separate RST and RESET nets**. RST reaches
Propeller U7 pin 11 and Q1 collector; RESET reaches the 6502/6821. The drawing
also depicts **DTR -> C9 -> Q1 -> Propeller RST**. That is a concrete path to
inspect against the September observation of a four-conductor connection.
It is not proof that the installed breakout routes DTR.

The recorded 3.3V switch position also differs from ReActiveMicro's 5V
programming guidance. Identify the installed module's supply/VCCIO connections
and measure the rails before deciding whether any setting is wrong. Generic
documentation is insufficient to justify changing it.

The manual, drawing, and unchanged candidate source identify the Propeller as
the CPU clock source. A verified PHI0 point can therefore add useful coverage.
Candidate startup display behavior is a hypothesis to compare, not evidence
that the installed firmware rebooted. Source revisions, hashes, applicability,
and the unresolved physical differences are in the linked reference.

## Rehearsal results

| Synthetic scenario | Owner opens | Result |
|---|---:|---|
| Stable | 1 | Completed, saved baseline/event/log |
| Missing RESn coverage | 0 | Stopped before owner |
| Unstable idle | 0 | Detected baseline edge and stopped |
| Capture not ready | 0 | Stopped before owner |
| Capture failure | 1 | Stopped, retained partial trace and log |
| Reset during open | 1 | Stopped, retained trace, flagged operator recovery |

Every scenario used zero real device opens, zero transmit calls, and zero
retries. Owner invocations occurred after five simulated seconds of pre-event
coverage. Simulated duration was bounded to 42 seconds including baseline.
The 1 kHz fixtures test sequencing and output preservation; they do not validate
USB streaming, SSH coordination, or a physical reset detector. Detailed events
and executed helper hashes are in the
[rehearsal summary](../captures/2026-09-11-propeller-rehearsal-summary.json).

## Reproduction and validation

Use the repository's Python 3.12 environment with its dev dependencies installed.
From the repository root:

```bash
python -m tools.sigrok_summary docs/captures/2026-09-02-ft232r-open-analyzer/passive-idle.sr --expected-samples 48000000
python -m tools.sigrok_summary docs/captures/2026-09-02-ft232r-open-analyzer/host-open-no-transmit.sr --expected-samples 120000000
python -m tools.propeller_rehearsal --out out/propeller-new-rehearsal
python -m pytest -q
```

Use a fresh rehearsal output directory; existing files are never overwritten.
The parser supports this packet's sigrok v2, one-device, one-byte digital layout,
up to eight probes and 512 MiB uncompressed; unsupported layouts fail explicitly.
Tests compare counts to an independent bitwise oracle and cover numeric chunk
ordering, archive/read-boundary edges, disabled bits, invalid metadata, early
stops, preserved outputs, and accidental live-backend construction.

Final local validation: **146 tests passed** in 1.26 seconds; Ruff passed for
the configured repository scope and all four new Python files; mypy passed for
35 source files; repository validation returned no errors; the deterministic
demo reported `serial_opened=false`. `git diff --check` passed. The initial
full-suite run caught links to this then-unwritten report; after completing it,
the full suite and link validation passed. No failure was waived.

## Remaining physical dependency and first local action

Alex needs current board/breakout photos, a continuity/DC-voltage meter, and
secure insulated grabbers to verify a Propeller RST point and the power/DTR
routing. A scope is the follow-on for short analog rail/ground disturbances.
The cloud session has no access to strathex-P1 or its USB devices.

**First local Codex action:** fetch PR #6 in the P1's existing checkout while
preserving local work, then execute the host-readiness steps in the
[handoff](propeller-codex-handoff.md). That work can finish before wiring. Keep
analyzer USB on P1 and Replica USB on the Pi for the initial comparison; the
new attended capture adds verified RESn coverage to the previous UART channels.
