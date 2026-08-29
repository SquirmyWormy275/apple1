# B01 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Apple-1 BASIC supports integers only; `PRINT 38/9` gives 4 | B-INTEGER |
| `MOD` gives the remainder; `PRINT 38 MOD 9` gives 2 | B-MOD |
| Integer variables are a letter or a letter and a digit; strings are a letter plus `$` | B-VARNAMES |
| Strings must be dimensioned; maximum length 255 | B-DIM |
| `INPUT` always adds a question mark and it cannot be turned off | B-INPUT-Q |
| Arithmetic works from the command line without a program | B-IMMEDIATE |
| `10 PRINT "HELLO WORLD"` / `20 GOTO 10` as a worked example | OWAD ch. 5 p. 130 |
| On the original, BASIC was in RAM at `$E000` and reloaded every power-up | M-BASIC-RAM |
| On the replica documented by Owad, Integer BASIC is in ROM at `$E000`-`$EFFF` | M-REPLICA-MAP |
| The Replica 1 Plus ROM holds 4 KB BASIC, 256 bytes Monitor, just under 4 KB Krusader | R-ROM-SPLIT |
| `E000R` enters BASIC; `F000R` enters Krusader, written by Ken Wessen | R-BASIC-ENTRY, R-KRUSADER |
| `line-input-0300.hex` reads `$D011` and `$D010` and calls `$FFEF` | REPO `software/ram-only/README.md`; A05 |

## No BASIC was run

There is **no runnable BASIC environment in this repository**. The curriculum
brief for B01 anticipates this and asks for small pseudocode snippets in that
case.

Every BASIC line quoted in this packet comes from a published source, principally
OWAD chapter 5. None has been executed by this author, on hardware or otherwise.
The assembly-side description in `assets/same-job-two-ways.txt` is deliberately
written as pseudocode rather than as a byte listing, so that no reader mistakes it
for a runnable artifact.

Recorded as **V-20**: all BASIC behavior in the B-series is cited from
documentation, never observed.

## The comparative claims

The cost-and-benefit table in `ANSWERS.md` Part D contains claims that are
general computing knowledge rather than Apple-1-specific facts: that interpreted
code runs slower than native instructions, that an interpreter occupies memory,
that editing a source line is easier than re-deriving a byte list. These are not
cited and do not carry Apple-1-specific claims.

The two rows that *are* Apple-1-specific are "what must already be present,"
which rests on M-BASIC-RAM and M-REPLICA-MAP, and the 4 KB figure, which rests on
R-ROM-SPLIT.

## Deliberate simplifications

1. **"Interpreted" is used loosely.** How Apple-1 BASIC actually represents and
   executes a program is not described, because no source in this project
   documents it in that detail.
2. **The assembly `PRINT` equivalent is pseudocode, not a real listing.** Writing
   a real one would require choosing a string representation and an end marker,
   which are exactly the decisions the lesson is pointing at.
3. **Krusader is mentioned but not taught.** Part F asks only where it sits
   between the two.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-20 (new).** No BASIC in this library has been executed. All behavior is
  cited from OWAD chapter 5.
- **V-4 applies** to the ROM contents claims: R-ROM-SPLIT is from the Replica 1
  Plus manual and M-REPLICA-MAP is from OWAD's Replica I. The lesson does not
  claim what is in this board's ROM.
- **V-8 applies.** Nothing here concerns this machine's state.

## What this lesson does not establish

It does not establish that BASIC is present on this project's board, or that any
BASIC line in it would run there. It authorizes no firmware load, EEPROM write,
CFFA1 write, serial-port open, or physical modification, and gives no instruction
to type anything on hardware.
