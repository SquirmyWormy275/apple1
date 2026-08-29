# R04 Answer key

Design work has no single correct answer. What follows is a worked example and
the criteria to judge a learner's map against.

## Worked map

```text
        [1] THE LANDING
         |            \
       north          east
         |               \
    [2] THE STORE     [3] THE STAIR
       ROOM               |
         |              down
       (key here)          |
                      [4] THE CELLAR
                        (ending)
```

| From | Direction | To | Reverse |
|---|---|---|---|
| 1 | North | 2 | South from 2 to 1 |
| 1 | East | 3 | West from 3 to 1 |
| 3 | Down | 4 | **None.** Deliberate: the cellar door shuts. |

**Three tests:**

- Reachable from room 1: **all four**.
- Dead ends: **room 4**, which is the ending, so this is correct rather than a
  fault.
- Can the player get stuck? **No.** Room 4 is an ending; every other room has a
  way back.
- Reachable ending: **yes**, room 4.

**State:** position (4 values), has-key (1 flag), cellar-door-opened (1 flag).
Two flags and a position.

## Acceptance criteria for a learner's map

**Part A.** Four rooms, all named, every exit marked, and a traced path from room
1 to each. A map with an unreachable room has not passed and should be fixed
before Part B rather than noted in it.

**Part B.** All four questions answered. A dead end is only acceptable if it is
an ending, and the learner should say so.

**Part C.** Every exit listed as a pair. Missing reverses are fine *if the
learner says they meant it*. "I did not notice" is the finding.

**Part D.** Position always needed. Flag count computed. Most four-room stories
use fewer than eight flags, so **yes, they fit in one byte**, which is a nice
thing for a learner to discover: an entire small world's memory is one byte plus
a position.

**Part E.** Eight to twelve lines, read aloud, with the three faults marked. A
transcript with no faults marked usually means it was not read aloud.

**Part F.** Honest answers. Faults 5 and 6 require checking the flags against the
transcript, not the map.

## Part F: why 5 and 6 are different

Faults 1 to 4 are visible on the map. You can see an unreachable room.

**Fault 5, a flag checked but never set,** means a door that can never open. On
the map it looks like a normal exit. The player finds it locked forever and has
no way to know the key does not exist.

**Fault 6, a flag set but never checked,** means an item that does nothing. The
player finds the key, carries it around, and it never matters. Less harmful and
more common.

Both are invisible on a map because a map shows places, not conditions. Catching
them needs a separate list: every flag, where it is set, where it is checked. Any
flag missing either column is a fault.

That list is worth making, and it is the same idea as A06's design card: a
routine question that catches what inspiration does not.

## Part G: the locked door

Acceptance: the flag is named, the place it is set is a room the player can reach
*without* already needing the flag, and both walks complete.

The common mistake is putting the key behind the door it opens. It is obvious
when stated and easy to do accidentally, and re-walking the map without the key
is what catches it.

## Try a variation

Same as Part G. The two walks are the test: without the key the player should be
able to reach the key; with it, the door. If the no-key walk cannot reach the
key, the design is circular.

## README: Check your understanding

1. **Where the player is, what they carry, and what has happened.** Position,
   items, events.
2. **It is content that will never be seen.** Every word written for it is wasted,
   and if it contains something the story needs, such as a key, the story cannot
   be completed.
3. **Because a map is small enough to check completely and a program is not.**
   Every structural fault is obvious on a map and invisible in code, and finding
   them costs minutes on paper and hours afterwards.
