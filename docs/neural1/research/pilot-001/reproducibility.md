# Reproducibility

Authoritative campaign ID: `N1-P-057141928BD15B0C`. Verify the release bundle before replay. Reproduction requires the exact runtime revision, registry digests, campaign specification, provider executables, model blobs, and recorded seeds. Use `neural1 verify-bundle BUNDLE`, then `neural1 run-campaign SPEC REGISTRY --output OUTPUT` only when the exact models are available.

The runtime commit was `2097423645c549a5cfff1827838022b8b71fca10`.
An exact fail-closed lookup replay verified all 156 successful transcript
records against the recorded `(prompt, logical agent ID, seed)` tuples. Model
generation itself should not be rerun to claim byte identity; use the replay
records. The first thermal-stop summary is retained as
`summary.thermal-stop.json`, and the final summary records the bounded resume.
