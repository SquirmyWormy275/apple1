# Visitor mode

Spoken scripts for showing this machine to someone who did not come looking for
it. Three lengths, plus a question sheet.

| File | Length | Use it when |
|---|---|---|
| `02-minute-tour.md` | 2 minutes | Someone paused on their way past |
| `05-minute-tour.md` | 5 minutes | They asked a question and stayed |
| `15-minute-tour.md` | 15 minutes | They sat down, or you have a small group |
| `visitor-questions.md` | As needed | Anything they ask |

## The three rules these scripts are built on

**1. Every tour works with no powered hardware.** Each script has a fallback
section, and in practice the fallback *is* the tour. The machine can sit there
being looked at. Nothing you say depends on it doing anything.

This is not caution about bad luck. In this project the machine has an
unresolved serial fault, an opened serial session is blocked pending a
measurement test card and an explicit operator start, and running any program on
it is a separate operator-led decision that a demonstration does not get to make.

**2. Name the object correctly, every time.** This is a **Replica 1 Plus**, a
modern reproduction. It is not one of the roughly two hundred 1976 boards. Every
script says so in the first thirty seconds, and saying it costs nothing: the true
version is just as interesting.

**3. Nobody touches the hardware. Including you.**

## The boundary, in the words to actually say

> "You're welcome to look as closely as you like. I'd ask you not to touch the
> board or the cables. Not because it's precious, though it is, but because
> we're partway through diagnosing a fault and anything that moves has to get
> written down."

That sentence does real work. It gives a reason, it does not scold, and it tells
the truth.

If someone reaches anyway, put yourself between them and the board and keep
talking. Do not grab their hand.

## What a host may and may not do

| | |
|---|---|
| **Fine** | Talking. Pointing. Showing paper cards. Letting people look closely. Answering "I don't know." |
| **Not during a tour** | Powering on. Pressing reset. Connecting anything. Typing on it. Opening a serial port. Moving a jumper or switch. Running any program. |

The second column is not a list of things needing extra care. It is a list of
things that do not happen on a tour, at all, under any circumstances, including
when a visitor asks nicely and especially when the tour is going well.

## What these scripts do not establish or authorize

- **No script claims the machine works.** None of them says it powers on,
  displays text, reads a keypress, or moves a byte over its serial port, because
  none of that is established.
- No script makes a claim about the value, rarity, or authenticity of any object.
- Nothing here authorizes a firmware load, EEPROM write, CFFA1 write,
  serial-port open, or physical modification.

Sources for every historical claim in these scripts are listed at the foot of
each file and key into `../SOURCES.md`.
