# R04 Interactive fiction

**Audience:** BUILD
**Time:** 60 minutes
**Status:** OFF-DEVICE
**Prerequisites:** B02, R02

## You will learn

By the end, you can design a small world as a map of rooms and exits, decide what
the story has to remember, and test the design by walking it before any of it is
written as a program.

## Why this matters

Interactive fiction was one of the things small text machines were genuinely good
at. It needs no graphics, no sound, and very little memory. What it needs is
careful thought about structure, which is exactly the thing that transfers to
every other kind of program.

The world is yours. This lesson is about giving it a shape that works.

## First result

A four-room map with exits marked and every room reachable.

## What you need

Paper and a pencil. `assets/story-map.txt`. Nothing powered on.

## Activity

1. Look at the three-room example at the top of `assets/story-map.txt`.
2. Draw your own map of four rooms in the space below, marking the exits between
   them.
3. Trace a path from room 1 to every other room. That is your first result.

## Explain what happened

**A room is a description and a set of exits.** That is all a room needs to be.
The description is what the player reads; the exits are where they can go. Both
are just data, and a program that handles one room handles all of them.

**Exits are the structure.** A map where every room connects to every other is a
world with no shape. A map that is a straight line is a corridor. The interesting
shapes are in between: loops the player can go round, a room with three ways in
and one way out, a door that only opens later.

**Exits should usually work both ways, and it is worth deciding deliberately when
they do not.** If north from room 1 leads to room 2, does south from room 2 lead
back? Usually yes, and a player will assume so. A one-way exit is a legitimate
design choice and a cruel accident, and the difference is whether you meant it.

**State is what the story remembers between turns.** Three kinds cover almost
everything:

*Where the player is.* One value. Every story needs it.

*What they carry.* A list, or on a small machine a handful of yes-or-no flags:
has the key, has the lamp.

*What has happened.* Also flags: the door is unlocked, the guard has been spoken
to. This is the one people forget, and it is what makes a world feel like it
responds rather than resets.

**Everything else follows from those.** A locked door is a check on a flag. An
ending is a room with no exits and a message. A puzzle is a flag that some other
room sets.

**Testing a map means walking it.** Three questions, all answerable on paper
before any program exists:

*Can you reach every room?* Start at room 1 and follow exits. A room nobody can
reach is content you will never see.

*Can you get stuck?* A room with no exit out, that is not an ending, traps the
player. Sometimes intentional and usually not.

*Is there an ending?* A story with no reachable ending is not finished, it just
stops.

**Why walk it rather than write it.** Because a map is small enough to check
completely, and a program is not. Every one of those three faults is invisible in
code and obvious on a map. This is A06's design card applied to a world instead
of a utility.

**A small transcript is the other half of the test.** Write out, as dialogue,
what the player types and what the machine says for a short journey. Reading it
aloud catches things the map does not: descriptions that do not say what the
exits are, a prompt that gives no clue what to type, an ending that arrives with
no warning.

## Try a variation

Add one locked door to your map. Say which flag it checks, where that flag gets
set, and then re-walk the map twice: once as a player who has not found the key,
and once as a player who has. Check that both journeys work.

## Check your understanding

1. What three kinds of state does a small story need?
2. What is wrong with a room that cannot be reached?
3. Why walk the map on paper rather than testing the program?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

This lesson carries no Apple-1-specific claim beyond the display conventions.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- No story here has been implemented or run, on any machine.
- Nothing about this project's board.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
