# Experiment runtime

A manifest fixes schema, experiment, seed, target, maturity, model record,
configuration, and optional fork ancestry. The run ID is a stable digest of
those scientific inputs. Snapshots contain a versioned header and the exact
64 KiB image. Forks identify the base run, fork point, and one changed factor.
Replay recreates identity; replay providers refuse prompts absent from the
recording. Events are JSONL and append-only by convention.

## Campaign execution

`neural1-campaign-0.1` expands the ordered Cartesian product of experiment,
model ID, and seed into stable cell IDs. It fixes generation count, logical
agent count, RAM and token bounds, matched-control description, generation
settings, and a hard wall-clock ceiling. Model IDs resolve through a separate
registry; the campaign has no parameter-count or backend field.

Each generation appends and `fsync`s its transcript before an atomic checkpoint
replacement. A checkpoint stores a content hash and a path relative to the run
root, so the record remains portable. Resume verifies the snapshot hash and
continues at the next generation. Completed cells are immutable/idempotent.
The test suite compares interrupted/resumed execution with uninterrupted
execution at transcript and final snapshot level.

Cancellation is cooperative: creating `CANCEL` under the campaign directory
stops at a generation boundary. Deadline/cancelled and incomplete cells remain
in the summary and Pilot report.
