# X05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## The card comes from the curriculum

Every section of `assets/author-card.txt` maps onto a requirement already in
`docs/apple1-learning-library-curriculum.md`.

| Section | Source |
|---|---|
| 1, 2, 3, 11: ID, audience, time, prerequisites | The authoring template's header block, and the audience table (LOOK / LEARN / BUILD / STUDY with target times) |
| 4: learning objective | The template's "By the end, you can [observable learner action]" |
| 5, 6: first visible result in three actions | Library design rule 2, "Put a visible result within the first three learner actions," and the template's Activity block |
| 7: sources | Design rule 3, and the review gate item "Every technical and historical claim has a source note" |
| 8: status label | Design rule 5, "Mark every runnable artifact OFF-DEVICE, RAM-ONLY, or LIVE BY SEPARATE APPROVAL" |
| 9: answer key plan | The review gate item "Any program has a deterministic expected result and an answer key"; the X05 brief, which requires an answer key plan |
| 10: what it does not establish | The review gate item "The lesson says what it does **not** establish" |
| 12: the safety gate | Design rule 6, which lists firmware loading, EEPROM writing, CFFA1 modification, serial-port opening, and automated physical-device control |

The X05 brief asks for a filled curriculum-author card requiring learning
objective, first result, sources, status label, and answer key plan. All five are
sections 4, 5, 7, 8, and 9.

## The additions beyond the curriculum

Section 12 extends design rule 6 with **wiring or soldering**, which comes from
`docs/preservation-dossier.md`'s "Current boundaries" rather than from the
curriculum's rule 6. The two documents cover different lists and the card merges
them.

Section 7's "claims with no source yet" line has no direct counterpart in the
curriculum. It reflects what every packet in this library actually does, which is
carry a numbered verification list, and it is added because the practice has
proven more useful than the rule required.

Recorded as **V-35**: section 7's unsourced-claims prompt and section 12's wiring
line are this library's additions to the curriculum's stated requirements. Both
are consistent with existing project documents; neither is quoted from one.

## The review gate

Part H reproduces the seven-item checklist from the curriculum's "Review gate
before adding a lesson to the card catalog" section, unchanged.

**No lesson currently in this library has formally been through that gate.** The
answer key says so rather than implying the proposal is being held to a standard
the catalog already meets. Each existing packet carries its own source notes with
open verification items, and page numbers throughout inherit **V-1**.

Recorded as **V-36**: the curriculum's review gate has not been formally applied
to any packet in this library. Running it is an outstanding task for the
repository owner before anything goes on the card.

## The Part C item 2 answer

The claim that "a program entered and running" cannot be a first result rests on:

| Claim | Key |
|---|---|
| The RAM-only artifacts carry no live-run authority | REPO `docs/apple1-software-library.md` |
| Hand entry or loading on a live Apple-1 is a separate, operator-led step | REPO `docs/apple1-software-library.md` |
| A learner must be able to finish without opening a serial port or changing hardware | REPO curriculum review gate |

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-35 (new).** Two card sections extend the curriculum's stated requirements.
- **V-36 (new).** The review gate has not been applied to any existing packet.
- **V-8 applies.** Nothing here concerns the machine's state.

## What this lesson does not establish or authorize

**A completed author card is a proposal, not an approval.** It adds nothing to the
catalog, grants no authority, and does not exempt a proposed lesson from the
review gate. It authorizes no firmware load, EEPROM write, CFFA1 write,
serial-port open, or physical modification, and no lesson proposed through it may
contain any of those either.
