# Experiment runtime

A manifest fixes schema, experiment, seed, target, maturity, model record,
configuration, and optional fork ancestry. The run ID is a stable digest of
those scientific inputs. Snapshots contain a versioned header and the exact
64 KiB image. Forks identify the base run, fork point, and one changed factor.
Replay recreates identity; replay providers refuse prompts absent from the
recording. Events are JSONL and append-only by convention.
