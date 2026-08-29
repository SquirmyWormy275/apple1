# R05 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Eight bits make a byte; bit values 128 down to 1; hex from nibbles | A-TABLE, A-HEX; C03 |
| Display material is 40 columns of upper-case printable ASCII | E-WIDTH |

## No sound capability is claimed, and here is why

This is the constraint the R05 brief exists to enforce.

**No source in this project's collection documents a sound capability for the
Apple-1 or the Replica 1 Plus.** OWAD chapter 7, "Understanding the Apple I,"
covers the processor, memory, the 6821 PIA, keyboard input, and video output, and
concludes with a summary naming those subsystems. Sound is not among them. The
Briel manual material available to this library covers setup, the Woz monitor,
BASIC, Krusader, and the ROM layout, and does not address sound.

**That is an absence of material, not a documented absence of capability.** The
lesson and its answer key are careful to say "not addressed by any source here"
rather than "the machine cannot make sound," and Part F trains the learner to
make exactly that distinction. Converting silence in the sources into a negative
claim would be the S04 error running backwards.

Recorded as **V-27**: whether either machine has any sound capability is unknown
to this library. Nothing in this packet should be edited to assert either answer
without a source.

## No sound artifact exists

The curriculum brief for R05 asks that the lesson stay conceptual "unless a
verified, compatible sound artifact is added later." **None has been.** There is
no sound file, no byte list intended to produce sound, and no measurement
anywhere in this repository.

The rhythms in this packet are clapped by the learner. Nothing is played by any
machine.

If a verified artifact is ever added, this lesson would need: a source for the
capability, an exact file, an expected result, a status label, and a stop
condition, exactly as M03 has for the emulator. It has none of those now because
it needs none.

## The encoding is general

Slot-based rhythm encoding, the per-slot versus per-pattern cost argument, and the
bit-order ambiguity are general ideas, not Apple-1 material, and are not cited.
The bit-order point is a real property of any packed encoding and is demonstrated
by the Part D exercise rather than asserted.

## Deliberate simplifications

1. **Pitch is not encoded at all**, which the Part G answer names as the largest
   omission.
2. **Only equal-length slots are considered.** Rhythms that do not divide evenly
   are outside the scheme.
3. **No audio physics.** Frequency, waveform, and envelope are not mentioned.

## Claims needing verification

- **V-27 (new).** Whether the Apple-1 or the Replica 1 Plus has any sound
  capability is not established by any source in this project, in either
  direction.
- **V-7 applies** for the character canvas.
- **V-8 applies.** Nothing here concerns this board's state.

## What this lesson does not establish

It makes no claim about sound on any machine. Nothing has been played. It
authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
