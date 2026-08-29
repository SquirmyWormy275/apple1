# M01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| The Monitor has three basic functions | R-MON-3 |
| `300[RETURN]` inspects; `300.32F` inspects a block; `300:FF` writes; `300R` runs | R-MON-SYNTAX |
| A block examine shows up to eight locations per line | R-MON-8 |
| Writing responds with the location's previous contents | R-MON-SYNTAX; the manual's worked exchange `300:FF` then `0300:E1` |
| Wozniak coined "monitor" for a program that watched the keyboard in place of front-panel switches | WOZ-FWD p. 17 |
| The Monitor is 256 bytes | WOZ-FWD p. 17; M-ROM |
| The Monitor occupies `$FF00`-`$FFFF` | M-ROM |
| `E000R` enters BASIC on a replica with BASIC in ROM | R-BASIC-ENTRY; M-REPLICA-MAP |
| The Altair used lights and switches | H-ALTAIR; H-KBD-STD |
| Programs must return to the Monitor deliberately; exit via `JMP $FF1F` | E-EXIT |
| The Monitor's `R` leaves no return address on the stack | E-EXIT |

## The `0300: E1` example

The value `E1` in `assets/three-jobs.txt` and Part C is taken verbatim from the
Briel manual's worked example. It is **not** a claim that `$0300` contains `$E1`
on any machine. In the manual it is illustrative of whatever happened to be
there, which on a freshly powered machine is uninitialized memory.

This is flagged because a learner could easily read it as a fact about a
specific board. `STATUS.md` repeats the point.

## Deliberate simplifications

1. **The Monitor's fourth behavior is not mentioned.** The listing shows a
   backspace and an escape handler as well as the three commands. Those are line
   editing, not jobs you aim at an address, and including them would blur the
   lesson's shape.
2. **"Not an operating system" is argued informally.** No definition of an
   operating system is offered, because a LOOK-level lesson does not need one
   and any definition offered would need defending.
3. **The `.` block syntax is shown but the underlying mode byte is not.** The
   Monitor tracks three internal modes; that is M02 and W-MODES territory.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-4 applies.** R-MON-3, R-MON-SYNTAX, R-MON-8, and R-BASIC-ENTRY are from the
  Replica 1 Plus manual. They describe documented replica behavior. The lesson
  attributes them to "the Monitor" as documented and makes no claim about this
  board.
- **V-8 applies.** No command in this lesson has been observed on this project's
  machine.

## What this lesson does not establish

It does not show that this project's Replica 1 Plus responds to any Monitor
command. It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port
open, or physical modification, and gives no instruction to type anything on
hardware.
