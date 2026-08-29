# H03 Why provenance matters

**Audience:** STUDY
**Time:** 45 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S04, H02

## You will learn

By the end, you can fill in an evidence card for an item, and state precisely
what a checksum establishes and what only a provenance record can.

## Why this matters

H02 was about words. This is about what stands behind them. A label is a claim,
and a claim without a record is a rumour with good posture.

The distinction this lesson turns on is between **identity** and **authenticity**,
and they are much further apart than they sound.

## First result

One evidence card, filled in, including field 10.

## What you need

Paper. `assets/evidence-card.txt`. One item you have to hand: a book, a file, a
photograph, anything. Nothing powered on.

## Activity

1. Read the ten fields on `assets/evidence-card.txt`.
2. Fill one in for an item you have, writing "not recorded" wherever you do not
   know.
3. Fill in field 10, what the card does not establish. That is your first result.

## Explain what happened

**Identity is "this is that file."** A SHA-256 hash is a long number computed
from a file's contents. Change one byte anywhere and the number changes
completely. So if you hash a file today and hash it again in ten years and the
numbers match, the file has not changed.

That is what a hash establishes, and it is genuinely valuable. It is also all it
establishes.

**Authenticity is "this is what it claims to be."** That a manual is unchanged
since you hashed it says nothing about whether it came from the manufacturer,
whether it describes the machine beside it, or whether it is a scan of a
photocopy of a reprint.

**A hash cannot answer a single authenticity question.** Not one. It is a perfect
answer to a different question.

This is why this project's archive tool is paired with a requirement for a human
note. The tool creates a SHA-256 inventory from files an operator names
explicitly. Beside each manifest, the repository asks for a note covering the
original location, the source or provenance, permission, the date, and whether
the file is an original, a derivative, or a working copy.

The hash carries identity. The note carries everything else, and only a person
can write it.

**Provenance is a chain, and it is only as good as its weakest link.** "Bought
from a dealer in 2019, who bought it from an estate in 2011, whose owner is said
to have purchased it new" has three links and the last one is the vaguest. That is
normal. What matters is that the vagueness is visible rather than smoothed over.

**Write "not recorded" and mean it.** The most damaging thing you can put on an
evidence card is a plausible guess, because a guess becomes a fact the moment
somebody reads the card without knowing it was a guess. Two years later nobody
remembers which fields were solid.

A card full of gaps is honest and useful. A card with no gaps is usually a card
somebody filled in from memory.

**Field 10 is the one people skip.** Writing down what a record does *not*
establish is the single most useful line on the card, because a record left silent
about its limits will be read as establishing whatever the reader needs. This is
S04's whole lesson applied to a filing system.

**Hash it when it arrives, not later.** A hash taken today establishes identity
from today. If a file changed last year, hashing it now records the changed
version as the reference. This is why the repository asks for a read-only
duplicate of raw captures before annotation: capture first, then work on a copy,
so the original stays fixed.

**A worked example from this project.** This library's shared source pool records
an open item: the project's knowledge base indexes a file named
`Replica_One_Plus_Manual__June_2014.pdf`, while the collection folder holds
`Replica_One_Plus_Manual_-_June_2014.pdf`. They are presumed to be the same June
2014 edition. No hash comparison has been run, so that presumption is exactly
that.

One command would settle it. Until somebody runs it, "presumed the same" is the
honest wording, and this library uses it.

## Try a variation

Take the evidence card you filled in and give it to somebody else without
explaining it. Ask them what they now believe about the item. Compare against what
you intended the card to say.

## Check your understanding

1. What does a matching SHA-256 hash establish?
2. Name one authenticity question a hash can answer.
3. Why is "not recorded" better than a plausible guess?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The archive tool's behavior and the required human note are this repository's.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- **It authenticates nothing** and makes no claim about any object's originality
  or value.
- It resolves no open provenance question in this project, including the manual
  identity item it uses as an example.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
