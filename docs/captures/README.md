# Capture record format

Store each hardware observation in its own timestamped directory. Retain raw
bytes and unmodified instrument output; do not summarize over the evidence.

For the currently blocked `FT232R open -> garbled display` symptom, use the
[logic-analyzer open-event test card](logic-analyzer-open-event-test-card.md).
It permits passive measurement and one controlled no-transmit open only; it
does not authorize a serial retry or a firmware/hardware change.
Use its [trace worksheet template](logic-analyzer-trace-worksheet-template.md)
to retain point identification, timing, raw files, and the decision result.

Every capture record must state:

- target by-id and by-path identity;
- board revision, power source, USB topology, and physical changes (normally
  `none` during characterization);
- owner/tool version and requested DTR/RTS state;
- test card, timestamps, raw transmit/receive bytes, and instrument files;
- one of `PASS`, `STOP`, or `INCONCLUSIVE`, plus the recovery action.

Use the troubleshooting form: `Symptom -> Hypothesis -> Test -> Result -> Conclusion`.
