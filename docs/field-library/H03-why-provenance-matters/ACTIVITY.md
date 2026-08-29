# H03 Activity: fill an evidence card

**Status:** OFF-DEVICE. Paper only. **No object is authenticated and no hardware
is touched.**

## Part A: one card (this is the first result)

Fill `assets/evidence-card.txt` for an item you have to hand. Write "not
recorded" wherever you do not know. Field 10 is required.

## Part B: identity or authenticity

For each question, say whether a SHA-256 hash can answer it.

| # | Question | Hash? |
|---|---|---|
| 1 | Is this the same file I hashed last year? | |
| 2 | Did this come from the manufacturer? | |
| 3 | Has anyone edited it? | |
| 4 | Does this manual describe the board next to it? | |
| 5 | Are these two files identical? | |
| 6 | Is this scan made from an original or a photocopy? | |
| 7 | Is this the firmware on the chip? | |

Count the yeses.

## Part C: the chain

> "Bought from a dealer in 2019, who bought it from an estate in 2011, whose
> owner is said to have purchased it new."

| Link | What supports it | How strong |
|---|---|---|
| Dealer to you, 2019 | | |
| Estate to dealer, 2011 | | |
| Purchased new | | |

Which link is weakest, and what would strengthen it?

## Part D: spot the guess

One of these cards contains an invented field. Find it and say how you can tell.

**Card 1**
> Item: vendor firmware source archive. Source: downloaded from the vendor site,
> URL not recorded. Retrieved: not recorded. Type: working copy. Permission: not
> recorded.

**Card 2**
> Item: vendor firmware source archive. Source: vendor website. Retrieved:
> 14 March 2023. Type: original. Permission: freely distributed.

## Part E: field 10 practice

Write field 10, "what this does not establish," for each.

| Item | Does not establish |
|---|---|
| A hashed copy of the Replica 1 Plus manual | |
| A photograph of the board's serial number | |
| The vendor `110REV03` source archive | |
| A recorded emulator run | |

## Part F: the open question in this project

This library records that the project index and the collection folder hold
manual filenames that differ, and that no hash comparison has been run.

1. What would a matching hash establish?
2. What would it still not establish?
3. What would a mismatch mean?
4. Is this a problem, or just an unclosed item?

## Part G (optional, STUDY): the read-only rule

This repository asks for a read-only duplicate of raw captures before
annotation.

1. Why before rather than after?
2. What goes wrong if you annotate first and copy later?
3. Does hashing remove the need for the duplicate?

## What this activity does not do

It fills in records on paper. **It authenticates nothing** and authorizes no
hardware action.
