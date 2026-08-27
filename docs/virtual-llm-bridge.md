# Virtual Apple-1 LLM bridge

`tools/virtual_bridge.py` is the complete software-side rehearsal path for the
Apple-1 terminal project. It runs a RAM-program in the local 6502 harness,
obtains a response from either a deterministic demo reply or an explicitly
selected local Ollama model, formats it for 40 columns in upper-case printable
ASCII, and records an optional JSONL transcript.

It never imports `serial_owner`, enumerates a COM/TTY device, opens the FT232R,
or writes firmware. `serial_opened` is always `false` in its output.

## Deterministic demo

```powershell
python .\tools\virtual_bridge.py `
  --program .\software\ram-only\line-input-0300.hex `
  --input "ASK`r" `
  --reply "The virtual terminal is ready." `
  --transcript .\out\virtual-demo.jsonl
```

## Local-model rehearsal

Only use this after Ollama is intentionally installed and a local model is
available. The command has no fallback to cloud services or serial hardware.

```powershell
python .\tools\virtual_bridge.py `
  --program .\software\ram-only\line-input-0300.hex `
  --input "WHAT IS A TRANSISTOR?`r" `
  --ollama phi4-mini
```

The virtual result proves only the software protocol and output presentation.
It does not establish serial timing, Propeller behavior, an Apple-1 display
path, or authorization for a live-device session.
