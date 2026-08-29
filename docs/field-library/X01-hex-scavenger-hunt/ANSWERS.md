# X01 Answer key

Keep this closed until the hunt has been attempted. The hints are on the sheet.

## Part A: the first three

| # | Answer | Working |
|---|---|---|
| 1 | `10` | Line `0300` holds `$0300` to `$0307`; `$0305` is the sixth byte on it. |
| 2 | `20` | Line `0308` holds `$0308` to `$030F`; `$030D` is the sixth byte on it. |
| 3 | `$0319` | 26 bytes from `$0300`. Start plus count minus one. |

## Part B: find the instructions

| # | Answer |
|---|---|
| 4 | **`$0317`.** Working back: `4C` at `$0317` is a three-byte jump ending at `$0319`, which is the last byte. |
| 5 | **Three bytes**, `4C 1F FF`. |
| 6 | **`$FF1F`.** The operand `1F FF` is low byte first. |
| 7 | **`20` is at `$030D`**, and it is `JSR $FFEF`. The operand `EF FF` reads as `$FFEF`, the Monitor's echo routine. |

## Part C: find the addresses

Four addresses are referenced, at three absolute and one indexed:

| Referenced | From |
|---|---|
| `$D011` | `$0302`, `AD 11 D0` |
| `$D010` | `$0307`, `AD 10 D0` |
| `$0400` | `$030A`, `99 00 04` |
| `$FFEF` | `$030D`, `20 EF FF` |
| `$FF1F` | `$0317`, `4C 1F FF` |

That is five, not four. The question says four and it is wrong on purpose; a
learner who finds five and says so has done better than one who stops at four.

If a learner reports exactly four, ask which they left out. It is usually
`$0400`, because the `,Y` form looks unfamiliar, or `$FFEF`, because `20` is less
recognisable than `4C`.

## Part D: count

| # | Answer |
|---|---|
| 8 | **26 bytes.** |
| 9 | **14 bytes** have bit 7 set: `A0`, `AD`, `D0`, `FB`, `AD`, `D0`, `99`, `EF`, `FF`, `C9`, `8D`, `F0`, `EB`, `FF`. Count the first hex digit being 8 or higher, per C03's rule. |
| 10 | **`D0` appears twice, at `$0304` and `$0309`, and it means the same thing both times: the high byte of an address.** Once for `$D011` and once for `$D010`. |

Question 10 is worth expanding. `D0` is *also* the opcode for `BNE`, and it does
not appear as an opcode anywhere in this program. A learner who says "it might be
a branch" has spotted the real ambiguity, and the answer is that context decides:
these two `D0` bytes are the second operand byte of three-byte instructions, so
they cannot be opcodes. You know that only by having found the instruction
boundaries first.

That is the whole point of the M02 skill, and this is where it pays.

## Part E: read Dump Two

| # | Answer |
|---|---|
| 11 | **`WELL DONE`.** Subtract `$80` from each byte: `D7 C5 CC CC A0 C4 CF CE C5` becomes `57 45 4C 4C 20 44 4F 4E 45`, which is `W E L L space D O N E`. |
| 12 | **`8D`, a carriage return with the high bit set.** `$0D` plus `$80`. |
| 13 | **They are padding.** The message plus its carriage return is ten bytes and the dump is laid out eight per line, so the remaining six bytes of the second line are filled with `00` to complete it. They are not part of the message. |

## Part F: the trap

| # | Answer |
|---|---|
| 14 | **No.** It is invented for this puzzle and says so directly above itself. |
| 15 | **No**, and this is the subtler one. Dump One's *bytes* are real: they are `line-input-0300.hex` from this repository. But the dump is a **file laid out to look like a memory display**. Nobody read those bytes out of a machine's memory. |
| 16 | **By the labels on the sheet**, which is exactly why they are there. Dump Two carries an explicit disclaimer. Dump One names its source file. Without those two lines, a future reader would have a page of hex with addresses on it and no way to tell what it was. |

Question 15 catches almost everybody, and it should. "Real bytes" and "a reading
from a machine" are different claims, and a display that looks like a Monitor dump
invites the second when only the first is true.

## Try a variation and Part G

Acceptance: the message decodes correctly, every byte has bit 7 set, the layout
is eight per line with correct addresses, and the sheet says whether it is real or
invented. That last item is the one to insist on.

## README: Check your understanding

1. **Nothing in the dump does.** You find instruction boundaries by starting from
   a known point and working forward by instruction length, or backward from the
   end. The bytes themselves carry no markers.
2. **Because the 6502 stores two-byte values low byte first.** `1F` is the low
   half and `FF` the high half, giving `$FF1F`. Reading them in written order
   gives `$1FFF`, which is a different address entirely.
3. **Because ASCII assigns nothing above 127.** Looking up `$D7` finds no entry.
   The high bit is a marker added around the character, not part of it.
