# Repository governance

This directory documents how the Apple1 repository is organized, audited, and migrated without collapsing preservation evidence, educational content, experimental software, or historical research into one authority class.

## Start here

- [Project map](../PROJECT-MAP.md) — human navigation from the repository root.
- [Repository architecture](architecture.md) — durable directory taxonomy and authority boundaries.
- [Repository audit — 2026-08-30](audit-2026-08-30.md) — baseline inventory, risks, and consolidation findings.
- [Git archaeology](git-archaeology-2026-08-30.md) — branch classifications and unique-lineage findings.
- [Provenance audit](provenance-audit-2026-08-30.md) — source, hash, rights, and attribution state.
- [Migration ledger](migration-v1.md) — what this architecture pass changed and deliberately did not change.
- [Fresh-checkout validation](fresh-checkout-validation.md) — acceptance commands and final validation evidence.

## Governing rule

A file's location does not by itself make its contents authoritative. Authority comes from the file's declared role, provenance, validation state, and the domain-specific gates described in [architecture.md](architecture.md).

Preserved artifacts are not editable documentation. Research staging is not authoritative historical runtime data. Emulator results are not live hardware observations. Scientific run evidence is not generated build debris.
