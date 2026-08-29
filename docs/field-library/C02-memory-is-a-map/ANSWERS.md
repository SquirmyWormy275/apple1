# C02 Answer key

## Part A: place the addresses

| Address | Region |
|---|---|
| `$0300` | System and user RAM. Where this repository's RAM-only programs are written to be entered. |
| `$0400` | System and user RAM. The buffer those programs write characters into. |
| `$01FF` | The 6502 stack, which occupies `$0100`-`$01FF`. `$01FF` is its base, and it grows downward from there. |
| `$D011` | The PIA. The keyboard control register, holding the key-ready flag. Hardware, not memory. |
| `$FF1F` | Monitor ROM. It is the label `GETLINE` in the Monitor listing. |
| `$9000` | Unused on the original design. Nothing is wired there. |

### The byte question

`$A0` at `$0300` is **all of these, depending**. The correct reason: memory does
not record what kind of thing a byte is. Only the program's treatment of it
decides. If the CPU fetches it as an opcode it is `LDY` immediate; if a program
loads and compares it, it is the number 160; if it goes to the display it is a
character code with the top bit set.

## Part B: read or write

| Region | Answer |
|---|---|
| `$0300` user RAM | **Yes.** Ordinary read-write memory. |
| `$0100`-`$01FF` stack | **Yes**, and the CPU writes there itself during `JSR` and pushes. Writing there deliberately with other data is a good way to corrupt a return address. |
| `$D012` display register | **Something else happens.** The write is not stored for later reading. It hands a character to the video circuitry. |
| `$FF00`-`$FFFF` Monitor ROM | **No.** Read-only memory. A write instruction executes without error and changes nothing. |
| `$9000` unused | **Something else happens**, and what exactly is not defined. Nothing is wired there on the original design, so a read returns whatever the bus happens to be carrying. |

The row worth discussing is the ROM one. The write does not fail loudly. It just
does nothing, which is harder to debug than an error.

## Part C: the same byte, three ways

1. **As an instruction.** The CPU treats it as an opcode naming an action.
2. **As a number.** 193 in decimal, compared arithmetically.
3. **As a character code.** Handed to the video circuitry, which looks up a
   shape for it.

The byte is identical in all three cases. Nothing about it changed.

## Part D: little-endian drill

| Address | Bytes, low first |
|---|---|
| `$D011` | `11 D0` |
| `$0400` | `00 04` |
| `$FF1F` | `1F FF` |
| `$0300` | `00 03` |

Going the other way: **`00 04` means `$0400`.**

Check yourself against a real line: `line-input-0300.hex` contains
`99 00 04`, which is `STA $0400,Y`, and `4C 1F FF`, which is `JMP $FF1F`.

## Part E: the original and the replica

Two differences stated in the lesson:

1. **More RAM.** The original had 4 KB of user space at `$0000`-`$0FFF`; the
   replica design documented by Owad has 32 KB, `$0000`-`$8000`. Easier: more
   room for programs and data, and no need to be frugal.
2. **BASIC in ROM instead of RAM.** On the original, `$E000`-`$EFFF` was RAM and
   BASIC had to be reloaded from cassette or typed in at every power-up. On the
   replica it is in ROM and is there immediately. Easier, and by a wide margin.

## Part F: what the map does not tell you

Any three of: whether this particular board has the RAM the design calls for;
what is actually programmed into its ROM; whether the PIA registers respond;
whether the board powers on at all; whether a given address has been modified by
a previous owner; what firmware version any microcontroller on it is running.

The map describes a design. A board is an object.

## README: Check your understanding

1. **65,536 locations.** Sixteen bits gives 2 to the sixteenth, which is 65,536,
   and each distinct value on the address bus names one location.
2. **Because `$D010` is not storage.** It is a hardware register. Reading it asks
   the keyboard circuitry for its current value rather than retrieving a byte
   somebody previously stored. This is memory-mapped I/O.
3. **That it was RAM, not ROM.** RAM loses its contents when power is removed.
   Anything that has to be reloaded every power-up is living in RAM.
