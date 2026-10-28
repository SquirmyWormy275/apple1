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
