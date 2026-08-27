# Apple1 Replica 1 Plus

This repository preserves evidence and off-device tooling for a Replica 1 Plus
serial investigation. It does not authorize a firmware load, EEPROM write,
temporary wiring, soldering, or other physical modification.

## Start here

- [Preservation dossier](docs/preservation-dossier.md): collection inventory,
  chain of custody, and hard safety boundaries.
- [Firmware baseline](docs/firmware-baseline.md) and
  [recovery evidence ledger](docs/recovery-evidence-ledger.md): candidate-source
  provenance and the gates that still block any persistent firmware action.
- [Serial troubleshooting](docs/troubleshooting.md) and
  [capture protocol](docs/serial-test-protocol.md): the current live STOP
  result and the next evidence gate.
- [Read-only support bundle](docs/host-support-bundle.md): portable, explicit
  evidence collection with hashes and no serial-device access.
- [Firmware behavior model](docs/firmware-behavior-model.md): executable
  pre-change contract for a future single-writer candidate.
- [RAM-only software library](docs/apple1-software-library.md) and
  [emulator/demo guide](docs/emulator-demo-guide.md): safe software rehearsal
  and deterministic terminal formatting.

## Verification

```powershell
python -m pytest tests -q
```
