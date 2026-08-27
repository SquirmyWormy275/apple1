# Capture record format

Store each hardware observation in its own timestamped directory. Retain raw
bytes and unmodified instrument output; do not summarize over the evidence.

Every capture record must state:

- target by-id and by-path identity;
- board revision, power source, USB topology, and physical changes (normally
  `none` during characterization);
- owner/tool version and requested DTR/RTS state;
- test card, timestamps, raw transmit/receive bytes, and instrument files;
- one of `PASS`, `STOP`, or `INCONCLUSIVE`, plus the recovery action.

Use the troubleshooting form: `Symptom -> Hypothesis -> Test -> Result -> Conclusion`.
