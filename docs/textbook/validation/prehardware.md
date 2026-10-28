# Pre-hardware verification

This edition adds a real Apple-1 Integer BASIC interpreter, actual CFFA1 firmware
execution, a RAM card reader and a reproducible core image build. The artifacts
are labeled host/virtual evidence; no Replica, serial port or physical card is
opened by these tools.

The [core build receipt](card-build.json) records baseline/image identities,
independent ProDOS inventory, original-file preservation, all-page reader checks,
and six clear/load/execute BA1 comparisons. The source image remains unchanged.
The candidate image itself is generated output, not a replacement preservation
baseline.

The [packet review](../../field-library/review/README.md) records the structural
gate and source qualifications. The [storyboard](../../hardware/build-storyboard/README.md)
has empty physical asset/measurement slots ready for the finished setup.

[Earlier native course receipt](README.md) · [Card guide](../../../cf-card/README.md) ·
[Textbook home](../README.md)

Workstation/Pi test results and the final clean-checkout checks are recorded in
the release PR and its CI. The earlier 439-test/100-lab native receipt remains
a dated result rather than being silently rewritten.

## Completed release checks

| Host / route | Result |
|---|---|
| Workstation, Python 3.12 | 483 tests; 110 exact example reruns; Ruff, mypy (40 modules), repository/link validation and approved-source export pass |
| Pi, Python 3.13.5 | 483 tests; 110 exact reruns; repository validation; every card page and all six BA1 restores pass |
| Independent Pi image build | Image **and complete build receipt** match the workstation byte for byte |
| Fresh checkout with CRLF policy and a new venv | 483 tests, 110 exact reruns, validation, mypy and the off-device demo pass; Git status stays clean |

The [machine-readable check record](prehardware-checks.json) identifies the
source/capture manifests and candidate image. Clean-checkout review caught
missing LF policy for the assembly source; it is now explicit. The documented
venv is ignored by Git. The Pi finished at 49.4 C with throttled flags 0x0.
No installed-release update follows from staging this source on the SSD.
