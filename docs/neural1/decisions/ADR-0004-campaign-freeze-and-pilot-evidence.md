# ADR-0004: freeze the campaign core before real-model pilots

**Status:** accepted

## Decision

Real-model pilots begin only after the campaign schemas, scheduler,
checkpoint/resume behavior, experiment drivers, META store, and bundle verifier
pass unit/property/integration tests and a clean fresh-checkout validation.
Material changes restart those gates. The pilot has a twelve-hour maximum and
is an infrastructure qualification, not an automatic source of scientific
findings.

The initial matched comparison retains Qwen2.5-Coder 1.5B, SmolLM2 1.7B, and
TinyLlama 1.1B. TinyLlama is an intentional weak baseline. Exact backend,
digest, quantization, and context metadata live in the model registry so a
future 3B–4B record does not change experiment definitions.

## Consequences

Debugging uses fake/replay providers. Interesting pilot output receives only
the causal/evidence level supported by its records. A derived Pilot 001 report
is generated only after the authoritative records and bundle verification
exist. The physical adapter remains unavailable throughout.
