# R04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## No Apple-1 claims

This lesson makes no claim about the Apple-1, the Replica 1 Plus, or any
historical software. Rooms, exits, flags, and map-walking are general design
ideas and are not cited.

The only repository-derived constraints are the display conventions carried over
from R01: 40 columns of upper-case printable ASCII for the asset (E-WIDTH), which
`assets/story-map.txt` observes and which was checked against
`tools/apple1_text.format_for_apple1` during authoring.

**No claim is made that interactive fiction ever ran on an Apple-1.** The README
says such programs suit small text machines in general. The nine cassette
programs Apple sold are listed in the shared pool (H-NINE) and none of them is
interactive fiction, so no such claim would be supportable from these sources
anyway.

## The one-byte observation

The answer key notes that a four-room story's flags typically fit in one byte.
This is arithmetic: eight flags per byte, and small stories use fewer than eight.
It is not a claim that anyone implemented a story this way.

## Deliberate simplifications

1. **Parsing is not covered at all.** How a program would understand what the
   player typed is a substantial topic and is not part of the design work here.
   The transcript exercise sidesteps it by having the learner write both sides.
2. **No implementation is discussed**, in BASIC or assembly. The lesson stops at
   design, which is what the curriculum brief asks for: a branching story map with
   a small test transcript.
3. **Room descriptions are not length-limited** in the exercise, though a real
   implementation on a 40-column display would need to think about it.

## Claims needing verification

- **V-7 applies** for the character canvas.
- **V-8 applies** trivially: nothing here concerns this board.
- No new verification items. This packet asserts nothing that could be wrong
  about the machine, because it asserts nothing about the machine.

## What this lesson does not establish

Nothing about any machine. No story has been implemented or run. It authorizes no
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
