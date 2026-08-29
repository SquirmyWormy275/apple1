# X01 Hex scavenger hunt

**Audience:** LEARN
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S03, C02, C04, M02

## You will learn

By the end, you can read a memory dump, locate specific values in it, and
interpret them as addresses, instructions, or text as the situation requires.

## Why this matters

This is a consolidation exercise. Everything it needs you already have: hex from
S03, addresses from C02, character encoding from C04, and listing anatomy from
M02. What it adds is the practice of using them together against a dump you have
not seen before, which is what reading real memory is actually like.

## First result

The first three answers on the hunt sheet.

## What you need

Paper. `assets/hunt-sheet.txt`, which has both dumps and five hints.
`ANSWERS.md`, which you should not open until you have tried.

## Activity

1. Look at Dump One on `assets/hunt-sheet.txt`. It is a real repository
   artifact.
2. Answer questions 1 to 3 in `ACTIVITY.md` Part A.
3. Check those three against `ANSWERS.md`. That is your first result.

## Explain what happened

**A dump is addresses down the side and bytes across.** Each line begins with the
address of its first byte, and each byte after that is one address further along.
Eight per line here, which is what the Monitor's own block display uses.

Nothing marks where instructions begin, so finding an instruction means working
out where the previous one ended, which is M02's skill.

**Two dumps, and they are different kinds of thing.** Dump One is real: it is
`line-input-0300.hex` from this repository, laid out as a Monitor-style block.
Dump Two is invented for this puzzle and says so on its face; it is not a reading
from any machine.

That labeling is not decoration. A dump that looks like a reading and is not is
exactly the kind of thing that ends up cited as evidence three years later.

**Hunting for an address inside an instruction.** The bytes `4C 1F FF` contain an
address, and it reads backwards: low byte first, so `1F FF` is `$FF1F`. Finding
addresses inside instructions means expecting them reversed and remembering that
the byte before them says which instruction it is.

**Hunting for text.** Dump Two is text with the high bit set, as C04 covered.
Subtract `$80` from each byte and look up the result. Do it in the other order and
you find nothing, because ASCII assigns nothing above 127.

**Why a scavenger hunt and not a quiz.** Because searching is the skill. Being
told "at `$0317` there is a jump" teaches nothing; being asked "where does this
program end and how do you know" makes you count, check, and be sure. The hints
are there so the searching stays productive rather than becoming guessing.

**Use the hints when you are stuck, not before.** They are on the sheet rather
than in the answer key deliberately. A hint that shortens a search is helping; an
answer that ends it is not.

## Try a variation

Write your own dump-two style puzzle: encode a short message with the high bit
set, lay it out eight bytes per line with addresses, and give it to somebody who
has done C04. Include one hint.

## Check your understanding

1. In a dump, what tells you where an instruction begins?
2. Why does `4C 1F FF` contain the address `$FF1F` rather than `$1FFF`?
3. Why must you subtract `$80` before looking up a character from Dump Two?

## Answer key

See `ANSWERS.md`, which is a separate file so it can stay closed.

## Sources and boundaries

Dump One is a repository artifact. Dump Two is invented and labeled as such.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- **Dump Two is not a reading from any machine** and must never be cited as one.
- Nothing here is a reading from this project's board, including Dump One, which
  is a file laid out for display rather than memory that was inspected.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
