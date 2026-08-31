# Methodology

Pilot 001 used the frozen `neural1-campaign-0.1` specification, fixed model registry, matched control `identical zero-filled 4K world, driver version, generation count, agent count, and seed across model families`, seeds [101, 211, 307], 12 requested generations, 2 logical agents per cell, 4096 bytes of allowed RAM, and a hard wall-clock limit of 43200 seconds. Contexts were isolated by logical agent ID. All model responses, WozMon outputs, checkpoints, errors, and token metadata were recorded.

The matrix order was experiment, model, then seed. The operator added a
thermal safety stop when TCPU/x86 package sensors reached 102 C. Because this
criterion was not preregistered in the campaign specification, it is reported
as an operational intervention and a threat to completeness. No response was
manually repaired or reclassified. The strict WozMon parser in the frozen
runtime determined action validity.

After cooldown, one bounded resume continued the interrupted SmolLM2 cell from
generation 9 and completed it. Cancellation was immediately reasserted before
the matrix could continue. Unit/property tests establish exact deterministic
resume for the fake provider; this pilot establishes successful stateful resume
for one real-model cell only.
