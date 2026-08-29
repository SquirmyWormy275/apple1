# X02 Activity: find it, fix it, show it

**Status:** OFF-DEVICE. Paper, optionally the M03 emulator on an ordinary
computer. **Neither program is entered on the Replica 1 Plus.**

## Part A: trace first (this is the first result)

Fill in the six-row table on `assets/broken-loop.txt` and answer the three
questions under it. **Do this before looking for the bug.**

## Part B: state the discrepancy

| | |
|---|---|
| What it was supposed to do | |
| What it actually does | |
| The difference, in one sentence | |

## Part C: find the bug

| | |
|---|---|
| Address of the bug | |
| Byte as written | |
| Byte it should be | |
| How you know | |

## Part D: the after trace

Trace the corrected program.

| Pass | Y before | Stored at | Y after |
|---:|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

| | |
|---|---|
| Stores | |
| Highest address written | |
| Matches the intention? | |

## Part E: predict the emulator

Before running anything, predict both versions.

| Version | Predicted buffer | Predicted instructions |
|---|---|---|
| As written | | |
| Corrected | | |

Then check against `ANSWERS.md`, or run them yourself in the M03 emulator using
scratch copies. **Do not add either program to `software/ram-only/`.**

## Part F: why it is dangerous

| # | Symptom | Present? |
|---|---|---|
| 1 | The program crashes | |
| 2 | It fails to return to the Monitor | |
| 3 | It writes to an obviously wrong address | |
| 4 | It produces no output | |
| 5 | It takes visibly longer | |
| 6 | It does one thing more than intended | |

How many of the first five would a casual test catch?

## Part G: three wrong fixes

Each of these "fixes" the symptom. Say what is wrong with each.

1. Change `A0 00` to `A0 01`.
2. Change `D0 F8` to `D0 FA`.
3. Leave the program alone and write the intention as six characters instead of
   five.

Fix 3 is the interesting one.

## Part H (optional): plant your own

Take the corrected program, change exactly one byte to introduce a different
bug, and give it to somebody with the intention written at the top. Do not tell
them where you changed it.

## What this activity does not do

It traces and corrects a program on paper, and optionally rehearses it
off-device on an ordinary computer. Neither version is entered on hardware and no
hardware action is authorized.
