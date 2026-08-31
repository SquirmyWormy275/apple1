# Runtime performance

`python -m neural1.benchmark` measures WozMon transaction throughput and
snapshot/restore cost on the current host. Results include iteration count and
artifact bytes. They are environment-local diagnostics, not Raspberry Pi or
physical Apple-1 claims. Model latency/token rate is `NOT MEASURED` until a
provider is explicitly benchmarked. Record CPU, RAM, OS, Python, storage,
provider/model hash, concurrency, thermal state, and raw output for Pi runs.
