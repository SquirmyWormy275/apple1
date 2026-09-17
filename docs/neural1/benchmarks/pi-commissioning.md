# Raspberry Pi commissioning benchmark

Use an explicit absolute output path. A diagnostics-only command is:

```sh
python -m neural1.benchmark --hardware-report --output /absolute/private/native-hardware.json
```

This records the native host's model (when available), architecture, memory,
Python/runtime Git revision, CPU governor, thermal readings, throttling status,
free space and elapsed time. It does not identify that host as the intended Pi.
Power supply and cooling observations must come from the operator. Existing
report files are never overwritten.

Workloads require the commissioned SSD's real mount root and filesystem UUID:

```sh
python -m neural1.benchmark --output /mnt/neural1-ssd/logs/benchmark.json \
  --ssd-root /mnt/neural1-ssd --expected-uuid ACTUAL_FILESYSTEM_UUID
```

Use the deployment's actual paths and UUID. The command verifies mount identity,
role and free space before workload stages and refuses fallback report writes
if that volume disappears. It measures one world, snapshot/restore and bounded
1/4/16-world scaling. Its default is 1000 monitor operations; no physical I/O is
opened. Results and snapshots remain under the explicit output path.

Add `--registry /absolute/deployment-registry.json --model MODEL_ID` for a single
provider response capped at 64 output tokens and a 30-second transport timeout.
The report includes exact provider `ModelRecord`, prompt/error/token counts and
mean latency, with raw provider recording alongside the artifacts. No token rate
is invented when backend timing is absent. This diagnostic response does not
establish strict-parser or scientific acceptance. Models are tested one at a
time; no concurrent residency is assumed.

Temperature and memory checks stop new benchmark stages (default 75 C and
256 MiB available RAM). They are **not** continuous inference thermal control.
Use the installed application's monitored bounded runner for end-to-end thermal,
parser, family, lifecycle and persistence acceptance. A standalone benchmark
report cannot replace those gates or actual Pi identity verification.
