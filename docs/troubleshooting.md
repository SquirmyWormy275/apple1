# Replica 1 Plus serial troubleshooting record

## Current position — reviewed October 28, 2026

Serial-open display corruption remains unresolved. The latest executed test is
September 2; a working Pi and verified CF installation do not repair this link.
[Issue #17](https://github.com/SquirmyWormy275/apple1/issues/17) now tracks the
[bounded repair plan](hardware/replica-repair-plan.md) and its
[history/source register with eight recovered photographs](hardware/repair-context-2026-10-28/README.md).

The later September 12–13 conversation revised the earlier measurement-first
strategy: basic power/selector checks, compatible firmware recovery using a
spare EEPROM while preserving the original, at most one justified further
substitution, then vendor repair/replacement. No oscilloscope purchase or
complete root-cause diagnosis is required before that controlled repair route.
Prepare the actual compatible image/uploader/rollback package first; it has not
been verified as built. Finite acceptance is three cold boots, five normal serial
connections, keyboard/both serial directions and a short CFFA1 operation.

[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) preserves real runner and
host/Pi preparation. It does not establish probe qualification, a completed new
capture or unattended authority. The optional measurement route remains in the
new plan. No new reading, reset trace, firmware load or live serial action was
performed by this documentation update.

The dated observations below remain unchanged. Their session-specific STOP and
spent-open records are historical evidence, not a requirement to finish an
unlimited diagnostic campaign before considering the later preserved-original
repair strategy. Any next physical session uses its own reviewed procedure;
this consolidation does not execute it. See [current status](STATUS.md) for the
separate Pi and CF work.

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
