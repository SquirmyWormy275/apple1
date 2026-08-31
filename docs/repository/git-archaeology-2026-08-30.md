# Git archaeology — 2026-08-30

## Baseline

Live `main` at the start of this architecture branch:

```text
3c06a857b93409e4c681e1d794fa757bf66db3cc
```

No tags were present in the live GitHub tag refs at audit time.

The handoff also contained an older flattened Git metadata snapshot. It was useful for secondary history inspection but was not treated as current because its `origin/main` (`3d440fa8...`) was 28 commits behind live GitHub.

## Branch classification

| Branch | Tip at audit | Relationship to starting `main` | Classification | Decision |
|---|---|---|---|---|
| `main` | `3c06a857...` | baseline | ACTIVE | Target branch. Never force-reset. |
| `refactor/repository-architecture-v1` | created from starting main | exact branch point | ACTIVE | This audit/migration branch. |
| `archive/neural1-1976-research-2026-08-30` | `f1ac1958...` | diverged; 34 commits unique to archive lineage | ARCHIVE — KEEP | Frozen by design. Do not modify or delete. |
| `research/neural1-agenda-1976-sources` | `f1ac1958...` | same tip as frozen archive | ARCHIVE — KEEP | Alias/reference to frozen research lineage; retain. |
| `integration/neural1-1976-research` | `adca5452...` | diverged; 9 commits ahead of merge base, 13 behind main | SUPERSEDED / UNIQUE COMMIT LINEAGE | Retain. Key integrated blobs are byte-identical on current main, but commit lineage is unique. Not a deletion candidate in this pass. |
| `feature/neural1-off-device-completion` | `006b9667...` | strict ancestor; 0 commits ahead, 13 behind | MERGED | No missing work. Retain unless a later branch-retirement policy explicitly removes merged feature refs. |
| `research/display-history-finalization` | `3c06a857...` | same tip as starting main | MERGED | No missing work. |
| `capture-docs-snapshot-2026-08-28` | `b42c4cf5...` | strict ancestor; 0 ahead | ARCHIVE — KEEP | Preservation-oriented snapshot; retain. |
| `cf-card-backup-2026-08-28` | `7bf47f7f...` | strict ancestor; 0 ahead | ARCHIVE — KEEP | Preservation backup; retain. |
| `preserve/cf-card-2026-08-28` | `7bf47f7f...` | same tip as CF backup | ARCHIVE — KEEP | Explicit preservation ref; retain. |
| `propeller-recovery-backup-2026-08-28` | `9051c76e...` | strict ancestor; 0 ahead | ARCHIVE — KEEP | Recovery/preservation semantics justify retention. |
| `propeller-serial-recovery` | `7d2716db...` | strict ancestor; 0 ahead | MERGED | No unreachable work; retain in this pass because the physical serial investigation remains active but blocked. |

## Frozen archive verification

The required frozen archive branch remains at:

```text
archive/neural1-1976-research-2026-08-30
f1ac1958c2e8906510fc963422ed1801f0231b1b
```

It is deliberately not a simple ancestor of main. That divergence is not a defect; it preserves the research tranche's original lineage.

A representative preserved research file, `docs/neural1/research/1976-multiverse-source-ledger.md`, has the same blob SHA (`d08dbd354c5acfeff07268be05938fc2981c1c6c`) at the frozen archive tip and current main. This demonstrates that archive divergence and current content integration can coexist.

## 1976 integration branch: unique lineage versus missing content

`integration/neural1-1976-research` contains nine commits not reachable from starting main. That initially looks like stranded work, but representative integration outputs were compared by blob identity:

| Path | Integration blob SHA | Starting-main blob SHA | Result |
|---|---|---|---|
| `neural1/history.py` | `564f0899...` | `564f0899...` | identical |
| `data/neural1/history/1976-research-index.json` | `35d17af1...` | `35d17af1...` | identical |
| `tools/neural1_validate.py` | `a9b71d04...` | `a9b71d04...` | identical |
| `docs/neural1/research/1976-multiverse-source-ledger.md` | `d08dbd35...` | `d08dbd35...` | identical on the preserved research lineage/current main sample |

Conclusion: the branch has **unique commit history**, but the audited core integration content is already present on main through a different integration path. It is therefore not appropriate to cherry-pick those nine commits wholesale, and it is also not appropriate to delete the branch as though its lineage were meaningless.

## Commits not reachable from main

The two intentional categories observed are:

1. the frozen 1976 research lineage (`f1ac1958...`), which contains unique archival commits by design;
2. the superseded `integration/neural1-1976-research` lineage, which contains unique integration commits but audited core blobs already present on main.

No other audited live branch contained commits ahead of starting main.

## Worktrees and stashes

GitHub branch/ref APIs do not expose another machine's local worktrees or local stashes. The bundled handoff Git metadata did not show separate worktree or stash refs. This report therefore does **not** claim that every possible developer machine has no local uncommitted work; it records only what was observable from the supplied snapshot and live remote refs.

No `reset --hard`, `clean`, branch deletion, force push, or history rewrite was performed.

## Retirement policy

This pass deliberately deletes **no branches**. A future retirement pass may remove a merged feature branch only after confirming it has:

- zero commits unique to the branch;
- no preservation/recovery/archive semantics;
- no external references relying on the branch name;
- no active PR or worktree dependency.

Archive, backup, preservation, and recovery branches are out of scope for routine cleanup.
