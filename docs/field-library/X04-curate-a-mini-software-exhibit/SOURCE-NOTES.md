# X04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## The artifacts and their classifications

| Artifact | Claim | Key |
|---|---|---|
| `line-input-0300.hex` | 26 bytes; reads a key when `$D011` indicates ready, stores at `$0400,Y`, echoes through `$FFEF`, stops after CR, returns to the Monitor | REPO `software/ram-only/README.md` |
| Both `.hex` files | RAM-only candidates with **no live-run authority** | REPO `docs/apple1-software-library.md` |
| Both | Retained from confirmed learning exercises in the project handover; author not named | REPO `software/ram-only/README.md` |
| `line-input-echo-0300.hex` | Does not return to the Monitor; final instruction `JMP $0300` | `../EMULATOR-RUNS.md`; M05 |
| Woz Monitor listing | Reprinted in the Replica 1 Plus manual, Appendix C | W-FF00, W-FF1F, W-FFEF |
| `110REV03` source | Immutable candidate evidence, not the installed EEPROM image | E-110REV03 |
| Emulator runs | ROM-free harness; emulates no Propeller, serial hardware, or ROM image; a run does not waive a hardware evidence gate | E-EMU-SCOPE; REPO `docs/emulator-demo-guide.md` |
| The Briel manual | Documents the Replica 1 Plus, June 2014 | BRIEL |
| Owad's book | Documents the original Apple-1, the Replica I, and the Replica I TE | OWAD; **V-4** |
| This library's lessons | Carry unverified page numbers and open verification items | **V-1** and the per-packet source notes |

## The record-field requirements

| Card field | Source |
|---|---|
| 4, 5, 6: origin, maker, permission | REPO `docs/collection-archive.md`, which requires a human note covering original location, source or provenance, access permission, and date; REPO `docs/preservation-dossier.md` evidence rule 3 |
| 7: status label | REPO `docs/apple1-learning-library-curriculum.md`, library design rule 5 |
| 9: what this does not prove | REPO `docs/apple1-learning-library-curriculum.md`, the X04 writing brief, which asks explicitly for rights and provenance prompts and a "what this does not prove" field |

Field 9 is the one the curriculum names directly for this lesson, which is why the
template marks it required and the answer key refuses a card without it.

## The worked set is honest about gaps

Several fields in the worked cards read "not recorded." Those are real: the
repository does not name an author for the RAM-only programs, and it does not
record the retrieval route or terms for the vendor source archive. Inventing
plausible entries would have made a tidier example and a dishonest one, and would
have modelled exactly the behavior H03 Part D warns about.

## Part E item 8

The entry saying this library's own lessons do not prove they have passed the
curriculum's review gate is accurate. The review gate exists in
`docs/apple1-learning-library-curriculum.md` as a checklist to be applied before a
lesson is added to the card catalog. No lesson in this library has been through it;
each carries its own source notes with open verification items, and page numbers
throughout inherit **V-1**.

Including that on the list was deliberate. An exhibit lesson that exempted itself
would fail its own standard.

## Rights questions are asked, not answered

**This library resolves no rights or permission question.** The vendor source
archive's terms, the manual scan's terms, and the provenance of the RAM-only
programs are all unrecorded in this project. The lesson asks for them and requires
the learner to write what they would find out and from whom, rather than leaving a
blank that reads as "checked."

Recorded as **V-34**: rights and permission status is unrecorded for the vendor
source archive, the manual scan, and the RAM-only programs. This is an open item
for the repository owner, and this library cannot close it.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-4 applies** to Owad's coverage, per Part E item 7.
- **V-6 carried forward** in Part E item 6, the manual filename discrepancy.
- **V-34 (new).** Rights and permission status is unrecorded for several
  artifacts.
- **V-8 applies.** No artifact here establishes anything about the board.

## What this lesson does not establish or authorize

It resolves no rights question, authenticates nothing, and makes no claim about
value. It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port
open, or physical modification, and no artifact is run or displayed on any
machine.
