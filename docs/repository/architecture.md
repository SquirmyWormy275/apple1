# Repository architecture

## Design objective

The Apple1 repository is a preservation collection, educational product, experimental-computing system, and research record. Its architecture therefore optimizes for **authority boundaries and reproducibility**, not for minimizing the number of top-level directories.

The central rule is:

> Models may propose. Deterministic systems verify. Recorded evidence establishes observations. Physical hardware later settles physical reality.

A second rule applies to historical material:

> Research staging is not authoritative runtime evidence.

## Domain model

```text
APPLE1 REPOSITORY
|
+-- PRESERVATION -------- captured/external artifacts and chain of custody
|
+-- COMPUTER ------------ ordinary Apple-1 / Replica-1 use
|
+-- FIELD LIBRARY ------- source-grounded education and rehearsal
|
+-- NEURAL1 ------------- virtual experimental-computing runtime
|    |
|    +-- META/1 --------- epistemic/scientific layer
|    |
|    +-- 4K MIND
|    +-- 1976 MULTIVERSE
|    +-- SELFHOST/1
|    +-- 256-BYTE UNIVERSE
|    +-- RAM REPUBLIC
|
+-- RESEARCH DATA ------- staged and future authoritative structured data
|
+-- CF EXPORT ----------- host-side deployment staging; never the preserved card
```

`COMPUTER` remains conceptually sovereign. NEURAL1 must never be a hidden dependency for ordinary Apple-1 use.

## Durable directory taxonomy

```text
.github/                  CI and repository automation
art/                      original project ASCII/art sources + provenance
cf-card/                  host-side CF source registry/export control plane
configs/                  versioned runtime/campaign configuration
data/                     structured research data by authority state
docs/                     human-facing documentation and committed evidence
  collection/             accession records for collection objects
  captures/               captured experimental/troubleshooting evidence
  field-library/          learner/teacher/visitor product
  hardware/               hardware interpretation/reference
  neural1/                NEURAL1 architecture, methods, experiments, research
  peripherals/            peripheral history/research products
  reference/              external-reference provenance and rights records
  repository/             repository governance/audit/migration records
  visual-system/          project visual design rules
firmware/                 preserved/candidate firmware source
neural1/                  installable Python runtime
preservation/             preserved byte artifacts and manifests
schemas/                  machine-readable data contracts
software/                 Apple-1 software artifacts by execution authority
tests/                    deterministic tests
 tools/                    host-side utilities and validators
wiki/                     derived GitHub-wiki-facing navigation
```

This architecture intentionally leaves mature subtrees in place. A move is justified only when the current location creates an authority ambiguity, broken ownership boundary, or maintenance hazard.

## Authority classes

Every durable artifact must be understandable as one of these classes.

### SOURCE

Editable project-authored source: Python, tests, schemas, configuration, educational source, project ASCII art, and host-side exporters.

### AUTHORITATIVE DATA

Structured records whose domain-specific promotion gate has passed. Historical authority requires source identity, provenance, claim review, temporal eligibility, and the hashes required by policy.

The current 1976 MULTIVERSE corpus has **zero** authoritative runtime component records.

### RESEARCH STAGING

Potentially strong research that has not passed the authority gate. Staging may be committed and cited as research, but runtime code must not silently treat it as authoritative fact.

### TEST FIXTURE

Synthetic or deliberately controlled input used to test deterministic behavior. A fixture is never an observation merely because a test passes.

### GENERATED OUTPUT

Reproducible local build/run output. Default location is `out/` or another explicitly ignored local state directory. Generated output is not committed unless deliberately promoted into a documented evidence package.

### PRESERVED ARTIFACT

A captured or externally sourced byte artifact retained for identity/provenance. It must not be silently normalized or modernized. Hash-sensitive line endings and LFS policy are part of preservation behavior.

### DERIVED DOCUMENTATION

Human interpretation of source, data, or evidence. It may summarize but must not erase uncertainty or become a substitute for the underlying record.

## Preservation boundary

`preservation/` is the byte-preservation layer. Editable interpretation belongs under `docs/`.

Examples:

```text
preservation/manuals/.../files/*.pdf   PRESERVED ARTIFACT
preservation/.../*manifest*.json       PRESERVATION METADATA
docs/preservation-dossier.md           DERIVED DOCUMENTATION
```

`firmware/vendor/110REV03/` is a candidate-source preservation area with its own provenance record. Its contents are not proof of installed firmware and are not a recovery image.

## 1976 MULTIVERSE authority pipeline

```text
RESEARCH_STAGING
       |
       +-- identify exact source
       +-- acquire source artifact
       +-- record SHA-256 when policy requires it
       +-- extract bounded claim
       +-- review claim against source
       +-- validate date/cutoff eligibility
       +-- record rights/provenance/evidence quality
       |
       V
REVIEWED PROMOTION DECISION
       |
       V
AUTHORITATIVE HISTORICAL CORPUS
```

No promotion may occur because a research note sounds credible, because a model recalls a fact, or because a missing price would be convenient to estimate. Unknown prices remain null. LLM-generated price estimates are forbidden.

## Pilot evidence policy

Scientific evidence that begins life as generated runtime output may be deliberately committed. Such a package must identify:

- campaign/run identity;
- exact model/provider records;
- completeness/incompleteness;
- interruptions and stop reasons;
- hashes or release bundle identity;
- negative results;
- limitations;
- physical-safety state.

Pilot 001 is such a committed evidence package and is not disposable build output.

## Field Library boundary

The Field Library is an educational product, not a second research authority system.

```text
SOURCE NOTES / PRIMARY EVIDENCE
              |
              V
       LEARNER LESSON
              |
       deterministic exercise
              |
              V
        EMULATOR EVIDENCE
```

AI assistance may explain or navigate the corpus. It does not replace deterministic assembler/emulator evidence. A lesson's OFF-DEVICE/RAM-ONLY/LIVE status is an execution-authority label, not merely a pedagogical tag.

## CF-card architecture

The repository source tree is **not** the deployable CF-card layout.

```text
PRESERVED ORIGINAL CF IMAGE
preservation/cf-card/...
        |
        | never modified in place
        |
        +--------------------------------+
                                         |
PROJECT AUTHORED SOURCE                  |
docs/field-library/                     |
software/                               |
        |                                |
        V                                |
cf-card/manifests/current.json           |
        |                                |
        V                                |
tools/export_cf_card_sources.py          |
        |                                |
        V                                |
out/cf-card-staging/                     |
        |                                |
        V                                |
VALIDATED DEPLOYMENT CANDIDATE ----------+
```

The exporter is host-side only. It does not mount, format, image, or write a physical card.

## Art and heritage references

```text
art/                     original project art / generated project ASCII
art/provenance/          provenance for project visual assets
docs/reference/          metadata about external heritage references
external/                ignored local checkout; never release authority
```

Third-party heritage material remains reference-only unless rights are explicitly established. Public availability is not a redistribution license.

## Wiki policy

`wiki/` is a derived presentation/navigation layer intended for GitHub Wiki use. It must link to repository-authoritative docs rather than becoming an independent source of technical truth. Substantive technical changes belong in `docs/`, source, data, or preservation records first.

## Configuration authority

`pyproject.toml` is the canonical CI/editable-install configuration. `requirements-dev.txt` is retained as an alternate development/hardware-tool dependency list because it includes `pyserial`; it must not silently become the CI authority unless CI is deliberately changed.

## Physical safety boundary

Repository architecture must make it possible to develop, test, and demonstrate without physical access.

The architecture pass does not authorize:

- opening a physical serial device;
- transmitting to the Replica;
- firmware loading;
- EEPROM writes;
- CFFA1 writes;
- GPIO;
- wiring/jumper/solder changes;
- cameras or physical qualification.

Serial-capable source may exist for preserved diagnostic work, but CI and deterministic demonstrations must use fakes/mocks/off-device paths and retain `serial_opened=false`.

## Validation architecture

A valid checkout should prove:

1. the package installs from declared dependencies;
2. source is lint/type clean;
3. the full test suite passes;
4. schemas are valid and required committed instances conform;
5. first-party relative Markdown links resolve;
6. art constraints/provenance pass;
7. core repository domains and evidence anchors exist;
8. 1976 staging cannot contain authoritative IDs;
9. deterministic demo completes with `serial_opened=false`;
10. validation creates no tracked-file diff.

## Change rules

- Prefer `git mv` for justified moves in a normal checkout.
- Never rewrite preserved artifacts to fit a new layout.
- Never move a scientific evidence package into generic generated output.
- Never merge research staging into authority for cosmetic completeness.
- Preserve public Python/CLI interfaces unless a real maintainability or correctness benefit justifies a change.
- Do not create new schemas, layers, or folders merely for symmetry.
- Archive historical guidance only when its current status is explicit and links remain navigable.
