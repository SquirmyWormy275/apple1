# Capture record format

Store each hardware observation in its own timestamped directory. Retain raw
bytes and unmodified instrument output; do not summarize over the evidence.

For the currently blocked `FT232R open -> garbled display` symptom, use the
[logic-analyzer open-event test card](logic-analyzer-open-event-test-card.md).
It permits passive measurement and one controlled no-transmit open only; it
does not authorize a serial retry or a firmware/hardware change.
Use its [trace worksheet template](logic-analyzer-trace-worksheet-template.md)
to retain point identification, timing, raw files, and the decision result.

The [2026-09-02 instrumented run](2026-09-02-ft232r-open-analyzer/README.md)
is complete as executed, `INCONCLUSIVE` as to root cause, and
`COMPLETE_WITH_EXTERNAL_MEDIA`. Its single controlled open is spent.

Every capture record must state:

- target by-id and by-path identity;
- board revision, power source, USB topology, and physical changes (normally
  `none` during characterization);
- owner/tool version and requested DTR/RTS state;
- test card, timestamps, raw transmit/receive bytes, and instrument files;
- one of `PASS`, `STOP`, or `INCONCLUSIVE`, plus the recovery action.

Result and packet completeness are separate. Version 2 packets record
`execution_status`, `packet_status`, and `portability_status`. Display and
probe media may either be non-empty local files with verified hashes or
externally held, hash-identified evidence with a local custody and inspection
record. Bare placeholders such as `UNAVAILABLE`, `MISSING`, or `N/A` are not
evidence. External custody can yield a complete packet while reducing its
portability; a later verified media transfer upgrades portability without
changing the experiment or its result.

Use the troubleshooting form: `Symptom -> Hypothesis -> Test -> Result -> Conclusion`.
