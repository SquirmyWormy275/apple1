# Worksheet 3: what you saw and what you concluded

**Time:** 30 minutes core, 50 with the extension
**You need:** this sheet, a pencil. Worksheets 1 and 2 help.
**Status:** OFF-DEVICE. Nothing is powered on, connected, or run on any Apple-1.

## What you'll be able to do afterwards

- Write down what you expect *before* you look, and say why that order matters.
- State one hypothesis that could be shown false.
- Decide whether an observation means keep going or stop.

---

## Part A: the two columns

This is the whole method. Two columns, and you fill the left one in first,
always.

```text
WHAT I EXPECTED   |  WHAT HAPPENED
------------------+------------------
                  |
                  |
                  |
------------------+------------------
```

**Why first?** Because once you have seen a result, your memory of what you
expected quietly shuffles closer to it. That is not dishonesty, it is how memory
works, and writing it down first is the only defence.

---

## Part B: a program that is wrong

This is meant to store the letter `A` at `$0400` through `$0404`. Five copies.

```text
0300  A0 00     LDY #$00
0302  A9 41     LDA #$41
0304  99 00 04  STA $0400,Y
0307  C8        INY
0308  C0 06     CPY #$06
030A  D0 F8     BNE $0304
030C  4C 1F FF  JMP $FF1F
```

You need two rules:

- `CPY #n` compares Y with n, and sets the "equal" flag if they match.
- `BNE addr` goes to addr **if they did not match**. Otherwise it carries on.

**Trace it before you look for anything wrong.** Fill every row.

| Pass | Y before | Stored at | Y after |
|---:|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

How many stores happened? ______

Highest address written? ______

Was that what it was meant to do? ______

---

## Part C: say the difference out loud

| | |
|---|---|
| What it was supposed to do | |
| What it actually does | |
| The difference, in one sentence | |

---

## Part D: one hypothesis

A usable hypothesis names a cause and predicts something specific you could go
and check. "Something's wrong with the loop" is not one.

> I think the cause is _______________________________________________
>
> If I'm right, then changing _______________________________________
>
> should produce ____________________________________________________
>
> and nothing else should change.

Now find it. **Which single byte is wrong, at which address, and what should it
be?**

_______________________________________________

---

## Part E: why this kind is dangerous

Tick every symptom this program shows.

- [ ] It crashes
- [ ] It fails to return to the Monitor
- [ ] It writes to an obviously wrong address
- [ ] It produces no output
- [ ] It takes noticeably longer
- [ ] It does one thing more than it was meant to

**How many of the first five would a quick test catch?** ______

So how would anyone ever find this?

_______________________________________________

---

## Part F: change one thing

For each, say how many things changed and whether you could interpret the
result.

| What was done | Things changed | Can you interpret it? |
|---|---|---|
| Ran the same thing again | | |
| Fixed one byte, ran it again | | |
| Fixed one byte, changed the input, used a different computer | | |

---

## Part G: keep going, or stop?

Some observations are a puzzle to follow up. Others mean end the session.

The rule this project works to: **if the display changes unexpectedly, or the
machine resets by itself, or something's identity drifts, or bytes don't match,
write STOP, get back to a known state, and don't start another test.**

Mark each **continue** or **STOP**.

| Observation | Continue or STOP |
|---|---|
| A paper trace gives an unexpected number | |
| The machine's display garbles during a test | |
| A byte list you copied doesn't match the original | |
| The machine resets by itself | |
| Your prediction was wrong, but it behaved the same way twice | |

**What separates the two groups?**

_______________________________________________

---

## Part H: a real one

Earlier in this project, someone opened the serial port from the host computer
and the display garbled. They wrote that down and stopped.

1. What is the observation, stated as narrowly as you can?

   _______________________________________________

2. Name two things somebody might have done next that would have destroyed the
   evidence.

   _______________________________________________

3. Why is that record still useful now?

   _______________________________________________

*This is history, not a procedure. Nobody is repeating it.*

---

## Part I: the word "so"

Split each sentence into what was done, what was seen, and what it was taken to
mean. Then say which parts will still be true in five years.

1. "Opened the port and the display garbled, **so** the serial path is broken."
2. "Pressed reset and got a backslash, **so** the ROM is the original one."

Notice where the word **so** sits in both.

---

## Extension, optional, needs a computer

Not required, and worth no more than the paper work.

On an ordinary computer with this repository and Python, run both versions of
the Part B program in the emulator described in `docs/emulator-demo-guide.md`.
Predict both results first, then compare.

**Do not attempt this on the Replica 1 Plus.** This worksheet grants no
authority to run anything on it.

---

## Off-device alternative

**The whole worksheet is the off-device version.** Part B is a paper trace and
needs no computer at all. Only the extension uses one, it is marked optional,
and skipping it costs nothing.

---

## Sources and boundaries

Instruction meanings: OWAD Appendix D. `$41` as `A`: A-CHART. `$FF1F` as the
Monitor warm entry: W-FF1F. The STOP rule: E-STOP, from
`docs/preservation-dossier.md`. The serial incident in Part H: E-FT232-STOP,
summarised from that dossier's "Current boundaries"; the primary record with its
date and operator lives in the project's evidence ledger, which is verification
item V-13. Keys resolve in `../SOURCES.md`.

**The program in Part B is a teaching artifact** written for this library. It is
not in `software/ram-only/`, has not been through that library's acceptance
process, and carries **no hardware authority**.

**This worksheet authorizes nothing.** No firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification. The serial incident is
recounted as a past observation and must not be reproduced.
