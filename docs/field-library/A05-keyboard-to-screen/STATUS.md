# A05 Status

**Lesson mode: OFF-DEVICE**

**Artifact classification: RAM-ONLY, no live-run authority.**

Those are two different statements and both matter. The lesson reads a program
and optionally rehearses it off-device. The program itself is classified in
`docs/apple1-software-library.md` as a RAM-only candidate with no live-run
authority, and nothing in this lesson changes or grants that.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/four-stages.txt` | Annotated listing, 40 columns | No |

## Exact file discussed

`software/ram-only/line-input-0300.hex`. 26 bytes. Load address `$0300`,
occupying `$0300` to `$0319`. Buffer at `$0400`. Quoted unmodified; this packet
adds nothing to `software/ram-only/` and contains no entry procedure.

Part G also reads `software/ram-only/line-input-echo-0300.hex`, 41 bytes.

## Expected result

For the optional off-device rehearsal, exactly the values recorded in
`../EMULATOR-RUNS.md`:

| Input | Screen | Buffer | Returned | Instructions |
|---|---|---|---|---:|
| `A` + CR | `A` CR | `A` CR | true | 20 |
| `HI` + CR | `HI` CR | `HI` CR | true | 30 |
| `HELLO` + CR | `HELLO` CR | `HELLO` CR | true | 60 |
| `APPLE-1` + CR | `APPLE-1` CR | `APPLE-1` CR | true | 80 |

For the paper work, the Part D trace ends with `$C8 $C9 $8D` at `$0400` to
`$0402`.

## Known limitations

- The program has a second, undocumented exit at 128 characters. Whether it is
  deliberate is unknown and is presented as an open question (V-18).
- No backspace, no explicit bounds check, no buffer terminator, no case handling.
- Part F's instruction costs are rough estimates for weighing trade-offs.
- The echo variant read in Part G does not return to the Monitor (see M05).

## Stop condition

Not applicable to the paper work. For optional off-device rehearsal, M03's stop
condition applies: a result differing from the table is a software finding to
record per `docs/emulator-demo-guide.md`, not a reason to approach hardware.

**For any future operator-led session with this artifact, which this lesson does
not authorize**, the acceptance card in `docs/apple1-software-library.md` governs:
photograph the initial monitor prompt, confirm no host serial process has the
FT232R open, enter or load exactly one program, exercise only its documented
behavior, and on unexpected output reset to the monitor prompt, record `STOP`,
and start nothing else.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No entry of this program on hardware. **No live-run
authority is created, implied, or advanced by completing this lesson**, and a
display echo obtained anywhere does not establish serial transmission.
