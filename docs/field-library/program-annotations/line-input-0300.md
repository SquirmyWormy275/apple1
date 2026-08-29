# `line-input-0300.hex` annotated

**Status: OFF-DEVICE annotation of a RAM-ONLY artifact with no live-run
authority.**

## What it is for

It collects the characters you type into a buffer in memory, showing each one on
the display as it arrives, and stops when you press Return.

That is a line editor. In 26 bytes.

## Load address and size

**Load address `$0300`. 26 bytes, occupying `$0300` through `$0319`.**

The address is in the filename, not in the file. This repository stores
address-free byte lists deliberately, so that a file cannot disagree with itself
about where it belongs.

The last address is start plus count minus one: `$0300` + 26 - 1 = `$0319`. Not
`$031A`. The first byte uses up the first address.

*Source: E-RAMONLY.*

## Input and output

| | |
|---|---|
| **Input** | Characters from the keyboard, read through `$D010` when `$D011` says one is waiting. Each arrives with bit 7 set, so `A` is `$C1` rather than `$41`. |
| **Output, on screen** | Every character echoed as it is typed, via the Monitor's `ECHO` routine. |
| **Output, in memory** | The typed characters at `$0400` onward, **including the carriage return**. |
| **Output, in registers** | Y is left holding the count of characters stored before the Return. The program does not clear it, and promises nothing about it. |

*Source: P-KBD, P-HIGHBIT, W-FFEF.*

## Memory it uses

| Address | Role |
|---|---|
| `$0300`-`$0319` | The program itself |
| `$0400` onward | The buffer, one byte per character |
| `$D010` | Keyboard character, read-only to this program |
| `$D011` | Keyboard ready flag, read-only to this program |
| `$FFEF` | Monitor `ECHO`, called as a subroutine |
| `$FF1F` | Monitor warm entry, jumped to at the end |

Nothing else is touched. Note the clearance: the program ends at `$0319` and the
buffer starts at `$0400`, 230 bytes clear. That survives the program growing.

*Source: P-KBD, W-FFEF, W-FF1F.*

## The listing

```text
0300  A0 00      LDY #$00      Y = 0, start of buffer
0302  AD 11 D0   LDA $D011     read the keyboard ready flag
0305  10 FB      BPL $0302     not ready yet? go back and look again
0307  AD 10 D0   LDA $D010     take the character
030A  99 00 04   STA $0400,Y   store it at $0400 + Y
030D  20 EF FF   JSR $FFEF     ask the Monitor to display it
0310  C9 8D      CMP #$8D      was that a carriage return?
0312  F0 03      BEQ $0317     yes: leave the loop
0314  C8         INY           no: move along one
0315  10 EB      BPL $0302     and go back for the next character
0317  4C 1F FF   JMP $FF1F     hand control back to the Monitor
```

Disassembled by hand from the byte list. The boundaries land exactly on `$0319`,
the branch offsets resolve to instruction boundaries rather than mid-instruction,
and the result is consistent with the recorded emulator runs.

## Stage by stage

**Setup, `$0300`.** One instruction. Y is the position in the buffer and it
starts at zero. It has to be outside the loop; running it again would send every
character back to the start.

**Wait for a key, `$0302` to `$0305`.** Read `$D011`, and branch back to that
same read while the result is *plus*, meaning bit 7 is clear. So the program
spins here until bit 7 of `$D011` becomes 1, which is the hardware saying a
character is waiting.

Note this is a **bit test done with a branch**, not a comparison. The program
never asks "is `$D011` equal to something." It asks "is its top bit set."

**Take the character, `$0307`.** Read `$D010`. The byte arrives with bit 7 set,
which is why every comparison later uses a high-bit value.

**Store it, `$030A`.** `STA $0400,Y` writes to `$0400` plus whatever is in Y.
One instruction that reaches a different address every time round, which is the
entire reason index registers exist.

**Show it, `$030D`.** `JSR $FFEF` calls the Monitor's echo routine and comes
back. `JSR` rather than `JMP` because we want to return: the routine ends in
`RTS`, which returns to `$0310`.

Calling into the Monitor's ROM like this is the closest thing this machine has
to a library. You do not write display code; you jump to the display code that is
already there.

**Test and repeat, `$0310` to `$0315`.** Compare against `$8D`, a carriage
return with the high bit set. Leave if it matched. Otherwise advance Y and go
back.

## How it ends

**`4C 1F FF` at `$0317`, which is `JMP $FF1F`.**

`$FF1F` is inside the Monitor ROM. In the Monitor's own listing it carries the
label `GETLINE`, the point where the Monitor starts collecting a fresh line of
input. Jumping there is the program saying "I am finished, you have the keyboard
back."

**Why a jump and not `RTS`.** `RTS` pulls a return address off the stack, and it
only works because some earlier `JSR` put one there. The Monitor's `R` command
does not do a `JSR`; it jumps. So an `RTS` here would pull two leftover bytes
that were never meant as an address and jump to whatever they spell.

The repository states this rule directly, and it is worth reading as a statement
about the Monitor rather than about `RTS`: this same program uses `RTS`
correctly, indirectly, every time `JSR $FFEF` returns.

*Source: E-EXIT, quoted from `software/ram-only/README.md`; W-FF1F, W-FFEF.
Note V-14: that the Monitor's `R` jumps rather than calls is taken from the
repository's own statement, not yet confirmed against the `RUN` routine's bytes
in the Monitor listing.*

**There is a second way out.** `BPL $0302` at `$0315` tests the flags left by
`INY`. So the loop also ends when Y reaches `$80`, that is after 128 characters,
and control falls through to the same jump. The program exits cleanly and says
nothing about why.

Whether that limit was designed or is an incidental consequence of choosing a
conditional branch where an unconditional one would have done **cannot be
determined from the bytes**. Recorded as V-18.

## Expected emulator behavior

Recorded in `../EMULATOR-RUNS.md`, run in `tools/apple1_emulator.py`:

| Input | `screen_text` | `buffer_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---|---:|
| `A` + CR | `A` CR | `A` CR | true | 20 |
| `HI` + CR | `HI` CR | `HI` CR | true | 30 |
| `HELLO` + CR | `HELLO` CR | `HELLO` CR | true | 60 |
| `APPLE-1` + CR | `APPLE-1` CR | `APPLE-1` CR | true | 80 |

The instruction count fits `10 x (characters + 1)` across all four. That is an
empirical fit over four inputs, not a derivation from the loop, and is recorded
as V-12.

Two details of the harness worth knowing when reading those numbers. It applies
the high bit to your input itself, so you type plain `HI` and the program sees
`$C8 $C9`. And `screen_text` is reported with the high bit stripped, so it reads
as ordinary text.

*Source: E-EMU-SCOPE; the harness's own `byte | 0x80` on input and `mpu.a & 0x7F`
on echo.*

## Limitations

- **No backspace.** A mistyped character is in the buffer for good.
- **No explicit length limit.** The 128-character exit is a side effect, not a
  designed bound, and it produces no message.
- **No buffer-full handling.** If Y did wrap past 255 it would return to `$0400`
  and overwrite from the start; in practice the `BPL` exit fires first, at 128.
- **No lower-case handling.** The repository's firmware behavior model rejects
  case conversion until measured rather than guessed.
- **No terminator beyond the stored CR.** Anything reading the buffer must stop
  at `$8D` itself.

## What this does not prove or authorize

It does not show that this program has ever run on this project's Replica 1
Plus, that the board reads a keypress, that its display works, or that the
Monitor routine at `$FFEF` exists on that machine. Everything above is read from
bytes or observed in a software model.

The artifact remains RAM-ONLY with **no live-run authority**. This annotation
contains no entry procedure and authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
