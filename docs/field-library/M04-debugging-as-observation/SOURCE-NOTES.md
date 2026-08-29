# M04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The STOP rule: on display change, reset, identity drift, or byte mismatch, record `STOP`, recover to the known monitor state, do not continue | E-STOP; REPO `docs/preservation-dossier.md` evidence rule 6 |
| On unexpected output, reset to the monitor prompt, record `STOP`, and do not start another program | REPO `docs/apple1-software-library.md`, acceptance card item 5 |
| Opening the FT232R from the host produced a display-garbling `STOP` result | E-FT232-STOP |
| An opened serial session and transmit test remain blocked pending a measurement test card and an explicit operator start | REPO `docs/preservation-dossier.md`, "Current boundaries" |
| Facts are recorded separately from hypotheses and vendor claims | REPO `docs/preservation-dossier.md`, evidence rule 1 |
| A discrepancy in an emulator run is retained as a software issue | REPO `docs/emulator-demo-guide.md` |
| The expected values used in Part A | `../EMULATOR-RUNS.md` |
| `99 00 04` is the `STA $0400,Y` instruction in the cited listing | REPO `software/ram-only/line-input-0300.hex`; M02 |

## The FT232R account is history, not procedure

This is the most important note in the packet.

The lesson uses a real recorded incident from this project because a real one
teaches better than an invented one. It is described as something that already
happened and was recorded. At no point does the lesson describe how to open a
serial device, and Part E asks the learner to reason about what was done, not to
do it.

The repository's position is unchanged and is restated in `STATUS.md`: an opened
serial session or transmit test is blocked until a measurement test card is ready
and an operator explicitly starts that single step.

## The Part A scenario is hypothetical

The empty-buffer situation in Part A **did not occur**. It is constructed for the
exercise, chosen because it is the symptom the M02 transcription error (`04`
becoming `40`) would actually produce.

This is stated so that no future reader mistakes the worksheet for a record of an
observed failure. The recorded runs, all of which passed, are in
`../EMULATOR-RUNS.md`.

## Deliberate simplifications

1. **One hypothesis at a time.** Real debugging often holds several. The
   discipline of writing one and testing it is the teachable part.
2. **"Change one thing" is stated as an absolute.** There are cases where a
   coordinated change is the only way forward. A LEARN-level lesson does not need
   the exceptions.
3. **No distinction is drawn between reproducing and diagnosing.** Part C item 1
   touches it; the fuller treatment belongs with X02.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-13 (new).** The FT232R account is summarized from the preservation
  dossier's "Current boundaries" section. The primary record of that event, with
  its date, operator, and exact observation, lives in the project's
  chain-of-custody and evidence ledger rather than in this packet. A reviewer
  should confirm the summary against the primary record before this lesson goes
  on the card, and the lesson should not acquire any detail the primary record
  does not support.
- **V-8 applies.** No observation in this packet was made on this board by this
  author.

## What this lesson does not establish or authorize

It establishes nothing about the machine. It authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification. The FT232R
incident is recounted, not reproduced, and reproducing it is specifically outside
what this or any lesson permits.
