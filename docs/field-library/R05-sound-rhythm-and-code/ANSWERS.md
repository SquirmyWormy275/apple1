# R05 Answer key

## Part A: clap and encode

| Row | Pattern | Bits | Hex |
|---|---|---|---|
| 1 | `X . . . X . . .` | `1000 1000` | `$88` |
| 2 | `X . X . X . X .` | `1010 1010` | `$AA` |
| 3 | `X . . X . . X .` | `1001 0010` | `$92` |

## Part B: decode

| Byte | Bits | Slots that sound |
|---|---|---|
| `$88` | `1000 1000` | 1 and 5 |
| `$A4` | `1010 0100` | 1, 3, and 6 |
| `$FF` | `1111 1111` | All eight |
| `$00` | `0000 0000` | None |
| `$C0` | `1100 0000` | 1 and 2 |
| `$81` | `1000 0001` | 1 and 8 |

`$00` is worth a moment: it is a valid rhythm, and it is silence for eight slots.
An encoding that can represent nothing happening is more useful than one that
cannot.

## Part C: what the byte does not say

| Property | Captured? |
|---|---|
| Which slots have an event | **Yes.** This is the only thing it captures. |
| How fast | No |
| How loud | No |
| How long each lasts | No |
| What sound | No |
| How many repeats | No |

One yes and five noes. The encoding is exact about one property and silent about
everything else.

## Part D: the handover test

No fixed answer. The reliable findings:

- **Tempo will differ**, always. Nothing in the byte suggests one.
- **The starting point may differ** if the other person is unsure whether bit 7 or
  bit 0 is slot 1. That is a real ambiguity and the grid resolves it by
  convention, not by anything intrinsic.
- **Loudness and accent will differ**, because people naturally accent the first
  slot and nothing said to.

**For each difference: the byte was not wrong.** It did not carry the
information. That distinction is the whole exercise, and a learner who says "they
clapped it wrong" has missed it. There is no wrong, because there was no
specification.

The bit-order ambiguity is the interesting one, because it means the *same byte*
can decode two ways depending on an unstated convention. That is not a missing
property; it is a genuine defect in the encoding as handed over, fixable only by
stating the convention alongside it.

## Part E: extending the encoding

| Addition | Extra storage | Per what |
|---|---|---|
| Tempo for the whole pattern | 1 byte | Per pattern, not per slot. Cheap. |
| Loudness, four levels, per slot | 2 bits per slot, so 2 bytes for eight slots | Per slot. Triples the total. |
| Note length, sustained or not | 1 bit per slot, so 1 extra byte | Per slot. Doubles it. |
| Two instruments | Doubles everything | Per instrument. |
| Sixteen slots | 1 extra byte at the base encoding | Per slot count. |

**Anything per-slot multiplies; anything per-pattern adds.** Tempo is one byte
however long the pattern; loudness is two bits every slot forever. That is the
useful generalisation, and it is why per-pattern properties are nearly free and
per-slot ones are not.

## Part F: the honest limits

| # | Verdict | Why |
|---|---|---|
| 1 | **Supported** | Eight bits, eight slots. Arithmetic. |
| 2 | **Supported** | By the stated convention, bit 7 first. |
| 3 | **Not addressed by any source here** | No source in this project documents sound capability for the Apple-1. This is not "no," it is "nothing here says." |
| 4 | **Not addressed by any source here** | Same. The Replica 1 Plus manual sections available to this library do not cover sound. |
| 5 | **Supported** | Demonstrated in Part C and by the handover test. |

Items 3 and 4 are the ones to be careful about. **"Not addressed" is not the same
as "no."** A learner who writes "unsupported, so the machine cannot make sound"
has converted an absence of evidence into a negative claim, which is the S04 error
in its less common direction.

If someone wants to know whether these machines can produce sound, the answer is:
look it up in a source, because this library does not know.

## Part G: design a better encoding

No single answer. Acceptance criteria:

- Total size stated in bytes, with the arithmetic shown.
- Bit-order or slot-order convention stated explicitly, since Part D showed what
  happens when it is not.
- **At least one thing it still discards is named.** This is the deliverable. An
  answer claiming to discard nothing has not been examined.

A worked example:

> Sixteen slots. Two bytes for on/off, two bytes for sustain, one byte for
> tempo. Five bytes total. Slot 1 is bit 7 of the first byte; slots run left to
> right through both bytes.
>
> **Still discards:** loudness, what instrument, how many repeats, any timing
> that is not an exact multiple of the slot, and anything about pitch. Pitch is
> the big one: this encodes rhythm, and a tune needs notes.

That last observation is the best available answer to the whole lesson. Even a
five-byte encoding is a rhythm encoding, and a tune is a different problem.

## Try a variation: sixteen slots

Two bytes. **The order must be stated**, because there is no way to infer whether
the first byte is slots 1 to 8 or the low half of a sixteen-bit value read some
other way. Hand it over and the recipient will pick a convention, and it may not
be yours.

The lesson repeats: an encoding needs its conventions written down beside it, or
it is not an encoding, it is a private note.

## README: Check your understanding

1. **`$C0` is `1100 0000`, so slots 1 and 2**, two events at the start and then
   six empty slots.
2. **Any three of:** tempo, loudness, note length, what sound, number of repeats,
   accent.
3. **Because note length is a per-slot property.** One extra bit per slot, across
   eight slots, is one extra byte, which doubles an encoding that was one byte.
   Per-slot properties multiply with the length; per-pattern properties do not.
