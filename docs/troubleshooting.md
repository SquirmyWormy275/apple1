# Replica 1 Plus serial troubleshooting record

## 2026-08-27 — FT232R open with no transmit

**Symptom**

The Replica display became garbage when the Pi opened the FT232R. No payload
was transmitted.

**Hypothesis**

Opening the host serial device changes an FT232R/board control path that
disturbs the Replica; the precise electrical mechanism is unknown.

**Test**

The exclusive owner validated both recorded USB identities, requested DTR and
RTS low before the pyserial open, held the session for about 0.2 seconds,
drained startup bytes, and closed. Raw owner evidence is
`captures/2026-08-27-open-no-transmit-retry1.jsonl`.

**Result**

The owner opened at `2026-08-27T16:42:20.901092+00:00`, drained no bytes, and
closed normally. The display became garbage. A physical Reset restored a stable
monitor prompt and flashing `@` cursor.

**Conclusion**

**STOP.** A host serial open alone is sufficient to disturb this board. The
record does not prove whether DTR, RTS, reset routing, another FT232R control
line, or board power behavior caused it; no scope or logic-analyzer measurement
was available. Do not transmit, adjust pacing, load Propeller RAM, program
EEPROM, or repeat an open until the board-path investigation has measurement
coverage.

## 2026-09-02 — instrumented FT232R open with no transmit

**Result:** The one authorized controlled open reproduced dense display
corruption. The owner log records DTR and RTS requested false, an empty startup
drain, no transmit event, and a 202.5 ms session. Across the complete 30-second,
4 MS/s capture, TX-O and RX-I remained digitally high with zero threshold
crossings. Physical Reset restored a live cursor while stale display garbage
remained; CLEAR was not pressed.

**Conclusion:** Execution is `COMPLETE`; the root-cause result is
`INCONCLUSIVE`; the packet is `COMPLETE_WITH_EXTERNAL_MEDIA`. UART-data
transitions and wired DTR/RTS through the installed four-conductor interconnect
are unsupported as the mechanism. Unobserved `RESn` and analog power/ground,
regulator, sub-threshold, and shared CFFA1 load effects remain unresolved. The
controlled open is spent and no follow-on live action is authorized. See the
[evidence packet](captures/2026-09-02-ft232r-open-analyzer/README.md).
