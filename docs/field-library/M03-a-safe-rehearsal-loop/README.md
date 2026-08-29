# M03 A safe rehearsal loop

**Audience:** BUILD
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** C05, M02

## You will learn

By the end, you can run one of this repository's RAM-only programs in the
project emulator, predict its result before running it, and state precisely what
a matching result does and does not establish.

## Why this matters

Predicting on paper is good. Predicting on paper and then checking is better,
because it tells you when your model of the program is wrong. The emulator gives
you that loop with nothing at risk: no hardware, no power, no chance of leaving
a machine in a state somebody has to recover.

The habit this lesson builds is not "run the emulator." It is **write your
prediction down first**. A run you did not predict teaches you almost nothing,
because whatever comes out will look reasonable in hindsight.

## First result

One recorded run whose observed output you predicted correctly beforehand.

## What you need

- A computer with Python and this repository. Not the Apple-1.
- `docs/emulator-demo-guide.md`, which has the setup commands.
- `assets/rehearsal-card.txt`, printed or copied out.

Do not connect the emulator to any serial device. The emulator guide says this
directly, and it is the one way this off-device lesson could stop being
off-device.

## Activity

1. Fill in the top half of `assets/rehearsal-card.txt` for
   `software/ram-only/line-input-0300.hex`, including your **prediction**, before
   running anything.
2. Follow `docs/emulator-demo-guide.md` to install the development requirements
   and run that program with the input `HI` followed by a carriage return.
3. Fill in the observed half of the card and compare. That is your first result.

## Explain what happened

**What the harness is.** `tools/apple1_emulator.py` is a small, deliberately
narrow program. Its own documentation is blunt about the limits: it is ROM-free,
it models the keyboard registers and the Monitor's `ECHO` and warm-entry calls
that these programs need, and it emulates no Propeller, no serial hardware, and
no Apple-1 ROM image.

That narrowness is a feature. A full-machine emulator would invite the belief
that a passing run says something about the machine. This one cannot be mistaken
for the Replica 1 Plus, because it is visibly missing most of it.

**What it reports.** Four fields: the screen text, the buffer contents, whether
the program returned to the Monitor warm entry, and how many instructions ran.

**The recorded results.** These runs have been performed and written down in
`../EMULATOR-RUNS.md`:

| Input | Screen | Buffer | Returned | Instructions |
|---|---|---|---|---:|
| `A` + CR | `A` CR | `A` CR | true | 20 |
| `HI` + CR | `HI` CR | `HI` CR | true | 30 |
| `HELLO` + CR | `HELLO` CR | `HELLO` CR | true | 60 |

Two things are worth noticing. The screen and the buffer agree, which is the
program working: it stores each character and echoes it. And the instruction
count follows a pattern, ten per character plus ten, which lets you predict a run
you have not done.

**Reproducible means it gives the same answer every time.** Same bytes, same
input, same four numbers. If you get something different, the interesting
question is what differed: a changed byte, a different input, a different version
of the harness. A run that varies between attempts is telling you something is
not pinned down.

**The boundary, stated plainly.** A green result here is evidence about twenty-six
bytes of 6502 code. It is not evidence that this project's Replica 1 Plus powers
on, that its display works, that its keyboard is read, that its Propeller is
running the firmware anyone thinks it is, or that a byte can cross its serial
port. The repository's emulator guide puts it as a rule: do not use a successful
emulator run to waive a hardware evidence gate.

The reason this matters here more than usual is that this repository has an open
serial fault. A working rehearsal is exactly the kind of result that tempts
someone to conclude the software side is fine and move on to hardware. It does
not license that move.

## Try a variation

Predict the instruction count for the input `APPLE-1` before running it, using
the pattern in the table. Then run it. Recording a correct prediction of a number
you had never seen is a stronger result than any single run.

## Check your understanding

1. Why does the rehearsal card ask for a prediction before the observation?
2. The harness reports `returned_to_monitor`. Why is that worth reporting
   separately from the screen text?
3. A rehearsal passes. Name three specific things about the physical machine
   that remain exactly as unknown as before.

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The harness scope is quoted from its own documentation; the recorded results are
in `../EMULATOR-RUNS.md`; the evidence rule is the repository's. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish:

- Nothing about the Replica 1 Plus. Not one field of the harness output is a
  measurement of hardware.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification. The emulator must not be connected to a serial device.
