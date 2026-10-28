# Native course verification

The [pre-hardware extension](prehardware.md) adds the later BASIC/card checks.
The results below retain their original 439-test/100-lab scope.

The [October 28 UTC receipt](pi-20261028.json) records the expanded course
running on the actual Raspberry Pi 5 in an isolated SSD checkout and test
environment. The globally installed NEURAL1 release was unchanged.

All 439 tests passed. All 100 examples reproduced their retained stdout, with
source and image hashes verified. Repository validation, Ruff and mypy also
passed. The receipt names the exact capture-manifest digest; that manifest
identifies the teaching source files and retained evidence used by the run.

These checks execute deterministic software fixtures and offline replays. Fresh
inference is separately retained in the [native chapter](../native/README.md).
Neither this receipt nor the virtual CPU tests establish physical Replica
acceptance, a native BASIC interpreter, historical source clearance, or a new
system-wide deployment acceptance.

[Textbook home](../README.md) · [Review and corrections](../review.md)
