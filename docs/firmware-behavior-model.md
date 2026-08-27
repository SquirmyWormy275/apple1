# Firmware behavior model: pre-change executable contract

`tools/firmware_behavior.py` is a pure Python model for a possible future
single-writer keyboard-bus design. It does not parse, compile, alter, or prove
the current Propeller firmware.

It locks down three deliberately conservative expectations for review before
any Plus-source work starts:

1. The first planned monitor stimulus is only uppercase printable seven-bit
   ASCII plus carriage return. Lower-case conversion, high-bit conversion, and
   LF handling are rejected until measured rather than guessed.
2. PS/2 and serial producers feed one FIFO service path. The model records the
   producer for every queued byte and preserves arrival order.
3. A full queue is a recorded `queue_full_stop`, not a silent discard, retry,
   reordering, or an excuse to speed up pacing.

The model retains only a bounded recent-event history (256 events by default),
so a long off-device simulation cannot consume unbounded memory. A future
measurement tool must persist raw evidence separately rather than treating this
model's in-memory trace as a capture format.

Run the off-device contract tests:

```powershell
python -m pytest tests\test_off_device_package.py -q
```

The model is a design constraint for a future firmware candidate, not evidence
that the currently installed EEPROM has a queue, a single writer, or the same
byte contract.
