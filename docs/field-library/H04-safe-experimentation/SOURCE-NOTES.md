# H04 Source notes

Keys refer to the shared pool in `../SOURCES.md`. **Every boundary in this packet
is quoted or restated from this repository's own documents. None is this
library's invention.**

## The red list

| Item | Source |
|---|---|
| Firmware loading, EEPROM writing, CFFA1 modification, serial-port opening, automated physical-device control | REPO `docs/apple1-learning-library-curriculum.md`, library design rule 6, which lists exactly these five and says they must not appear in a lesson |
| Temporary CA2 wiring, soldering, resistor installation, uploader use, RAM load, EEPROM action | REPO `docs/preservation-dossier.md`, "Current boundaries": "No temporary CA2 wiring, soldering, resistor installation, uploader use, RAM load, or EEPROM action belongs in ordinary development work." |
| ROM-bank change | REPO `software/ram-only/README.md`: "Do not combine a program run with an open serial session, firmware action, ROM-bank change, or CFFA1 write." |
| CA2 to Propeller voltage hazard | REPO `docs/hardware/plus-io-map.md`: "Do not attach a direct CA2-to-Propeller wire: CA2 can be 5 V and Propeller GPIO is 3.3 V." |
| Jumper and DIP state recorded while powered down only, with a photograph before and after any intentional change | REPO `docs/preservation-dossier.md`, baseline inventory checklist |

## The standing block

| Claim | Source |
|---|---|
| Opening the FT232R from the host has already produced a display-garbling `STOP` result | E-FT232-STOP; REPO `docs/preservation-dossier.md`, "Current boundaries" |
| An opened serial session or transmit test is blocked until the measurement test card is ready and an operator explicitly starts that single step | REPO `docs/preservation-dossier.md`, "Current boundaries", quoted almost verbatim |

## Amber

| Claim | Source |
|---|---|
| The RAM-only programs are candidates with **no live-run authority** | REPO `docs/apple1-software-library.md`, contents table, "Hardware authority" column |
| Hand entry or loading on a live Apple-1 is a separate, operator-led step | REPO `docs/apple1-software-library.md`, opening paragraph |
| The acceptance card: photograph the monitor prompt, record power and USB topology, confirm no host process has the FT232R open, enter exactly one program preserving the byte record, exercise only documented behavior, and on unexpected output reset, record `STOP`, and start nothing else | REPO `docs/apple1-software-library.md`, "Acceptance card for a future single program run" |
| Display echo does not establish Pi-side receipt | REPO `docs/apple1-software-library.md` |

## Green

| Claim | Source |
|---|---|
| The emulator is an off-device rehearsal environment; do not connect it to the physical serial device; a successful run does not waive a hardware evidence gate | REPO `docs/emulator-demo-guide.md` |
| The archive tool works only on explicitly named files and does not inspect or open serial hardware | REPO `docs/preservation-dossier.md`, evidence rule 5; `docs/collection-archive.md` |
| Photographs and baseline inventory recording | REPO `docs/preservation-dossier.md`, baseline inventory checklist |

## No procedure for any amber or red action appears in this packet

This was checked deliberately during authoring, and it is the most important
property of the packet.

The lesson **names** categories so a reader can recognise them. It does not
describe how to perform any of them. Specifically: no serial-port opening steps,
no byte-entry procedure, no firmware or EEPROM steps, no CFFA1 steps, no wiring
instructions, no jumper procedure.

The CA2 voltage hazard is stated as a warning with its reason, quoted from the
project's own hardware notes, so that a reader who has the idea recognises it as
a known bad one. Nothing about how such a connection would be made appears
anywhere.

## The Part B item 5 answer

The claim that *writing* a firmware-loading lesson is itself red follows from
curriculum rule 6, which constrains what a lesson may contain rather than what a
person may do. This is the library's own governing rule applied to itself.

## Claims needing verification

- **V-13 carried forward from M04.** The FT232R account is summarized from the
  preservation dossier's "Current boundaries." The primary record with date,
  operator, and exact observation lives in the project's chain-of-custody and
  evidence ledger. A reviewer should confirm the summary against the primary
  record.
- **V-8 applies.** This lesson describes boundaries, not the machine's state.
- No new verification items. Everything here is quoted or restated from existing
  project documents, deliberately, so that the boundaries in this lesson cannot
  drift from the ones the project actually holds.

## What this lesson does not establish or authorize

It grants nothing. It lifts nothing. It advances nothing toward a live session.
It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification, and it contains no procedure for any of them.
