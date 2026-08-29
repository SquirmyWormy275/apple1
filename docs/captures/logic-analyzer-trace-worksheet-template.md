# Logic-analyzer trace worksheet template

Copy this file into the timestamped capture directory created by the
[open-event test card](logic-analyzer-open-event-test-card.md). Complete it
from raw files and contemporaneous observations; leave an item `UNOBSERVED`
rather than filling a gap from memory.

## Identity and safety preflight

| Field | Recorded value |
|---|---|
| UTC date/time and operator | `UNFILLED` |
| Board revision and visible board identifier | `UNFILLED` |
| Board power source | `Pi USB host only / UNFILLED` |
| FT232R voltage-switch position | `UNFILLED` |
| USB by-id and by-path identity | `UNFILLED` |
| Analyzer make/model/firmware | `UNFILLED` |
| Analyzer input rating and probe type | `UNFILLED` |
| Analyzer power source | `UNFILLED` |
| Ground point and evidence it is ground | `UNFILLED` |
| Physical changes made for this card | `none / UNFILLED` |
| Known recovery action | `physical Reset; confirm stable monitor prompt / UNFILLED` |

## Channel evidence

| Channel | Logical name | Physical point | How the point was identified | Expected/verified domain | Safe to capture? |
|---:|---|---|---|---|---|
| GND | Board/USB ground | `UNFILLED` | `UNFILLED` | Reference | `YES / NO` |
| 0 | Propeller `RESn` | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 1 | FT232R TX-to-Propeller path | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 2 | FT232R DTR | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 3 | FT232R RTS | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 4 | Propeller P30, optional | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 5 | Propeller P31, optional | `UNFILLED` | `UNFILLED` | `UNVERIFIED` | `YES / NO` |
| 6 | 6821 CA1, deferred | `UNFILLED` | `UNFILLED` | `UNVERIFIED; may be 5 V` | `YES / NO` |
| 7 | 6821 CA2, deferred | `UNFILLED` | `UNFILLED` | `UNVERIFIED; may be 5 V` | `YES / NO` |

## Acquisition record

| Field | Passive idle capture | Controlled host-open capture |
|---|---|---|
| Native raw-file name and SHA-256 | `UNFILLED` | `UNFILLED` |
| Start/end UTC | `UNFILLED` | `UNFILLED` |
| Sample rate and retained pre-trigger duration | `UNFILLED` | `UNFILLED` |
| Trigger signal/edge | `UNFILLED` | `UNFILLED` |
| UART decoder settings, if used | `NOT USED / UNFILLED` | `NOT USED / UNFILLED` |
| Display-video file and timing method | `UNFILLED` | `UNFILLED` |
| Host owner JSONL file and SHA-256 | `not applicable` | `UNFILLED` |
| Board display before test | `UNFILLED` | `UNFILLED` |
| Board display after test | `UNFILLED` | `UNFILLED` |

## Controlled-open command record

Use this section only after the analyzer is armed, the known stable prompt is
visible, and the test-card preflight passed. It documents the no-transmit
action; it is not permission to run it early.

```bash
# On the Pi, from the copied repository. Do not add --transmit.
python3 tools/serial_owner.py session --capture \
  captures/YYYY-MM-DD-ft232r-open-analyzer/owner.jsonl
```

| Check | Result |
|---|---|
| Both recorded USB identities resolved to the same device | `PASS / STOP / UNFILLED` |
| No other process owned the serial device | `PASS / STOP / UNFILLED` |
| Owner requested DTR=false and RTS=false before opening | `PASS / STOP / UNFILLED` |
| No `--transmit` option was supplied | `PASS / STOP / UNFILLED` |
| Owner start/close times | `UNFILLED` |

## Time-correlated observations

| UTC / relative time | Source | Event | Raw-file location or frame | Observation only; no inference |
|---|---|---|---|---|
| `UNFILLED` | `analyzer/video/owner` | `UNFILLED` | `UNFILLED` | `UNFILLED` |
| `UNFILLED` | `analyzer/video/owner` | `UNFILLED` | `UNFILLED` | `UNFILLED` |
| `UNFILLED` | `analyzer/video/owner` | `UNFILLED` | `UNFILLED` | `UNFILLED` |

## Troubleshooting conclusion

**Symptom:** `UNFILLED`

**Hypothesis:** `UNFILLED`

**Test:** `Passive idle, then one no-transmit exclusive-owner open; channels: UNFILLED.`

**Result:** `UNFILLED`

**Conclusion:** `PASS / STOP / INCONCLUSIVE — UNFILLED`

**Permitted next step:** `UNFILLED`

**Recovery performed and result:** `UNFILLED`

## Evidence checklist

- [ ] Native, unmodified analyzer files retained.
- [ ] Display video retained.
- [ ] Owner JSONL retained for the controlled-open phase.
- [ ] Probe-point photos and identification evidence retained.
- [ ] Manifest validates with `python3 tools/capture_manifest.py metadata.json`.
- [ ] Raw capture, video, host log, and worksheet agree on ordering.
- [ ] No transmit, firmware, EEPROM, jumper, power-source, or wiring change occurred.
- [ ] Result is classified `PASS`, `STOP`, or `INCONCLUSIVE` and recovery is recorded.
