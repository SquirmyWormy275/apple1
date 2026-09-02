# External display-video evidence record

The display was an Eyoyo LCD. The MOV bytes are not stored in this repository and were not available to Codex during packet closure. The hashes and observations below were supplied by the preceding assistant session, which reported direct frame inspection. Frame-exact synchronization with the logic trace is not claimed.

| File | Duration | Observed size | SHA-256 | Custody | Reported observation |
|---|---:|---:|---|---|---|
| `IMG_1353.mov` | 62.73 s | 60.7 MB | `daa8c84f62bdcc12e59a513ca72d3689745b4ccfafda10dac64640e864871ae1` | Operator iPhone; preceding assistant sandbox | Eyoyo LCD with dense pseudo-random ASCII and no clean Monitor prompt. The long clip includes blank blue at approximately 30 s and full garbage at approximately 50 s, spanning more than one visible display state. |
| `IMG_1354.mov` | 9.87 s | 10.8 MB | `2c72eeb1af73cb76aaabc3f21ad2ffaeb83617aab2beca960dd754965d7061bb` | Operator iPhone; preceding assistant sandbox | Eyoyo LCD showing dense pseudo-random ASCII and no clean Monitor prompt. |

These videos corroborate the observed display state and change. They do not measure analog voltage, establish a reset transition, or provide frame-exact trace synchronization. If verified MOV copies later enter this packet, recompute and compare their hashes, add them to `SHA256SUMS`, and update custody and portability status. That archival upgrade does not require another hardware run and does not change the scientific result.
