# Worksheet 1: hex and binary

**Time:** 25 minutes core, 40 with discussion
**You need:** this sheet, a pencil. Optionally eight coins per pair.
**Status:** OFF-DEVICE. Nothing is powered on or connected.

## What you'll be able to do afterwards

- Convert any number from 0 to 255 into hexadecimal, and back.
- Build any byte out of eight ones and zeros.
- Say why programmers use base sixteen instead of ordinary numbers.

---

## Part A: the first sixteen

Ordinary counting has ten symbols, 0 to 9. When you run out you start a new
column. Hexadecimal has sixteen symbols. The first ten are the ones you know, and
then letters take over.

Fill this in. The first ten are not a trick.

```text
 DEC | HEX        DEC | HEX
-----+-----      -----+-----
  0  |             8  |
  1  |             9  |
  2  |            10  |
  3  |            11  |
  4  |            12  |
  5  |            13  |
  6  |            14  |
  7  |            15  |
```

**Stop here and check with your teacher.** Everything else rests on this.

---

## Part B: why sixteen?

A byte is eight switches. Each switch is on or off, so a byte holds 256
different patterns, numbered 0 to 255.

1. Sixteen times sixteen is ______.

2. So how many hex digits does it take to write any byte? ______

3. How many ordinary decimal digits does it take to write 9? ______
   And to write 255? ______

4. In one sentence: why is a fixed width useful when you are writing down a long
   list of bytes?

   _______________________________________________

---

## Part C: build a byte

Each column is worth double the one on its right.

```text
+---+---+---+---+---+---+---+---+
|128| 64| 32| 16|  8|  4|  2|  1|
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```

Write 1 under the columns you switch on, 0 everywhere else. Add up the ones you
switched on to check.

| Number | Your eight bits |
|---:|---|
| 65 | |
| 200 | |
| 128 | |
| 255 | |
| 13 | |
| 141 | |

**Look at your last two rows.** 13 and 141. What is the *only* difference
between them?

_______________________________________________

---

## Part D: the free shortcut

Split any eight bits down the middle into two groups of four. Each group of four
is worth 0 to 15, which is exactly one hex digit. No arithmetic needed.

```text
     1100 1000
     ----+----
      C     8      =  $C8  =  200
```

Convert these by splitting. Do not add anything up.

| Binary | Hex |
|---|---|
| `0000 1111` | |
| `1010 0101` | |
| `1111 0000` | |
| `1000 1101` | |
| `1101 0000` | |

---

## Part E: both directions

**Decimal to hex.** Divide by 16. The whole part is the first digit, the
remainder is the second.

| Decimal | Hex |
|---:|---|
| 16 | |
| 32 | |
| 100 | |
| 200 | |
| 255 | |

**Hex to decimal.** Multiply the first digit by 16 and add the second.

| Hex | Decimal |
|---|---:|
| `$10` | |
| `$41` | |
| `$7F` | |
| `$8D` | |
| `$FF` | |

---

## Part F: five worth memorising

These turn up constantly. Cover one column and recite the other.

| Hex | Decimal | What it is |
|---|---:|---|
| `$0D` | 13 | Carriage return, the Enter key |
| `$20` | 32 | Space |
| `$41` | 65 | Capital A |
| `$80` | 128 | Just the top bit, on its own |
| `$FF` | 255 | Every bit set, the biggest byte |

---

## Part G: the odd one out

Three of these are the same number written differently. Which one is not, and
what is it instead?

`$1F`   31   `$F1`   16 + 15

_______________________________________________

---

## Part H: read the message

On this machine, a character coming from the keyboard arrives with its top bit
switched on. So the letter `A`, normally 65 or `$41`, arrives as `$C1`.

To read a message back you take 128 off each byte first, *then* look it up.

Decode this. The letter values you need are on the sheet your teacher has.

```text
C8  C9  A0  D4  C8  C5  D2  C5
```

Minus `$80` each: __ __ __ __ __ __ __ __

Message: _______________________________

**Why does taking the top bit off have to come first?**

_______________________________________________

---

## Extension, if you finish early

1. What is the *smallest* number you cannot write in a single byte?

2. `$41` is `A` and `$61` is `a`. Work out which single bit is different, and
   what it is worth.

3. Eight coins, heads for 1. Have someone set a number under 256 and read it as
   fast as you can. Then swap. Time each other.

---

## Off-device alternative

**This worksheet is already entirely off-device** and needs nothing but paper.

If you have no printer: draw the eight columns on any paper and write the values
128, 64, 32, 16, 8, 4, 2, 1 underneath. That is the only apparatus in the whole
sheet.

---

## Sources and boundaries

Hex notation with `$`, and two hex digits per byte: A-HEX. Number equivalences:
A-TABLE. Character values, and `$0D`, `$20`, `$41`: A-CHART. The keyboard high-bit
convention: P-HIGHBIT, from the Woz Monitor listing. Keys resolve in
`../SOURCES.md`. The arithmetic itself is ordinary arithmetic and is not cited.

**This worksheet does not establish anything about this project's machine.** It
authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
