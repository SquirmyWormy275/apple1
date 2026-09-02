# Logic-analyzer trace worksheet

Capture: `docs/captures/2026-09-02-ft232r-open-analyzer/`

## Identity and safety preflight

| Field | Recorded value |
|---|---|
| UTC date/time and operator | 2026-09-02, approximately 01:48Z through 03:20Z. Operator: Alex Kaper. |
| Board revision and visible board identifier | Silkscreen `replica I plus`, `www.brielcomputers.com`, `Distributed By: ReActiveMicro.com`. No revision marking observed. Revision `UNVERIFIED`. |
| Board power source | `UNVERIFIED`. Single micro-USB from a Pi 5 USB-A host port supplying 5 V and enumerating the FT232R. Board ON/OFF switch set to ON. No second supply. Sole-supply status not independently verified. |
| FT232R voltage-switch position | `3.3V`, read from the breakout by the operator. Not moved. |
| USB by-id and by-path identity | by-id `usb-FTDI_FT232R_USB_UART_00000000-if00-port0`; by-path `platform-xhci-hcd.0-usbv2-0:2:1.0-port0`. Both resolved to `/dev/ttyUSB0`. A third path, the `usb-` variant, also resolves to the same node. |
| Analyzer make/model/firmware | SparkFun TOL-18627. `fx2lafw` 0.1.7-1 uploaded to device RAM. USB `0925:3881`. |
| Analyzer input rating and probe type | 5.25 V max, 2.0 V min Vih, vendor-published for this part number, not measured on this unit. Female-to-female jumper leads; no clips or grabbers. |
| Analyzer power source | USB from the Omarchy laptop. No analyzer power or reference output lead touched the Replica. |
| Ground point and evidence it is ground | `GND` pin on the four-pin `USB INTERFACE` header, silkscreen-labelled. Analyzer-side GND taken from the CH7-side position, avoiding the CH6-adjacent position that SparkFun cautions may not be ground on some units. No continuity verification: no multimeter available. |
| Physical changes made for this card | `none` |
| Known recovery action | Physical Reset; do not press CLEAR; do not repeat the open. |

## Channel evidence

| Channel | Logical name | Physical point | How the point was identified | Expected/verified domain | Safe to capture? |
|---:|---|---|---|---|---|
| GND | Board/USB ground | `GND` pin, four-pin `USB INTERFACE` header | Silkscreen label | Reference | `YES` |
| 0 | FT232R `TX-O` | `TX-O` pin, same header | Silkscreen label | 3.3 V, switch-position derived, not measured | `YES` |
| 1 | FT232R `RX-I` | `RX-I` pin, same header | Silkscreen label | 3.3 V, switch-position derived, not measured | `YES` |
| n/a | Propeller `RESn` | Not identified | No labelled point, no applicable schematic, no multimeter for continuity | `UNVERIFIED` | Not attempted |
| n/a | FT232R `DTR` | Not routed to the board | Breakout pad unpopulated; only four pins connect the breakout to the mainboard | n/a | Unreachable |
| n/a | FT232R `RTS` | Not routed to the board | As above | n/a | Unreachable |
| n/a | Propeller P30/P31 | Not identified | Optional; not pursued | `UNVERIFIED` | Not attempted |
| n/a | 6821 CA1/CA2 | Deferred by test card | May be 5 V; points and domains not independently established | `UNVERIFIED` | Not attempted |

Note: pin 1 of the four-pin header, labelled `3.3V`, is a supply rail and was deliberately left unprobed. Confirmed bare by the operator before power-on.

## Acquisition record

| Field | Passive idle capture | Controlled host-open capture |
|---|---|---|
| Native raw-file name and SHA-256 | `passive-idle.sr`, `72ed1c99ed43bf9cea7a55c0cf6cc3e6edc9a29b2d8751dadb61601b8e7b9a24` | `host-open-no-transmit.sr`, `96de5b49b387a53b87dbe9bacd471e6c11e2989a008f517db40b43cf736e9770` |
| Start/end UTC | 03:07:11Z to 03:07:23Z | approximately 03:15:57Z to 03:16:27Z |
| Sample rate and retained pre-trigger duration | 4 MS/s, 48,000,000 samples, 12 s. No trigger. | 4 MS/s, 120,000,000 samples, 30 s. Approximately 8 to 10 s before the open, approximately 20 s after. |
| Trigger signal/edge | `NONE`; continuous host-streamed capture, no hardware trigger on this analyzer class | `NONE`; same. Correlation by owner JSONL timestamp. |
| UART decoder settings, if used | `NOT USED` | `NOT USED` |
| Display evidence and timing method | Eyoyo LCD observed stable; external media custody is documented in `display-video-record.md`. | `IMG_1353.mov` and `IMG_1354.mov`, externally held and hash-identified in `external-media-manifest.json`. Preceding assistant session reported direct frame inspection. Codex did not inspect the MOV bytes. Frame-exact synchronization is not claimed. |
| Host owner JSONL file and SHA-256 | `not applicable` | `owner.jsonl`, `97e65d983facd8a9af0f9389c5769ac24b1a8dde0d656f929eba8033b88c5e09` |
| Board display before test | Stable Woz Monitor prompt, flashing `@` | Stable Woz Monitor prompt, flashing `@` |
| Board display after test | Unchanged, stable throughout | Garbage. After physical Reset: live flashing cursor with the pre-existing garbage still on screen, since Reset does not clear the video buffer. |

## Controlled-open command record

Run from `~/apple1-serial-recovery` on the Pi:

```bash
.venv/bin/python tools/serial_owner.py session \
  --capture captures/2026-09-02-ft232r-open-analyzer/owner.jsonl
```

| Check | Result |
|---|---|
| Both recorded USB identities resolved to the same device | `PASS` |
| No other process owned the serial device | `PASS` (`fuser` exit 1; `/proc` fd scan found nothing; `lsof` not installed on the Pi) |
| Owner requested DTR=false and RTS=false before opening | `PASS` (recorded in the `opened` event) |
| No `--transmit` option was supplied | `PASS` (no `transmit` event in the log) |
| Owner start/close times | opened 03:16:05.950187Z; startup_drained 03:16:06.150539Z, `payload_hex` empty; closed 03:16:06.152701Z. Total 202.5 ms. |

## Time-correlated observations

| UTC / relative time | Source | Event | Raw-file location or frame | Observation only; no inference |
|---|---|---|---|---|
| 03:07:11Z to 03:07:23Z | analyzer | Passive baseline | `passive-idle.sr` | D0 and D1 constant high for the full 12 s. No transitions. |
| ~03:15:57Z | analyzer | Capture armed | `host-open-no-transmit.sr`, sample 0 | Board at stable prompt. |
| 03:16:05.950187Z | owner | `opened` | offset approximately 8 to 10 s into the trace | DTR and RTS requested false. |
| 03:16:06.150539Z | owner | `startup_drained` | as above | Zero bytes received, `payload_hex` empty. |
| 03:16:06.152701Z | owner | `closed` | as above | Session ended normally. |
| during the session | video / operator | Display corrupted | externally held phone recording; see `display-video-record.md` | Eyoyo LCD became dense pseudo-random ASCII; no clean Monitor prompt was visible in the inspected clips. |
| ~03:16:27Z | analyzer | Capture ended | sample 120,000,000 | 30.000 s captured, no dropped samples. |
| across all samples | analyzer | No edges | whole file | D0 and D1 each constant high across all 120,000,000 samples. Zero transitions on either channel. |
| after capture end | operator | Physical Reset | phone recording | Processor restarted, cursor live, pre-existing garbage still displayed. |

## Troubleshooting conclusion

**Symptom:** An ordinary FT232R host open with no transmitted payload garbles the Replica display and requires physical Reset.

**Hypothesis:** A host-open control-line transition reaches or correlates with the Propeller reset path; secondarily, the open creates unexpected activity on the FT232R-to-Propeller UART path.

**Test:** Passive idle, then one no-transmit exclusive-owner open, with channels: GND reference, CH0 on FT232R `TX-O`, CH1 on FT232R `RX-I`. `RESn` not captured.

**Result:** `INCONCLUSIVE`

**Conclusion:** The disturbance reproduced during one controlled open with DTR and RTS requested false, no transmitted payload, and no received startup bytes. Across the full 30-second capture, `TX-O` and `RX-I` remained digitally high with zero threshold crossings. DTR and RTS are not routed through the installed four-conductor breakout-to-board interconnect. A UART-data-transition mechanism and a wired DTR/RTS-control mechanism are therefore not supported. Unobserved `RESn`, analog rail or ground disturbance, regulator/FT232R power behavior, sub-threshold transients, and shared-load interaction involving CFFA1 remain unresolved. The execution is `COMPLETE`, the scientific result is `INCONCLUSIVE`, and the packet is `COMPLETE_WITH_EXTERNAL_MEDIA`.

**Permitted next step:** No follow-on live authority. The single controlled open is spent. A later verified transfer of the MOV files may upgrade packet portability without rerunning the experiment.

**Recovery performed and result:** Physical Reset. Processor restarted, cursor live. Static garbage persisted because Reset does not clear the video buffer. CLEAR was not pressed; the open was not repeated.

## Evidence checklist

- [x] Native, unmodified analyzer files retained.
- [x] Display evidence retained externally with hashes, custody, inspection attribution, and observations in `display-video-record.md` and `external-media-manifest.json`.
- [x] Owner JSONL retained for the controlled-open phase.
- [x] Probe-point evidence and its silkscreen identification basis retained in `probe-point-record.md`; external photographs are not misrepresented as local files.
- [x] Packet status records external media and reduced portability separately from the `INCONCLUSIVE` result.
- [x] Manifest validates with `python3 tools/capture_manifest.py metadata.json`.
- [x] Raw capture, external display record, host log, and worksheet agree on ordering.
- [x] No transmit, firmware, EEPROM, jumper, power-source, or wiring change occurred.
- [x] Result is classified `INCONCLUSIVE` and recovery is recorded.
