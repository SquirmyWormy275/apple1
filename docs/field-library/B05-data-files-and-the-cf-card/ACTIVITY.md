# B05 Activity: sort the files

**Status:** OFF-DEVICE. Paper only. **No card is inserted, read, or written at
any point in this activity.**

## Part A: six files (this is the first result)

Mark each **C** (content), **X** (executable code), or **B** (backup). Some may
be more than one; say so and say in what context.

| # | File | C/X/B | Reason |
|---|---|---|---|
| 1 | A scanned PDF of the Replica 1 Plus manual | | |
| 2 | `line-input-0300.hex` | | |
| 3 | A second copy of that manual on a different drive | | |
| 4 | The vendor `110REV03` source archive | | |
| 5 | A photograph of the board's serial number | | |
| 6 | A SHA-256 manifest listing every file above | | |

File 6 is the interesting one.

## Part B: what would ruin it

For each, name the failure that would matter most.

| File | Worst failure |
|---|---|
| A lesson stored as plain text | |
| A firmware image | |
| A photograph of a serial number | |
| A backup of the whole collection | |

## Part C: the same bytes, three roles

`line-input-0300.hex` appears in three situations. Say which kind it is in each,
and what would count as damage.

1. Quoted in A05 for a learner to read.
2. Entered into memory at `$0300`.
3. Copied to a second drive alongside the rest of the repository.

## Part D: does the hash help

For each question, say whether a SHA-256 hash of the file answers it.

| # | Question | Does the hash answer it? |
|---|---|---|
| 1 | Is this the same file that was hashed? | |
| 2 | Is this the firmware installed on the board? | |
| 3 | Has anyone modified it since? | |
| 4 | Will anyone be able to open it in 2050? | |
| 5 | Did it come from the vendor? | |
| 6 | Are there two identical copies in different places? | |

## Part E: proximity is not provenance

A lesson describing the Woz Monitor sits on this project's CF card, in the same
box as this project's Replica 1 Plus.

1. What does that arrangement establish about the board?
2. What would somebody be tempted to conclude?
3. Name a plausible way the two could disagree.

## Part F: the undecided part

The curriculum states that the card boot and menu mechanism is intentionally
undecided.

1. Name three things you do not know about how this library would be used on a
   card.
2. For each, say what would go wrong if a lesson quietly assumed an answer.

## Part G (optional, STUDY): write a retention note

Write the human note the collection archive asks for, beside a manifest, for one
file of your choosing. Include original location, source, permission, date, and
whether it is an original, a derivative, or a working copy.

## What this activity does not do

It classifies files on paper. **No card is read or written.** It authorizes no
hardware action of any kind.
