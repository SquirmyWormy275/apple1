# M02 Activity: mark the listing

**Status:** OFF-DEVICE. Paper only. **This activity is reading practice. No byte
in it is to be entered on any machine.**

## Part A: mark the real listing (this is the first result)

Complete `assets/marking-worksheet.txt`, questions 1 to 5, using
`software/ram-only/line-input-0300.hex`.

## Part B: address arithmetic

| Load address | Byte count | Address of last byte |
|---|---:|---|
| `$0300` | 26 | |
| `$0300` | 41 | |
| `$0400` | 8 | |
| `$0300` | 1 | |

## Part C: which byte is where

Using the real listing, give the byte at each address.

| Address | Byte |
|---|---|
| `$0300` | |
| `$0305` | |
| `$030D` | |
| `$0317` | |
| `$0319` | |

## Part D: same bytes, different address

A listing containing `4C 1F FF` is written for `$0300`. Someone loads it at
`$0500` instead.

1. What do those three bytes mean?
2. Does that instruction still work correctly at the new address?
3. Now consider `10 FB`, a branch. Does *that* still work at the new address?
4. State the general rule you have just discovered.

## Part E: check the transcription

Two people copied the same listing. Find every difference. Do not assume the
first is correct.

```text
A:  A0 00 AD 11 D0 10 FB AD 10 D0 99 00 04 20 EF FF
B:  A0 00 AD 11 DO 10 FB AD 10 D0 99 00 40 20 EF FF
```

For each difference, say whether it is a *transcription* error that a machine
would reject outright, or one it would accept and run wrongly. The second kind
is the dangerous kind.

## Part F (optional): design a checking format

Propose a way of writing a 26-byte listing on paper that makes errors easy to
catch. State what your format costs as well as what it buys.

## What this activity does not do

It reads and counts bytes on paper. It enters nothing anywhere, runs nothing,
and authorizes no hardware action.
