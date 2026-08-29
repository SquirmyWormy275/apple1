# H04 Safe experimentation

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S04, M04

## You will learn

By the end, you can take any action you might want to try and place it in one of
three bins: do it now, do not start it yourself, or not in a lesson at all.

## Why this matters

Curiosity is the reason anyone is here, and it is also the thing most likely to
put a machine into a state nobody can recover. The point of a boundary is not to
stop you learning. It is to make sure the thing you are learning from is still
there tomorrow.

This project has a machine with an unresolved fault and a recorded incident. The
boundaries below are not hypothetical, and they are not this lesson's invention.
They are the project's own, restated.

## First result

Six actions sorted green, amber, or red.

## What you need

Paper. `assets/decision-card.txt`. Nothing powered on, which is itself the
lesson.

## Activity

1. Read the three bins on `assets/decision-card.txt`.
2. Sort the six actions in `ACTIVITY.md` Part A.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**Green means off-device: nothing powered, connected, or changed.** Reading,
paper work, tracing, running the repository emulator on an ordinary computer,
hashing files somebody named explicitly. Every lesson in this library is green,
including this one.

Green needs no permission because there is nothing to permit. No machine is
involved, so no machine can end up in a state somebody has to recover.

**Amber means a RAM-only candidate.** This project holds two programs that could
one day be entered by hand into RAM in a separate, operator-led session. The
software library classifies them as candidates with **no live-run authority**.

That phrase is doing real work. It does not mean "not yet approved by a form."
It means nobody has granted it, this library cannot grant it, and reading about
the programs, tracing them, and rehearsing them off-device does not move them any
closer to being run.

**Amber is not yours to start.** If you find yourself wanting to, that wanting is
the signal that the boundary is doing its job.

**Red means it does not belong in a lesson at all.** The curriculum's own rule
lists them: firmware loading, EEPROM writing, CFFA1 modification, serial-port
opening, and automated physical-device control. The preservation dossier adds
temporary CA2 wiring, soldering, resistor installation, uploader use, RAM load,
and EEPROM action, and says none of it belongs in ordinary development work.

No lesson in this library contains a procedure for any of them, and this lesson
does not either. Naming a category is not describing how to do it.

**The standing red in this project, stated as history.** Opening the FT232R from
the host has already produced a display-garbling `STOP`. An opened serial session
or transmit test is blocked until a measurement test card is ready and an operator
explicitly starts that single step.

That is a record of something that happened and a boundary that follows from it.
It is not an instruction, and it is not a thing to try in order to see it again.

**One specific hazard worth knowing, because knowing is protective.** The
project's own hardware notes warn against attaching a direct wire between CA2 and
the Propeller: CA2 can be 5 V and Propeller GPIO is 3.3 V. That is recorded here
so a reader who has the idea knows it is a known bad one, not so anyone can act
on it. It is red.

**Why "when in doubt it is not green."** Because the cost is asymmetric. Treating
a green action as amber costs you a little time. Treating an amber action as green
can cost an irreplaceable object, or an evidence trail that took months to build.

**And the honest note.** Boundaries like these can feel like being kept away from
the interesting part. What they actually protect is your ability to keep going.
An unrecoverable machine ends the project; a paused one does not.

## Try a variation

Take something you would genuinely like to try on this machine. Sort it honestly.
If it is amber or red, write down what would have to exist before it could
proceed, and who would have to decide.

## Check your understanding

1. Which bin is every lesson in this library, including this one?
2. What does "no live-run authority" mean, precisely?
3. Why does "when in doubt it is not green" follow from the costs involved?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Every boundary here is quoted or restated from this repository's own documents.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** contain or authorize:

- **No procedure for any red action appears anywhere in this packet.** Categories
  are named so they can be recognised; none is described.
- It grants no authority of any kind, and completing it advances nothing toward a
  live session.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
