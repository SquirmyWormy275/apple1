# Repository records

These records explain how the Apple-1 repository is organized and how its
sources, preserved artifacts, research, and software evidence are kept distinct.
For everyday navigation, use the [project map](../PROJECT-MAP.md). For the
working state and open integration work, use [current status](../STATUS.md).

## Current review

[September 16 repository review](review-2026-09-16.md) records the documentation
refresh, the Pi completion branch missing from `main`, and the separate
Propeller preparation PR. It does not replace the earlier audits or claim a new
hardware acceptance run.

## Architecture and historical records

- [Repository architecture](architecture.md): directory roles, evidence classes,
  preservation boundaries, and change rules.
- [August 30 audit](audit-2026-08-30.md) and [authority-aware inventory](inventory-v1.md):
  the baseline inventory and consolidation findings.
- [August 30 Git archaeology](git-archaeology-2026-08-30.md): branch classifications
  and unique-lineage findings at that review date, not a live branch inventory.
- [August 30 provenance audit](provenance-audit-2026-08-30.md): source identity,
  hashes, rights, and attribution gaps.
- [Architecture migration ledger](migration-v1.md): what that pass changed and
  deliberately retained.
- [Fresh-checkout acceptance record](fresh-checkout-validation.md): earlier
  acceptance evidence. Use the [current validation commands](../../README.md#development-and-validation)
  and the checks on the exact PR head for a new change.

## Reading the records

A file's location does not establish its truth or completeness. Preserved
artifacts are not editable prose; staged research is not authoritative runtime
data; emulator results are not physical observations. Scientific run evidence,
including incomplete or negative results, is not disposable build output.

Keep detailed audit history here. Entry pages should explain the present state
plainly and link to the relevant record instead of repeating the entire chain.
