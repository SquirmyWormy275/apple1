# M02 Answer key

## Part A: mark the real listing

1. **The load address is `$0300`,** and you know it from the filename:
   `line-input-0300.hex`. The file itself contains only bytes. This is the
   repository's address-free convention.

2. First three bytes:

   | Address | Byte |
   |---|---|
   | `$0300` | `A0` |
   | `$0301` | `00` |
   | `$0302` | `AD` |

3. **26 bytes.**

4. **`$0319`.** Start `$0300` plus 26 minus 1 = `$0319`. Not `$031A`.

5. **The split falls after `EB`.** `10 EB` is a two-byte branch instruction
   ending at `$0316`, and `4C 1F FF` is the three-byte jump at `$0317` to
   `$0319`. So `EB` belongs to the previous instruction and the final three bytes
   are one instruction: `JMP $FF1F`.

## Part B: address arithmetic

| Load address | Count | Last byte |
|---|---:|---|
| `$0300` | 26 | `$0319` |
| `$0300` | 41 | `$0328` |
| `$0400` | 8 | `$0407` |
| `$0300` | 1 | `$0300` |

The last row is the check on the rule: one byte occupies exactly the load
address and nothing further.

## Part C: which byte is where

| Address | Byte |
|---|---|
| `$0300` | `A0` |
| `$0305` | `10` |
| `$030D` | `20` |
| `$0317` | `4C` |
| `$0319` | `FF` |

Counting tip: `$030D` is the 14th byte, because `$0D` is 13 and the first byte
is at offset 0.

## Part D: same bytes, different address

1. **`JMP $FF1F`.** Jump to `$FF1F`, the Monitor's warm entry.
2. **Yes.** The target `$FF1F` is written inside the instruction as an absolute
   address. It does not care where the instruction itself sits.
3. **No.** `10 FB` is `BPL` with a *relative* offset of minus five. It computes
   its target from its own position. Moved to a new address it still lands five
   bytes back from wherever it now is, which relative to the program is the same
   place. So in fact **the branch survives the move and the jump survives too**,
   for opposite reasons.

   The instructions that break are absolute references to addresses *inside the
   program*. This listing has none, which is why it happens to be relocatable.

4. **The rule:** relative references move with the program; absolute references
   do not. A listing is safe to relocate only if every absolute address it
   contains points outside itself. Do not assume a listing is relocatable, check.

If a learner answers 3 with "no, it breaks," walk them through it. The intuition
that branches break and jumps survive is backwards, and this is the exercise that
fixes it.

## Part E: check the transcription

Two differences.

| Position | A | B | Kind |
|---|---|---|---|
| 5th byte | `D0` | `DO` | **Rejected.** `O` is a letter, not a hex digit. The repository's own loader raises a format error on a non-hex byte. A machine or a person will catch this. |
| 13th byte | `04` | `40` | **Accepted and run wrongly.** `40` is a perfectly valid byte. Nothing flags it. |

The second is the dangerous one. In context these bytes are `99 00 04`, which is
`STA $0400,Y`. Version B gives `99 00 40`, which is `STA $4000,Y`: a store to a
completely different address, with no error and no warning. The program would
appear to run and would write its characters into the wrong place.

**A is correct.** It matches the repository artifact.

## Part F: design a checking format

No single answer. Good proposals usually include some of: fixed groups of eight
with an address label per line, matching the Monitor's own output format; a byte
count written at the end; a simple checksum; or splitting into rows and columns
so both can be totalled.

Every one of them costs something: more to write, more to get wrong when
transcribing the checking apparatus itself, and a format that no longer matches
the repository's stored artifact. A learner who names a cost as well as a benefit
has answered the question.

## Try a variation: eight per line versus one run

**Eight per line is easier to check by eye,** because a difference between two
short columns is visually obvious while a difference between two long lines is
not, and because each line carries its own address so you can locate an error
rather than just detect one. It also matches what the Monitor prints, so a
listing and a screen can be compared line against line.

**The single run is better for storage and for tooling.** It has no formatting
to parse, no addresses that could disagree with the filename, and no way for a
line label to drift out of step with its contents. The repository stores the
awkward-to-read form on purpose and expects a person to reformat it when they
need to read it.

## README: Check your understanding

1. **`$0319`.** Start plus count minus one.
2. **So the two cannot disagree.** A file carrying its own load address could be
   copied, edited, or renamed into a state where the address inside contradicts
   the address outside. Keeping it in the filename means there is one statement
   of where the program goes, not two.
3. **You can still work out** the byte count, the instruction boundaries relative
   to the start, any relative branches, and roughly what the program does. **You
   cannot work out** where any absolute reference to its own body points, whether
   it will run correctly anywhere in particular, or whether an address inside it
   is meant to be part of the program or a target outside it.
