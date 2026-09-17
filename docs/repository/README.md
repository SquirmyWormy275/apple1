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

The combined Pi/documentation head passed all steps in
[validation run 35191157942](https://github.com/SquirmyWormy275/apple1/actions/runs/35191157942).
It includes two regression tests keeping the lesson index aligned with the
actual 42-packet catalog. SP01 already existed; the older index omitted its row.
No lesson review gate was closed by correcting that index.

Both histories were retained through merge commits. Source publication did not
change the installed Pi release, rerun acceptance, or qualify the physical
Replica. The Propeller diagnostic-preparation work in
[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) remains separate.

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
