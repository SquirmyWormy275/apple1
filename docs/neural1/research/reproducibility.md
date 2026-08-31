# Reproducibility

A serious run requires its manifest, runtime revision, exact provider/model
record, seed, initial snapshot, prompts/policies, append-only events, artifact
hashes, and scoring/analysis version. `python -m neural1.demos` is the current
reproduction entry point. Fake-provider output validates plumbing only. Replay
must fail closed when an exact recorded prompt/agent/seed tuple is absent.
