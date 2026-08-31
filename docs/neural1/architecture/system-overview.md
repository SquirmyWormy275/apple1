# System overview

NEURAL1 is a Python package layered beside the existing preservation tooling.
`world.py` owns a deterministic 64 KiB image with a configured experimental
RAM window. Agents receive `WozMonSession`, never the world or its privileged
host read/write verifier. `runtime.py` identifies runs from canonical inputs,
stores manifests and append-only events, and delegates bytes to a SHA-256
content-addressed store. `models.py` isolates logical agent state from shared
model weights. `experiments.py` contains experiment policies, not separate
runtimes. `meta.py` turns results into claims linked to evidence.

The existing `tools/apple1_emulator.py` remains authoritative for repository
RAM-only program execution. NEURAL1 does not claim to ship the WozMon ROM or a
cycle/electrical Replica emulator.

See [ADR 0001](../decisions/ADR-0001-shared-virtual-runtime.md).
