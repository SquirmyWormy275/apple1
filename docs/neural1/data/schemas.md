# Data schemas and formats

All records carry `neural1-0.1` directly or through their manifest. JSON uses
sorted keys for stable identity; JSONL holds append-only events; binary snapshots
use `N1SNAP1 START BUDGET GENERATION\n` followed by exactly 65,536 bytes.
Artifacts use lowercase SHA-256. Run manifests record target/maturity/model/
seed/config and fork metadata. Lineage records kind/hash/parents/mutation.
Claims and proof capsules are described in the META documentation.

Breaking schema changes require an explicit migration; old raw records remain
immutable. Host-only experiment stores live outside CF-card trees. Only reviewed
machine-facing text/binaries may be exported to `cf-card/` through its existing
manifest process.

Machine-readable initial contracts live in `schemas/neural1/`. The 1976
MULTIVERSE rejection fixture is explicitly marked synthetic under
`neural1/fixtures/`; it is not an authoritative component record.
