# Recorded emulator runs

Reference runs performed while authoring this library, so lessons can state an
expected result that was actually observed rather than predicted.

## Harness

`tools/apple1_emulator.py` from this repository, unmodified, with `py65`
installed from `requirements-dev.txt`. Per its own docstring, the harness is
ROM-free: it models the keyboard registers and the Monitor `ECHO` and warm-entry
calls that the RAM-only programs need, and it emulates no Propeller, no serial
hardware, and no Apple-1 ROM image.

The runs below were executed off-device, on a Linux host, not on the Replica 1
Plus and not on the project workstation. They are software evidence about the
byte lists in `software/ram-only/`. They are not evidence about hardware.

## `line-input-0300.hex`

| Input | `screen_text` | `buffer_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---:|---:|
| `A` + CR | `A\r` | `A\r` | true | 20 |
| `HI` + CR | `HI\r` | `HI\r` | true | 30 |
| `HELLO` + CR | `HELLO\r` | `HELLO\r` | true | 60 |
| `APPLE-1` + CR | `APPLE-1\r` | `APPLE-1\r` | true | 80 |

The instruction count follows `10 * (n + 1)` for `n` typed characters before the
carriage return, across all four runs. This is a property of this harness
counting these instructions, not a timing claim about any machine.

## `line-input-echo-0300.hex`

| Input | `screen_text` | `buffer_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---:|---:|
| `HI` + CR | `HI\rHI\r` | `HI\r` | **false** | 50 |

## Finding: the echo program does not return to the Monitor

`software/ram-only/README.md` states the general rule "Exit via `JMP $FF1F`."
`line-input-0300.hex` follows it and the harness confirms
`returned_to_monitor: true`.

`line-input-echo-0300.hex` does not. Its final instruction is `JMP $0300`, a
jump back to its own start, and the harness reports
`returned_to_monitor: false`. Reading the byte list confirms this:

```text
0317: A0 00      LDY #$00
0319: B9 00 04   LDA $0400,Y
031C: 20 EF FF   JSR $FFEF
031F: C9 8D      CMP #$8D
0321: F0 03      BEQ $0326
0323: C8         INY
0324: 10 F3      BPL $0319
0326: 4C 00 03   JMP $0300
```

This is not presented as a defect. It may well be intended: the program is
described in `docs/apple1-software-library.md` as reading the buffer back
"before starting over." But it means the second program has no self-directed
exit to the Monitor, and any future operator-led session involving it would end
by reset rather than by the program returning on its own.

**This is flagged for the repository owner's review.** No lesson in this library
treats `line-input-echo-0300.hex` as returning to the Monitor, and no lesson
proposes running either program on hardware.

## C05 lesson program

Not a repository artifact. Ten bytes written for the C05 state-trace worksheet
and executed during authoring so the lesson could state an observed result.

```text
A9 41 69 01 8D 00 04 4C 1F FF
   LDA #$41 / ADC #$01 / STA $0400 / JMP $FF1F
```

| Variant | `A` | `$0400` | `returned_to_monitor` | `instructions` |
|---|---|---|---:|---:|
| As written | `$42` | `$42` | true | 4 |
| With leading `CLC` (`18`) | `$42` | `$42` | true | 5 |

The two agree because the harness begins with the carry clear. The version
without `CLC` therefore produces a correct answer while depending on state it
never established. C05 is built around exactly that: the transcript confirms the
arithmetic and hides the defect.

The initial-carry behavior was confirmed by reproducing the run directly against
the `py65` MPU model. It is observed, not a documented guarantee of the harness.
Recorded as verification item V-11 in `C05-instructions-change-state/SOURCE-NOTES.md`.

## A03 lesson programs

Not repository artifacts. Eleven bytes each, written for the A03 countdown
worksheet. Neither reads the keyboard, so these were run directly against the
`py65` NMOS 6502 model rather than through `tools/apple1_emulator.py`, whose
command line requires a keyboard input string.

```text
A  A2 05 CA D0 FD 8E 00 04 4C 1F FF    LDX #$05 / DEX / BNE / STX $0400 / JMP
B  A2 05 CA 10 FD 8E 00 04 4C 1F FF    same, but BPL instead of BNE
```

| Program | `DEX` passes | Final X | `$0400` | Instructions |
|---|---:|---|---|---:|
| A (`BNE`) | 5 | `$00` | `$00` | 13 |
| B (`BPL`) | 6 | `$FF` | `$FF` | 15 |

One byte apart, one extra pass, and a final value at the opposite end of the
range. This is A03's off-by-one puzzle.

## A04 lesson program

Not a repository artifact. Twenty-five bytes written for the A04
choose-the-message worksheet, run through `tools/apple1_emulator.py`.

```text
AD 11 D0 10 FB AD 10 D0 C9 D9 F0 05 A9 CE 4C 13 03 A9 D9 20 EF FF 4C 1F FF
```

| Input | `screen_text` | `returned_to_monitor` | `instructions` |
|---|---|---|---:|
| `Y` + CR | `Y` | true | 9 |
| `N` + CR | `N` | true | 10 |
| `Q` + CR | `N` | true | 10 |

The harness rejects input not ending in a carriage return, so a CR is supplied
even though this program reads only the first key and never consumes it.

The one-instruction difference between the `Y` and `N` paths is the `JMP` that
the non-adjacent path needs in order to skip over the adjacent one.

## X02 lesson programs

Not repository artifacts. Fifteen bytes each, written for the X02 fix-the-loop
worksheet, differing in one byte.

```text
BROKEN     A0 00 A9 41 99 00 04 C8 C0 06 D0 F8 4C 1F FF
CORRECTED  A0 00 A9 41 99 00 04 C8 C0 05 D0 F8 4C 1F FF
```

| Version | `buffer_text` | `returned_to_monitor` | `instructions` |
|---|---|---:|---:|
| Broken (`CPY #$06`) | `AAAAAA`, six characters | true | 27 |
| Corrected (`CPY #$05`) | `AAAAA`, five characters | true | 23 |

Both return cleanly and both write plausible data to a plausible address. The
only difference is one character and four instructions. This is why X02 insists
on tracing against a written intention rather than looking for a symptom: there
is no symptom.

A carriage return was supplied to satisfy the harness, which rejects input not
ending in one. Neither program reads the keyboard and the input is never
consumed.

## Programs written for lessons carry no hardware authority

The C05, A03, A04, and X02 byte sequences above were written to teach something. They
are not in `software/ram-only/`, have not been through the acceptance card in
`docs/apple1-software-library.md`, and must not be treated as candidates for a
hardware session.

## What these runs do not establish

An emulator result is software evidence. It does not establish that the Replica
1 Plus powers on, that its display works, that its keyboard is read, that its
serial path carries a byte, or that the EEPROM installed on the board contains
the Monitor these programs call into. Per `docs/emulator-demo-guide.md`, a
successful emulator run does not waive a hardware evidence gate.
