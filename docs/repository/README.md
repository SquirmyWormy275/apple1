# Repository records

For everyday navigation, use the [project map](../PROJECT-MAP.md). For working
software and remaining work, use [current status](../STATUS.md). This directory
holds the supporting architecture, integration history, and preservation reviews.

## Main integration — September 16, 2026

The polished navigation and native Pi source are now integrated into `main`:

| Change | Merge record |
|---|---|
| Documentation and navigation refresh | [PR #8](https://github.com/SquirmyWormy275/apple1/pull/8), merge `1098952fb3d3055fff59233d2620836e95a3963a` |
| Native Pi implementation, evidence, and catalog reconciliation | [PR #7](https://github.com/SquirmyWormy275/apple1/pull/7), merge `f219439005f2859c30865be8b4ad915f2bf55281` |
| Integration records and one-time branch cleanup | [PR #9](https://github.com/SquirmyWormy275/apple1/pull/9), merge `d05aece74185aa6952322cee81758960ef07f83f` |

The combined Pi/documentation head passed all steps in
[validation run 35191157942](https://github.com/SquirmyWormy275/apple1/actions/runs/35191157942).
It includes two regression tests keeping the lesson index aligned with the
actual 42-packet catalog. SP01 already existed; the older index omitted its row.
No lesson review gate was closed by correcting that index.

Both histories were retained through merge commits. Source publication did not
change the installed Pi release, rerun acceptance, or qualify the physical
Replica. The Propeller diagnostic-preparation work in
[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) remains separate.

## Branch cleanup

[Cleanup run 35191704681](https://github.com/SquirmyWormy275/apple1/actions/runs/35191704681)
completed successfully. It removed eight integrated topic refs and its own
merged housekeeping branch after checking exact tips, main ancestry, open pull
requests, and tip stability immediately before deletion. Their commits remain
reachable through `main`; no history was rewritten.

| Removed topic ref | Tip retained in main ancestry |
|---|---|
| `docs/repository-polish-2026-09-16` | `0fd59645ddfe883ac6994764cfb52d496764f301` |
| `neural1/pi-completion-r3` | `fbba2097e3f1f1af858ca3d09b0609b8cb7155b7` |
| `commission/neural1-storage-tooling-v1` | `2262e9e3bfda99b6b844b95ad9ae6033ea1d48c0` |
| `docs/neural1-pi-image-archaeology` | `603af1b7e6e6298001374359b44adcf54673e2db` |
| `feature/neural1-off-device-completion` | `006b9667fb49870a1ec4ef73e1740a862bb2395d` |
| `refactor/repository-architecture-v1` | `d6280a3d51e9f1b09eca54582254334d75db3545` |
| `research/apple1-display-history` | `3c06a857b93409e4c681e1d794fa757bf66db3cc` |
| `research/display-history-finalization` | `3c06a857b93409e4c681e1d794fa757bf66db3cc` |

The housekeeping ref `chore/main-cleanup-2026-09-16` at
`ffe07d37c48741370df55e1836037b2711e9e0a0` was also removed after its merge.
`integration/neural1-1976-research` failed the ancestry check and was retained;
no claim is made that all its original commits are integrated. Archive, backup,
preservation, capture-snapshot, historical Propeller, and active-work refs were
excluded from deletion and rechecked afterward. Ten branches remained, including
`main` and those retained records.

The temporary cleanup workflow was removed after its observed run. The ordinary
read-only validation workflow is unchanged; no ongoing deletion job is installed.
Its eight local cleanup simulations and byte-identity check are documented in
the PR, while the run log records the actual remote results.

## Architecture and historical records

- [Repository architecture](architecture.md): directory roles, evidence classes,
  preservation boundaries, and change rules.
- [September 16 pre-integration review](review-2026-09-16.md): the inspection
  that found the Pi work outside main. Its unmerged-branch statements describe
  that earlier snapshot, not the present repository.
- [August 30 audit](audit-2026-08-30.md) and [authority-aware inventory](inventory-v1.md):
  baseline inventory and consolidation findings.
- [August 30 Git archaeology](git-archaeology-2026-08-30.md): branch classifications
  and unique-lineage findings at that date, not a live branch inventory.
- [August 30 provenance audit](provenance-audit-2026-08-30.md): source identity,
  hashes, rights, and attribution gaps.
- [Architecture migration ledger](migration-v1.md): what that pass changed and
  deliberately retained.
- [Fresh-checkout acceptance record](fresh-checkout-validation.md): earlier
  evidence. Use the [current commands](../../README.md#development-and-validation)
  and checks on the exact revision for new work.

## Reading the records

A file's location does not establish its truth or completeness. Preserved
artifacts are not editable prose; staged research is not authoritative runtime
data; emulator results are not physical observations. Scientific run evidence,
including incomplete or negative results, is not disposable build output.

Keep audit history here. Entry pages should explain the present state plainly
and link to relevant records instead of repeating the entire chain. Merged topic
branch names may be retired after ancestry checks; preservation, backup, archive,
and active-work refs are retained.
