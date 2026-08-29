# H03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The archive tool creates a SHA-256 inventory from only the files an operator names, and does not crawl, copy, or publish | REPO `docs/collection-archive.md` |
| Beside each manifest, retain a human note covering original location, source or provenance, permission, date, and whether the file is an original, a derivative, or a working copy | REPO `docs/collection-archive.md` |
| Hashes establish file identity at capture time; they do not prove a manual, photo, or candidate source describes the installed firmware or current board | REPO `docs/collection-archive.md`; E-NOPROOF |
| Hash every copied source, capture, binary, and photo manifest with SHA-256 | REPO `docs/preservation-dossier.md`, evidence rule 2 |
| Preserve the original filename, source URL or physical origin, retrieval date, and any licence note | REPO `docs/preservation-dossier.md`, evidence rule 3 |
| Store a read-only duplicate of raw captures before annotation | REPO `docs/preservation-dossier.md`, evidence rule 4 |
| Record facts separately from hypotheses and vendor claims | REPO `docs/preservation-dossier.md`, evidence rule 1 |
| The vendor `110REV03` source is candidate evidence, not the installed image | E-110REV03 |
| The manual filename discrepancy, with no hash comparison run | **V-6** |
| Emulator runs are evidence about a byte sequence, not hardware | E-EMU-SCOPE |

## The ten-field card

The evidence card's fields are drawn from the repository's own requirements:
fields 3 to 7 map directly onto what `docs/collection-archive.md` and the
preservation dossier's evidence rules 2 and 3 ask for.

**Fields 9 and 10 are additions.** No source in this project asks for "what this
establishes" and "what it does not establish" as record fields. They are added
because the repository's evidence rule 1 requires facts to be recorded separately
from hypotheses, and because S04's habit is the whole point of this lesson.

Recorded as **V-30**: fields 9 and 10 are this library's addition to the
repository's documented record requirements. If the project adopts them, the
collection archive documentation would need updating to match. If it does not,
this lesson should say they are a teaching device rather than project practice.

## How SHA-256 works is not explained

The lesson says a hash is a long number computed from a file's contents, that
changing one byte changes it completely, and that matching hashes mean an
unchanged file. It does not explain the algorithm, discuss collision resistance,
or claim anything about cryptographic strength.

That is deliberate. Everything the lesson needs follows from the property the
repository already relies on, and a STUDY-level lesson on provenance does not need
cryptography.

## The worked example is this project's own open item

The manual filename discrepancy in the README and Part F is **V-6** from the
shared pool, used as the worked example rather than an invented one. The lesson
does not resolve it, states that one command would, and models the "presumed the
same" wording this library actually uses.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-6 carried forward**, as the lesson's worked example.
- **V-30 (new).** Evidence-card fields 9 and 10 are this library's addition, not
  documented project practice.
- **V-23 carried forward from B05:** manifest self-integrity is unaddressed in
  this project's documentation, and this lesson does not address it either.
- **V-8 applies.** Nothing here establishes anything about this board.

## What this lesson does not establish

It authenticates nothing, resolves no open provenance question in this project,
and makes no claim about any object's originality or value. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
