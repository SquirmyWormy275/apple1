# Answer key

Working shown, not just answers. Open questions have acceptance criteria so two
teachers mark two learners the same way.

---

# Worksheet 1: hex and binary

## Part A: the first sixteen

| Dec | Hex | | Dec | Hex |
|---:|---|---|---:|---|
| 0 | 0 | | 8 | 8 |
| 1 | 1 | | 9 | 9 |
| 2 | 2 | | 10 | A |
| 3 | 3 | | 11 | B |
| 4 | 4 | | 12 | C |
| 5 | 5 | | 13 | D |
| 6 | 6 | | 14 | E |
| 7 | 7 | | 15 | F |

The first ten being unchanged surprises people who expected hex to be alien
throughout. Only six symbols are new.

## Part B: why sixteen?

1. **256.**
2. **Two.**
3. **One** for 9, **three** for 255.
4. Accept anything recognising that **a fixed width makes errors visible**: bytes
   line up in columns, a missing or extra digit shows immediately, and you can
   count bytes by counting pairs. Reject "because computers use hex" ,  they do
   not; hex is a convenience for people.

## Part C: build a byte

| Number | Bits | Working |
|---:|---|---|
| 65 | `0100 0001` | 64 + 1 |
| 200 | `1100 1000` | 128 + 64 + 8 |
| 128 | `1000 0000` | 128 alone |
| 255 | `1111 1111` | everything |
| 13 | `0000 1101` | 8 + 4 + 1 |
| 141 | `1000 1101` | 128 + 8 + 4 + 1 |

**13 against 141: bit 7, and nothing else.** In decimal those two numbers look
unrelated. In binary they differ by one switch. This single observation is the
most useful thing on the sheet and is worth pausing the room for.

## Part D: the free shortcut

| Binary | Hex |
|---|---|
| `0000 1111` | `$0F` |
| `1010 0101` | `$A5` |
| `1111 0000` | `$F0` |
| `1000 1101` | `$8D` |
| `1101 0000` | `$D0` |

Watch for learners adding up rather than splitting. The point is that no
arithmetic is needed.

## Part E: both directions

| Decimal | Hex | Working |
|---:|---|---|
| 16 | `$10` | one sixteen, no ones |
| 32 | `$20` | two sixteens |
| 100 | `$64` | 100 / 16 = 6 r 4 |
| 200 | `$C8` | 200 / 16 = 12 r 8; 12 is C |
| 255 | `$FF` | 15 r 15 |

| Hex | Decimal | Working |
|---|---:|---|
| `$10` | 16 | |
| `$41` | 65 | 4 x 16 + 1 |
| `$7F` | 127 | 7 x 16 + 15 |
| `$8D` | 141 | 8 x 16 + 13 |
| `$FF` | 255 | 15 x 16 + 15 |

## Part G: the odd one out

**`$F1`.** `$1F`, 31, and 16 + 15 are all thirty-one. `$F1` is 15 x 16 + 1 =
**241**.

The lesson: reversing two hex digits does not reverse the number, it changes it
into a different one entirely. That is why transcription order matters when
copying byte lists.

## Part H: read the message

| Byte | minus `$80` | Char |
|---|---|---|
| `C8` | `$48` | H |
| `C9` | `$49` | I |
| `A0` | `$20` | space |
| `D4` | `$54` | T |
| `C8` | `$48` | H |
| `C5` | `$45` | E |
| `D2` | `$52` | R |
| `C5` | `$45` | E |

**`HI THERE`.**

**Why strip first:** ASCII assigns nothing above 127. Looking up `$C8` finds no
entry at all. The top bit is a marker wrapped around the character, not part of
it.

## Extension

1. **256.** Everything from 0 to 255 fits; 256 is the first that does not.
   *(Asking for the largest number you cannot write has no answer, which is
   itself worth mentioning if a learner spots it.)*
2. **Bit 5, worth 32.** `$41` is `A`, `$61` is `a`. One bit separates upper from
   lower case throughout ASCII.
3. No written answer. Watch whether they start adding from the left; the fast
   readers do.

---

# Worksheet 2: the memory map

## Part A: place the address

| Address | Region |
|---|---|
| `$0300` | System and user RAM. Where this repository's small programs go. |
| `$0400` | System and user RAM. The buffer those programs write into. |
| `$01FF` | The stack, which occupies `$0100`-`$01FF`. |
| `$D011` | The PIA. Hardware, not memory. |
| `$FF1F` | Monitor ROM. |
| `$9000` | Unused. Nothing is wired there. |

## Part B: can a program write there?

| Region | Answer |
|---|---|
| `$0300` user RAM | **Yes.** Ordinary read-write memory. |
| `$D012` display register | **Something else happens.** The write is not stored for later reading; it hands a character to the video circuitry. |
| Monitor ROM | **No.** |
| `$9000` unused | **Something else happens**, and what exactly is undefined. Nothing is wired there. |

**Why a silent ROM write is harder to debug than an error:** because nothing
tells you. The instruction runs, the program continues, and the value you thought
you stored simply is not there. An error would point at the line; silence makes
you look everywhere else first.

## Part C: the same byte, three ways

**All of these, depending.**

Accept any reasoning that lands on: **memory does not record what kind of thing a
byte is.** Only the program's treatment decides. Fetched as an opcode it is an
instruction; loaded and compared it is the number 160; sent to the display it is
a character code.

Reject answers that pick one and defend it as the "real" meaning. There is no
real meaning; that is the idea.

## Part D: backwards addresses

| Address | Bytes |
|---|---|
| `$D011` | `11 D0` |
| `$0400` | `00 04` |
| `$FF1F` | `1F FF` |

`00 04` means **`$0400`**.

## Part E: the collision

1. **`$0319`.** Start plus count minus one. A learner answering `$031A` has made
   the classic off-by-one and should be walked back to "the first byte uses up
   the first address."
2. **`$0310` is inside the program.** Writing data there overwrites the
   program's own instructions while it is running.
3. **It would look like almost anything.** The program might work for a few
   characters then behave strangely, or jump somewhere meaningless, or stop
   responding, because the bytes it is about to execute have been replaced with
   text. **It would not look like a misplaced buffer**, which is what makes this
   class of mistake expensive.
4. **`$0400`**, a full 256 bytes clear, or **`$0320`**, just past the last byte.
   `$0400` is safer because it survives the program growing; `$0320` is only safe
   for a program of exactly this length.

## Part F: what a map can't tell you

Any three of: whether this board actually has the RAM the design calls for; what
is really programmed into its ROM; whether the PIA registers respond; whether it
powers on; whether a previous owner modified it; what firmware any
microcontroller on it is running.

**The map describes a design. A board is an object.** If a learner writes that
sentence in their own words, they have understood the whole worksheet.

## Extension

1. **You stop worrying about collisions and size.** With 4 KB you count bytes;
   with 32 KB you can put the buffer a comfortable distance away and stop
   thinking about it.
2. **They would have to type or load BASIC in all over again**, from scratch,
   because it lived in RAM and RAM forgets.
3. No single answer. Good ones: a program can check the flag and read the data
   with almost the same instruction; they are two registers of the same physical
   chip, so they were always going to be neighbours. Accept anything reasoned.

---

# Worksheet 3: what you saw and what you concluded

## Part B: the trace

| Pass | Y before | Stored at | Y after |
|---:|---|---|---|
| 1 | `$00` | `$0400` | `$01` |
| 2 | `$01` | `$0401` | `$02` |
| 3 | `$02` | `$0402` | `$03` |
| 4 | `$03` | `$0403` | `$04` |
| 5 | `$04` | `$0404` | `$05` |
| 6 | `$05` | `$0405` | `$06` |

**Six stores. Highest address `$0405`. No, it was meant to do five, ending at
`$0404`.**

## Part C: say the difference

| | |
|---|---|
| Supposed to do | Store `$41` at `$0400` to `$0404`. Five copies. |
| Actually does | Stores `$41` at `$0400` to `$0405`. Six copies. |
| Difference | It writes one byte too many, at `$0405`. |

## Part D: one hypothesis

**The wrong byte is `06`, at address `$0309`.** It should be `05`.

That byte is the operand of `CPY #$06`, the instruction sitting at `$0308`. The
loop ends when Y equals the compare value, and Y reaches 6 only after six
increments, which means six stores.

Accept any hypothesis that names a specific cause, predicts a specific
observation, and could be shown false. Reject restatements of the symptom.

## Part E: why this kind is dangerous

Only the **last** box is ticked: it does one thing more than it was meant to.

**None of the first five would a quick test catch**, because none of them
happens. The program runs, returns cleanly, and writes plausible data to a
plausible address.

**So how would anyone find it?** Only by comparing against a written statement of
what it was supposed to do. Without a recorded intention this bug is
undetectable, which is the argument for writing the intention down first.

## Part F: change one thing

| What was done | Things changed | Interpretable? |
|---|---|---|
| Ran it again | 0 | **Yes.** It reproduces or it does not, and both are information. |
| Fixed one byte, ran again | 1 | **Yes.** The best case. |
| Fixed a byte, changed input, different computer | 3 | **No.** If it works you cannot say which change mattered, and you may have masked one fault with another. |

## Part G: keep going, or stop?

| Observation | Answer |
|---|---|
| Paper trace gives an unexpected number | **Continue.** A puzzle, and no machine is involved. |
| Display garbles during a test | **STOP.** "If the display changes." |
| Copied byte list doesn't match | **STOP.** "Or bytes mismatch." |
| Machine resets by itself | **STOP.** "A reset occurs." |
| Prediction wrong, behaviour consistent | **Continue.** Your model was wrong, which is a finding. Consistency is the good case. |

**What separates them: whether a physical machine has been left in a state
somebody has to recover.** Paper surprises are puzzles. Machine surprises are
incidents.

## Part H: a real one

1. **"Opening the FT232R from the host produced a garbled display."** That is the
   whole fact. It does not say what broke or why, and its narrowness is what
   makes it durable.
2. Any two of: opening it again to see whether it repeated; swapping the cable
   and retrying; changing settings and retrying; power-cycling and carrying on
   with the planned tests. Each replaces one clean observation with a muddle.
3. **Because it was recorded intact at the time and nothing was changed
   afterwards.** A preserved observation stays evidence. A disturbed one becomes
   an anecdote.

## Part I: the word "so"

| Sentence | Did | Saw | Concluded | Still true in five years |
|---|---|---|---|---|
| 1 | Opened the port | The display garbled | The serial path is broken | **Did and Saw.** The conclusion is one hypothesis among several. |
| 2 | Pressed reset | A backslash appeared | The ROM is the original one | **Did and Saw.** A backslash shows something responded like a monitor; any compatible image would do the same. |

**"So" is where the observation ends and the guessing starts.** Once learners
see it in these two sentences they start noticing it in their own writing, which
is the entire point of the exercise.

## Extension

Observed results, recorded in `../EMULATOR-RUNS.md`:

| Version | Byte at `$0309` | Buffer | Instructions | Returned |
|---|---|---|---:|---|
| As written | `06` | `AAAAAA`, six | 27 | true |
| Corrected | `05` | `AAAAA`, five | 23 | true |

**Both return cleanly. Both write believable data.** The entire difference is one
character and four instructions, and neither is visible unless you were counting.

---

# Marking notes

Two habits worth more than correctness:

**Did they write "unknown" where the value is unknown?** A learner who filled in
`$00` for an unestablished memory location has invented a fact. Catch that ahead
of any arithmetic slip.

**Did they label their guesses?** Especially in worksheet 3 Part I. A learner who
writes "I think, but haven't checked" is doing the thing this whole library is
about.

# Sources

All keys resolve in `../SOURCES.md`. Number equivalences A-TABLE, hex notation
A-HEX, character values A-CHART, keyboard high bit P-HIGHBIT. Memory layout
M-64K, M-ROM, M-RAM-ORIG, M-BASIC-RAM, M-PIA-RANGE, M-STACK, M-REPLICA-MAP.
Monitor warm entry W-FF1F. Repository program and buffer addresses E-RAMONLY.
The STOP rule E-STOP; the serial incident E-FT232-STOP with V-13 on its primary
record. Instruction meanings from OWAD Appendix D.

# What this key does not establish

No answer in it claims this project's machine works in any respect. The worksheet
3 program is a teaching artifact with no hardware authority. Nothing here
authorizes a firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
