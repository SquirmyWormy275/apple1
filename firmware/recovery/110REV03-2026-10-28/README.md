# Staged Replica 1 Plus recovery — 110REV03

**Built and verified on the laptop; on-board recovery remains paused.** This is
a controlled vendor-baseline recovery candidate. A successful build does not
establish that the installed firmware was corrupt or that this image fixes the
serial-open fault.

[Loading procedure](LOADING.md) · [Build record](build-record.json) ·
[Checksums](SHA256SUMS) · [Download bundle](../releases/README.md) ·
[Repair issue #17](https://github.com/SquirmyWormy275/apple1/issues/17)

## Ready files

| File | Purpose |
|---|---|
| [replica-110REV03.binary](images/replica-110REV03.binary) | **6,992 bytes**. Input to the staged serial loader for both RAM and spare-EEPROM modes. |
| [replica-110REV03.eeprom](images/replica-110REV03.eeprom) | **32,768 bytes**. Complete compiler-produced EEPROM layout for inspection/compatible external tooling; the serial commands use the `.binary` file. |
| [Linux x86-64 tools](bin/linux-x86_64/) | Built OpenSpin compiler and PropLoader uploader for this laptop. Neither runs automatically. |
| [Pinned source archives](sources/) | Exact OpenSpin/PropLoader source snapshots for rebuilding without a network download; vendor source remains under `firmware/vendor/110REV03/`. |
| [Manifest](manifest.json) and [logs](logs/) | Per-file hashes, build/loader evidence and tool help. |
| [Bench record template](bench-session-template.json) | Blank physical setup, observations, image identity and acceptance record. |

Program SHA-256:
`aa024b93ea3294b70e88992b5b002a46958c617873a330b82e87feaa26e7d0a5`

EEPROM SHA-256:
`3d6238f3cfba84667e2747572a1ef1f71da77b6f5225af7f6926145d2c3b7686`

## Verify without touching hardware

From the repository root, or the extracted bundle's top directory:

```bash
python3 tools/replica_recovery.py verify
sha256sum -c firmware/recovery/110REV03-2026-10-28/SHA256SUMS
```

`verify` checks package/source/tool hashes, P1 header/pointers, clock settings,
checksum, initial call frame and EEPROM padding. It opens ordinary files only.
`commands` prints future loader commands; it never runs them. `rebuild` compiles
software and never opens a serial port. None of these modes uploads firmware.

## Rebuild offline

Requires Linux, Python 3.12+, GNU Make, GCC/G++ (or Clang/Clang++), and standard
C/C++ headers/libraries. The source archives are already included. Choose an
output directory that does not exist:

```bash
python3 tools/replica_recovery.py rebuild --out /tmp/apple1-recovery-rebuild
```

This builds the compiler and loader, creates a separate vendor-source stage,
compiles both images and **requires byte equality with the staged images**.
The output includes logs and `rebuild-report.json`. On another Linux architecture,
including a Pi, use its locally rebuilt `proploader-linux-build/bin/proploader`;
the bundled x86-64 executable cannot run on ARM. No Pi was changed by this work.

The supplied laptop executables are dynamically linked: OpenSpin requires
GLIBC symbols through **2.43**, PropLoader through **2.42**, plus the recorded
libstdc++/C++ ABI symbols. Older Linux systems need a local source rebuild.
Exact runtime requirements are in `build-record.json`. Tool executable hashes
can differ across host/compiler versions; firmware image equality is the check.

## Provenance and checks performed

- All nine preserved vendor source hashes passed before/after compilation.
- OpenSpin `d1991aa821179209cbd21396dfd1d88f226eb99d`, version 1.00.81;
  PropLoader `a1b4cd87cedfb1141d9be888335bca130b486425`.
- Separate clean GCC and Clang builds of these pinned tools produced identical
  program and EEPROM images. Both use OpenSpin's compiler implementation;
  this is not a comparison against the old Windows Propeller Tool binary.
- Four filename-case aliases exist **only in temporary build stages**:
  `fullduplex.spin`, `keyboard.spin`, `aigeneric_driver.spin`, `Font_ATARI.spin`.
  Their targets and exact source hashes are recorded. Vendor bytes were not edited.
- PropLoader's own image-validation/configuration path accepted both image
  formats. RAM/spare-EEPROM command variants then failed as expected against an
  explicitly nonexistent private path. A corrupted-image control was rejected
  before port opening. These tests do not exercise a serial handshake or EEPROM.
- `SOURCE_DATE_EPOCH=1793145600` fixes the tool build date to October 28 UTC.
  The original archive's `-t` tree-only compiler option returns nonzero; successful
  `-b`/`-e` build logs retain the object tree without relying on that status.
- A fresh vendor RAR download is retained with a hash. It is a source-provenance
  reference, not the build input or a proof of the installed EEPROM contents.

See [notices](NOTICE.md) for third-party attribution. [The main repair plan](https://github.com/SquirmyWormy275/apple1/blob/main/docs/hardware/replica-repair-plan.md)
retains the time/cost limits, optional diagnostics, substitution and vendor exits.
The physical session still needs current board/interface matching, power readings,
a verified programming reset route, a compatible spare EEPROM and operator
observation. No additional root-cause or oscilloscope campaign is imposed.
