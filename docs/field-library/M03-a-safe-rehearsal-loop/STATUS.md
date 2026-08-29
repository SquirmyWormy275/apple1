# M03 Status

**Mode: OFF-DEVICE**

This lesson runs software. It is the library's rehearsal lesson, and rehearsal
in this repository means the constrained emulator on an ordinary computer, never
the Replica 1 Plus.

## Runnable material

| Item | Detail |
|---|---|
| **Exact files** | `software/ram-only/line-input-0300.hex` (26 bytes) and `software/ram-only/line-input-echo-0300.hex` (41 bytes), both existing repository artifacts, unmodified |
| **Harness** | `tools/apple1_emulator.py`, unmodified, per `docs/emulator-demo-guide.md` |
| **Where it runs** | An ordinary computer with Python. Not the Apple-1, and not connected to it |
| **Optional scratch work** | Part F asks the learner to copy a byte list to a scratch file before altering a byte. `software/ram-only/` must be unchanged afterwards |

This packet creates no new artifact in `software/ram-only/`.

## Expected result

Exact and recorded in `../EMULATOR-RUNS.md`.

| Program | Input | Screen | Buffer | Returned | Instructions |
|---|---|---|---|---|---:|
| `line-input-0300.hex` | `A` + CR | `A` CR | `A` CR | true | 20 |
| `line-input-0300.hex` | `HI` + CR | `HI` CR | `HI` CR | true | 30 |
| `line-input-0300.hex` | `HELLO` + CR | `HELLO` CR | `HELLO` CR | true | 60 |
| `line-input-0300.hex` | `APPLE-1` + CR | `APPLE-1` CR | `APPLE-1` CR | true | 80 |
| `line-input-echo-0300.hex` | `HI` + CR | `HI` CR `HI` CR | `HI` CR | **false** | 50 |

## Known limitations

- The harness is ROM-free and models no Propeller, no serial hardware, and no
  ROM image. Its four output fields describe a software model.
- `line-input-echo-0300.hex` does not return to the Monitor. Its final
  instruction is `JMP $0300`. This is stated in the lesson, recorded in
  `../EMULATOR-RUNS.md`, and flagged for the repository owner.
- The instruction-count rule is empirical over four inputs (V-12).

## Stop condition

**If a run does not match the table above:** stop, record both the expected and
the observed values, and retain it as a software issue per
`docs/emulator-demo-guide.md`. Do not adjust the recorded expectations to match
a new observation without establishing which changed and why.

A mismatch is a software finding. It is **not** a reason to approach the
hardware, and it does not indicate a fault in the machine. There is no machine
state to recover, because no machine was involved.

**If any step of this lesson would require connecting to a serial device, that
step is wrong and should not be performed.** The emulator guide prohibits it,
and this project has a recorded display-garbling `STOP` from a previous host-side
serial open.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine. **A successful
rehearsal does not waive any hardware evidence gate**, and specifically does not
support any conclusion about the open serial fault.
