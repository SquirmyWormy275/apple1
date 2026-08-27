# Logic-trace packet validation

`tools/trace_packet.py` validates the non-electrical completeness of a future
logic-analyzer packet. It is deliberately separate from the prepared open-event
test card and cannot arm an analyzer, open the serial device, or collect a
trace.

The packet must record a PASS/STOP/INCONCLUSIVE result, `physical_changes:
none`, analyzer model/input rating, at least one safely identified channel,
native raw-capture file, display video, and the exclusive owner's JSONL log.
It must include either a safely evidenced `RESn` channel or an explicit
`resn_unavailable_reason`; the latter keeps the result correlation-only.

```powershell
python .\tools\trace_packet.py .\docs\captures\YYYY-MM-DD-ft232r-open-analyzer\metadata.json
```

Validation does not turn an incomplete physical-point identification or a
missing voltage-domain check into a pass. The live action remains one controlled
no-transmit open under the existing test card, followed by STOP on any display
corruption or reset evidence.
