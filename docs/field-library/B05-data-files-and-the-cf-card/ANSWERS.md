# B05 Answer key

## Part A: six files

| # | File | Kind | Reason |
|---|---|---|---|
| 1 | Scanned manual PDF | **C** | Read by a person. A flipped byte is a blemish, not a failure. |
| 2 | `line-input-0300.hex` | **C or X, depending** | Content when read in a lesson; executable code when entered into memory. |
| 3 | Second copy of the manual elsewhere | **B**, and also **C** | It is a backup by role and content by kind. Both are correct. |
| 4 | Vendor `110REV03` source | **C**, arguably **X** | It is source, not a built image, so nothing executes it directly. The repository classifies it as candidate evidence, not the installed image. Treating it as executable code is exactly the error S04 uses as its worked example. |
| 5 | Photograph of a serial number | **C** | Evidence to be looked at. Its value is in being legible and unaltered. |
| 6 | SHA-256 manifest | **C**, and something else besides | See below. |

**File 6 is the interesting one.** A manifest is content: a list of hashes a
person reads. But its whole purpose is to establish something about *other*
files, which means it has a property none of the others do: **it must itself be
protected, and it cannot protect itself.** A manifest whose integrity you cannot
vouch for tells you nothing, because anyone who altered a file could alter its
hash in the same manifest.

A learner who spots that has found the real answer.

## Part B: what would ruin it

| File | Worst failure |
|---|---|
| A lesson as plain text | Nobody can find it, or the format becomes unreadable. Plain text is unusually safe here, which is why this library uses it. |
| A firmware image | One changed byte, undetected. |
| A photograph of a serial number | Being illegible, or losing the record of what it is a photograph of. An unlabelled photo is nearly worthless. |
| A backup of the collection | Being stored in the same place as the original, so one event destroys both. |

## Part C: the same bytes, three roles

| Situation | Kind | What counts as damage |
|---|---|---|
| Quoted in A05 for reading | **Content** | A typo in a quoted byte, which would teach the wrong thing but harm nothing else. |
| Entered into memory at `$0300` | **Executable code** | Any single wrong byte, which may produce a program that runs and misbehaves. |
| Copied to a second drive | **Backup** | The copy living somewhere that shares a failure with the original. |

**The bytes are identical in all three.** What differs is what you are relying on
them for, and therefore what would count as them being damaged. That is the
lesson.

## Part D: does the hash help

| # | Question | Answer |
|---|---|---|
| 1 | Same file that was hashed? | **Yes.** This is exactly what a hash answers. |
| 2 | Is this the installed firmware? | **No.** File identity says nothing about a chip. |
| 3 | Modified since? | **Yes**, provided you have the earlier hash and trust it. |
| 4 | Openable in 2050? | **No.** A hash says nothing about formats or software. |
| 5 | Did it come from the vendor? | **No.** Origin is a provenance record, not a hash. The repository asks for the source URL, retrieval date, and permission note separately, precisely because the hash cannot carry them. |
| 6 | Two identical copies in different places? | **Yes**, if you hash both and compare. |

Three yeses and three noes, and the noes are the ones people assume are yeses.

## Part E: proximity is not provenance

1. **It establishes that a file is on a card, and that the card is in a box.**
   Nothing more.
2. **Somebody would be tempted to conclude that the lesson describes this
   machine**, or that this machine has the Monitor the lesson describes, or that
   the two were verified against each other by whoever put them together.
3. **A plausible disagreement:** the lesson describes the documented Woz Monitor
   at `$FF00`. This board's EEPROM contents are unestablished; the repository
   treats the vendor source as candidate evidence only. If this board carried a
   modified or different image, the lesson and the machine would disagree, and
   nothing about their being in the same box would reveal it.

This is S04's statement (b) arriving from a different direction.

## Part F: the undecided part

Three things not known, from many possible:

1. **Whether there is a file system at all**, and if so which.
2. **Whether there is a menu or index**, and how a reader would find a lesson.
3. **Whether anything boots from the card**, or whether it is storage only.

Also acceptable: directory layout, filename length limits, whether the machine
can read the card unaided, what software would display a lesson.

**What goes wrong if a lesson assumes an answer:** it acquires a dependency
nobody agreed to. If a lesson says "select item 3 from the menu," then either a
menu now has to exist, or the lesson is wrong. Written down and stored, that
assumption becomes something a future reader takes as a statement of fact about
the project. Worse, a lesson that assumes a boot workflow is describing a
procedure on hardware that nobody has approved.

## Part G: write a retention note

A sample:

> **File:** `Replica_One_Plus_Manual_-_June_2014.pdf`
> **Original location:** Collection folder, "Manuals and Documentation".
> **Source:** Briel Computers product documentation, June 2014 edition. Exact
> retrieval route not recorded at time of filing.
> **Permission:** Vendor product manual retained for the owner's own reference.
> No redistribution assumed.
> **Date filed:** Not recorded.
> **Original, derivative, or working copy:** Believed a working copy of a vendor
> PDF. Not established whether it is the vendor's original file.

Note how many fields end in "not recorded." That is the honest state of a note
written after the fact, and it is far more useful than a confident invention. A
learner whose note has no gaps in it has probably guessed.

The shared source pool for this library records a related open item: the project
index holds a file named `Replica_One_Plus_Manual__June_2014.pdf` while the
collection folder holds `Replica_One_Plus_Manual_-_June_2014.pdf`, and no
SHA-256 comparison has been run between them.

## Try a variation

No single answer. The common finding is that people can answer the content and
code questions about their own files and cannot answer the backup question,
because they have a copy somewhere but have never asked whether it would survive
the same event.

## README: Check your understanding

1. **Because it shares every failure with the original.** Card lost, both copies
   lost. A backup's value is entirely in being independent.
2. **The firmware image.** A flipped byte in a manual is a visible typo in one
   word and the document still works. A flipped byte in an image may change an
   instruction, and nothing announces it.
3. **Nothing.** It establishes that a file is on a card. Proximity is not
   provenance, and no arrangement of storage is evidence about a chip.
