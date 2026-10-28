# 10. Understand deployment without confusing it with a lab

The worked examples run in a checkout. The commissioned Pi is a pinned,
configured deployment with an identified SSD, native model store, resource
guards, and user-service workers. Installing the Python package alone does not
create that environment.

## Read the installed identity first

The [September closeout](../../neural1/operations/pi-closeout-2026-09-10.md)
identifies the actual Pi application and installer revisions. Publishing a new
GitHub source version does not update it. The current source adds contextual
help, shorter SOURCE syntax, and readable output options; use the closeout's
command list for the recorded installed release.

On that existing installation the entry point is `neural1`. Begin with HELP,
STATUS, MODELS, and LESSONS. These discover capabilities and current state before
a run. Model selection validates its live identity; a remembered preference is
not permission to replace the registry or weights.

## Storage is part of correctness

A missing mount can leave an ordinary directory with the same path. Writing
there would put state on the wrong disk. F25 shows the storage guard rejecting
such a directory without creating fallback files. Free space alone cannot
establish identity. The configured UUID, mount source, role, capacity, and
resolved paths are checked before work.

F17 inspects an authored tiny image file; it never opens a real disk. F24 plans,
copies, and verifies tiny files between disposable fixture directories. It
retains the source. Those examples teach formats and integrity without claiming
a dedicated SSD was commissioned.

## Worker lifecycle and resource stops

Installed workers use systemd user services, task identities, locks, durable
logs, and watchdog checks. Temperature, available memory, storage identity,
capacity, and current Pi throttling conditions can stop work. A worker log is
not proof of a successful scientific task, and repeated retries can duplicate
work or hide an unresolved resource problem.

The native closeout records actual cancellation/resume and late-SSD startup.
F16/L06 read that retained evidence. They do not newly test power behavior,
network reliability, service ownership, or cooling.

## What belongs to an operator procedure

`neural1-storage` can inspect images, baseline a mounted rootfs, initialize role
markers, plan/copy/verify a migration, and finalize verified temporary-source
deletion. The last step is destructive and deliberately separate. The Pi
installer changes a pinned deployment and makes backups; it is not first-launch
setup for a lesson. Physical serial, firmware, EEPROM, CFFA1, GPIO, and wiring
procedures remain outside this automatic course.

Use the [operator guide](../../neural1/operations/terminal-application.md),
[SSD commissioning record](../../neural1/operations/ssd-commissioning.md), and
[Replica investigation](../../troubleshooting.md) for those environments.
The [coverage register](../coverage.md) marks operator-only surfaces explicitly.
It does not turn a syntax example or a retained record into a newly executed test.

## Practice

Explain the difference between a directory, a mounted volume, its identity,
a model store, and a qualified model record. Then explain how you would recognize
an interrupted run without editing its cancellation files. Use the documented
STATUS/SHOW/TRANSCRIPT outputs and the saved evidence relationships.

[Textbook home](../README.md) · [Previous chapter](09-campaigns-evidence-and-recovery.md) · [Next chapter](11-preservation-and-teaching.md)
