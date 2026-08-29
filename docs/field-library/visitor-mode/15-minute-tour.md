# Fifteen-minute tour

For someone who sat down, or a small group. They do something with their hands,
and they leave with a habit rather than a fact.

Three sections of roughly five minutes. Stop after any of them if attention
goes.

---

# Part one: the object (0:00 to 5:00)

## 0:00 The hook

> "Everything that machine knows how to do when you switch it on is 256 bytes of
> software. I can print it on one sheet of paper."

## 0:30 What it is

> "Replica 1 Plus. It's a modern reproduction of the Apple-1, which Steve
> Wozniak designed in 1976. About two hundred originals were made and this isn't
> one of them, it was built decades later to the same design."

> "I'm careful about that wording, and it's worth saying why. An original and a
> replica are different objects with different histories. Nobody's being fooled
> here, but people do get fooled, and the fix is just to say the true thing out
> loud every time."

## 1:30 What $666.66 bought

> "In 1976 that price got you the board. Not a computer. A board. You supplied
> the keyboard, the power supply and the screen yourself, and then you had a
> computer."

> "Which sounds primitive until you hear what it replaced. The machine everyone
> knew at the time, the Altair, you programmed by flipping switches. One bit at a
> time. Then you read the answer off a row of lights."

## 3:00 The actual leap

> "So the new thing here wasn't the computer. It was that you typed on it. A
> keyboard went in, a screen came out, and that was the normal way to use it.
> That's the whole innovation and it doesn't sound like one until you've tried
> the switches."

> "Wozniak didn't design this from scratch either, which I like. He'd already
> built a terminal, a keyboard and a display for talking to a big machine
> somewhere else. He bolted a processor and some memory onto the thing he
> already had."

## 4:30 The community bit

> "By 1977 there was an owners' club. About thirty people, swapping programs by
> post, working out how to add more memory. Apple actually sent its own
> customers to them for support."

> "Thirty people. That's a village hall. And their newsletter is a historical
> source now, because somebody kept it."

---

# Part two: how it thinks (5:00 to 10:00)

## 5:00 Hand out the byte strips

Give each person a bit strip and a pencil.

> "Eight boxes. Each one's worth what's written under it: 128, 64, 32, 16, 8, 4,
> 2, 1. Put a 1 in a box to switch that value on, then add up the ones you
> switched on. Make me 65."

Wait. Let them get it wrong once; the correction is the learning.

> "64 and 1. Everything else off. That's `0100 0001`, and that is exactly how the
> number 65 sits in that machine's memory."

## 7:00 Turn it into a letter

> "Now. 65 is also the letter A. Not sort of, and not by a convention I'm
> hand-waving at. A standards committee wrote down that 65 means A, and every
> machine since has agreed."

> "So make me 66."

They will flip one box.

> "And that's B. Which means adding one to a letter gives you the next letter.
> That one fact is doing a *lot* of work inside every program you've ever used."

## 8:30 The idea worth keeping

> "Here's the part I'd actually like you to leave with. That byte you built.
> Is it the number 65? Is it the letter A? Or is it an instruction telling the
> processor to do something?"

Let the pause sit.

> "It's whichever one the program treats it as. Memory doesn't record what kind
> of thing it's holding. It's just 65. And that's not a design flaw, it's the
> design, and it's why a program that jumps to the wrong address doesn't politely
> fail, it starts executing your holiday photos."

---

# Part three: how we work on it (10:00 to 15:00)

## 10:00 The honest status

> "You'll notice I haven't switched it on. There's a fault on the serial port and
> we don't know what it is yet."

> "What happened was: somebody opened the port from the host computer, and the
> display garbled. So they wrote down exactly that, and stopped."

## 11:00 Why stopping is the interesting part

> "The instinct is to try it again. Different cable, different settings, see if
> it happens twice. And if you do that, you've now got four things that might
> have caused it and no clean record of the first one."

> "So the rule here is: display changes, or it resets by itself, or something's
> identity drifts, or bytes don't match, you write STOP, you get it back to a
> known state, and you don't start another test."

> "A stop is a result. It's not a failure to get a result."

## 12:30 The habit

> "The other half of it is writing down what you expect *before* you look. Two
> columns: what I expected, what happened. And you fill the left one in first,
> always."

> "Because if you look first, your memory of what you expected quietly rearranges
> itself to be closer to what you saw. That's not you being dishonest, that's
> just how memory works, and writing it down first is the only defence."

## 13:30 The bit that isn't about computers

> "That habit transfers. 'The display garbled when I opened the port' is a fact.
> 'The serial path is broken' is a guess. They're both reasonable sentences but
> only one of them is still going to be true in five years."

> "Watch for the word *so* in the middle of a sentence. That's usually where the
> observation ends and the guessing starts."

## 14:30 Close

> "There's a written library that goes from this to reading actual machine code,
> forty lessons of it, and the first one assumes nothing. Happy to point you at
> it."

---

## The boundary

Say it once, early, as you hand out the strips:

> "Paper's all yours. The board and the cables I'd ask you not to touch. We're
> mid-diagnosis and anything that moves has to get written down."

With a group, watch hands during Part three, when people relax and drift.

## Off-device fallback

**The entire fifteen minutes runs with no powered hardware.** Bit strips, byte
cards, and talking. The machine is scenery.

If it is absent, Part one becomes a photograph and Parts two and three are
unchanged.

## Materials

Print at 40 columns.

Bit strip, one per person:

```text
+---+---+---+---+---+---+---+---+
|128| 64| 32| 16|  8|  4|  2|  1|
+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |
+---+---+---+---+---+---+---+---+
```

Byte card, front and back:

```text
FRONT:  C8  C9  A0  D4  C8  C5  D2  C5

BACK:   TAKE 128 OFF EACH, LOOK IT UP
        H  I     T  H  E  R  E
```

## Sources

- 256-byte monitor; Wozniak combining an existing terminal with a processor and
  memory: WOZ-FWD p. 17.
- $666.66, bare board, buyer-supplied peripherals: H-PRICE, H-BARE, H-SUPPLY.
- About two hundred made: H-MADE; see V-2 on the three distinct counts.
- Keyboard and display as standard I/O; the Altair's lights and switches:
  H-KBD-STD, H-ALTAIR.
- Owners Club founded 1977, roughly thirty members, Apple directing customers to
  it: H-CLUB.
- ASCII assigning 65 to A, as a published standard: A-CHART, A-ASCII. The script
  deliberately gives no date for the standard, because the only date in this
  project's sources is Owad's reference to the 1968 specification revision
  (A-ASCII-1968), which is not the same as the original agreement.
- FT232R open producing a display-garbling STOP; the stop rule: E-FT232-STOP,
  E-STOP.
- Replica 1 Plus as a modern product: BRIEL.

## What this tour does not establish

No claim that the machine works. The serial account is a recorded past
observation, not a procedure. No claim about value, rarity, or authenticity. No
firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification is authorized or described.
