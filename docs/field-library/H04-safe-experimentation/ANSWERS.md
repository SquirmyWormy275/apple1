# H04 Answer key

## Part A: six actions

| # | Action | Bin | Reason |
|---|---|---|---|
| 1 | Trace on paper | **Green** | Nothing powered, connected, or changed. |
| 2 | Run in the emulator on a laptop | **Green** | Off-device software on an ordinary computer. The emulator guide permits it and forbids connecting it to a serial device. |
| 3 | Type its bytes into the Monitor | **Amber** | A RAM-only candidate. The artifact carries no live-run authority, and entering it is a separate operator-led step under the software library's acceptance card. |
| 4 | Open the FT232R to see what happens | **Red** | This is the standing block. It has already produced a display-garbling `STOP`, and an opened session is blocked pending a measurement test card and an explicit operator start. |
| 5 | SHA-256 of a named manual | **Green** | The archive tool works only on files an operator names and does not open serial hardware. |
| 6 | Wire CA2 to a Propeller pin | **Red** | Wiring is red on its own, and this specific one is called out as hazardous: CA2 can be 5 V and Propeller GPIO is 3.3 V. |

Action 4 is the one people misjudge, because "to see what happens" sounds like
curiosity rather than a test. It is a test, it has been run, and the result is
recorded.

## Part B: ten more

| # | Bin | Note |
|---|---|---|
| 1 | **Green** | Reading a source archive changes nothing. |
| 2 | **Red** | EEPROM action. |
| 3 | **Green** | Powered off, nothing changed. The preservation dossier asks for exactly this in its baseline inventory. |
| 4 | **Red** | The dossier records jumper and DIP state **while powered down only**, with a photograph before and after any intentional change. Doing it powered is outside that. |
| 5 | **Red** | Writing the lesson is itself outside the curriculum's rules. Rule 6 excludes firmware loading from lessons; a lesson describing how would violate it. |
| 6 | **Green** | Paper. |
| 7 | **Red** | CFFA1 write. |
| 8 | **Green** | Off-device, and it is what `../EMULATOR-RUNS.md` records. |
| 9 | **Red** | A physical change to the machine. |
| 10 | **Green** | Paper. |

Item 5 is the subtle one: some red actions are red as *writing*, not just as
doing. This library cannot contain a firmware-loading procedure even if nobody
ever follows it.

## Part C: what would have to exist

| Action | What must exist | Who decides |
|---|---|---|
| Entering a RAM-only program | A photographed initial monitor prompt, a recorded power and USB topology, confirmation that no host serial process has the FT232R open, the exact byte record retained, and a prepared reset recovery. All from the software library's acceptance card. | The operator, in a separate session. Not this library, not a learner, not a lesson. |
| An opened serial session | A measurement test card, ready. | An operator, explicitly starting that single step. |
| Any EEPROM action | Nothing in this project currently authorizes it. It is excluded from ordinary development work. | Not addressed by any current document; it would need a decision that does not yet exist. |

The third row's honest answer is that there is no process for it, which is
different from there being a process nobody has completed.

## Part D: the standing red

1. **The display garbled.** Opening the FT232R from the host produced a
   display-garbling `STOP` result.
2. **An opened serial session and a transmit test are blocked.**
3. **Two things:** a measurement test card must be ready, and an operator must
   explicitly start that single step.
4. **No.** This lesson lifts nothing. It restates a boundary; it has no power to
   change one.

## Part E: the asymmetry

| | Cost if wrong |
|---|---|
| Green treated as amber | A little time, and a question asked that did not need asking. Recoverable in minutes. |
| Amber treated as green | A machine in an unknown state, an evidence trail broken, possibly damage to an object that cannot be replaced. Recoverable slowly or not at all. |

**One sentence:** the cost of being too careful is minutes and the cost of being
too casual can be permanent, so a doubtful action should be treated as the more
expensive kind.

## Part F: what this lesson does not contain

Three, from many:

1. **How to open a serial port.** Absent because it is red, and because this
   project has a standing block on it.
2. **How to enter a program on the Monitor.** Absent because entry is amber and
   operator-led; the acceptance card in the software library governs it, and a
   lesson that walked a learner through it would be granting what it cannot
   grant.
3. **How to write the EEPROM, or the CF card, or move a jumper safely.** Absent
   because all are red, and because "safely" would be a claim this library cannot
   support.

The general principle: this lesson names categories so a reader can recognise
them. Recognising is green. Describing how would not be.

## Part G: your own case

No fixed answer. Acceptance: honest sorting, and for anything not green, a
statement of what would have to exist and who would decide.

The instruction to be honest about how much you want to do it is deliberate. A
person who writes "I would very much like to try this and it is amber" has
understood the lesson better than one who claims not to be tempted.

## Try a variation

Same as Part G.

## README: Check your understanding

1. **Green.** Every lesson in this library is off-device, including this one.
2. **That nobody has granted permission to run it on hardware, that this library
   cannot grant it, and that reading, tracing, or rehearsing it off-device does
   not move it closer to being run.** It is not a pending approval; it is an
   absence of authority.
3. **Because the costs are not symmetric.** Being over-cautious costs minutes.
   Being under-cautious can cost an irreplaceable machine or an evidence trail
   that took months to build. When the downside is that lopsided, the doubtful
   case belongs on the expensive side.
