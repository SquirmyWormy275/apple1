# Repository architecture migration v1

## Branch and baseline

- Starting main: `3c06a857b93409e4c681e1d794fa757bf66db3cc`
- Migration branch: `refactor/repository-architecture-v1`
- Policy: additive/conservative; no force push, history rewrite, archive-branch edits, physical access, or evidence deletion.

## Migration strategy

The audit found that the substantive repository domains are already more mature than the handoff's proposed example tree. The migration therefore avoids bulk directory churn and instead establishes a durable governance/navigation layer, repairs misleading status, and strengthens validation.

## Added

| Path | Purpose |
|---|---|
| `docs/PROJECT-MAP.md` | Human `START HERE` map across preservation, COMPUTER, Field Library, NEURAL1, META/1, Pilot 001, MULTIVERSE, displays, CF-card, and art. |
| `docs/repository/README.md` | Repository-governance index. |
| `docs/repository/audit-2026-08-30.md` | Repository-wide inventory and risk audit. |
| `docs/repository/architecture.md` | Durable taxonomy and authority model. |
| `docs/repository/git-archaeology-2026-08-30.md` | Live branch classification and unique-lineage analysis. |
| `docs/repository/provenance-audit-2026-08-30.md` | Provenance, rights, hash, and authority status. |
| `docs/repository/migration-v1.md` | This ledger. |
| `docs/repository/fresh-checkout-validation.md` | Final acceptance record, completed after CI/fresh-checkout gates. |

## Updated

The implementation phase is expected to update these existing files without changing their domain meaning:

- `README.md` — point new contributors to the project map and repository-governance index.
- `docs/plans/2026-08-25-1324-fix-replica1-propeller-serial-plan.md` — mark the historical implementation-ready plan superseded/blocked by the later FT232R STOP evidence; original plan body remains preserved.
- `tools/neural1_validate.py` — expand repository validation to first-party Markdown and durable structural anchors while retaining historical-research and art gates.
- `.github/workflows/ci.yml` — if needed, add explicit post-demo assertions/clean-tree validation without removing any existing command.
- tests — add regression coverage for repository structure/validator behavior as justified.

## Intentionally not moved

| Path | Reason |
|---|---|
| `docs/neural1/research/pilot-001/` | Scientific evidence package; its current explicit location is meaningful and linked. |
| `data/neural1/history/` | Correct structured-data layer; authority is controlled by status/schema/runtime gate, not a cosmetic directory rename. |
| `docs/neural1/research/1976-*` | Human research staging belongs with NEURAL1 research; moving it would create link churn without improving authority. |
| `preservation/` | Byte-preservation layer is already distinct from editable docs. |
| `firmware/vendor/110REV03/` | Candidate firmware provenance is established at this path; do not churn hash-sensitive preserved source. |
| `cf-card/` | Already a host-side manifest/export control plane, not the raw preserved card. |
| `docs/field-library/` | Mature product-like corpus with extensive internal links and status records. |
| `docs/peripherals/displays/` | Newly coherent research product with evidence/rights/source separation. |
| `wiki/` | Retained as derived GitHub-wiki-facing navigation; documented as non-authoritative rather than duplicated/rebuilt. |

## Similar material retained, not deduplicated

- `research-agenda.md` versus `research-agenda-v1.md`: overview versus detailed agenda.
- repository-wide audit versus `docs/neural1/audit-2026-08-30.md`: different scope and historical role.
- general versus Pilot-specific negative-results documents: different evidence scope.
- `cf-card/` versus `preservation/cf-card/`: authored export control versus immutable preserved baseline.

## Retired / archived

No preserved artifact, scientific evidence package, branch, or unique research file is deleted in v1.

The old serial repair plan remains at its historical path but receives a current-status warning rather than being moved. This preserves incoming links and plan history while preventing date-guessing from being the only signal that physical execution is blocked.

## Branch handling

No existing branch is deleted. In particular:

- `archive/neural1-1976-research-2026-08-30` remains frozen at `f1ac1958...`;
- `integration/neural1-1976-research` remains available as unique integration lineage even though audited core blobs are already present on main;
- preservation/backup/recovery refs remain intact.

## Physical boundary

No migration step opens a serial port, transmits to the Replica, loads firmware, programs EEPROM, writes CFFA1, operates GPIO, changes wiring/jumpers/solder, uses a camera, or runs physical qualification.

## Completion rule

This ledger is complete only after the branch has passed the fresh-checkout acceptance commands, deterministic demo, repository validator, clean-tree/adversarial review, and final current-main reconciliation. The exact final evidence is recorded in `fresh-checkout-validation.md`.
