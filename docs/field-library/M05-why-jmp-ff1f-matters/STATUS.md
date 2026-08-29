# M05 Status

**Mode: OFF-DEVICE**

No new runnable artifact. The two listings are existing repository artifacts,
quoted for reading. Optional verification uses the M03 emulator.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/exit-annotation.txt` | Annotated listing, 40 columns | No |

**Exact files referenced:** `software/ram-only/line-input-0300.hex` (26 bytes,
load address `$0300`) and `software/ram-only/line-input-echo-0300.hex` (41 bytes,
load address `$0300`). Both unmodified. This packet adds nothing to
`software/ram-only/` and contains no entry procedure.

## Expected result

Determinate:

- Program One's exit is `4C 1F FF` at `$0317`, meaning `JMP $FF1F`.
- Program Two's final instruction is `4C 00 03` at `$0326`, meaning `JMP $0300`,
  which is not an exit.
- Emulator confirmation: `returned_to_monitor` is true for Program One and false
  for Program Two, per `../EMULATOR-RUNS.md`.
- Part F's instruction boundaries land on `$0328`, the 41st byte.

## Known limitations

- **`line-input-echo-0300.hex` has no self-directed exit.** Stated as observed
  behavior, not as a defect. Whether the restart is intended is an open question
  for the repository owner (V-15).
- The claim that the Monitor's `R` performs a jump rather than a `JSR` rests on
  the repository's own README rather than on the `RUN` routine's bytes in the
  Monitor listing (V-14).

## Stop condition

Not applicable to the paper work. For optional emulator use, M03's stop
condition applies: a result differing from the recorded table is a software
issue, not a reason to approach hardware.

**Relevant to any future operator-led session, though this lesson authorizes
none:** a session using `line-input-echo-0300.hex` would end by reset rather
than by the program returning to a Monitor prompt, because the program does not
return. That is a planning consideration for whoever eventually prepares such a
session under `docs/apple1-software-library.md`, and it is recorded here because
this is where the finding is explained.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine. Nothing in this
packet authorizes entering either program on hardware or running either program
on the Replica 1 Plus.
