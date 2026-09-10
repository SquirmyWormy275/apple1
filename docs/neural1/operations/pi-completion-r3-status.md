# Revision 3 execution status

This is the preserved pre-deployment checkpoint. It is superseded by
[native Pi acceptance](pi-acceptance-2026-09-10.md), which records the installed
application, actual Pi runs and remaining preservation work.

Status: **PARTIAL — native Pi deployment and acceptance blocked by local access.**

The execution branch began from a clean checkout and freshly fetched upstream
`2c40f1c5c63a083184eb724df4500cd1427bd3d2`. Existing qualified model manifests
and every referenced staged blob were independently rehashed and matched; no
model download or preservation-image rebuild was performed. The existing
manual supplied the separately reviewed year-end 1976 console corpus.

Implemented and software-tested:

- terminal operations, complete-checkout resource resolution, local provider
  identity checks, service-backed run lifecycle, nonce-confirmed startup,
  bounded cancellation, result browsing, META ingestion and complete exports;
- provider endpoint transport, private observation feedback and context resets,
  RAM participant observations, committed-turn recovery and truthful failures;
- specialized family dispatch, executable positive/negative controls, strict
  exact-256 handling and qualified legal SELFHOST ancestry;
- verified atomic no-clobber migration and UUID/mount/path/capacity checks;
- guarded native-Pi installer with reversible configuration backups, native
  runtime reuse, SSD-dependent provider service and account-scoped persistence;
- explicit-path native diagnostics and bounded benchmark integration.

Validation: 129 focused NEURAL1/storage tests pass; Ruff, mypy and repository
validation pass. Deterministic demos remain explicitly synthetic/virtual.
The broader software suite records 187 passing tests and one pre-existing
firmware byte-provenance failure: two working files have LF bytes while their
Git attributes require CRLF. Read-only canonical Git checkout filtering verifies
all nine recorded artifact hashes. Firmware artifacts/manifests were not changed.
Serial tests use mocked transport; no physical serial device was opened.

Two small host-only genuine-provider attempts were thermally stopped before a
completed model response. The first sampled 100.05 C after a 73.05 C sample;
a second, with 25% service CPU quota and smaller batches, stopped at 75 C.
Their failed evidence is retained privately. Neither demonstrates accepted live
model execution, and neither counts as Pi acceptance. Task-owned host model
services were stopped.

The card and new SSD were reidentified. A dedicated public login key was added
to the existing target account with a verified backup; existing public host-key
identity was pinned privately. Protected network/SSH/account/store inspection
still required native sudo authentication. The card remained on the workstation,
with no verified live Pi connection or observed Pi model/RAM.

The Pi installer has not been executed. SSD commissioning, native model/store
qualification, actual ordinary launch, all live family runs, recovery/export
acceptance, service restart, controlled reboot and measured resource behavior
remain unverified. No DONE or deployed-revision claim is made. Private completion
ledger, logs, access receipt and morning report are retained outside Git.

See [terminal application](terminal-application.md) for implemented usage and
explicit scientific scope. Completing physical access and native authentication
is required before deployment can continue; it is not replaced by laptop tests.
