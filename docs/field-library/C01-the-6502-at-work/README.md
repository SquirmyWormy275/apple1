# C01 The 6502 at work

**Audience:** LEARN
**Time:** 30 minutes
**Status:** OFF-DEVICE
**Prerequisites:** S02, S03

## You will learn

By the end, you can say what the CPU does, describe the three-step loop it never
leaves, and read a real instruction out loud in plain English.

## Why this matters

People describe a CPU as the "brain," which suggests it decides things. It does
not. It repeats one loop forever: fetch a byte, work out which action that byte
names, do it. Everything a computer has ever done is that loop running fast.

Once you see the loop, machine code stops being cryptic. It is a list of actions
in the order they will be taken.

## First result

Three real instructions, read aloud in English.

## What you need

Paper. `assets/fetch-decide-act.txt`. Nothing powered on.

## Activity

1. Read `assets/fetch-decide-act.txt` once.
2. Read these three lines out loud, using the pattern "verb, what, where":

   - `LDA #$00` becomes "load the accumulator with the number zero."
   - `LDA $D011` becomes "load the accumulator with whatever is at address
     `$D011`."
   - `STA $0400` becomes "store the accumulator into address `$0400`."

3. Cover them. Say each one again from the mnemonic alone. That is your first
   result.

## Explain what happened

**What the CPU is.** The Apple-1 uses a MOS 6502, a *microprocessor*: one chip
that reads instructions and carries them out. It has almost no memory of its
own. What it has is a handful of *registers*, tiny named storage locations
inside the chip, each holding one byte.

Three registers matter for now:

- **A**, the *accumulator*. The main working register. Most arithmetic and most
  data movement passes through it.
- **X** and **Y**, the *index registers*. Mostly used for counting and for
  stepping through a list of memory locations one at a time.

There is also the **program counter**, which is not a byte but an address: it
holds the location of the next instruction. It is the CPU's place in the book.

**The loop.** Fetch, decide, act.

*Fetch:* read the byte at the address in the program counter.

*Decide:* that byte is an *opcode*, a number that names one specific action.
`$AD` names one action, `$A0` names another. Some actions need extra bytes after
the opcode, called the *operand*, saying what to act on.

*Act:* carry it out, then move the program counter past everything just used, so
it points at the next opcode.

That is all. There is no step where the CPU considers alternatives.

**Reading an instruction.** Humans write opcodes as three-letter *mnemonics*.
`LDA` is Load Accumulator. `STA` is Store Accumulator. `LDY` is Load Y. The
letters are an abbreviation of an English sentence, and reading them back as
that sentence is most of what "knowing assembly" means at this stage.

The character after the mnemonic changes the meaning completely:

- `LDA #$00` has a `#`. The `#` means *immediate*: the value itself. Load the
  number zero.
- `LDA $D011` has no `#`. It means *absolute*: an address. Go to `$D011` and load
  whatever is sitting there.

That single character is the difference between the number 53 and the contents
of house number 53. Getting it wrong is the most common beginner error in 6502,
and it is worth over-learning now.

**Why so few instructions do so much.** The 6502 has no instruction for "print a
message" or "read a line." It has load, store, add, compare, jump, and a few
dozen more. Everything else is built by arranging those. A program that reads a
line of typed text is roughly: check a flag, load a byte, store it, repeat.

## Try a variation

`LDY #$00` appears as the first instruction of both RAM-only programs in this
repository. Say what it does in English, then say why a program that is about to
step through a list of memory locations would start that way.

## Check your understanding

1. What is the difference between `LDA #$41` and `LDA $41`?
2. The program counter holds an address, not a byte. Why does that distinction
   matter?
3. A CPU has no instruction meaning "stop." What does a halted machine actually
   do?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

Instruction names and meanings come from Owad's instruction reference; the
worked instructions are taken from the repository's own RAM-only byte lists.
Citations in `SOURCE-NOTES.md`.

What this lesson does **not** establish: it describes the 6502 instruction set,
not the state of this project's machine. Nothing was executed on hardware. It
authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
