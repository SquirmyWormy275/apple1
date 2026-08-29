# Teacher guide

Read this once before running anything. It is about how the sessions go, not
what is in them.

## The whole thing in one paragraph

You are teaching three ideas. That numbers can be written in more than one way,
and one of those ways fits the hardware. That memory is a row of numbered boxes
and nothing in a box says what kind of thing it is. And that what you saw and
what you concluded are different sentences. The Apple-1 is the setting, not the
subject.

## Supplies

**For every session:**

- Printed worksheets, one per learner
- Pencils, and erasers, because being able to change your mind matters here
- Something to write on the wall or a board

**Worksheet 1 additionally:**

- Optional: eight coins per pair, for the byte-building game. Heads is 1.

**Worksheet 3 additionally:**

- Nothing extra. Optionally a computer with the repository and Python, for the
  extension only.

**Never:** the Replica 1 Plus, powered or connected.

## Timing, honestly

The stated times assume a group that asks questions.

| Worksheet | Core | With discussion and extensions |
|---|---|---|
| 1, hex and binary | 25 min | 40 min |
| 2, memory map | 30 min | 45 min |
| 3, debugging | 30 min | 50 min |

**The first ten minutes of worksheet 1 take longer than you expect** and
everything after goes faster. Do not rush the 0-to-15 table; it is load-bearing.

## Learning objectives

Written as things you could watch someone do.

**Worksheet 1.** Converts a number under 256 to hexadecimal and back. Builds any
byte from its bit values. Explains why hex rather than decimal.

**Worksheet 2.** Places an address in the right region of a memory map. Explains
why the same byte can be a number, a letter, or an instruction. Spots when a
program and its data would collide.

**Worksheet 3.** Writes an expectation before observing. States one hypothesis
that could be shown false. Decides whether an observation means continue or
stop.

## What actually goes wrong

**Worksheet 1: "why are there letters in the numbers."** Do not explain base
sixteen first. Have them count on their fingers past nine and notice they need
new symbols. Then A to F is obvious rather than arbitrary.

**Worksheet 1: bit numbering.** Bit 0 is on the *right*. Everyone gets this
wrong once. Let them, then point at it.

**Worksheet 2: "how can it be a letter and an instruction."** This is the
genuinely hard idea in the set and it is worth the time. The move that works: ask
them what the number 65 in their head *is*. It is not anything until they decide
to count sixty-five things with it.

**Worksheet 3: everybody wants to fix it first.** They will spot a suspicious
byte before they have traced anything. Make them trace. The discrepancy should
find them; if they go hunting they will find something plausible and stop.

**Worksheet 3: "but it worked."** The program in that worksheet runs cleanly and
returns properly and is wrong. Some learners will not accept a bug they cannot
see fail. That reaction *is* the lesson.

## Discussion prompts that reliably work

Use these when a group finishes early or goes quiet.

- **"What's the smallest number you can't write in one byte?"** (256. And the
  reason is the interesting part.)
- **"If memory doesn't know what kind of thing it's holding, how does anything
  ever work?"** (Because the program decides, consistently. Reliability is a
  property of the program, not the memory.)
- **"Is a wrong answer arrived at by correct reasoning better or worse than a
  right answer arrived at by luck?"** Genuinely arguable. Let them argue.
- **"We don't know what firmware is on this machine. Why not just look?"**
  (Because there is no approved way to read it back here yet, and guessing would
  put a claim in the record that nobody measured.)
- **"What's something you believe about a machine you own, that you've never
  checked?"** This one lands with adults.

## Age notes

**Around twelve.** Worksheet 1 works as-is. Worksheet 2 needs the collision
exercise done together rather than alone. Worksheet 3's extension is too much;
stop at the trace.

**Teenagers.** All three as written. The debugging one lands hardest with anyone
who has already written code and been burned.

**Adults with no background.** Identical to twelve-year-olds and often slower to
start, because they expect it to be beyond them. Say early that there is no maths
in it. That single sentence changes the room.

**Mixed groups.** Pair an adult with a younger learner and give them one
worksheet between them. It works better than it sounds; the adult reads and the
younger one usually spots the pattern first.

## Marking

`answer-key.md` gives working, not just answers. For open questions it gives
acceptance criteria.

Two habits worth marking for, above correctness:

- **Did they write "unknown" where the answer is unknown?** A learner who wrote
  `$00` for an unestablished value has invented a fact, and that is a more
  important thing to catch than an arithmetic slip.
- **Did they mark their guesses as guesses?** In worksheet 3 especially.

## The boundary, if the machine is in the room

> "You're welcome to look. I'd ask you not to touch the board or the cables. Not
> because it's fragile, but because we're partway through diagnosing a fault and
> anything that moves has to get written down."

Nothing in these worksheets needs the machine. If a learner asks to try
something on it, the answer is that it would be a separate session run by an
operator with a record being kept, and that today is not that. Then show them the
paper version, which is easier to see anyway.

## Sources

Historical claims in the worksheets carry keys resolving in `../SOURCES.md`.
The programs used in worksheet 3 are teaching artifacts written for this library
and carry **no hardware authority**; they are not in `software/ram-only/` and
have not been through that library's acceptance process.

## What this guide does not establish or authorize

It makes no claim about this project's machine working. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification, and no activity in this folder brings a learner into contact with
the hardware.
