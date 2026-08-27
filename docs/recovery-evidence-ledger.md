# Firmware recovery evidence ledger

Status: **not eligible for EEPROM programming**.

The manufacturer `110REV03` archive is a hash-verified source candidate only.
It is not an EEPROM readback, not a recovery image, and not authorization to
compile for a device load. This ledger is the required evidence index before a
future RAM-only evaluation can even be proposed.

| Gate | Required evidence | Current state | Evidence path / SHA-256 |
|---|---|---|---|
| Board identity | Revision, labels, and photo record | Partial | `docs/hardware/plus-io-map.md` |
| Candidate provenance | Source URL, immutable archive, per-file hashes | Present | `firmware/vendor/110REV03/provenance.json` |
| Installed-image proof | EEPROM readback or manufacturer-confirmed exact image | Missing | — |
| Recovery image | Revision-compatible binary/image, distinct from source | Missing | — |
| Recovery provenance | Origin, license, retrieval date, hash | Missing | — |
| Toolchain | Versioned compiler/uploader installed and verified off-device | Missing | — |
| Recovery rehearsal | RAM load and restore observed with captured result | Missing | — |
| Reset/open cause | Measured control, USB, and board-path evidence | Blocked at STOP | `docs/troubleshooting.md` |
| RAM-only acceptance card | Video, PS/2, both serial paths, reset/cold-boot checks | Not started | — |
| EEPROM authorization | Explicit user approval after all preceding gates | Not requested | — |

## Rules for updating this ledger

- Add evidence, never overwrite an earlier result. Corrections reference the
  earlier row and explain the new measurement.
- A source checksum proves only the bytes copied into the repository. It does
  not prove what the board executes.
- A recovery image requires two retained copies, independent SHA-256 checks,
  documented revision compatibility, and a rehearsed restore before any
  persistent-write discussion.
- An EEPROM row may be marked eligible only after an explicit user approval;
  this file itself grants no authority.
