# Worksheet 2: the memory map

**Time:** 30 minutes core, 45 with discussion
**You need:** this sheet, a pencil. Worksheet 1 helps but is not required.
**Status:** OFF-DEVICE. No address on this sheet is offered as one to look at on
a machine.

## What you'll be able to do afterwards

- Take an address and say which region of the machine it falls in.
- Explain why the same byte can be a number, a letter, or an instruction.
- Spot when a program and its data are about to collide.

---

## The map

This is the documented layout of the **original** Apple-1. It is a picture of a
published design, not a reading taken from any particular board.

```text
$FFFF +----------------------------+
      | MONITOR ROM        256 B   |
$FF00 +----------------------------+
      |                            |
      | UNUSED                     |
      |                            |
$F000 +----------------------------+
      | BASIC AREA          4 KB   |
      | (RAM ON THE ORIGINAL, SO   |
      |  BASIC HAD TO BE RELOADED  |
      |  EVERY POWER-UP)           |
$E000 +----------------------------+
      |                            |
      | UNUSED                     |
      |                            |
$D013 +----------------------------+
      | PIA: KEYBOARD IN, VIDEO OUT|
$D010 +----------------------------+
      |                            |
      | UNUSED                     |
      |                            |
$1000 +----------------------------+
      | SYSTEM AND USER RAM 4 KB   |
      |                            |
      |  $0400 A BUFFER            |
      |  $0300 WHERE SMALL         |
      |        PROGRAMS ARE PUT    |
      |  $0100 THE STACK           |
      |  $0000 ZERO PAGE           |
$0000 +----------------------------+
```

Most of the 64 KB is connected to nothing at all.

---

## Part A: place the address

Write the region each address falls in.

| Address | Region |
|---|---|
| `$0300` | |
| `$0400` | |
| `$01FF` | |
| `$D011` | |
| `$FF1F` | |
| `$9000` | |

**Stop and check.** These six recur throughout the rest of the library.

---

## Part B: can a program write there?

Answer yes, no, or "something else happens."

| Region | Writable? |
|---|---|
| `$0300`, user RAM | |
| `$D012`, the display register | |
| `$FF00`-`$FFFF`, Monitor ROM | |
| `$9000`, unused | |

The ROM row is worth a moment. A write instruction aimed at ROM **runs without
any error at all** and changes nothing. Why is that harder to debug than an
error would be?

_______________________________________________

---

## Part C: the same byte, three ways

Address `$0300` holds the value `$A0`.

Tick what `$A0` is:

- [ ] the number 160
- [ ] an instruction
- [ ] a character
- [ ] all of these, depending

Explain your answer in one sentence.

_______________________________________________

**This is the big idea on this sheet.** Take your time over it.

---

## Part D: backwards addresses

The 6502 stores a two-byte address with the **low half first**. So an
instruction meaning "jump to `$FF1F`" is written in memory as `4C 1F FF`.

Write these as they would appear in a listing.

| Address | Bytes, low first |
|---|---|
| `$D011` | |
| `$0400` | |
| `$FF1F` | |

Going the other way: the bytes `00 04` inside an instruction mean which address?

______

---

## Part E: the collision

A program is loaded at `$0300` and is 26 bytes long. A learner decides to use
`$0310` for their data.

1. What is the last address the program occupies?

   ______

   *(Careful. Start plus count minus one.)*

2. What goes wrong?

   _______________________________________________

3. Here is the part that matters. What would this look like to someone watching
   the machine? Would it say "your data is in the wrong place"?

   _______________________________________________

4. Give two addresses that would be safe, and say which is safer and why.

   _______________________________________________

---

## Part F: what a map can't tell you

You have memorised the map. List three things you still would not know about one
specific board sitting in front of you.

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## Extension, if you finish early

1. The original had 4 KB of user RAM. A later replica design has 32 KB. What
   does the extra room let you stop worrying about?

2. On the original, BASIC lived in RAM. What did that mean for someone who
   wanted to use BASIC twice in one afternoon with a power cut in between?

3. `$D010` and `$D011` are next to each other and do completely different jobs.
   Why might a designer put a piece of data and its "is it ready" flag in
   adjacent locations?

---

## Off-device alternative

**Already fully off-device.** No machine is involved and no address here is
offered for inspection on hardware.

If you have no printer, the map can be drawn on a board as five stacked boxes
with the addresses written up the side. The exercise works identically.

---

## Sources and boundaries

64 KB of addressable space: M-64K. Monitor ROM 256 bytes at `$FF00`-`$FFFF`:
M-ROM. Original RAM layout, 4 KB at `$0000` and 4 KB at `$E000`: M-RAM-ORIG.
BASIC in RAM and reloaded every power-up: M-BASIC-RAM. PIA at `$D010`-`$D012`:
M-PIA-RANGE. Stack at `$0100`-`$01FF`: M-STACK. `$FF1F` as the Monitor warm
entry: W-FF1F. `$0300` and `$0400` as this repository's program and buffer
addresses: E-RAMONLY. Later replica with 32 KB user space: M-REPLICA-MAP. Keys
resolve in `../SOURCES.md`.

**The map is a model.** It reproduces documentation of the original Apple-1
design. It is not a survey of this project's board, and the Replica 1 Plus
differs from both the original and from the replica Owad documents. See V-4 and
V-8.

**This worksheet authorizes nothing.** No firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification, and it contains no procedure
for examining memory on a machine.
