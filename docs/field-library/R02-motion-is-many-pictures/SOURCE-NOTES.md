# R02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Once a character is sent to the display it cannot be modified; it leaves by scrolling off the top or by clearing the whole display | P-VIDEO-WRITEONLY |
| The video section is text only, storing character codes rather than pixels | P-VIDEO-TEXT |
| Display material is 40 columns of upper-case printable ASCII | E-WIDTH |

## Everything else is general

Frames, state, position and direction, loop seams: none of these are
Apple-1-specific and none are cited. They are general animation and programming
ideas, worked here on a character grid because that is this library's canvas.

The 20-column field on the frame sheet is a working choice, narrower than 40 so
that the sheet fits three frames legibly. No display dimension is implied.

## No timing claim is made anywhere

This is the constraint the R02 brief exists to enforce, and it is worth recording
precisely what was done.

**No file in this packet states a frame rate, a character-output speed, a
duration, or a smoothness claim for any machine.** The README says timing matters
and then says explicitly that this library makes no claim about it and that
nobody in this project has measured it. Part F makes two timing claims and marks
both unsupported, one of them with an invented-sounding number specifically so a
learner practises rejecting it.

If a future editor wants to state a timing figure, it needs a measurement and a
source. There is currently neither.

## The in-place erasure point

Part F item 3 is marked **contradicted** rather than merely unsupported, and that
is a stronger claim, so it is worth showing the basis. OWAD ch. 7 p. 234 states
that once a character is sent to the display it cannot be modified, and that it
remains until it scrolls off the top or the display is manually cleared
(P-VIDEO-WRITEONLY).

That describes the **original Apple-1's** video section. **V-4 applies**: later
replicas use different video hardware, and OWAD's own sidebar records that the
Replica I TE moved video and keyboard handling to a Parallax Propeller
(P-PROPELLER). Whether the same write-once constraint holds on a Propeller-based
board is **not established by any source in this project**.

The lesson's wording is careful about this: it says "on this machine" in the
learner text, which is looser than the sources support. Recorded as **V-25**: the
write-once display constraint is documented for the original Apple-1. Its
applicability to the Replica 1 Plus is unverified, and a reviewer should either
confirm it or soften the lesson's phrasing to "the documented Apple-1 design."

## Deliberate simplifications

1. **Scrolling is mentioned but not described.** How it is triggered and what it
   costs are not covered by any source here.
2. **Nothing is said about how a frame would be produced in practice** on this
   machine, because doing so would require the timing and display behavior the
   packet declines to claim.
3. **Speed as state** appears in Part D but acceleration does not.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-25 (new).** The write-once display constraint is sourced for the original
  Apple-1; its applicability to the Replica 1 Plus is unverified, and the learner
  text's phrasing is looser than the source supports.
- **V-4 applies** for the same reason.
- **V-7 and V-24 apply** as in R01 for the character canvas.
- **V-8 applies.** No animation here has been displayed anywhere.

## What this lesson does not establish

No timing behavior of any machine. No animation has been displayed. It authorizes
no firmware load, EEPROM write, CFFA1 write, serial-port open, or physical
modification.
