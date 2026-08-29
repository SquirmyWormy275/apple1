# Serial characterization protocol

## Non-negotiable rules

- Use the serial-owner tool, never a terminal emulator, `cat`, shell redirect,
  or per-byte open/close loop.
- Bind both recorded identities: the FT232R by-id symlink and its physical
  by-path symlink. The current FTDI USB serial is `00000000` and is not enough
  by itself.
- A `probe` is read-only. A `session` is a distinct, operator-approved action
  that may open the device; it must not be run until reset evidence is ready.
- Treat an unexpected reset, video change, byte mismatch, or identity change as
  `STOP` and retain the capture.

## Safe deployment and probe

After copying this repository to the Pi, the only permitted first command is:

```bash
python3 tools/serial_owner.py probe
```

Expected result: JSON showing the recorded by-id, by-path, and that both
resolve to `/dev/ttyUSB0`. This command imports no serial driver and does not
open the device.

## First opened-session test card (not authorized yet)

Before an opened session, prepare a capture manifest containing board revision,
power source, USB topology, timestamps, and the `STOP` recovery action. Then
record video and, if available, reset/control-line evidence. For the known
reset-on-open symptom, follow the
[logic-analyzer open-event test card](captures/logic-analyzer-open-event-test-card.md)
before any further serial action. The owner requests DTR and RTS low before the
open, uses 9600 8N1 with all flow control disabled, and retains its JSONL
capture.

Only after a repeatable non-resetting open may the owner transmit the first
payload: 7-bit uppercase `TEST` plus CR, starting at 500 ms per character.
Each faster pacing test is a separate capture card.
