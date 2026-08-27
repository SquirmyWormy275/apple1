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
