# H05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Record facts separately from hypotheses and vendor claims | REPO `docs/preservation-dossier.md`, evidence rule 1 |
| Record a photograph before and after any intentional change; record jumper and DIP state while powered down only | REPO `docs/preservation-dossier.md`, baseline inventory checklist |
| Complete a chain-of-custody row before changing the setup or collecting a live capture | REPO `docs/preservation-dossier.md`, chain-of-custody record |
| Preserve retrieval date and origin alongside copied material | REPO `docs/preservation-dossier.md`, evidence rule 3 |
| Opening the FT232R produced a display-garbling `STOP`, which was recorded | E-FT232-STOP |
| The Apple I Owners Club was founded in 1977 with about thirty members, who exchanged programs and compiled a software library | H-CLUB |
| The club published a newsletter, quoted in Owad's chapter 1 | OWAD ch. 1 p. 26, "Apple I Owners Club Premier Newsletter" |
| A dealer's account of an unsold board kept for 25 years and auctioned in 2001 | OWAD ch. 1 p. 34; H01 |
| The Replica 1 Plus manual is dated June 2014 | BRIEL |
| A display echo does not establish serial receipt (Part B item 2 reasoning) | REPO `docs/apple1-software-library.md`; M03 |
| A backslash at reset is documented replica behavior and identifies no particular ROM image | R-RESET; E-110REV03; S04 |

## The log-entry fields

The six fields are drawn from the repository's own requirements. Date, who, and
what-was-done map onto the chain-of-custody record's columns. The separation of
"what I saw" from "what I thought it meant" is evidence rule 1 restated for a
personal log.

**"What I am not sure about" is this library's addition**, as evidence-card
fields 9 and 10 were in H03. No project document asks for an uncertainty field.

Recorded as **V-31**: the uncertainty field is a teaching device added by this
library, not documented project practice. It is consistent with evidence rule 1
but is not required by it.

## The Owners Club framing

The README's argument that ordinary paperwork becomes a source rests on a real
example from this project's own collection: the Owners Club newsletter is
reproduced in Owad's chapter 1 and is cited elsewhere in this library for the
club's founding and membership. It was a small group's internal circular and it
is a historical source now.

That is stated as an observation about this specific document, not as a general
claim about what survives. H01's Part F covers the survivorship question and
notes the bias explicitly.

## Part B item 1 uses this project's own incident

The first sentence in Part B is the FT232R event written the way somebody might
casually log it, with the observation and the conclusion joined by "so." The
answer key separates them and notes that the conclusion is one hypothesis among
several.

This is deliberate: the exercise uses a real recorded event rather than an
invented one, and it does not endorse the conclusion. **V-13 carried forward:**
the account is summarized from the preservation dossier, and the primary record
lives in the project's chain-of-custody and evidence ledger.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-13 carried forward** for the FT232R account.
- **V-31 (new).** The uncertainty field is this library's addition.
- **V-8 applies.** Nothing here concerns this board's state.

## What this lesson does not establish or authorize

Nothing about this project's machine. **Writing a log entry describing an action
does not authorize that action.** This packet authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification.
