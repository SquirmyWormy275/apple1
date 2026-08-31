# Reproducibility

A serious run requires its manifest, runtime revision, exact provider/model
record, seed, initial snapshot, prompts/policies, append-only events, artifact
hashes, and scoring/analysis version. `python -m neural1.demos` is the current
reproduction entry point. Fake-provider output validates plumbing only. Replay
must fail closed when an exact recorded prompt/agent/seed tuple is absent.

## Off-device campaign sequence

The first real-model campaign follows this gate order: implementation; unit,
property, and integration tests; fresh-checkout validation; local provider and
model qualification; Pilot 001; analysis; report and proof-capsule generation;
final fresh-checkout validation; then fast-forward to `main`. Real-model output
is never used to debug a materially changing runtime. A material runtime,
schema, scheduler, checkpoint, experiment, META, or bundle change restarts the
pre-pilot validation gates.

The campaign command records exact prompts and results. `export-bundle` copies
the authoritative directory and creates a SHA-256 manifest; `verify-bundle`
rejects missing, changed, unsafe, and unlisted files. The Pilot report is a
derived interpretation. It must not replace the bundle.

```bash
neural1 run-campaign SPEC REGISTRY --output OUT
neural1 evaluate-campaign OUT/campaigns/CAMPAIGN_ID
neural1 export-bundle OUT RELEASE --reproduce '...exact command...'
neural1 verify-bundle RELEASE
neural1 pilot-report OUT/campaigns/CAMPAIGN_ID REGISTRY docs/neural1/research/pilot-001
```
