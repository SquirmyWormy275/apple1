# Five-minute tour

For someone who asked a question and stayed. Two ideas instead of one, and they
handle something.

---

## 0:00 The hook

> "The entire operating system on that machine is 256 bytes. I'll show you how
> small that is in a second."

## 0:20 What it is, precisely

> "It's a Replica 1 Plus. Modern reproduction of Wozniak's 1976 Apple-1. There
> were about two hundred originals; this isn't one of them. It was built later,
> to the same design, and it even has a few things the original didn't."

If they ask what things:

> "BASIC and an assembler, built into the chip. On a real 1976 machine you had to
> load BASIC off a cassette tape every single time you switched it on. Every
> time. If the power blinked, you did it again."

That detail lands better than any specification.

## 1:00 Idea one: it was a board, not a computer

> "Here's what $666.66 bought you in 1976. A circuit board. That's all. No case,
> no keyboard, no power supply, no screen. You went and found those yourself.
> The thing you bought was the flat green part."

> "Which tells you who it was for. This wasn't a product for your dad. It was for
> someone who already knew what a circuit board was."

## 2:00 Idea two: a byte is only what you treat it as

Hand them the byte card. Let them hold it.

> "Every one of those is a number between 0 and 255. Nothing more. Now, if a
> program decides they're letters..."

Give them the decode card.

> "...take 128 off each one, look it up, and there's your message. But the exact
> same numbers, if the processor had *jumped* to them instead of reading them,
> would have been instructions. Actions. And it would have done them."

> "Memory doesn't remember what kind of thing it's holding. Only the program
> decides. That's not a quirk, that's the whole design, and it's why a program
> that goes to the wrong address does something spectacular rather than just
> failing."

## 3:30 The question back

> "So: this byte's 65, which is A. What's B?"

Then, once they answer:

> "Right. And that's why you can turn a letter into the next letter by adding
> one. It sounds trivial. It's how half of text processing works."

## 4:15 What we're actually doing with it

> "Honestly, right now, we're stuck. There's a fault on the serial port. We
> opened it once, the display garbled, and we wrote that down and stopped."

> "That sounds like a failure. It isn't really. Stopping and writing it down is
> the whole job. If we'd kept poking it we'd have four different symptoms and no
> idea which one was first."

Visitors respond well to this. It is honest, and it is a better lesson about
technical work than a working demo would be.

## 5:00 Where to go next

> "The written lessons start from zero, and there are forty of them. S01 assumes
> nothing at all."

---

## The boundary

Say it when you hand over the card, not before:

> "You can hold that, that's paper. The board I'd ask you not to touch, or the
> cables. We're mid-diagnosis and anything that moves has to get logged."

## Off-device fallback

Nothing in this tour needs the machine powered, connected, or working. The two
cards and your voice carry all five minutes.

If the machine is not present at all, the 1:00 section becomes "here's a photo of
what $666.66 bought" and nothing else changes.

## Sources

- 256-byte monitor: WOZ-FWD p. 17.
- $666.66, bare board, buyer supplied keyboard, power supply, display: H-PRICE,
  H-BARE, H-SUPPLY.
- About two hundred made: H-MADE, with V-2 on the three different counts.
- BASIC in RAM on the original, reloaded every power-up: M-BASIC-RAM.
- Replica ROM holding BASIC and an assembler: R-ROM-SPLIT, R-KRUSADER.
- The FT232R open producing a display-garbling STOP: E-FT232-STOP.
- Byte values, high-bit convention: A-CHART, P-HIGHBIT.

## What this tour does not establish

It makes no claim that the machine works. The serial account is a recorded past
observation, **not** a procedure and not something to reproduce. No claim about
value or authenticity. No hardware action authorized.
