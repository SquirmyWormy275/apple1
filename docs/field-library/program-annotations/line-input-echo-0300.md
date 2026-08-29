# `line-input-echo-0300.hex` annotated

**Status: OFF-DEVICE annotation of a RAM-ONLY artifact with no live-run
authority.**

## What it is for

It collects a typed line exactly as `line-input-0300.hex` does, then reads the
buffer back out to the display a second time, then starts over.

The repository describes it as a **display-path exercise**, and is explicit that
it is not proof of serial transmission.

*Source: REPO `software/ram-only/README.md`.*

## Load address and size

**Load address `$0300`. 41 bytes, occupying `$0300` through `$0328`.**

`$0300` + 41 - 1 = `$0328`.

**Its first 23 bytes are identical to `line-input-0300.hex`.** The two programs
diverge at `$0317`, where one jumps to the Monitor and this one begins a second
loop.

## Input and output

| | |
|---|---|
| **Input** | Keyboard characters through `$D010` when `$D011` says one waits, each with bit 7 set. |
| **Output, on screen** | Each character as typed, **then the whole buffer again**. The line appears twice. |
| **Output, in memory** | The typed characters at `$0400` onward, including the carriage return. |
| **Then** | It returns to its own start and waits for another line, indefinitely. |

## Memory it uses

Identical to the first program: `$0300`-`$0328` for itself, `$0400` onward for
the buffer, `$D010` and `$D011` read-only, `$FFEF` called.

**It never touches `$FF1F`.** That absence is the subject of this annotation.

## The listing

```text
0300  A0 00      LDY #$00      Y = 0
0302  AD 11 D0   LDA $D011     keyboard ready?
0305  10 FB      BPL $0302     not yet, look again
0307  AD 10 D0   LDA $D010     take the character
030A  99 00 04   STA $0400,Y   store at $0400 + Y
030D  20 EF FF   JSR $FFEF     display it
0310  C9 8D      CMP #$8D      carriage return?
0312  F0 03      BEQ $0317     yes: go to the playback stage
0314  C8         INY           no: advance
0315  10 EB      BPL $0302     and read the next character
                               --- first 23 bytes end here ---
0317  A0 00      LDY #$00      Y = 0 again, back to buffer start
0319  B9 00 04   LDA $0400,Y   read a character back OUT of the buffer
031C  20 EF FF   JSR $FFEF     display it
031F  C9 8D      CMP #$8D      was that the stored carriage return?
0321  F0 03      BEQ $0326     yes: playback finished
0323  C8         INY           no: advance
0324  10 F3      BPL $0319     and read the next buffered character
0326  4C 00 03   JMP $0300     start the whole program again
```

Boundaries land exactly on `$0328`. Branch offsets resolve to instruction
boundaries. `$F3` is minus 13: `$0326` - 13 = `$0319`.

## Stage by stage

**Stages one to five are the first program**, unchanged: setup, wait, take,
store, show, test, repeat. See `line-input-0300.md` for those.

**Playback, `$0317` to `$0324`.** This is the new part, and structurally it is
the same loop with the input step removed.

Reset Y to zero. Then `LDA $0400,Y` reads *from* memory where the first loop's
`STA $0400,Y` wrote *to* it. Same addressing mode, opposite direction. Display
it, check whether it was the stored carriage return, advance, repeat.

This is why the first loop stores the carriage return rather than discarding it:
the second loop uses that stored `$8D` as its stopping marker. The two halves
are coupled through one byte in memory.

**Restart, `$0326`.** `JMP $0300`, back to the program's own first instruction.

## How it ends

**It does not.**

The final instruction is `4C 00 03`, `JMP $0300`. There is no instruction
anywhere in this program that returns control to the Monitor.

Run in the repository emulator it reports `returned_to_monitor: false`, which
confirms by observation what the bytes already say.

### Does it follow the repository's exit rule?

`software/ram-only/README.md` gives the rule: **"Exit via `JMP $FF1F`."**

`line-input-0300.hex` follows it. **This program does not.**

### Is that a defect?

**This annotation does not say.** Two readings are available and the bytes do not
settle between them.

The reading that it is intended: `docs/apple1-software-library.md` describes this
program as reading the buffer back "before starting over." That is a description
of a loop. If restarting is the design, the general exit rule simply was not
written with this program's shape in mind.

The reading that it is an oversight: the rule is stated generally, this program
is the only artifact that breaks it, and nothing documents the exception.

**What would settle it** is a statement from whoever wrote or adopted the
artifact. That is a question for the repository owner, not something a reader can
resolve from a listing. Recorded as **V-15**.

### The consequence, which is not in dispute

Whatever the intent, the effect is definite: **a session using this program would
end by pressing reset, not by the program handing control back.**

Anyone planning such a session needs to know that beforehand rather than
discovering it with the machine running. The acceptance card in
`docs/apple1-software-library.md` requires a prepared reset recovery, so this is
a planning input for that card, not a new requirement.

*This annotation does not authorize such a session and does not describe how to
conduct one.*

## Expected emulator behavior

Recorded in `../EMULATOR-RUNS.md`:

| Input | `screen_text` | `buffer_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---|---:|
| `HI` + CR | `HI` CR `HI` CR | `HI` CR | **false** | 50 |

Two things to read carefully there.

**`screen_text` shows the line twice** and `buffer_text` shows it once. That is
correct: the buffer holds one copy, and the display received it twice.

**`returned_to_monitor` is false.** The harness reports this because the program
arrived back at its own load address with no input remaining. It did not hit
`$FF1F`, because nothing in the program goes there.

*Source: E-EMU-SCOPE; the harness's own early-return branch on reaching the load
address with input exhausted.*

## Limitations

Everything limiting `line-input-0300.hex` applies here, plus:

- **No exit.** Covered above. The only way out is a reset.
- **The playback loop trusts the buffer.** It walks forward until it finds
  `$8D`. If the buffer did not contain one, it would keep reading past the end
  until Y reached `$80` and its own `BPL` stopped it.
- **The second loop inherits the first loop's 128-character bound** by the same
  accidental mechanism, not by design.
- **It proves nothing about serial.** The repository is explicit: this is a
  display-path exercise, and a display echo does not establish that a byte
  reached anything else.

That last point is worth dwelling on, because this is exactly the program whose
output most looks like evidence of a working data path and is not.

## What this does not prove or authorize

It does not show that this program has ever run on this project's Replica 1
Plus. It does not show that the display works, that a key is read, or that any
byte crosses the serial port. A line appearing twice on a screen is a statement
about a display path, and not even an observed one here.

The artifact remains RAM-ONLY with **no live-run authority**. This annotation
contains no entry procedure and authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
