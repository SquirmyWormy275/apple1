# B05 Data, files, and the CF card

**Audience:** STUDY
**Time:** 40 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S04, A06

## You will learn

By the end, you can look at a stored file and say whether you are relying on it
as content, as executable code, or as a backup, and say what would have to be
true for each of those to be safe.

## Why this matters

This library is intended for archival storage on this project's CF card. That
raises a question the lessons themselves cannot answer: what does it mean to
trust something because it is on a card?

The honest answer is that it depends entirely on what you are trusting it for,
and that the three kinds of trust have almost nothing in common.

## First result

Six example files sorted into the three kinds, with a reason each.

## What you need

Paper. `assets/three-kinds.txt`. Nothing powered on and no card in anything.

## Activity

1. Read the three boxes on `assets/three-kinds.txt` and the question each one
   ends with.
2. Sort the six files in `ACTIVITY.md` Part A, giving one reason each.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**Content is judged by whether a person can still read it.** A lesson, a manual,
a photograph. A corrupted byte in the middle of a paragraph is a typo. The
document survives. What kills content is format: a file nobody has software for
is lost even though every byte is intact.

**Executable code is judged by exactness.** One wrong byte is not a typo. M02's
transcription exercise showed it: `04` becoming `40` gave a program that ran
perfectly and wrote to the wrong place. Code has no redundancy and no
proofreading. This is why the repository hashes things.

**A backup is judged by independence.** A second copy on the same card is not a
backup; it is two copies of a file that will be lost together. The question is
not "does a copy exist" but "would the copy survive whatever destroys the
original."

**The same bytes can be all three.** `line-input-0300.hex` read in A05 is
content. The same bytes entered into memory would be executable code. A copy of
the file elsewhere is a backup. Nothing about the file changed; what changed is
what you are relying on it for, and therefore what would count as it being
damaged.

That is the whole idea, and it is why "is this file OK" is not a question with an
answer until you say what for.

**What a card does and does not establish.** A file being on a card establishes
that a file is on a card. It does not establish that the file is the one you
think, that it has not changed, that it will still be readable in ten years, or
that anything on the card describes the machine next to it.

That last one is worth stating plainly. A lesson stored on this project's CF card
that describes the Woz Monitor is describing a documented design. Its presence on
the card belonging to a particular machine adds no evidence whatever about that
machine. Proximity is not provenance.

**What this repository does about it.** The collection archive tool creates a
SHA-256 inventory from files an operator names explicitly. It does not crawl,
copy, or publish. Beside each manifest the repository asks for a human note
recording original location, source, permission, date, and whether the file is an
original, a derivative, or a working copy.

The hash answers exactly one question: is this file byte-for-byte the file that
was hashed? That is the question that matters for executable code, and it is
close to useless for the "will anyone be able to read this" question that matters
for content.

**On the card mechanism itself.** How this library would be loaded, browsed, or
booted on the card is deliberately undecided in this project. The curriculum says
so directly: the catalog is defined, the boot mechanism is not. No lesson
including this one assumes a file system, a directory layout, a menu, or a boot
workflow, and none should acquire one until somebody decides.

If you find yourself reasoning "and then the card would load it," stop. That step
does not exist yet.

## Try a variation

Take one file you personally care about. Say which of the three kinds you rely on
it as, then answer that box's question honestly. Most people find the backup
question is the one they cannot answer.

## Check your understanding

1. Why is a second copy on the same card not a backup?
2. A manual and a firmware image both suffer one flipped byte. Which is in more
   trouble, and why?
3. What does a file's presence on this project's CF card establish about this
   project's board?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The archive and evidence rules are this repository's; the undecided card
mechanism is stated in its curriculum. Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish or assume:

- **No file system, directory layout, menu, or boot workflow is assumed.** The
  card mechanism is undecided in this project and this lesson does not decide it.
- Nothing about the state of this project's board or its CFFA1.
- It authorizes no firmware load, EEPROM write, **CFFA1 write**, serial-port
  open, or physical modification. Nothing here involves putting anything on a
  card.
