# Raspberry Pi commissioning benchmark

Run `python -m neural1.benchmark` on the final host and retain raw JSON with
runtime Git revision, platform, machine, Python, CPU governor, memory/storage,
power supply, thermal state, and elapsed wall time. The provider benchmark adds
exact `ModelRecord`, prompt count, errors, token counts where supplied, and mean
latency. It does not compute token rate when backend timing is absent.

Benchmark one world, snapshot/restore, increasing world counts, and logical
agent schedules separately. Then test model families sequentially so residency
is not assumed. No camera or physical Replica interface is involved.
