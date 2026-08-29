# Field Library glossary

Twenty-nine terms, in the order a newcomer meets them rather than alphabetically.
Each entry says plainly what the word means and then labels where the claim comes
from.

**How to read the source lines.** An entry marked **general computing concept**
is true of computers broadly and is not a claim about the Apple-1 or about this
project's board; those need no citation. An entry with a **Source** line makes an
Apple-1-specific or historical claim, and the key points into `SOURCES.md`, which
holds the exact wording each claim rests on.

**What this glossary does not establish.** Nothing here is a measurement of this
project's Replica 1 Plus. Several entries describe documented designs. A design
is not a reading from a board, and no entry should be quoted as evidence about
what this machine currently does.

---

## The objects

### Apple-1

A single-board computer designed by Steve Wozniak and sold in 1976. About two
hundred were made. The retail price of $666.66 bought the assembled circuit
board and nothing else, so a buyer still had to find a keyboard, a power supply,
and a video display before it would do anything.

What made it notable was not being first. It was that a keyboard and a display
were the ordinary way to use it, where competing hobby machines such as the
Altair were operated with rows of switches and lights.

*Source: H-MADE, H-PRICE, H-BARE, H-SUPPLY, H-KBD-STD. Note V-2: "made,"
"sold," and "bought by the Byte Shop" are three different counts in the sources
and must not be merged into one number.*

### Replica 1 Plus

A modern reproduction of that design, manufactured decades later and sold with
its own user manual dated June 2014. It behaves similarly to an original and its
ROM additionally holds BASIC and an assembler that no 1976 Apple-1 shipped with.

It is a replica. It is not an original Apple-1, and this library never calls it
one without qualification. **This project's machine is a Replica 1 Plus.**

*Source: BRIEL throughout; R-ROM-SPLIT. Note V-4: Owad's book documents the
original Apple-1 and the earlier Replica I and Replica I TE, which are different
products from the Plus.*

### CF card

A CompactFlash memory card. In this project it is intended as archival storage
for this library.

**How the card would be read, browsed, or booted is deliberately undecided.**
The curriculum says so directly: it defines the educational catalog and not the
card mechanism. No lesson here assumes a file system, a directory layout, a
menu, or a boot workflow, and none should acquire one until somebody decides.

*Source: REPO `docs/apple1-learning-library-curriculum.md`, opening paragraph and
the card-menu note.*

---

## Numbers and storage

### Bit

One yes-or-no value, written 1 or 0. The smallest thing a computer stores.

*General computing concept.*

### Byte

Eight bits in a row. A byte holds 256 different patterns, so it can represent a
number from 0 to 255. Note the range: 256 possibilities, and the largest is 255,
not 256.

*General computing concept.*

### Binary

Counting with two symbols instead of ten. Each column is worth double the one to
its right: 1, 2, 4, 8, 16, 32, 64, 128. To read a byte, add up the columns
holding a 1.

Bit 7 is the leftmost and largest, worth 128. The numbering runs right to left,
which catches people out, because we read text the other way.

*General computing concept.*

### Hexadecimal

Counting with sixteen symbols: 0 to 9, then A to F for ten through fifteen.
Written with a `$` in front, as in `$FF`, or sometimes `0x`.

Programmers use it because two hex digits describe exactly one byte, every time,
with nothing left over. Decimal does not divide into a byte cleanly, so byte
values would sometimes be two characters and sometimes three.

*Source: A-HEX for the prefix convention and the two-digits-per-byte property;
A-TABLE for the equivalences. The arithmetic itself is general.*

---

## Memory

### Address

A number that names one storage location. The 6502 puts a 16-bit number on its
address bus, giving 65,536 locations, `$0000` through `$FFFF`. Each holds exactly
one byte.

*Source: M-64K.*

### RAM

Random-access memory. Storage a program can read and write freely, which **loses
its contents when the power goes off**.

On the original Apple-1 this mattered concretely: BASIC lived in RAM, so it had
to be reloaded from cassette or typed in by hand every single time the machine
was switched on.

*Source: M-RAM-ORIG, M-BASIC-RAM. The general read-write-and-forgets property is
a general computing concept.*

### ROM

Read-only memory. Storage that keeps its contents with the power off, and that a
running program cannot change. A write instruction aimed at ROM executes without
complaint and changes nothing, which is harder to debug than an error would be.

*General computing concept. For where ROM sits on this machine, see memory map.*

### Memory map

A picture of which addresses hold what. On the original Apple-1: 4 KB of user
RAM from `$0000`, hardware registers around `$D010`, 4 KB for BASIC at `$E000`,
and 256 bytes of Monitor ROM at the very top, `$FF00` to `$FFFF`. Most of the
64 KB is connected to nothing at all.

**A memory map is a model.** It reproduces published documentation of a design.
It is not a survey of any particular board, and the Replica 1 Plus differs from
the original.

*Source: M-RAM-ORIG, M-PIA-RANGE, M-ROM, M-BASIC-RAM. Note V-4 and V-8.*

### RAM-only

This project's label for a program that could one day be entered by hand into
RAM, in a separate operator-led session. It writes nothing permanent: no ROM, no
CFFA1, no Propeller RAM, no EEPROM.

**RAM-only is not permission.** The two RAM-only programs in this repository are
classified as candidates with **no live-run authority**. Reading them, tracing
them, or rehearsing them off-device does not move them any closer to being run.

*Source: REPO `software/ram-only/README.md`; REPO `docs/apple1-software-library.md`,
"Hardware authority" column.*

---

## The processor

### CPU

Central processing unit. The chip that reads instructions and carries them out.
It repeats one loop forever: fetch the next instruction, work out which action it
names, do it. There is no step where it considers alternatives.

*General computing concept.*

### 6502

The microprocessor used in the Apple-1, made by MOS Technology. It has a small
number of registers rather than much internal storage, and a modest instruction
set from which everything else is built.

*Source: OWAD ch. 7, which documents the processor section of the machine.*

### Register

A tiny named storage location inside the CPU, holding one byte. The 6502's main
ones are **A**, the accumulator, where most work happens, and **X** and **Y**,
the index registers, used for counting and for stepping through memory.

The **program counter** is different: it holds an address rather than a byte, and
it is the CPU's place in the program.

*Source: OWAD ch. 7 p. 215 for the register set. The concept is general.*

### Instruction

One action for the CPU to perform. Written for humans as a three-letter
mnemonic plus, usually, something to act on: `LDA #$41` means load the
accumulator with the number `$41`.

*Source: OWAD Appendix D, the instruction reference. The concept is general.*

### Opcode

The single byte that names which action an instruction performs. `$4C` is a
jump; `$A9` is load-accumulator-immediate. Some instructions need extra bytes
after the opcode saying what to act on.

**Nothing in memory marks where an instruction begins.** You find the boundaries
by starting from a known point and stepping forward by each instruction's length.
Start at the wrong byte and you get a plausible-looking, entirely wrong reading.

*Source: OWAD Appendix D. The concept is general.*

---

## Software

### Program

A list of instructions in the order they will be carried out. On this machine a
program is often written down as a bare list of hex bytes plus the address the
first byte belongs at.

*General computing concept.*

### Source code

A program written in a form people can read, using names and mnemonics, before
it is turned into the bytes a machine runs.

**Having source is not having the thing that runs.** Three separate gaps sit
between them: whether that source was compiled, whether the result was
installed, and whether it is still there. This project's vendor `110REV03`
archive is recorded as candidate evidence, **not** as the image installed on this
board.

*Source: E-110REV03; REPO `docs/preservation-dossier.md`, "Current boundaries".*

### Monitor

Here, a **monitor program**: a small program stored permanently in a chip that
runs the moment you reset the machine, giving direct access to memory.

The word is confusing because "monitor" also means a display screen. This
library says *monitor program* for the software and *display* for the hardware.

*Source: WOZ-FWD p. 17, where Wozniak describes writing a short program that
watched the keyboard in place of front-panel switches and calls it a monitor.*

### Woz Monitor

The Apple-1's monitor program, 256 bytes, occupying `$FF00` to `$FFFF`. It does
three things and no more: show what is at an address, change what is there, and
start running at an address.

It is not an operating system. It manages no resources, has no concept of a
file, cannot list or stop anything, and offers no way to undo a change.

*Source: WOZ-FWD p. 17 for the size; M-ROM for the range; R-MON-3 and
R-MON-SYNTAX for the three functions, from the Replica 1 Plus manual. Note V-4:
the command syntax is documented replica behavior.*

### BASIC

A high-level programming language, easier to write than machine instructions
because it does bookkeeping for you. Apple-1 BASIC handles whole numbers only:
ask it for 38 divided by 9 and it answers 4, with `MOD` giving the remainder
separately.

*Source: B-INTEGER, B-MOD. Note V-20: no BASIC in this library has ever been
executed; every statement about it is cited from documentation.*

### Assembler

A program that turns readable mnemonics into machine bytes, working out opcodes,
addresses, and branch offsets for you. The Replica 1 Plus ROM contains one called
Krusader, written by Ken Wessen.

An assembler changes how you *write* a program, not what the program *is*.

*Source: R-KRUSADER, R-ROM-SPLIT.*

### Emulator

Software that imitates a machine so programs can be tried without hardware.

This repository's harness is deliberately narrow: it is ROM-free, it models only
the keyboard registers and the Monitor's echo and warm-entry calls that these
programs need, and it emulates **no Propeller, no serial hardware, and no
Apple-1 ROM image**.

**An emulator result is evidence about a byte sequence, never about hardware.** A
successful run does not waive a hardware evidence gate.

*Source: E-EMU-SCOPE; REPO `docs/emulator-demo-guide.md`.*

---

## Talking to the machine

### Terminal

A keyboard and a display used together to talk to a computer. Wozniak had
already built one before the Apple-1 and combined it with a processor and memory
rather than designing a computer from scratch.

*Source: WOZ-FWD p. 17.*

### Serial

Sending data one bit after another down a single wire, rather than several bits
side by side at once. Slower per wire and far simpler to connect.

**This project's serial path is under investigation and is not established as
working.** Opening the FT232R from the host has already produced a
display-garbling `STOP` result, and an opened serial session or transmit test is
blocked until a measurement test card is ready and an operator explicitly starts
that single step.

*Source: E-FT232-STOP; REPO `docs/preservation-dossier.md`, "Current boundaries".
The general concept is a general computing concept.*

### Baud

How fast a serial connection moves signal changes, in units per second. The
Replica 1 Plus reference settings recorded in this repository are 9600 baud, 8
data bits, one stop bit, no parity, no flow control.

Those are documented settings. **They are not a measurement of this board.**

*Source: R-SERIAL, from REPO `docs/reference/README.md` summarizing the manual.*

---

## Keeping records

### Checksum

A number computed from a file's contents such that changing any byte changes the
number completely. This project uses SHA-256.

**A checksum answers exactly one question: is this the same file it was?** It
cannot tell you where a file came from, whether it is genuine, whether anyone
will be able to open it in twenty years, or whether it describes the object
sitting next to it.

*Source: REPO `docs/collection-archive.md`; E-NOPROOF. The algorithm is a general
computing concept.*

### Provenance

The record of where something came from and what has happened to it since:
original location, source, permission, date, and whether the item is an
original, a derivative, or a working copy.

Provenance is what a checksum cannot supply. Identity says "this is that file."
Provenance says "and here is what it is."

*Source: REPO `docs/collection-archive.md`, which requires a human note beside
each manifest covering exactly those fields; REPO `docs/preservation-dossier.md`
evidence rules 2 and 3.*

---

## What this glossary does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No entry of any program on hardware.

Defining a word is not permission to do the thing it names. The entries for
serial, RAM-only, and CF card describe boundaries this project holds; they do not
relax them.
