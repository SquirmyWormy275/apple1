# Technical review and completion record

This revision turns the first edition's short assembly survey into a worked
sequence and adds fresh, retained local-model evidence. The course remains
explicit about which results are software observations and which require
physical measurements or further historical research.

## What changed after the first edition

| Finding | Correction and evidence |
|---|---|
| A forward data label could point one byte early | The assembler stabilizes instruction sizes before final encoding; a regression loads the actual table byte |
| A distant relative branch silently wrapped | Out-of-range displacements are rejected; tests exercise both -128/+127 endpoints and just-outside targets |
| Assembly concepts were mostly summarized | T01–T12 supply complete programs, state traces, predictions, captured outputs, variations and answers |
| A06's zero-length discussion claimed 256 stores | The exact DEY/BPL listing with Y=$FF performs one store at $04FF; the sixteen-byte original is also executed |
| M03's formula lacked a derivation and used a wrong nine-character example | Count setup, ordinary passes, CR path and exit separately; test empty input and both sides of the index boundary |
| X01 omitted C8 from its high-bit count | The preserved 26-byte artifact has 15 high-bit bytes; the executable companion counts them |
| X01 gave an intentionally wrong task count | Ask accurately for five operands/bases, then explicitly assess a separate claim of four |
| Video garbage was used as evidence of CPU RAM contents | The answer now states an explicit lack of an initialization contract; video is a separate observation |
| Native ASK selected an incomplete excerpt and marked an expanded refusal grounded | Query-specific action ranking, a complete M01 definition and refusal classification have regression checks; original Pi records stay unchanged |
| Source summaries carried reset, stack and range mistakes | Preserve the scans and record corrections; use the verified Monitor listing and executable CPU checks |
| The first edition had no fresh inference | Retain actual local requests, raw replies, model/blob identities and independent proposal evaluations; keep unsuccessful attempts |

## Manual checks

All five local manual files matched their existing preservation manifest by
SHA-256. No preserved PDF, vendor source or RAM `.hex` artifact was changed.
The manifest identifies a particular scan; it does not establish rights,
authenticity of a physical object, or correctness of every sentence in a source.

| Preserved source | Pages checked | What the check establishes |
|---|---|---|
| [Apple-1 Operation Manual](../../preservation/manuals/2026-08-28/files/Apple1%20Manual.pdf) | PDF p. 2 visually; p. 3 OCR corroboration | Original specification: 40 characters per line, 24 lines, automatic scrolling |
| [Replica 1 Plus manual](../../preservation/manuals/2026-08-28/files/Replica_One_Plus_Manual_-_June_2014.pdf) | Printed/PDF pp. 24, 30–32 visually | 9600 8N1/no flow-control reference; Monitor input buffer; R dispatch; documented register and vector locations |
| [Owad](../../preservation/manuals/2026-08-28/files/AppleIReplicaCreationTomOwad.pdf) | Printed/PDF pp. 216 and 218 visually | The scan contains the reset-vector, stack-description and inclusive-range discrepancies discussed below |

The original Operation Manual is image-only in this scan. OCR helped locate
text; visual inspection of its Specifications page supplied the display check.
The Briel pages show `RUN` at `$FF94` as `6C 24 00` (`JMP (XAML)`), and the
Hardware Notes explicitly list IN at `$0200`–`$027F`. These resolve V-14 and V-9.
The serial page describes a reference setup; this unit's known open-event fault
is still a separate investigation.

Owad p. 216 misidentifies the reset-vector locations and describes stack-pointer
direction/size incorrectly. Teach RESET at `$FFFC/$FFFD`; a stack push decrements
SP; page one contains 256 addresses. The source pool qualifies those errors.
The inclusive 32 KiB range is `$0000`–`$7FFF`; `$8000` is the next location.
The Briel reprint's printed vector bytes are not used to build or identify an
installed ROM. T12 supplies an explicit direct-CPU vector experiment instead.

This closes selected questions, not the library's entire historical review.
[V-1, V-36 and the other open items](../field-library/README.md#open-verification-items)
remain visible. A reproducible software companion does not grant physical CF
catalog approval or establish unverified dates, rights or manufacturing counts.

## Evidence you can reproduce

Every catalog example has unique source, raw stdout, a readable PNG, a stated
evidence mode, checks, a variation and an answer. `tools.textbook verify --rerun`
checks source/capture hashes and reproduces the deterministic output. Native
inference is kept in a separate record; N01 re-evaluates retained responses
without making fresh requests or claiming exact regeneration of model text.

A follow-up staged-source Pi request correctly enumerated all three Monitor
functions; its exact provider recording and source snapshots are retained.
This does not replace the global installed release or establish universal
model accuracy.

The [native walkthrough](native/README.md) explains the prompts, resource bounds,
identity checks, positive/negative controls and interpretation. The
[course guide](course-guide.md) supplies a sequence and observable assessments.
The [coverage register](coverage.md) inventories all original packets and public
command surfaces. The [6502 reference](reference/6502.md) lists the documented
instruction families and the CPU/world distinction.

## Physical follow-through

The user reports that the physical setup is not available yet. The book can
teach its documented design and rehearse its programs; it cannot manufacture
an instrumented physical capture. The known serial-open fault remains open.
[Preparing the physical chapter](reference/physical-session.md) specifies the
evidence and existing test-card sequence needed when that setup arrives.

## Release checks

The release must pass the full test suite, Ruff, mypy, repository validation,
all deterministic capture reruns, native-record verification and documentation
link checks. A clean-checkout walkthrough must reproduce the beginner route.
The pull request and CI run are the authoritative records of those checks;
this checklist does not substitute for them.

[Textbook home](README.md) · [Course guide](course-guide.md) · [Native evidence](native/README.md)

The earlier [native course receipt](validation/README.md) records 439 passing tests,
all 100 exact example reruns, repository validation, Ruff and mypy on the real
Pi. The workstation passed the same full suite and checks.


## Pre-hardware extension

The [packet review](../field-library/review/README.md) applies the structural
gate to all 42 packets and records targeted editorial corrections. The shared
quotation ledger matches 73 fragments to identified local scan pages; it does
not independently corroborate every historical assertion or clear rights.

The new [BASIC chapter](reference/basic.md) executes the preserved interpreter
on an NMOS 6502: six programs, actual INPUT/string/array behavior, intermediate
overflow and both quiz outcomes. The primary BASIC manual's printed p. 1 /
PDF p. 3 was visually checked for loading and cold/warm entry.

The [card edition](../../cf-card/README.md) implements the RAM reader and a
host image build using the actual CFFA1 ROM against modeled ATA. An independent
ProDOS reader validates allocation and preserved originals. Every page is
rehearsed, and all six generated BA1 programs are restored into cleared RAM and
run again. No serial port or physical card is opened by this build.

The [pre-hardware receipt](validation/prehardware.md) and final release checks
record the new scope. Physical acceptance, installed ROM identity, electrical
timing, credited build photographs and as-built dimensions remain separate.
The [storyboard kit](../hardware/build-storyboard/README.md) prepares those slots.
