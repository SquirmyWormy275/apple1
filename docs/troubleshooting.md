# Replica 1 Plus serial troubleshooting record

## Current position — reviewed September 16, 2026

The latest executed test recorded here is the September 2 instrumented
no-transmit open. It reproduced display corruption but did not establish the
root cause. A working NEURAL1 Pi does not resolve or qualify this physical link.

[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) preserves preparation for
a bounded capture and worker with reset coverage. It remains a separate review
and hardware-qualification task, not permission to launch an unattended test.
Its reported software checks do not measure analog rails or establish display
stability on the actual board.

No new multimeter readings, reset trace, firmware repair, or successful physical
qualification are asserted by this documentation update. Continue from the
[September 2 packet](captures/2026-09-02-ft232r-open-analyzer/README.md) and the
[serial protocol](serial-test-protocol.md); do not repeat an uninstrumented open
or substitute a firmware flash for the unresolved measurement step.

The dated observations below are retained unchanged. See
[current project status](STATUS.md) for the separate Pi and integration work.

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
