# H03 Answer key

## Part A: one card

Acceptance criteria:

- Field 10 is filled in. A card without it has not passed.
- At least one field says "not recorded" for an item the learner did not create
  themselves. A card with no gaps is usually a card filled in from memory.
- Field 6 distinguishes original, derivative, or working copy rather than being
  left blank.
- Field 9 and field 10 say different things. If they overlap, the learner has
  not separated what the record shows from what it is silent about.

## Part B: identity or authenticity

| # | Hash? | Why |
|---|---|---|
| 1 | **Yes** | This is exactly what a hash is for. |
| 2 | **No** | Origin is a provenance question. |
| 3 | **Yes**, if you have the earlier hash | Any edit changes the hash completely. |
| 4 | **No** | Correspondence between a document and an object is not a property of the file. |
| 5 | **Yes** | Hash both and compare. |
| 6 | **No** | What the scan was made from is not recoverable from the file's bytes. |
| 7 | **No** | This is the project's own open question, and no hash of a file can close it. |

**Three yeses out of seven**, and every yes is a variation of the same question:
"are these bytes those bytes." Every no is an authenticity question.

That is the shape to remember. A hash answers one question extremely well and no
others at all.

## Part C: the chain

| Link | Support | Strength |
|---|---|---|
| Dealer to you, 2019 | A receipt, a listing, correspondence | **Strong.** Recent, documented, both parties available. |
| Estate to dealer, 2011 | The dealer's own records, if kept | **Moderate.** Depends entirely on one party's records. |
| Purchased new | "Said to have," with no named source | **Weak.** Hearsay, unattributed, undated. |

**The weakest link is the last**, and note that it is also the most interesting
one, which is usually how this goes. What would strengthen it: a named person
making the statement, a purchase document, a period photograph, or a serial number
matching a dealer record.

What would *not* strengthen it: the object looking right. That is the H02
boundary.

## Part D: spot the guess

**Card 2 contains the invention.** Several signs:

- "Permission: freely distributed" is a legal conclusion stated as a fact, with
  no source given. Card 1 says "not recorded," which is the honest state.
- "Type: original" for a downloaded copy is almost certainly wrong. A download is
  a copy; the vendor holds the original.
- The precise date sits oddly beside the vague source. If the retrieval date was
  recorded, the URL usually was too.

**Card 1 looks worse and is better.** It is full of gaps, and every gap is
accurate. Card 2 reads as complete and two of its four fields are unsupported.

This is the exercise's whole point: a tidy record is not the same as a true one.

## Part E: field 10 practice

| Item | Does not establish |
|---|---|
| Hashed copy of the manual | That it is the vendor's original file, that this edition matches the board, or that the board behaves as documented. |
| Photograph of a serial number | That the number belongs to this board rather than another, unless the photograph shows enough context, or what the number means. |
| Vendor `110REV03` source | That it was compiled, that a build of it was installed, or that it is what is on the EEPROM now. This project records it as candidate evidence only. |
| A recorded emulator run | Anything about hardware. It is evidence about a byte sequence executed by a software model. |

## Part F: the open question

1. **A matching hash would establish that the two files are byte-for-byte
   identical**, so the index and the collection hold the same file under two
   names.
2. **It would still not establish** that the file is the vendor's original, that
   the edition is the one the board shipped with, or anything about the board.
3. **A mismatch would mean two different files.** Then the question becomes which
   one the library's citations refer to, and every page number in this library's
   source pool would need checking against the right one.
4. **An unclosed item**, and a small one. It is recorded, its consequence is
   understood, and one command settles it. The failure mode would be forgetting
   it, which is why it is written down as a numbered verification item rather
   than left as an impression.

## Part G: the read-only rule

1. **Because annotation changes the file**, and once changed there is no
   unmodified version left to go back to. The copy has to exist before the first
   edit or it never exists at all.
2. **You get a copy of an annotated file**, which preserves your interpretation
   along with the data and makes them impossible to separate later. Someone
   reading it cannot tell which marks were in the original capture.
3. **No.** Hashing an annotated file records the identity of the annotated file.
   It proves nothing was lost after that point, and the original is still gone.
   Hashing and duplicating solve different problems: one fixes identity going
   forward, the other preserves the thing itself.

## Try a variation

The usual result: the reader believes more than the card says, particularly about
origin. Fields left as "not recorded" are read as unimportant rather than
unknown, and field 10 is the only thing that reliably stops it.

If the reader's beliefs match the card exactly, the card is well written.

## README: Check your understanding

1. **That the file has not changed since it was hashed.** Byte-for-byte identity,
   nothing more.
2. **None.** A hash answers no authenticity question at all. If a learner offers
   one, look closely: it will turn out to be an identity question wearing
   different words.
3. **Because a guess becomes a fact as soon as someone reads it without knowing
   it was a guess.** A gap stays visibly a gap. Two years on, nobody remembers
   which fields were solid, and the honest record is the one that told you.
