# Model runtime

`ModelProvider.generate(prompt, agent_id, seed)` returns text plus optional
token, latency, and backend metadata. `ModelRecord` captures provider, family,
exact name, version/hash when available, quantization, context limit, and
generation settings. Fake and replay providers are implemented. Ollama,
llama.cpp, and Hailo remain adapters to commission later; no backend fallback
may open hardware or silently call a cloud service.

Many logical agent IDs may share one provider. Their context belongs to the
experiment scheduler, not to distinct copies of model weights. Throughput and
feasible Pi model sizes remain unmeasured.

Implemented opt-in providers are localhost Ollama HTTP and bounded llama.cpp
process execution. Both accept injectable transports for tests. llama.cpp uses
an argument array, `shell=False`, and a timeout. `RecordingProvider` appends
exact prompts, agent IDs, seeds, model records, results, token/latency metadata,
and structured errors; replay refuses absent tuples.
