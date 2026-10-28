# Next session: accept the CF edition on the finished Replica

**Handoff recorded October 28, 2026. Status: physical session pending.**
When the finished enclosure/setup is available, demonstrate the installed
reading edition and a saved BASIC lesson with the actual keyboard and display.
Keep photographs/video and a dated acceptance record, then update the public
documentation from those observations. No new card installation is required.
Track completion in [GitHub issue #15](https://github.com/SquirmyWormy275/apple1/issues/15).

## What is already complete

The [October 28 audit](AUDIT-2026-10-28.md) and
[machine-readable receipt](deployments/2026-10-28.json) record the installed
**386-file edition**: six unchanged originals, 50 core books, six BA1 BASIC
programs, 319 supplemental readers and the exact-source archive. Host execution
checked all 3,374 pages, the BASIC restores and 110 examples. The entire physical card
was written, flushed, reopened and read back; its 128,974,848 bytes matched:

```text
7dec8da958836b5a21413d424e18253186450a941711c313dbafce1ea7de8cc8
```

The deployed source snapshot is `760a84789be2b51f753d47997267ae6dc7123249`.
Later documentation commits do not change that frozen archive or the card.
The earlier October 27 edition is superseded. Start from the current receipt,
not its historical file counts. The [original files and full baseline image](original/README.md)
and [downloadable combined package](releases/README.md) remain preserved.

## Before operating the finished setup

1. Read [current status](../docs/STATUS.md), the [loading guide](DEPLOYMENT.md),
   the [physical-session chapter](../docs/textbook/reference/physical-session.md)
   and the [build storyboard](../docs/hardware/build-storyboard/README.md).
   Fetch current GitHub changes and check for concurrent documentation work
   before editing; preserve its navigation, captions and evidence.
2. Record the actual board/CFFA1/card identity, firmware/interpreter evidence,
   power source, connections, known working reset/recovery procedure and date
   with timezone. A matching source filename does not identify installed firmware.
   Establish normal power/reset and stable local keyboard/display operation
   before the reader trial. An unknown prerequisite stays pending.
3. Use the physical keyboard/display. This acceptance does not require opening
   USB serial. The recorded serial-open display fault remains unresolved;
   its separate [bounded repair plan](../docs/hardware/replica-repair-plan.md)
   and [issue #17](https://github.com/SquirmyWormy275/apple1/issues/17) track
   restoration. This CF trial does not require serial repair.
4. Preserve any new user BASIC work before loading a reader: they share RAM.
   Handle/remove/insert the card only with the assembly unpowered under its
   documented service procedure. Do not format, rebuild or rewrite the working
   card merely to resume this handoff. Any later media change needs a verified
   whole-card backup, target identification and its own new receipt.

The original ROM/flasher/updater files are preservation objects, not acceptance
steps. This session calls for no EEPROM/firmware update, wiring change or Pi
reinstallation.

## Run these bounded trials

Record each step's actual result, including a failure or a skipped prerequisite.
Use [the loading guide](DEPLOYMENT.md) for the complete menu conventions.

| Trial | Actions on the physical keyboard | Expected observation |
|---|---|---|
| Main reader | At Monitor enter `9000R`. Use `P` with an empty name for root, then `P` with `EDUCATION`. Use `L` for `READER`, accept `$0800`, `Q`, then `0800R`. | Book 00 / `READFIRST`, headed `APPLE-1 FIELD LIBRARY`, with readable layout. |
| Navigation | In book 00 use `N`, then `P`. Use `M` then `01` for S01; use `A` for its answer section. Use `M` then `00`, then `Q`. | Next/back return to the same page, book selection and answer jump work, and exit returns to Monitor. Compare with the [retained page text](education/pages/). |
| Supplemental reader | From Monitor use `9000R`, root via empty `P`, then `L` for `START.HERE`, accept `$1000`, `Q`, then `1000R`. Use Space, `B`, then `Q`. | The combined overview is readable; next/back and return to Monitor work. This interface uses different keys from the main reader. |
| Saved BASIC | Follow the sequence below using the identified interpreter. | The saved HELLO program lists correctly and prints the predicted greeting. |

For the BASIC trial, establish the interpreter described in the
[Integer BASIC reference](../docs/textbook/reference/basic.md). Cold-initialize
it at `E000R` **before** loading the saved program. Return to Monitor through
the setup's qualified physical reset path; enter `9003R` (the BASIC-return
CFFA1 entry). Select root, then `BASICLABS`; load `HELLO` with `L` and use `Q`
to return to warm BASIC. `LIST` should match
[HELLO.bas](../software/basic/HELLO.bas). Enter `RUN`, then `TOM` when prompted;
expect `HELLO TOM` and a return to the BASIC prompt.

Do not cold-start with `E000R` after loading: it clears the restored program.
The identified interpreter's warm entry is `$E2B3`; a BA1 auxiliary address is
not an ordinary binary launch address. If interpreter identity or the reset
transition cannot be established, record that trial as pending rather than
improvising an entry point.

A garbled display, unexpected reset, load error or output mismatch ends that
trial. Preserve the failing observation and use the recorded recovery action.
Do not turn a failure into repeated serial opens, card writes or firmware changes.

## Leave evidence another agent can inspect

Create a new dated directory such as
`docs/captures/YYYY-MM-DD-replica-cf-acceptance/` with a README containing:

- Setup, operator/credits, time basis, source revision, card receipt/hash and
  installed firmware/interpreter identity (or explicitly unknown).
- Each trial's exact keys/input, expected versus actual output, `PASS`, `STOP`
  or `INCONCLUSIVE`, any unexecuted step, and recovery action.
- Original photograph/video filenames, SHA-256 hashes, timestamps, custody and
  permission to publish; derived web assets with their own hashes and captions.
- The specific claims established and what remains untested. If serial was not
  opened, say so; no serial log is needed to establish a local keyboard trial.

Use the [capture conventions](../docs/captures/README.md) and storyboard
[caption template](../docs/hardware/build-storyboard/caption-template.md).
Use existing shot IDs **BUILD-06** (card/setup), **BUILD-12** (first observation),
**BUILD-13** (reader), **BUILD-14** (BASIC) and **BUILD-16** (finished exhibit).
Retain camera originals independently; publish credited derivatives and inspectable
evidence/custody records. Add actual measurements to a dated copy of the storyboard
template; preserve the R04 design reference and all earlier failed trials.

## Finish the documentation from the results

- Link the dated record from this handoff, [project status](../docs/STATUS.md),
  [physical-session chapter](../docs/textbook/reference/physical-session.md) and
  [storyboard](../docs/hardware/build-storyboard/README.md). Add real assets and
  captions to the storyboard's planned slots.
- Update the root README's CF section and `wiki/CF-Card-Library.md` with only
  the demonstrated results, limits and photographs. Publish the corresponding
  narrow change to the live GitHub Wiki, which has a separate Git repository;
  updating `wiki/` in the source repository alone does not publish it.
- Keep the October 28 storage receipt/audit immutable. Add the new hardware
  acceptance record separately, even if a trial fails. A successful local
  reader/BASIC trial does not resolve the serial/electrical fault or prove
  every page, program, Pi path or installed firmware has been tested physically.
- Run `python tools/neural1_validate.py .` and `git diff --check`, review the
  diff for concurrent changes,
  and close the tracking issue only after the required trials, evidence and
  public documentation are complete. Otherwise leave a precise next action.

[Card home](README.md) · [Loading guide](DEPLOYMENT.md) · [Installation audit](AUDIT-2026-10-28.md)
