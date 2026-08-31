# ADR-0002: Constrained interfaces and evidence

**Accepted.** Experimental agents receive WozMon sessions, not world/debugger
APIs. Models use provider adapters and share weights across logical identities.
Artifacts are SHA-256-addressed filesystem objects; lineage is an explicit DAG;
META uses a typed claim graph and portable proof capsules. These simple formats
are auditable and leave room for a later SQLite query index.
