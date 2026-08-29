# M03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key or basis |
|---|---|
| The harness is ROM-free and models only the keyboard registers and Monitor `ECHO` and warm entry; it emulates no Propeller, serial hardware, or ROM image | E-EMU-SCOPE |
| Setup and invocation commands | REPO `docs/emulator-demo-guide.md` |
| Emulator results never prove Replica 1 Plus electrical, Propeller, PS/2, FT232R, or timing behavior | REPO `docs/emulator-demo-guide.md` |
| Do not connect an emulator to the physical serial device; do not use a successful run to waive a hardware evidence gate | REPO `docs/emulator-demo-guide.md` |
| A discrepancy from the RAM-only library is retained as a software issue | REPO `docs/emulator-demo-guide.md` |
| Expected exit path is Monitor warm entry at `$FF1F`, not `RTS` | E-EXIT; REPO `docs/emulator-demo-guide.md` |
| `line-input-echo-0300.hex` is a display-path exercise, not proof of serial TX | REPO `software/ram-only/README.md` |
| All four recorded runs, and the echo-program result | `../EMULATOR-RUNS.md` |

## The recorded results are observations

Every number in this packet's answer key was produced by running the repository's
own harness during authoring and is written down in `../EMULATOR-RUNS.md` with
its inputs. They are facts in the S04 sense: someone ran something and recorded
what came out.

They are facts **about a byte sequence executed by a software model**. The
distinction is the entire subject of the lesson.

## The instruction-count pattern

`10 x (characters + 1)` is a generalization from four observed data points, not a
derivation from the code. It fits all four recorded runs. It is presented in the
lesson as a pattern to test by prediction, which is the honest framing: a learner
who predicts an unseen value and matches it has strengthened it, and a learner
who finds an input where it fails has found something worth recording.

It should not be treated as a property of the program until someone derives it
from the loop body. Recorded as **V-12**.

## The echo-program finding

Part D's conclusion that `line-input-echo-0300.hex` has no self-directed exit
rests on two independent things: the observed `returned_to_monitor: false`, and
direct reading of its final bytes `4C 00 03` as `JMP $0300`. Both are recorded in
`../EMULATOR-RUNS.md`.

The lesson deliberately does **not** call this a defect. The software library
describes the program as restarting by design. What the lesson states is the
consequence, which is not in dispute: the program does not return to the Monitor
on its own.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-11 applies** where processor start state could matter, though no part of
  this lesson depends on the initial carry.
- **V-12 (new).** The instruction-count rule is empirical over four inputs, not
  derived. Do not promote it to a stated property of the program without deriving
  it.
- **V-8 applies absolutely.** No field of the harness output is a measurement of
  this project's board.

## What this lesson does not establish

It establishes nothing about the Replica 1 Plus. It authorizes no firmware load,
EEPROM write, CFFA1 write, serial-port open, or physical modification, and it
instructs the learner not to connect the emulator to a serial device.
