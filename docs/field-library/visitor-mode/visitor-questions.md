# Visitor questions

What people actually ask, with answers short enough to say out loud.

Three rules for this sheet. Answers are what you'd *say*, not what you'd write.
Where the honest answer is "I don't know," it says so, because "I don't know" is
a complete answer and visitors respect it more than a guess. And nothing here
claims the machine works, because that isn't established.

---

## About the object

**"Is that a real Apple-1?"**

> "No, and thank you for asking directly. It's a Replica 1 Plus, a modern
> reproduction of the 1976 design. There were only about two hundred originals."

*The most important question on this sheet. Never soften it.*

**"So it's a fake?"**

> "No, a replica's an honest thing. It says what it is on the box and in the
> manual. A fake is a copy pretending to be an original, and nobody's pretending
> here."

**"What's it worth?"**

> "I genuinely don't know, and I'm not the person to ask. Originals and replicas
> are completely different markets. I'd steer well clear of guessing at a number
> while standing next to the thing."

*Never estimate. Not even a range, not even hedged.*

**"How much was the original?"**

> "$666.66, and that bought you the bare board. No case, no keyboard, no power
> supply, no screen. You found those yourself."

**"Why that price?"**

> "Wozniak liked repeating digits. The wholesale price to the shop was $500 and
> he picked the retail number because he thought it was funny."

**"How many are left?"**

> "I don't know. About two hundred were made and I've no reliable figure for
> survivors. Worth being careful with those numbers generally, because 'made',
> 'sold' and 'bought by one particular shop' are three different counts and they
> get mashed together a lot."

**"Did Steve Jobs build this one?"**

> "No. This one's modern. On the originals, Jobs was the one who wanted to sell
> them; Wozniak did the design."

---

## About how it works

**"How much memory does it have?"**

> "The original had 8 kilobytes, split in two halves. For scale, that's less than
> a single one of the photos on your phone, by a very long way."

**"Can it go on the internet?"**

> "No. There's nothing in it that could. It predates all of that by about two
> decades."

**"What can it actually do?"**

> "Let you type things in, store them, print them back, and run small programs
> you write yourself. There's a BASIC in this one and a little assembler. It's
> not going to do your taxes."

**"Is 256 bytes really the whole operating system?"**

> "The monitor program is, yes. It does three things: show you what's at a
> memory location, change it, and start running at it. That's the entire
> toolkit. Everything else you build on top."

**"What's a byte?"**

> "Eight switches, on or off. That gives you 256 combinations, so a byte holds a
> number from 0 to 255. That's it. Everything else is a lot of those."

**"Why hexadecimal? Why not normal numbers?"**

> "Because two hex digits describe exactly one byte, every time, with nothing
> left over. In ordinary decimal a byte's sometimes two digits and sometimes
> three, and then you can't tell where one ends."

---

## About switching it on

**"Can you turn it on?"**

> "Not today. There's a fault we're partway through diagnosing, and the rule
> we're working to is that nothing gets powered or connected outside a planned
> session with someone recording what happens."

*Do not soften this into "maybe later" if you know the answer is no.*

**"Can I type on it?"**

> "Afraid not, same reason. Happy to show you what typing on it would look like
> on paper, though, and honestly the paper version is easier to see."

**"What's wrong with it?"**

> "We don't know yet, and that's the honest answer. What we know is that opening
> the serial port from the host computer made the display garble. That's the
> whole fact. Everything past that is a guess and we're trying not to guess."

**"Have you tried turning it off and on again?"**

> "Ha. Sort of the opposite problem, actually. The temptation is to keep trying
> things, and every extra thing you try makes it harder to work out which one
> mattered. So we stopped and wrote it down instead."

**"Why not just try it and see?"**

> "Because 'try it and see' costs you the clean observation. Right now we've got
> one thing that happened, recorded properly. If we'd poked it six more times
> we'd have six symptoms and no idea of the order."

---

## About the work

**"Are you fixing it?"**

> "Slowly, and mostly by writing things down rather than by doing things. Most
> of the effort goes into not destroying the evidence."

**"Isn't that a bit obsessive?"**

> "Probably. But it's an object with a history, and once you've changed something
> without recording it, that information is gone permanently. Cheap to write it
> down, expensive not to."

**"What's that firmware source you mentioned? Doesn't that tell you what's on it?"**

> "It tells us what somebody wrote. It doesn't tell us it was compiled, or that
> the result was installed, or that it's still there. Three separate gaps, and
> having the file doesn't close any of them."

**"Do you know what's on the chip?"**

> "No. That's genuinely open. We'd need to read it back and compare, and there's
> no approved way to do that here yet."

---

## About learning it

**"Could I learn this?"**

> "Yes, and faster than you'd think. There's a written set that starts from
> absolutely nothing, no maths, no background. The first one's about telling
> three things apart that all get called 'an Apple-1'."

**"Is it hard?"**

> "It's small, which is different from easy but helps a lot. You can hold the
> whole machine in your head, and you can't do that with anything modern."

**"Where would I start?"**

> "S01. It takes about ten minutes and it's paper and a pencil."

**"Do I need to be good at maths?"**

> "No. You need to be able to count and divide by sixteen. That's the whole
> prerequisite."

---

## Awkward ones

**"Can I take a photo?"**

> "Of the machine, absolutely."

*Check your own venue's rules before saying yes to anything else.*

**"My uncle had one of these."**

> "He might well have had an Apple II, they're much more common and they look
> related. Worth asking him."

*Almost always the answer, and said kindly it's a nice moment rather than a
correction.*

**"You're wrong about [detail]."**

> "You might be right, I'd rather check than argue. Where did you read it?"

*Sometimes they are right. This library has thirty-six of its own open
verification items, so a host has no standing to be defensive.*

**Anything you don't know.**

> "I don't know. Here's how you'd find out, though."

*Never guess in front of a visitor. A guess repeated by them becomes a rumour
with your name attached.*

---

## Sources

- Replica versus original, and about two hundred made: BRIEL; H-MADE, with V-2
  on the three distinct counts.
- $666.66 retail, $500 wholesale to the Byte Shop, repeating digits: H-PRICE,
  H-WHOLESALE, WOZ-FWD p. 18.
- Bare board, buyer-supplied keyboard, power supply and display: H-BARE,
  H-SUPPLY.
- 8 KB of RAM on the original, in two halves: M-RAM-ORIG.
- 256-byte monitor with three functions: WOZ-FWD p. 17; R-MON-3.
- Two hex digits per byte: A-HEX.
- FT232R open producing a display-garbling STOP, and the stop rule: E-FT232-STOP,
  E-STOP.
- Vendor source as candidate evidence rather than the installed image:
  E-110REV03.
- Replica ROM contents: R-ROM-SPLIT, R-KRUSADER.

## What this sheet does not establish

No answer on it claims the machine powers on, displays, reads a key, or moves a
byte over serial. Several answers say plainly that those are unknown, which is
the accurate position. No claim about value, rarity, or authenticity. Nothing
here authorizes a firmware load, EEPROM write, CFFA1 write, serial-port open, or
physical modification.
