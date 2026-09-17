# Sanitized NEURAL1 closeout evidence

These extracts reuse completed commissioning evidence. No experiment, setup or
power test was repeated to publish them. See the [consolidated report](../../pi-closeout-2026-09-10.md).

- `completion-gates.json`: completion gates, preservation totals, limited downloads and limitations.
- `deployment-comparison.json`: recorded deployed revision and read-only comparison of 39 runtime source hashes.
- `startup-observation.json`: actual absent-SSD boot and automatic arrival observations; private machine identifiers omitted.
- `post-boot-run.json`: actual three-turn run, responses/parser outputs, deterministic execution, resource summary and original artifact hashes.
- `independent-review.json`: independent review of retained native evidence, with replay scope stated.
- `SHA256SUMS`: hashes of these published extracts and this README.

The original evidence remains in private commissioning storage and the Pi SSD's
`runs/console/campaigns/N1-P-5898735E8998CC35/` and `logs/commissioning-r3/`.
Original-file hashes embedded in extracts refer to those retained originals, not
to redacted JSON. The original proof bundle is in SSD `exports/` with run prefix
`N1-P-5898735E8998CC35-1789098479672419399`; the corresponding META claim is
`N1-C-5DA21D6803488059`. These hashes permit comparison when an authorized operator
has the originals; the public extracts do not replace a full private proof bundle.
