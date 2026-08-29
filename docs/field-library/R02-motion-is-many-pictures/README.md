# R02 Motion is many pictures

**Audience:** LEARN
**Time:** 35 minutes
**Status:** OFF-DEVICE
**Prerequisites:** R01

## You will learn

By the end, you can break a movement into frames, work out the small amount of
state that describes it, and say what a program would have to decide that a
picture cannot.

## Why this matters

Animation looks like a hard problem and is not. It is a sequence of still
pictures with one thing changed between them. The genuinely hard part is
noticing what has to be *remembered* from one frame to the next, and that is a
programming skill rather than an artistic one.

## First result

Six frames of a bouncing symbol, drawn.

## What you need

Paper and a pencil. `assets/frame-sheet.txt`. Nothing powered on.

## Activity

1. Look at frames 1 to 3 on `assets/frame-sheet.txt` and work out the rule.
2. Draw frames 4, 5, and 6 following the same rule.
3. Answer the question underneath: what happens when the ball reaches the wall?
   That is your first result.

## Explain what happened

**A frame is a still picture.** Motion is what a viewer infers when frames follow
each other quickly enough. Nothing in any individual frame is moving.

**The rule is a change, not a picture.** Frames 1 to 3 are not three drawings
someone made separately. They are one drawing plus a rule: move four columns
right. Once you have the rule you can generate any number of frames without
drawing them.

That is the shift worth making. An animation is not a collection of pictures. It
is a starting picture and a rule for the next one.

**State is what has to be remembered.** To produce the next frame you need to
know where the ball is now. That is one number: the position. When the ball has
to bounce, you also need to know which way it is going, because a ball at column
12 could be heading either way, and the picture alone does not say.

**Two numbers, and the whole animation follows.** Position and direction. Every
frame is drawn from those two, and every frame updates them. This is the same
idea as the C05 state trace: a small amount of state, changed a little at a time.

**The picture cannot decide the edge case.** When the ball reaches the wall, the
frames stop telling you what happens. Does it stop? Reverse? Vanish? Carry on
past? All four are consistent with frames 1 to 5, and the animation is not
specified until somebody chooses.

This is B03's ambiguity in a different costume. The frames looked complete and
were not, and the incompleteness was invisible until you reached the boundary. It
is also A06's "biggest" test case: the interesting behavior is at the edge.

**A subtlety about reversing.** If the ball bounces at column 16, does frame 7
show it at 16 again or at 12? Showing it at 16 twice makes it appear to pause at
the wall. Showing 12 immediately makes the bounce sharp. Neither is wrong, and
you will not know which you prefer until you decide it explicitly.

**On timing, carefully.** How fast frames replace each other determines whether a
viewer sees motion or a slideshow. That is a real consideration and this lesson
treats it conceptually only.

**This library makes no claim about timing on any machine.** Nothing here states
how long a frame would take to draw on an Apple-1 or a Replica 1 Plus, how fast
the display accepts characters, or whether animation would look smooth. Those are
measurements nobody in this project has made. If you find yourself wanting a
number, that is a measurement to propose, not a fact to assume.

**One thing that does follow from the documented design.** A character on the
display cannot be modified once sent. So a frame cannot be produced by erasing
the previous ball and drawing a new one in place. Whatever an animation on this
machine would look like, it is not that, and any design assuming it is has
assumed something the design documentation contradicts.

## Try a variation

Design a two-character animation: a ball and a paddle that follows it. Say how
much state you now need, and whether it is more than twice as much.

## Check your understanding

1. What is the smallest amount of state that describes a bouncing ball?
2. Why can you not tell from a single frame which way the ball is going?
3. Why can a frame on this machine not be made by erasing the old ball?

## Answer key

See `ANSWERS.md`.

## Sources and boundaries

The write-once display behavior is cited from Owad. Citations in
`SOURCE-NOTES.md`.

What this lesson does **not** establish:

- **No timing claim is made about any machine.** Not frame rate, not character
  speed, not smoothness. None of it has been measured in this project.
- No animation here has been displayed anywhere.
- It authorizes no firmware load, EEPROM write, CFFA1 write, serial-port open, or
  physical modification.
