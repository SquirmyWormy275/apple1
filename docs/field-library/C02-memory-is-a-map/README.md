# C02 Memory is a map

**Audience:** LEARN
**Time:** 35 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S03, C01

## You will learn

By the end, you can take an address, say which region of the machine it falls
in, and explain why the same byte can be a number, a letter, or an instruction.

## Why this matters

Every address in this library, `$0300`, `$0400`, `$D011`, `$FF1F`, is a location
on one map. Once the map is in your head, an address stops being a random
four-digit code and starts telling you something: this one is program space,
that one is a hardware register, that one is read-only.

## First result

Six addresses placed on the map.

## What you need

Paper. `assets/memory-map.txt` and `assets/address-worksheet.txt`.

## Activity

1. Study `assets/memory-map.txt` for two minutes. Note only the four boundaries:
   RAM at the bottom, the PIA around `$D010`, BASIC's area around `$E000`, the
   Monitor at the very top.
2. On `assets/address-worksheet.txt`, write the region for each of the six
   addresses.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**What an address is.** The 6502 puts a number on sixteen wires called the
address bus. Sixteen bits gives 65,536 distinct values, so the machine has
65,536 addressable locations, `$0000` through `$FFFF`. That is the whole map.
Each location holds exactly one byte.

**The map is not evenly used.** On the original Apple-1, most of it is empty.
There were 8 KB of RAM in a 64 KB space, split into two 4 KB pieces, plus a
handful of hardware registers and 256 bytes of ROM at the top. The vast majority
of addresses were connected to nothing at all.

**The four things that live somewhere specific.**

- **`$0000` upward: system and user RAM.** On the original this was 4 KB,
  `$0000` to `$0FFF`. Two parts of it have fixed jobs assigned by convention
  rather than by wiring: `$0000`-`$00FF` is called the *zero page*, and
  `$0100`-`$01FF` is the *stack*, which grows downward from `$01FF`.
- **Around `$D010`: the PIA.** These are not memory. They are hardware
  registers: the keyboard character, its flag, the display register, its control
  register. Reading `$D010` does not fetch a stored byte, it asks the keyboard
  hardware what it has. This is called *memory-mapped I/O*, and it is why S02's
  mailboxes had addresses.
- **`$E000`-`$EFFF`: Integer BASIC's area.** On the original this was RAM, so
  BASIC had to be loaded from cassette or typed in by hand every time the machine
  was switched on. Later replicas put BASIC in ROM here so it survives power-off.
- **`$FF00`-`$FFFF`: the Monitor ROM.** 256 bytes at the very top. It is at the
  top because the 6502 looks at the last two addresses in memory when it is
  reset to find out where to start, so the ROM has to reach that far.

**A byte is only what you treat it as.** This is the important idea in the
lesson. Memory does not remember what kind of thing it is holding. The value
`$A0` at address `$0300` is 160 as a number, is `LDY` as an instruction, and
would be a character with the top bit set if a program handed it to the display.
Nothing in the byte says which. The only thing that decides is what the program
does with it.

This is why a byte list entered at the wrong address does nothing useful, and
why `JMP` to the middle of some data will happily start executing it as
instructions.

**Where the repository's own programs sit.** The RAM-only byte lists in this
project are written for `$0300`, and they use `$0400` as a place to put the
characters they collect. Both are ordinary user RAM. Neither address is special
to the hardware; they were chosen because they are free.

**One wrinkle: bytes go in backwards.** In C01 you saw `LDA $D011` stored as the
bytes `AD 11 D0`. The address reads `11 D0`, low half first. The 6502 stores
two-byte values with the low byte first, a convention called *little-endian*.
When reading a listing, expect addresses to look reversed.

## Try a variation

`$FF1F` is inside the Monitor ROM. `$0300` is in user RAM. Explain why a program
can write to one and not the other, and what that means for where you can put
your own code.

## Check your understanding

1. How many addressable locations does the 6502 have, and how do you know from
   the width of the address bus?
2. Reading address `$D010` is not the same kind of act as reading `$0400`. Why?
3. On the original Apple-1, switching the machine off lost Integer BASIC. What
   does that tell you about `$E000`-`$EFFF` on that machine?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The map is drawn from Owad's Apple-1 memory map and the surrounding text.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish:

- **The map is a model.** It reproduces published documentation of the original
  Apple-1 design. It is not a reading taken from this project's board, and the
  Replica 1 Plus is documented to differ, notably in the amount of RAM and in
  having BASIC in ROM.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open,
  or physical modification. No address in this lesson is offered as something to
  go and look at on hardware.
