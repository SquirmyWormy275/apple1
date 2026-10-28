# 7. Understand a local language model before connecting it

A language model turns tokenized context into probable next tokens. Its text is
not an execution trace. NEURAL1 turns selected output lines into constrained
machine proposals and checks them independently. The model runs on the modern
host; the virtual 6502 does not contain its weights.

## The pieces of an inference stack

| Piece | What it contributes |
|---|---|
| Model weights | Learned numerical parameters |
| Tokenizer | Mapping between text and model-specific token sequences |
| Runtime/provider | Loading, request handling, generation, and accounting |
| Prompt/context | Current instructions, objective, and allowed observations |
| Parser | The accepted proposal syntax |
| World/evaluator | Deterministic execution and task criteria |
| Recording | Exact requests/responses and their provenance |

Run L01 before confusing tokens with words, characters, or Apple-1 bytes. An
Ollama reply can report prompt and output token counters; the adapter should
retain them rather than estimate them from word count. The L01 counters are
explicitly synthetic API metadata supplied by the mock.

## Quantization and memory

A nominal weight estimate is parameter count times bits per parameter divided
by eight. L02 computes 750,000,000 nominal bytes for 1.5 billion four-bit weights.
That is not total process RAM. Quantization metadata/scales, activations, runtime
buffers, and context/KV storage add overhead. A longer context can increase
resource use. Measure the identified runtime rather than promising a model will
fit from this arithmetic alone.

A GGUF file is an artifact format; a quantization label is not a complete model
identity. A friendly tag such as `latest` may change. A manifest digest and a
weight digest identify different objects. L05 teaches that distinction without
inventing licenses or qualified real-model metadata.

## Context is not durable machine memory

A model's conversation can be reset while virtual RAM persists. That separation
is an experimental factor in 4K MIND. Preserving a byte is easy to demonstrate;
showing that a fresh model can recover its meaning needs an actual experiment.
Run L03 and F15. Keep each agent's private observations separate even when
agents share weights or an allowed RAM world.

## Connect through a bounded interface

The local Ollama API uses the loopback server, normally
`http://localhost:11434/api`. `/api/tags` lists model records and digests;
`/api/generate` accepts a model, prompt, generation options, and streaming choice.
See the primary [API introduction](https://docs.ollama.com/api/introduction),
[model-list endpoint](https://docs.ollama.com/api/tags), and
[generation endpoint](https://docs.ollama.com/api/generate), checked October 27, 2026.
The project adapter validates local endpoints and bounds requests.

F21 exercises the actual request constructor with a mock opener. It performs no
inference. A real local run requires an installed provider, an available model,
qualified registry identity, resource bounds, and retained recordings. This
book build did not find a local Ollama service on the workstation, so its native
example is the retained, identified Pi run in F16/L06, not a new inference claim.

On the already commissioned Pi, use `MODELS`, inspect the registry choice, and
select a qualified ID with `MODEL model-id`; then use a bounded preset. Follow
the recorded operator guide for its installed revision. Do not download models,
change storage, or repeat commissioning merely to read this book.

## Evaluate the proposal

L04 demonstrates that prose, assembly mnemonics, and host shell text do not
become host actions. A syntactically accepted Monitor command can still implement
the wrong behavior. L08 requires both an authored positive control and a failing
negative control. A fixed seed is one input, not a guarantee of portability
across different weights, runtime builds, sampling settings, or hardware.

## Practice

Explain the complete path from prompt to accepted command to memory readback.
Name at least one failure at each boundary. Then compare a fixed-response run,
a mock-transport run, exact replay, and real-model inference. A good report labels
which one actually happened.

[Textbook home](../README.md) · [Previous chapter](06-algorithms-basic-and-creative-computing.md) · [Next chapter](08-experiments-and-controls.md)
