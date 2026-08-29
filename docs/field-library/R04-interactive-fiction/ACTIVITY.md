# R04 Activity: build a world

**Status:** OFF-DEVICE. Paper and pencil. Nothing is implemented or run.

## Part A: the map (this is the first result)

Draw four rooms on `assets/story-map.txt`, name each, and mark every exit. Then
trace a path from room 1 to each of the others.

## Part B: the three tests

| Test | Your answer |
|---|---|
| Rooms reachable from room 1 | |
| Rooms that are dead ends | |
| Can the player get stuck? | |
| Is there a reachable ending? | |

Fix anything that fails before continuing.

## Part C: exits both ways

List every exit as a pair.

| From | Direction | To | Reverse exists? |
|---|---|---|---|
| | | | |

For any missing reverse, say whether you meant it.

## Part D: state

| State | Your story needs it? | How many values |
|---|---|---|
| Where the player is | | |
| What they carry | | |
| What has happened | | |

Then: if every carried item and every event is a yes-or-no flag, how many flags
does your story use? Could they fit in one byte?

## Part E: the transcript

Write eight to twelve lines of transcript: what the player types and what the
machine replies, for a journey from room 1 to your ending.

Then read it aloud and mark anything that:

- does not tell the player what the exits are,
- gives no clue what they are allowed to type,
- ends without warning.

## Part F: break your own map

| # | Fault | Does your map have it? |
|---|---|---|
| 1 | A room nobody can reach | |
| 2 | A room with no way out that is not an ending | |
| 3 | An exit that goes one way with no reason | |
| 4 | An ending that cannot be reached | |
| 5 | A flag that is checked but never set | |
| 6 | A flag that is set but never checked | |

Faults 5 and 6 are the ones a map alone will not show you.

## Part G (optional): the locked door

Add one locked door. Name the flag, say where it is set, and re-walk the map both
with and without the key.

## What this activity does not do

It designs a world on paper. Nothing is implemented, nothing is run, and no
hardware action is authorized.
