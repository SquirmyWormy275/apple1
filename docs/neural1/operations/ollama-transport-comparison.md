# Explicit Ollama transport comparison

Status: **software-tested; native chat comparison and acceptance pending**.
Nothing here establishes that changing transports fixes model formatting.

The default remains `/api/generate`, sending `prompt` and reading the exact
`response` string. Setting `generation_defaults.api` to `chat` explicitly selects
`/api/chat`, sends one user message containing the existing bounded prompt, and
reads `message.content`. This follows Ollama's [generate](https://docs.ollama.com/api/generate)
and [chat](https://docs.ollama.com/api/chat) API contracts. The adapter keeps no
conversation history; each logical participant receives only its own assembled
prompt. There is no automatic transport fallback.

Optional `generation_defaults.keep_alive` is a top-level request field on both
endpoints, not a generation option. Omitting it preserves server defaults. The
factory separates `api`, `base_url`, `timeout_seconds` and `keep_alive` from
sampling options. Do not modify a deployment's qualified transport until actual
native requests, response records and strict-parser outcomes have been compared.

The returned text is unchanged, including whitespace and malformed command text.
The adapter does not extract command arrays from model-generated JSON, insert
missing commands, repair bytes or supply fallback responses. Each successful
HTTP result retains the original UTF-8 response body, its SHA-256, parsed server
metadata, endpoint, seed and stop reason for review. RecordingProvider therefore
preserves the raw provider evidence alongside the actual text sent to the parser.

Providers built from qualified registries record the manifest digest,
quantization, family and effective requested context in ModelRecord. The digest
is labelled as an **Ollama manifest**, not the underlying GGUF weight blob.
These fields preserve registry identity; they do not independently rehash model
weights or replace the installed application's live manifest check. Direct
unqualified adapter construction retains unavailable identity fields.

Software tests use synthetic HTTP responses only. They verify default request
compatibility, explicit chat routing, top-level residency, isolated messages,
raw text preservation, malformed response rejection and qualified record fields.
No model was downloaded or run on the development host for this change.
