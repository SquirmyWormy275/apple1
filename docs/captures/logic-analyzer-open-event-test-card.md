# Logic-analyzer test card: FT232R open with no transmit

## Purpose and boundary

This card records the electrical effect of **one** ordinary host serial open
on the Replica 1 Plus. It is a board-path characterization test, not a repair
attempt. Its only target is the confirmed symptom: an FT232R open with no
transmitted payload made the display garbled and required physical Reset.

The permitted sequence is passive capture at idle followed by one controlled
host open. Do not transmit bytes, change firmware, compile/load firmware,
program EEPROM, move jumpers, alter the FT232R voltage switch, or attach a
CA2-to-Propeller wire. Do not repeat the host open after a STOP result.

**Status:** prepared; not yet authorized/executed.

## Decision forks

| Gate | PASS / advance | STOP / retain evidence |
|---|---|---|
| Probe suitability | Analyzer inputs, probe ground, and voltage rating are known compatible with each selected net. | Analyzer model/rating, target point, voltage domain, or ground reference is uncertain. |
| Passive idle | Stable monitor prompt/cursor and no unexplained transition during the idle capture. | Video changes, reset activity, or unexpected bus traffic occurs before any open. |
| Controlled open | Evidence records the event and the machine remains stable. No transmit testing follows in this card. | Display changes, reset is observed/suspected, identity changes, capture is incomplete, or any result is non-repeatable. Recover with physical Reset and do not repeat the open. |

## Instrument setup: before any probe touches the board

1. Photograph the machine from above, the FT232R breakout, cable path, and
   proposed probe points. Record board revision, FT232R voltage-switch
   position, board power source, analyzer model, input rating, probe type, and
   analyzer power source.
2. Confirm that the analyzer is appropriate for the selected logic-voltage
   domains. CA1/CA2 may be 5 V; Propeller GPIO is 3.3 V. An input that cannot
   safely accept the measured/expected level is a STOP, not a reason to add a
   divider or temporary wire.
3. With board power **off**, identify each probe point from a visible label,
   continuity evidence, or an approved schematic. Record the physical location
   and its evidence. A logical signal name alone is not enough.
4. Attach the analyzer ground first to a confirmed board/USB ground point.
   Then attach only high-impedance passive inputs. Do not probe unknown pads,
   IC pins by guesswork, power rails as logic inputs, or any unverified 5 V
   signal with a 3.3 V-only analyzer.
5. Power the established Pi-to-FT232R path only. Never add a wall adapter or
   another 5 V source while the Pi USB host is connected.

## Channel plan

The physical point for every channel is deliberately blank until it is
identified on this specific Revision 0 board. A missing channel does not
authorize guessing; record it as unavailable.

| Priority | Logical signal | Voltage domain / state | Why capture it | Physical probe point and evidence |
|---:|---|---|---|---|
| Required | Board/USB ground | Reference | Common reference for all channels | `UNFILLED` |
| Required | Propeller `RESn` | Unverified; expected 3.3 V logic | Distinguishes a reset event from a firmware-only symptom. | `UNFILLED` |
| Required | FT232R TX-to-Propeller path | Unverified; do not infer direction from a label | Shows whether the UART data path changes when the port opens. | `UNFILLED` |
| Required when accessible | FT232R DTR | FT232R control output; level/routing unverified | Tests the reset-on-open control-line hypothesis. | `UNFILLED` |
| Required when accessible | FT232R RTS | FT232R control output; level/routing unverified | Tests the reset-on-open control-line hypothesis. | `UNFILLED` |
| Optional | Propeller P30 | Candidate-source property only | Correlates board serial output with the host-facing path. | `UNFILLED` |
| Optional | Propeller P31 | Candidate-source property only | Correlates board serial input with the host-facing path. | `UNFILLED` |
| Deferred | 6821 CA1 | Likely 5 V; exact mode unverified | Useful only after safe point identification. | `UNFILLED` |
| Deferred | 6821 CA2 | May be 5 V; exact mode unverified | Useful only after safe point identification; no direct connection to Propeller. | `UNFILLED` |

Capture at least `RESn` plus every safely identified FT232R control/path signal
before drawing a causal conclusion. If `RESn` cannot be safely captured, the
run can document correlation but cannot rule in or rule out a reset.

## Acquisition settings

- Set the capture length to include at least 5 seconds of idle pre-trigger and
  5 seconds after the host-open event. Use a longer window if the instrument
  permits it without reducing the selected channels below its usable sample
  rate.
- Select a sample rate at least 10 times the fastest signal transition that
  must be interpreted. For UART decode at 9600 baud, preserve the raw digital
  capture and use a rate high enough to show individual bit cells; do not rely
  only on decoded text.
- Use a falling-edge trigger on `RESn` when that net is safely identified.
  If it is unavailable, use a state/edge trigger on the safely identified DTR
  or RTS channel and retain the full raw pre-trigger buffer.
- Configure UART decoding only after recording the actual physical direction,
  polarity, and voltage-domain evidence. The known host configuration is 9600
  baud, 8 data bits, no parity, 1 stop bit, no flow control; this does **not**
  prove the board-side pin mapping or polarity.
- Synchronize a phone/video camera on the display with the operator narration:
  `idle`, `capture armed`, `owner invoked`, `display changed or stable`, and
  `physical Reset if needed`. A visible stopwatch or a spoken UTC timestamp is
  enough; exact frame sync is not claimed unless established.

## Execution sequence

### A. Passive baseline — no serial open

1. Establish the known stable monitor prompt and flashing cursor. Record the
   physical Reset recovery plan before continuing.
2. Start display video and arm the analyzer. Capture at least 10 seconds while
   no process opens `/dev/ttyUSB0`.
3. Stop and save the raw capture. If the display or selected signals are
   unstable, classify the card `STOP`; do not continue to B.

### B. One controlled open — no transmit

1. Re-establish the stable prompt if necessary. Verify the same recorded
   `/dev/serial/by-id/` and `/dev/serial/by-path/` identities. Confirm that no
   terminal emulator, `cat`, `echo`, IDE, getty, or other process owns the
   device.
2. Arm a fresh analyzer capture and start display video. Note the UTC time.
3. Run the existing exclusive owner’s approved **open-with-no-transmit**
   action once. It must request DTR and RTS low before opening, use 9600 8N1
   with flow control disabled, settle/drain only, and close. Do not substitute
   a shell redirect or terminal emulator.
4. Save raw analyzer data before decoding or interpreting it. If the display
   is garbled or a reset/suspected reset occurs, use the prepared physical
   Reset recovery action, record the recovery result, and stop.

## Required evidence packet

Create a new timestamped directory under `docs/captures/` containing:

```text
YYYY-MM-DD-ft232r-open-analyzer/
  metadata.json
  passive-idle.<instrument-extension>
  host-open-no-transmit.<instrument-extension>
  host-open-no-transmit.csv              # export only if native raw file is retained
  display-video.<extension>
  owner.jsonl
  worksheet.md
  photos/
```

`metadata.json` must pass `tools/capture_manifest.py` and additionally record
the analyzer model, input rating, probe type, channels, physical-point
evidence, sample rate, trigger, board power source, FT232R switch state,
operator, tool/owner version, and `physical_changes: none`.

Copy the [trace worksheet template](logic-analyzer-trace-worksheet-template.md)
into that directory before arming the analyzer.

The worksheet must keep this troubleshooting chain intact:

```text
Symptom -> Hypothesis -> Test -> Result -> Conclusion
```

## Interpretation rules

| Observation | Permitted conclusion |
|---|---|
| `RESn` transitions during host open, with display corruption | The open is correlated with a measured reset-path event; trace routing/polarity before any firmware work. |
| DTR/RTS changes but `RESn` is stable, with display corruption | Control-line change is correlated but not proven causal; inspect the traced board path and retain raw capture. |
| No captured control/reset transition, with display corruption | The selected channels do not explain the symptom. Do not infer a firmware cause; expand safe measurement coverage. |
| Machine remains stable through the one open | Record PASS for this card only; transmission/pacing needs a separate approved card. |
| Analyzer, target point, voltage, identity, or video evidence is incomplete | INCONCLUSIVE or STOP; no follow-on serial test. |

## Completion condition

This test card is complete only when raw traces, display evidence, host owner
log, probe-point evidence, and recovery outcome coexist in one capture packet.
It never authorizes firmware loading, EEPROM programming, soldering, a 100 kOhm
pull-up, or a CA2 connection.
