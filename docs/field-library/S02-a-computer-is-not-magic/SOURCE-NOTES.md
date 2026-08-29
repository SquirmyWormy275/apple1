# S02 Source notes

Keys refer to the shared pool in `../SOURCES.md`, which holds the exact wording
of each cited passage.

| Claim | Key |
|---|---|
| A keypress puts a seven-bit ASCII value on the data lines, with a strobe pulse | P-KBD-7BIT |
| The keyboard character is at `$D010`; the flag is at `$D011` | P-KBD |
| The CPU checks the flag at `$D011`, then reads `$D010` | P-KBD |
| The display register is `$D012` | P-DSP |
| The CPU checks bit 7 of `$D012` and waits for it to go low before writing | P-DSP-BUSY |
| Separate video circuitry turns the character code into a letter shape | P-VIDEO-TEXT |
| A character on the display cannot be modified afterward (Part C item 6) | P-VIDEO-WRITEONLY |
| Hexadecimal is written with a `$` prefix | A-HEX |
| Display text in this library is 40 columns of upper-case ASCII | E-WIDTH |

## Deliberate simplifications

These are teaching choices, not source claims. An educator should know where the
lesson is being loose.

1. **"The CPU checks the flag over and over."** The lesson calls this polling
   and leaves it there. The 6821 also has interrupt lines, which the Apple-1
   design does not use for this path. OWAD notes `IRQA` and `IRQB` are not used.
   Introducing interrupts here would cost more than it teaches.
2. **"A mailbox."** Memory-mapped I/O is presented as numbered slots. The lesson
   replaces the analogy with the real terms in the same section, as the
   curriculum brief for S02 requires.
3. **The control registers are not named.** `$D011` and `$D013` are control
   registers that do more than hold a flag. The lesson describes only the flag
   behavior it needs. C04 and M01 go further.
4. **Bit 7 of `$D012`** is called "the top bit" rather than "the Data Available
   line," which is what the hardware calls it. The real name is introduced in
   the C-series.

## Claims needing verification

- All page numbers inherit **V-1** from the shared pool.
- **V-4 applies.** OWAD's PIA description is of the Apple-1 and the Replica I.
  This lesson describes the *documented Apple-1 design*. It does not claim the
  Replica 1 Plus implements the sequence identically, and the Propeller-based
  video and keyboard path on later replicas is known to differ (P-PROPELLER).
- Nothing here was measured on this project's board (**V-8**).

## What this lesson does not establish

It does not show that this project's Replica 1 Plus reads a key, displays a
character, or moves a byte anywhere. It is a documented design described on
paper. It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port
open, or physical modification.
