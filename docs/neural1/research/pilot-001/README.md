# NEURAL1 Pilot 001

**Status:** MODEL-VALIDATED PILOT — NOT AUTOMATICALLY ESTABLISHED SCIENTIFIC FINDINGS

Pilot 001 exercised the frozen NEURAL1 campaign infrastructure against three local small-model families. Machine-readable campaign records and release-bundle hashes are authoritative; this package interprets them.

## Completion

- Campaign: `N1-P-057141928BD15B0C`
- Matrix cells: 45
- Completed: 6
- Incomplete/cancelled/not started: 39
- Seeds: 101, 211, 307
- Recorded turns: 156
- Recorded tokens: 38674
- Errors: 0
- Initial invocation wall time: 162.323 seconds
- Controlled resume invocation wall time: 15.639 seconds
- Total campaign-process wall time: 177.962 seconds
- Aggregate recorded model latency: 176.761 seconds
- Generated: 2026-08-31T04:07:16.966264+00:00

## Evidence interpretation

All automatically summarized phenomena are **OBSERVED** or **CANDIDATE DISCOVERIES**. No correlation, anomaly, convergence, or one-off structure is upgraded to causality or generality. Intervention-supported and replicated labels require their corresponding structured records.

## Outcome at a glance

Pilot 001 was cooperatively stopped when the host's TCPU and x86 package
sensors reached 102 C. Six of 45 cells completed; one TinyLlama cell retained a
six-generation cancelled checkpoint; 38 cells were not started. A bounded
resume completed the interrupted SmolLM2 cell from generation 9 without
changing its first 18 transcript records. This supplies real-model evidence
that checkpoint/resume plumbing works for that one cell, not a general
equivalence result.

Across 156 recorded turns, the strict parser accepted zero model responses as
WozMon commands. Responses commonly invented `LOAD`, emitted assembly/prose,
or asserted capabilities that WozMon does not have. This is a negative result
for the tested prompt/provider/model configurations. It is not evidence that
these model families can never operate WozMon, and it does not justify changing
the parser after seeing outcomes.

Qwen completed three matched 4K MIND seeds, SmolLM2 completed three, and
TinyLlama produced a partial cell only. The thermal stop therefore prevents the
planned three-family comparison and prevents conclusions about the other four
experiment families.

## Runtime metadata

```json
{
  "campaign_runtime_commit": "2097423645c549a5cfff1827838022b8b71fca10",
  "host": {
    "gpu": "NVIDIA GeForce RTX 4070 Laptop GPU",
    "gpu_memory_mib": 8188,
    "kernel": "Linux 7.1.9-arch1-2 x86_64",
    "nvidia_driver": "610.57.04",
    "python": "3.14.7"
  },
  "llama_cpp": {
    "archive_sha256": "91d7b03ddae498a39f28fdb85d84d2b4a0fd3838d10b4f897e0ef8975bb9b583",
    "build": 10621,
    "commit": "c1d0e7a00",
    "version": "0.3.0-dev"
  },
  "ollama": {
    "archive_sha256": "9785247dea264d9072f09f6c9c0eb4b8e666892826a3d8388eba3e8fb9ed1db9",
    "host": "127.0.0.1:11434",
    "keep_alive": "5m",
    "version": "0.33.2"
  },
  "pilot_execution": {
    "completed_cells": 6,
    "initial_invocation_seconds": 162.32332514799782,
    "matrix_cells": 45,
    "resume_invocation_seconds": 15.638716465997277,
    "resume_result": "interrupted cell completed from generation 9 checkpoint",
    "stop_reason": "cooperative cancellation after TCPU/x86 package sensors reached 102 C",
    "wall_clock_ceiling_seconds": 43200
  },
  "provider_qualification": {
    "llama_cpp": "qualification/llama-cpp.json",
    "ollama": "qualification/ollama.json"
  },
  "safety": {
    "cameras": false,
    "cffa1_writes": false,
    "eeprom_writes": false,
    "firmware_loading": false,
    "gpio": false,
    "physical_serial_opened": false,
    "target": "VIRTUAL"
  }
}
```

## Thermal/performance observations

The GPU rose from 45 C idle to 71 C, used about 3998 MiB, and peaked at 96%
sampled utilization. TCPU/x86 package samples rose from 65 C to 102 C; the
campaign then cancelled at a generation boundary. Sensors returned to roughly
73--76 C after model shutdown. The raw samples follow.

```text
{"monotonic_seconds": 113426.005527399, "nvidia": {"memory_used_mib": "4", "power_w": "2.14", "temperature_c": "45", "utilization_percent": "0"}, "recorded_at": "2026-08-31T04:02:27.496295+00:00", "thermal_zones_c": {"thermal_zone0": 54.0, "thermal_zone1": 20.0, "thermal_zone10": 46.0, "thermal_zone2": 51.05, "thermal_zone3": 46.05, "thermal_zone4": 46.05, "thermal_zone5": 40.05, "thermal_zone6": 48.05, "thermal_zone7": 65.05, "thermal_zone8": 65.0, "thermal_zone9": 65.0}}
{"monotonic_seconds": 113456.036636032, "nvidia": {"memory_used_mib": "1273", "power_w": "39.87", "temperature_c": "64", "utilization_percent": "94"}, "recorded_at": "2026-08-31T04:02:57.527404+00:00", "thermal_zones_c": {"thermal_zone0": 86.0, "thermal_zone1": 20.0, "thermal_zone10": 46.0, "thermal_zone2": 56.05, "thermal_zone3": 66.05, "thermal_zone4": 58.05, "thermal_zone5": 40.05, "thermal_zone6": 1.05, "thermal_zone7": 73.05, "thermal_zone8": 73.0, "thermal_zone9": 73.0}}
{"monotonic_seconds": 113486.085732931, "nvidia": {"memory_used_mib": "3998", "power_w": "39.99", "temperature_c": "67", "utilization_percent": "96"}, "recorded_at": "2026-08-31T04:03:27.576505+00:00", "thermal_zones_c": {"thermal_zone0": 89.0, "thermal_zone1": 20.0, "thermal_zone10": 46.0, "thermal_zone2": 62.05, "thermal_zone3": 70.05, "thermal_zone4": 64.05, "thermal_zone5": 42.05, "thermal_zone6": 1.05, "thermal_zone7": 100.05, "thermal_zone8": 99.0, "thermal_zone9": 99.0}}
{"monotonic_seconds": 113516.126677455, "nvidia": {"memory_used_mib": "3998", "power_w": "40.13", "temperature_c": "69", "utilization_percent": "61"}, "recorded_at": "2026-08-31T04:03:57.617452+00:00", "thermal_zones_c": {"thermal_zone0": 92.0, "thermal_zone1": 20.0, "thermal_zone10": 45.0, "thermal_zone2": 65.05, "thermal_zone3": 72.05, "thermal_zone4": 67.05, "thermal_zone5": 43.05, "thermal_zone6": 1.05, "thermal_zone7": 90.05, "thermal_zone8": 90.0, "thermal_zone9": 90.0}}
{"monotonic_seconds": 113546.169833147, "nvidia": {"memory_used_mib": "3998", "power_w": "40.15", "temperature_c": "70", "utilization_percent": "96"}, "recorded_at": "2026-08-31T04:04:27.660603+00:00", "thermal_zones_c": {"thermal_zone0": 96.0, "thermal_zone1": 20.0, "thermal_zone10": 44.0, "thermal_zone2": 66.05, "thermal_zone3": 72.05, "thermal_zone4": 68.05, "thermal_zone5": 44.05, "thermal_zone6": 1.05, "thermal_zone7": 99.05, "thermal_zone8": 99.0, "thermal_zone9": 99.0}}
{"monotonic_seconds": 113576.212233012, "nvidia": {"memory_used_mib": "3998", "power_w": "40.18", "temperature_c": "71", "utilization_percent": "61"}, "recorded_at": "2026-08-31T04:04:57.703000+00:00", "thermal_zones_c": {"thermal_zone0": 96.0, "thermal_zone1": 20.0, "thermal_zone10": 44.0, "thermal_zone2": 67.05, "thermal_zone3": 73.05, "thermal_zone4": 70.05, "thermal_zone5": 45.05, "thermal_zone6": 1.05, "thermal_zone7": 102.05, "thermal_zone8": 102.0, "thermal_zone9": 102.0}}
{"monotonic_seconds": 113606.238948261, "nvidia": {"memory_used_mib": "3998", "power_w": "15.73", "temperature_c": "62", "utilization_percent": "0"}, "recorded_at": "2026-08-31T04:05:27.729716+00:00", "thermal_zones_c": {"thermal_zone0": 86.0, "thermal_zone1": 20.0, "thermal_zone10": 44.0, "thermal_zone2": 67.05, "thermal_zone3": 65.05, "thermal_zone4": 68.05, "thermal_zone5": 46.05, "thermal_zone6": 1.05, "thermal_zone7": 74.05, "thermal_zone8": 74.0, "thermal_zone9": 74.0}}

```

See the linked methodology, matrix, comparisons, results, META findings, negative results, limitations, reproduction record, and follow-up experiments in this directory.
