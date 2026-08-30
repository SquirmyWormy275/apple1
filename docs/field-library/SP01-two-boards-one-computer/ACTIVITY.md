# SP01 Activity: trace two implementations of the same computer idea

**Status:** OFF-DEVICE. Use the ASCII atlas only.

## Part A: find the original-board landmarks

Use `card/original/`.

| Question | Answer |
|---|---|
| Where is the 6502? | |
| Where is the 6820 PIA? | |
| Which row contains RAM bank X? | |
| Which row contains RAM bank W? | |
| Which two rows are dominated by video-terminal hardware? | |

## Part B: identify the major substitution

Use `card/replica/`.

1. Which Replica IC absorbs video, serial, PS/2, and clock duties described by
   the manufacturer's manual?
2. Which single modern memory IC replaces the visual complexity of the original
   DRAM banks?
3. Which original-style keyboard path is retained alongside PS/2?

## Part C: match the implementations

Match each original function to its Replica implementation.

| Original | Replica choices |
|---|---|
| A. 4096 x 1 DRAM banks | 1. 6821 PIA |
| B. Discrete video terminal | 2. 62256 SRAM |
| C. 6820 PIA | 3. Propeller-centered I/O |
| D. Monitor PROM pair | 4. EPROM / modern ROM storage |
| E. ASCII-only keyboard path | 5. PS/2 plus ASCII option |

Write: `A=__ B=__ C=__ D=__ E=__`.

## Part D: follow one character

Read:

- `card/compare/07-keypress-original.txt`
- `card/compare/08-keypress-replica.txt`

Name the stage that changes most dramatically between the machines and the
stages that remain conceptually related.

## Part E: software contract

Read `card/compare/03-io-addresses.txt`.

Explain in two sentences why a program can care about `$D010`–`$D013` without
caring which physical video chips produce the final composite signal.

## Part F: evidence boundary

Read `card/evidence/00-live-unit.txt` and `card/evidence/01-boundary.txt`.

Which of these are supported?

1. The manufacturer's design uses a Propeller for several I/O functions.
2. This project's host sees an FT232R USB UART.
3. Every board-level signal path on this project's Replica is proven.
4. Opening the project's serial path is known safe.
5. The atlas is suitable as a probing diagram.
