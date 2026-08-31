# Provenance and rights audit — 2026-08-30

## Purpose

This report classifies the repository's major external/historical source families by identity, provenance, rights state, and authority. It does not invent missing licenses or treat ownership of a physical object as copyright permission.

Status vocabulary:

- **COMPLETE FOR CURRENT ROLE** — enough provenance exists for how the repository currently uses the material.
- **INCOMPLETE** — identity/provenance fields remain unresolved.
- **BLOCKED** — project policy forbids promotion/use until a named gate is satisfied.
- **RIGHTS REVIEW NEEDED** — source identity may be known, but redistribution/reuse rights are not established.
- **HASH ACQUISITION NEEDED** — source is identified but the policy-required local artifact/hash has not been captured.

## Audit table

| Source family | Location / record | Identity / hash | Rights state | Authority state | Audit status |
|---|---|---|---|---|---|
| Replica 110REV03 candidate firmware | `firmware/vendor/110REV03/` + `provenance.json` | Source URL, archive filename, retrieval date, per-file SHA-256 | Firmware copyright/license is not asserted by the provenance record | Candidate only; explicitly not EEPROM readback | **COMPLETE FOR CURRENT ROLE**; do not promote to installed/recovery firmware |
| Original Lexar CF capture | `preservation/cf-card/2026-08-28/` | Preserved image/manifest; `.img` is Git LFS managed | Collection preservation record governs project copy; embedded third-party software rights may vary | Preserved baseline only | **COMPLETE FOR CURRENT ROLE**; never edit in place |
| Preserved manual copies | `preservation/manuals/2026-08-28/` | Filenames, byte counts, SHA-256 manifest; copied byte-for-byte | Public redistribution rights are not established merely by owner authorization to preserve supplied copies | Preservation/reference copies, not hardware/firmware authority | **RIGHTS REVIEW NEEDED** |
| Apple-1 Operation Manual as 1976 research source | acquisition ledger + preserved copy | Project copy SHA-256 recorded; claim extraction pending | Preservation record exists; external redistribution license not established in the display rights review | `HASH_VERIFIED_SOURCE; CLAIM EXTRACTION PENDING` | **BLOCKED for authoritative claims until review**; rights review remains separate |
| MOS MCS6500 Hardware Manual Jan. 1976 | 1976 source acquisition ledger | Candidate URL known; local acquisition not complete | All rights reserved / do not vendor without review | No authoritative rows | **HASH ACQUISITION NEEDED / BLOCKED** |
| Motorola M6800 May 1975 data book | 1976 source acquisition ledger | Candidate URL known; hash pending | Rights not established; do not vendor | No authoritative rows | **HASH ACQUISITION NEEDED / RIGHTS REVIEW NEEDED** |
| Other 1976 MULTIVERSE seed sources | `docs/neural1/research/1976-multiverse-source-seed.json` and ledgers | Mixed candidate/acquired state | Per-source status required | Research staging only | **INCOMPLETE by design**; follow source ledger |
| Apple1-Slideshow | `docs/reference/apple1-slideshow.md` | Upstream project, author, pinned commit `d436e3b...`, retrieval date | No license grant found at reviewed revision | Heritage reference only | **BLOCKED FROM REDISTRIBUTION** |
| Project ASCII/portal art | `art/` + `art/provenance/` | Project provenance records present | Project-authored unless record says otherwise | Source/derived project art | **COMPLETE FOR CURRENT ROLE** |
| Wikimedia display-history images | display image-rights ledger | Canonical source/license records | Public-domain-in-US or CC BY-SA terms documented per image | Remote embeds, not local binary authority | **COMPLETE FOR CURRENT ROLE**, subject to stated jurisdiction/license caveats |
| Smithsonian VM-4092/VM-4209 photos | display image-rights ledger | Object pages identified | “Usage Conditions Apply”; no CC0 grant relied upon | Link-only | **BLOCKED FROM COPYING** |
| Auction/Sotheby's/Christie's/Digibarn/Registry images | display image-rights ledger | Sources identified | No general republication grant established / item-specific rights | Link-only | **BLOCKED FROM COPYING** |
| eBay seller VM-4209 photos | collection accession + rights ledger | Listing source recorded | Purchase does not transfer image copyright | Link/reference only | **BLOCKED FROM COPYING**; replace with owner-created photos after receipt if desired |
| Future owner VM-4209 photos | `docs/collection/sanyo-vm-4209-1979/` plan | Not yet captured at audit | Photographer/license must be recorded when created | Future collection evidence | **INCOMPLETE / FUTURE** |
| FT232R no-transmit STOP capture | `docs/captures/2026-08-27-open-no-transmit-retry1.*` | Timestamped metadata/JSONL and device identities recorded | Project-generated evidence | Authoritative observation for the recorded event; electrical cause remains unverified | **COMPLETE FOR CURRENT OBSERVATION** |
| Logic-analyzer future capture | `docs/captures/logic-analyzer-*` | Templates/test card only | Project-authored | Prepared procedure, not executed evidence | **INCOMPLETE / NOT EXECUTED** |
| Pilot 001 | `docs/neural1/research/pilot-001/` | Campaign/run/model metadata and release-bundle evidence documented | Project-generated research package; external model licenses tracked separately in qualification | Model-validated pilot evidence, not generalized scientific findings | **COMPLETE FOR CURRENT ROLE** |

## Preserved manuals: unresolved redistribution issue

The preservation README says the five supplied PDFs were copied byte-for-byte after the repository owner authorized public GitHub preservation. That establishes project intent and chain of custody, but not necessarily permission from each document's copyright holder.

Separately, the display-history rights review treats the Apple-1 Operation Manual scan as link-only because no redistribution permission was established in that review. These statements are not the same kind of claim, but together they expose a rights gap that should remain visible.

This pass therefore:

1. keeps the preserved bytes and hashes unchanged;
2. does not invent a license;
3. does not reinterpret owner authorization as a copyright grant;
4. records **RIGHTS REVIEW NEEDED** for public redistribution of the external manuals.

Any future decision to remove public binaries, replace them with hash-only manifests, or document an applicable legal basis should be a separate preservation/rights decision with its own migration record.

## 1976 MULTIVERSE provenance gate

A historical candidate can move toward runtime authority only when its applicable gate is complete:

```text
exact source identity
+ acquired artifact
+ policy-required SHA-256
+ bounded claim extraction
+ human/reviewer claim check
+ cutoff/date eligibility
+ evidence quality/provenance
= eligible for explicit promotion decision
```

This is an eligibility test, not automatic promotion. Current authoritative runtime record count remains zero.

Unknown prices remain `null`; no model-generated estimate may fill a historical ledger gap.

## Derived-file parentage

The following parent/derived relationships are intentional and should remain navigable:

- preserved manuals -> source notes / research claims / educational citations;
- serial capture metadata -> troubleshooting interpretation;
- Field Library source notes + emulator logs -> learner-facing lesson explanations;
- Pilot machine-readable records -> Pilot human-readable interpretation package;
- display evidence/source ledgers -> display history / Sanyo interpretations;
- Apple1-Slideshow source record -> heritage design reference only, not vendored art.

## Remaining provenance work queue

1. Complete source acquisition/hashing for blocked high-value 1976 candidates.
2. Perform claim extraction/review before any authoritative historical component promotion.
3. Resolve or explicitly document the legal basis for public redistribution of preserved third-party manuals.
4. Keep the Field Library open-verification register active; do not promote unresolved lesson claims by repetition.
5. Capture future VM-4209 owner photographs with photographer/date/edit/license metadata if they are added.
6. Execute no logic-analyzer or serial procedure under this repository-only architecture assignment; prepared cards remain non-evidence until separately authorized and performed.
