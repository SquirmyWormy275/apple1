# Multiverse JSON transport

The installed 1976 MULTIVERSE worker sets `format: "json"` only in its effective Ollama run registry. Ollama receives this as a top-level request field, as documented in its [chat API](https://docs.ollama.com/api/chat). Other family defaults and qualified source registries retain their existing settings.

The effective registry, provider model record, and response metadata retain the requested format. The adapter preserves the exact model response; Markdown fences are not stripped and strict proposal parsing remains unchanged. JSON syntax is not domain acceptance: unsupported components, memory sizes, or configurations remain negative scientific results. Earlier fenced responses remain recorded failures.
