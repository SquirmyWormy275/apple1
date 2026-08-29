# Teacher materials

For running this with a group: a classroom, a club, a museum workshop, a kitchen
table. Aimed at curious beginners from about twelve upward, including adults who
have never done this.

| File | What it is | Time |
|---|---|---|
| `teacher-guide.md` | How to run the sessions, what goes wrong, what to say | Read once |
| `worksheet-hex-and-binary.md` | Numbers the way the machine holds them | 40 min |
| `worksheet-memory-map.md` | Where things live and why it matters | 45 min |
| `worksheet-debugging.md` | Expected against observed, and when to stop | 50 min |
| `answer-key.md` | Every answer, with working shown | Reference |

## No prior knowledge assumed

No maths beyond counting and dividing by sixteen. No programming. No electronics.
A learner who has never seen hexadecimal can start at worksheet one and finish
worksheet three.

## Everything here is off-device

**Every activity in this folder is paper and pencil.** Nothing requires a
computer, and nothing at all requires the Apple-1 or the Replica 1 Plus.

Two activities offer an *optional* extension using the repository's emulator on
an ordinary computer. Both say so, both are marked optional, and both have the
paper version as the primary path rather than a fallback. If you have no
computers in the room, you lose nothing.

**No activity involves the Replica 1 Plus.** Not powering it on, not connecting
to it, not typing on it, not running anything on it. If the machine is in the
room it is scenery, and `../visitor-mode/README.md` has the words for that.

## What every activity gives you

Each worksheet is built so that:

- **Something visible happens in the first three actions.** A filled table, a
  built byte, a completed trace. Not twenty minutes of setup.
- **Every question has an answer**, in `answer-key.md`, with the working, not
  just the result.
- **Open-ended questions have acceptance criteria** rather than a single string,
  so two teachers marking two learners reach the same verdict.
- **Discussion prompts** are supplied, with the answers that usually come up.
- **Extensions** are there for whoever finishes early, and are genuinely harder
  rather than merely longer.

## Running them in order, or not

They are ordered but only worksheet three depends on the others, and lightly.

| Want to teach | Use |
|---|---|
| Number systems, encoding | Worksheet 1 alone |
| How memory is organised | Worksheet 2, ideally after 1 |
| Careful thinking and evidence | Worksheet 3, which is the one that transfers furthest |

If you can only run one, **run worksheet three.** It is about telling what you
saw from what you concluded, and that outlives every technical fact here.

## Sources and honesty

Historical and Apple-1-specific claims carry source keys that resolve in
`../SOURCES.md`. General computing facts are labelled as such and carry no
citation, because they need none.

This library keeps a register of its own open questions in `../README.md`, and
some of them touch these worksheets. Where that happens, the answer key says so.
A teacher who tells a class "this bit is genuinely unresolved" is modelling the
subject better than one who does not.

## What these materials do not establish or authorize

They make no claim that this project's machine powers on, displays, reads a key,
or moves a byte over serial. They make no claim about the value or authenticity
of any object. They authorize no firmware load, EEPROM write, CFFA1 write,
serial-port open, or physical modification.
