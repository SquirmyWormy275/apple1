# Firmware recovery evidence ledger

Current status: **recovery package and physical acceptance pending**. No EEPROM
was programmed by the October 28 history consolidation.

## Preserved-original repair route — October 28 reconciliation

The later September 12–13 conversation accepted a bounded recovery attempt,
without making complete root-cause measurement or a scope purchase mandatory.
Use the [current repair plan](hardware/replica-repair-plan.md), tracked in
[issue #17](https://github.com/SquirmyWormy275/apple1/issues/17).

| Requirement | Current evidence / remaining work |
|---|---|
| Board identity | [Eight recovered historical photographs](hardware/repair-context-2026-10-28/README.md) visibly establish Revision 0/ReActiveMicro/P8X32A-D40. Match present setup; selector/routing and voltages remain unmeasured. |
| Candidate provenance | `firmware/vendor/110REV03/provenance.json` present. Candidate source is not an installed-image identification or compiled recovery package. |
| Basic electrical suitability | New session must check supply, selector function and nominal 5V/3.3V rails before device loading. DC readings do not exclude transients. |
| Compatible recovery package | Still missing: versioned toolchain/uploader, exact commands, revision-compatible binary, hashes, two verified copies and inspectable rollback. |
| Preserve original | Remove only under the reviewed unpowered procedure; label/store original EEPROM unchanged. Compatible spare 24LC256 DIP-8 provides the persistent trial target. No installed-image readback is required to propose this route. |
| Active-image identity | Record RAM versus EEPROM boot and whether a Propeller reset discarded the temporary image. Avoid interpreting an old-image reboot as a candidate test. |
| Finite acceptance | Pending: three cold boots, five normal serial connections, local keyboard, both serial directions and CFFA1 operation. |
| Live execution | This documentation performs none. The next session needs its actual compatible package, current setup and reviewed procedure; preserve the original throughout. |

Successful recovery can restore use without proving the old EEPROM corrupt.
A failed bounded attempt leads to vendor repair/replacement, not unlimited gates
or purchases. The untouched original provides physical rollback to the old boot
path. It does not prove a healthy image or replace verification of the new one.

## Earlier original-EEPROM programming ledger

The following table preserves the older gate state. Its requirement to measure
reset/open cause before even proposing a RAM comparison is superseded **for the
preserved-original/spare route above**. Installed-image identity remains unknown;
that is an honest limit, not a reason to overwrite the original or prevent a
compatible spare trial. The stricter original-overwrite route is not enabled.

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

## Rules for updating the original-overwrite ledger

- Add evidence, never overwrite an earlier result. Corrections reference the
  earlier row and explain the new measurement.
- A source checksum proves only the bytes copied into the repository. It does
  not prove what the board executes.
- A recovery image requires two retained copies, independent SHA-256 checks,
  documented revision compatibility, and a rehearsed restore before any
  persistent-write discussion.
- An EEPROM row may be marked eligible only after an explicit user approval;
  this file itself grants no authority.
