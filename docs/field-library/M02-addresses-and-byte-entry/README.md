# M02 Addresses and byte entry

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S03, C02

## You will learn

By the end, you can read a byte listing, work out which address each byte
belongs to, and say why the load address is as important as the bytes
themselves.

## Why this matters

Every program in this repository is stored as a bare list of hex bytes with an
address in its filename. If you cannot map the list onto addresses, you cannot
check a transcription, you cannot find an instruction someone is referring to,
and you cannot tell whether two listings are the same program.

This lesson is entirely about reading. Nothing here is entered on a machine.

## First result

The first three bytes of a real repository listing, each labeled with its
address.

## What you need

Paper. `assets/listing-anatomy.txt` and `assets/marking-worksheet.txt`.

## Activity

1. Read `assets/listing-anatomy.txt`. It uses an invented eight-byte example so
   you can see the shape without worrying about what it does.
2. On `assets/marking-worksheet.txt`, mark the first three bytes of the real
   listing with their addresses.
3. Check against `ANSWERS.md`. That is your first result.

## Explain what happened

**A listing is bytes plus a starting point.** The bytes are the program. The
address says where the first one goes. Every byte after it goes one address
further along. That is the whole mapping, and it is just counting.

**The address is not in the file.** In this repository the byte lists are
"address-free": the file contains only bytes, and the address lives in the
filename. `line-input-0300.hex` is the byte list, and `0300` is where it belongs.
Keeping them separate is deliberate, because a listing that carried its own
address inside it could disagree with itself.

**The same bytes at a different address are a different program.** This is the
part that surprises people. Bytes that refer to addresses, like a jump, contain
those addresses inside themselves. Move the program without changing them and
the jumps still point where they always did, which is now the wrong place.

Some bytes are worse than that. A branch uses a *relative* offset, so it moves
with the program correctly. A jump uses an absolute address and does not. A
listing moved wholesale to a new address is usually a program that runs for a few
instructions and then goes somewhere meaningless.

**Counting bytes and finding the end.** Twenty-six bytes starting at `$0300`
occupy `$0300` through `$0319`, not through `$031A`. The first byte uses up the
first address, so the last address is the start plus the count minus one. This
off-by-one is the same one from C05's loop, in a different costume.

**Bytes do not announce where instructions begin.** A listing is a flat run of
numbers. Nothing in it marks the boundary between one instruction and the next.
You find the boundaries by starting at the first byte, working out how long that
instruction is, and stepping forward by that much. Start at the wrong byte and
you will get a plausible-looking but entirely wrong disassembly, because almost
any byte is a valid opcode.

That is why the load address matters so much, and why "start here" is
information the bytes cannot supply about themselves.

**On checking a transcription.** The practical use of all this is comparing two
copies of a listing. Count the bytes first; a different count means a definite
error. Then compare in fixed-size groups, because the eye is much better at
spotting a difference between two columns of eight than between two long lines.

## Try a variation

The Monitor prints inspected memory eight values to a line. The repository's byte
list is written as a single run. Say which format is easier to check by eye and
why, and what the single run is better for.

## Check your understanding

1. A listing of 26 bytes loads at `$0300`. What is the address of the last byte?
2. Why does this repository keep the load address in the filename rather than in
   the file?
3. You are given a byte list with no address at all. What can you still work out
   about it, and what becomes impossible?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The listing format and address-free convention come from this repository's
RAM-only README; the Monitor's display format from the Briel manual. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish or authorize:

- **It contains no entry procedure.** Working out which address a byte belongs to
  is not the same as entering it, and nothing in this packet tells anyone to type
  a byte into a machine.
- It shows nothing about this project's hardware.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
