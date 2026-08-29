# B05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The archive tool creates a SHA-256 inventory from only the files an operator names, and does not crawl, copy, or publish | REPO `docs/collection-archive.md` |
| Beside each manifest, retain a human note covering original location, source or provenance, permission, date, and whether the file is an original, a derivative, or a working copy | REPO `docs/collection-archive.md` |
| Hashes establish file identity at capture time; they do not prove a manual, photo, or candidate source describes the installed firmware or current board | REPO `docs/collection-archive.md`; E-NOPROOF |
| Hash every copied source, capture, binary, and photo manifest with SHA-256; preserve original filename, source URL or physical origin, retrieval date, and any license note | REPO `docs/preservation-dossier.md`, evidence rules 2 and 3 |
| Store a read-only duplicate of raw captures before annotation | REPO `docs/preservation-dossier.md`, evidence rule 4 |
| The vendor `110REV03` source is candidate evidence, not the installed EEPROM image | E-110REV03 |
| The library is intended for archival storage on the project CF card | REPO `docs/apple1-learning-library-curriculum.md`, opening paragraph |
| **The card boot and menu mechanism is intentionally undecided** | REPO `docs/apple1-learning-library-curriculum.md`: "The actual card boot/menu mechanism is intentionally undecided. This outline defines the educational catalog only." |
| Lessons must not assume a particular CFFA1 file system or boot workflow | REPO curriculum, the B05 writing brief |
| The manual filename discrepancy and absent hash comparison | **V-6** in `../SOURCES.md` |
| One wrong byte can produce a program that runs and misbehaves | M02 Part E, derived from the artifact |

## No card workflow is assumed anywhere

This is the constraint the B05 brief exists to enforce, and it is worth recording
what was done about it.

No file in this packet names a file system, a directory layout, a filename
convention, a menu, an index, a boot sequence, or any means by which a lesson
would be selected or displayed. Part F makes the absence of those the subject of
an exercise rather than working around it.

The word "card" appears only as a storage location, never as a mechanism.

## The Part A file 6 answer

The observation that a manifest cannot protect itself is reasoning, not a cited
claim. It follows from what a hash does: if an attacker or an accident can alter
a file, the same access generally alters the manifest entry beside it. The
repository does not discuss manifest integrity, which is why the answer key
raises it as an insight rather than citing a policy.

Recorded as **V-23**: manifest self-integrity is not addressed anywhere in this
project's documentation. Whether the manifests should themselves be protected,
and how, is an open question for the repository owner.

## The Part G sample note

The sample retention note deliberately contains several "not recorded" entries,
including the retrieval date and route for the Briel manual. Those gaps are real:
nothing in this project records them, and the sample would be dishonest if it
invented them. The note also carries forward V-6.

## Deliberate simplifications

1. **Three kinds is a coarse scheme.** Real archival practice distinguishes
   further: primary record, derivative, access copy, preservation master. The
   repository's own evidence rules are the fuller version.
2. **Format obsolescence is raised but not developed.** Part D item 4 touches it;
   the lesson does not go into migration strategies.
3. **No storage medium is recommended.** Recommending one would be advice this
   project has not asked for.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-6 carried forward** in the Part G sample note.
- **V-23 (new).** Manifest self-integrity is unaddressed in project
  documentation.
- **V-8 applies.** Nothing here establishes anything about this board or its
  CFFA1.

## What this lesson does not establish or authorize

It assumes and asserts nothing about how the card works. It authorizes no
firmware load, EEPROM write, **CFFA1 write**, serial-port open, or physical
modification, and no step in it involves inserting, reading, or writing a card.
