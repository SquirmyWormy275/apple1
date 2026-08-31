# Model comparison

TinyLlama is intentionally retained as the weak/small baseline. Differences are observations within this pilot, not general model rankings. Exact locally qualified identities appear below. Per-model outcome aggregates follow.

| ID | FAMILY | ROLE | BACKEND | NAME | PARAMETERS | QUANT | CONTEXT | SHA-256 | LICENSE |
|---|---|---|---|---|---|---|---|---|---|
| qwen25-coder-15b | qwen2.5-coder | coding-small | ollama | qwen2.5-coder:1.5b | 1543714304 | Q4_K_M | 32768 | d7372fd828518a4d38b1eb196c673c31a85f2ed302b3d1e406c4c2d1b64a0668 | Apache-2.0 (local GGUF metadata and bundled license layer) |
| smollm2-17b | smollm2 | general-small | ollama | smollm2:1.7b | 1711376384 | Q8_0 | 8192 | cef4a1e09247f018ca0c482ad4c2ce1474aba5e87f245dacf97f07948d05d8b4 | Apache-2.0 (local GGUF metadata and bundled license layer) |
| tinyllama-11b | tinyllama | weak-small-baseline | ollama | tinyllama:1.1b | 1100048384 | Q4_0 | 2048 | 2644915ede352ea7bdfaff0bfac0be74c719d5d5202acb63a6fb095b52f394a4 | NOT REPORTED BY LOCAL OLLAMA MODEL METADATA |

| MODEL | CELLS | TURNS | TOKENS | VALID ACTIONS | INVALID/PROSE | ERRORS | MODEL SECONDS |
|---|---|---|---|---|---|---|---|
| qwen25-coder-15b | 3 | 72 | 15281 | 0 | 72 | 0 | 45.692 |
| smollm2-17b | 3 | 72 | 20243 | 0 | 72 | 0 | 124.641 |
| tinyllama-11b | 1 | 12 | 3150 | 0 | 12 | 0 | 6.429 |

The Qwen and SmolLM2 rows each cover three completed 4K MIND seeds. The
TinyLlama row is one cancelled six-generation cell, so no matched three-family
outcome comparison is valid. Token and latency differences are descriptive and
confounded by model architecture, quantization, warm-up/load behavior, and the
thermal stop.
