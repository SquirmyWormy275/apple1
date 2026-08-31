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
| `docs/repository/audit-2026-08-30.md` | Repository-wide map, findings, risks, and consolidation conclusions. |
| `docs/repository/inventory-v1.md` | Authority-aware inventory with owner, source/generated, preservation, authority, currentness, duplication, destination, and concern fields. |
| `docs/repository/architecture.md` | Durable taxonomy and authority model. |
| `docs/repository/git-archaeology-2026-08-30.md` | Live branch classification and unique-lineage analysis. |
| `docs/repository/provenance-audit-2026-08-30.md` | Provenance, rights, hash, and authority status. |
| `docs/repository/migration-v1.md` | This ledger. |
| `docs/repository/fresh-checkout-validation.md` | Acceptance commands and validation evidence. |
| `docs/plans/README.md` | Current-status index for historical plans; the old serial-repair plan is explicitly blocked as execution authority by later STOP evidence. |
| `tests/test_neural1_repository.py` | Regression checks that historical research remains staging-only and deterministic demos never open physical serial. |

## Updated

- `README.md` — now points new contributors to the project map/governance layer and explicitly names the authority classes and current physical boundary.
- `docs/repository/README.md` — indexes the governance deliverables, including the authority-aware inventory.
- `tools/neural1_validate.py` — now validates durable repository anchors, all first-party Markdown relative links, existing schema instances, the full MULTIVERSE promotion policy, ASCII constraints, and art provenance.
- `.github/workflows/ci.yml` — retains every prior acceptance command and adds an explicit `serial_opened == false` assertion plus `git diff --exit-code` after validation/demo generation.

The historical file `docs/plans/2026-08-25-1324-fix-replica1-propeller-serial-plan.md` itself is deliberately **not edited**. Its original `implementation-ready` front matter is part of planning history. `docs/plans/README.md` supplies the current status and links the later STOP evidence so old planning state cannot be mistaken for present execution authority.

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
| `docs/peripherals/displays/` | Coherent research product with evidence/rights/source separation. |
| `wiki/` | Retained as derived GitHub-wiki-facing navigation; documented as non-authoritative rather than duplicated/rebuilt. |

No file or directory move was required in v1. That is intentional: the audit found that moving mature evidence-heavy trees would add history/link risk without repairing an authority boundary.

## Similar material retained, not deduplicated

- `research-agenda.md` versus `research-agenda-v1.md`: overview versus detailed agenda.
- repository-wide audit versus `docs/neural1/audit-2026-08-30.md`: different scope and historical role.
- general versus Pilot-specific negative-results documents: different evidence scope.
- `cf-card/` versus `preservation/cf-card/`: authored export control versus immutable preserved baseline.

## Retired / archived

No preserved artifact, scientific evidence package, branch, or unique research file is deleted in v1.

The old serial repair plan remains at its historical path and is de-authorized through the plans status index rather than rewritten or moved. This preserves incoming links and planning history while preventing date-guessing from being the only signal that physical execution is blocked.

## Branch handling

No existing branch is deleted. In particular:

- `archive/neural1-1976-research-2026-08-30` remains frozen at `f1ac1958c2e8906510fc963422ed1801f0231b1b`;
- `integration/neural1-1976-research` remains available as unique integration lineage even though audited core blobs are already present on main;
- preservation/backup/recovery refs remain intact.

## Validation changes

The validator and CI changes are additive:

1. require durable repository anchors instead of assuming documentation topology;
2. check relative links across all first-party Markdown rather than selected NEURAL1/art/wiki subsets;
3. independently enforce all historical-promotion safety flags, including null prices and the ban on LLM estimates;
4. run the existing full test suite plus new repository safety regressions;
5. require the deterministic demo summary to report `serial_opened=false`;
6. require validation/demo execution to leave tracked files unchanged.

A fresh GitHub Actions checkout at branch commit `7aed69c71e7ed987700c876d6d46bacfcd71f69f` passed editable install, Ruff, mypy (34 source files), all 99 tests, repository validation, deterministic demo, explicit serial safety assertion, and clean-tree assertion. Final documentation commits are re-run through the same gate before merge.

## Physical boundary

No migration step opens a serial port, transmits to the Replica, loads firmware, programs EEPROM, writes CFFA1, operates GPIO, changes wiring/jumpers/solder, uses a camera, or runs physical qualification.

## Completion rule

This ledger is complete only after the final branch documentation head has passed the same fresh-checkout acceptance commands, deterministic demo, repository validator, clean-tree/adversarial review, current-main reconciliation, and archive-ref check. Exact evidence is recorded in `fresh-checkout-validation.md` and in the final project report.
