# R02 Answer key

## Part A and Part B: the rule

| Frame | Ball column |
|---:|---:|
| 1 | 1 |
| 2 | 5 |
| 3 | 9 |
| 4 | 13 |
| 5 | 17 |
| 6 | 20, or 21 if the rule is applied blindly |

**The rule: move four columns to the right each frame.**

Frame 6 is the interesting one and is meant to be. Four more than 17 is 21, which
is outside a 20-column field. A learner who drew the ball at column 20 has
already made a decision about the wall without noticing; a learner who noticed
the problem has found the point of the exercise.

## Part C: the four endings

| Choice | Frames 7, 8, 9 | When it is right |
|---|---|---|
| Stops | Ball stays at the wall in all three | A progress bar reaching completion |
| Reverses | 17, 13, 9 | A ball in a game; anything oscillating |
| Vanishes | Empty field | Something leaving the scene, a projectile |
| Goes past the edge | Nothing visible, but the position keeps increasing | A scrolling world where the view is a window on something larger |

All four are legitimate designs. The mistake is not choosing one; it is not
noticing there was a choice.

## Part D: how much state

| Animation | State |
|---|---|
| Moving right, never bouncing | Position. One number. |
| Bouncing between two walls | Position and direction. Two. |
| Bouncing, changing speed | Position, direction, and speed. Three. |
| Two balls bouncing independently | Two positions and two directions. Four, and note it is exactly double. |
| Ball and a paddle that follows | Ball position, ball direction, paddle position. Three. |

The last row is the interesting one and is the Try a variation answer: **it is
less than double**, because the paddle's direction is derived from the ball's
position rather than remembered separately. When one thing follows another, you
store the leader and compute the follower.

## Part E: the double frame

1. Option A shows the ball at 17 twice; option B shows 17 then 13.
2. **Option A looks like a pause.** The ball appears to rest against the wall for
   a moment.
3. **Option B looks sharper.** The reversal is instant.
4. **Neither is wrong.** A ball hitting a hard wall might look better sharp; a
   ball hitting something soft might look better with the pause. It is a design
   decision, and it only becomes a bug if it happens by accident.

## Part F: what you cannot claim

| # | Verdict | Why |
|---|---|---|
| 1 | **Supported** | It is the definition the lesson works from. |
| 2 | **Unsupported** | Nothing in this project has measured display speed, and no source states one. |
| 3 | **Contradicted** | Owad's description is explicit: once a character is sent to the display it cannot be modified. It leaves by scrolling off or by clearing the whole display. |
| 4 | **Supported** | Derived in Part D and confirmed by the frames. |
| 5 | **Unsupported** | A specific timing figure, and no measurement exists anywhere in this project. |

Items 2 and 5 are the same failure at different confidence levels, and 5 is worse
because a number sounds like it came from somewhere.

Item 3 is worth dwelling on: it is not merely unsupported, it is contradicted by
the documented design. An animation design that assumes in-place erasure has
assumed something the documentation says is not available.

## Part G: a six-frame loop

A loop is invisible when frame 6 leads into frame 1 by the same rule that governs
every other transition. If the rule is "move four right, wrap at the edge," then
positions 1, 5, 9, 13, 17, 21-wrapping-to-1 form a cycle with no special case,
and no join is visible because there is no join.

**What makes the join invisible: the wrap is not an exception.** If instead you
draw five frames of motion and then jump back to the start, the sixth transition
behaves differently from the other five and the eye catches it.

The general rule: a loop looks seamless when the transition from last to first is
produced by the same rule as every other transition.

## Try a variation: ball and paddle

**Three numbers, not four.** Ball position, ball direction, paddle position. It
is less than twice the single-ball state, because the paddle "follows," which
means its position is computed from the ball's rather than remembered
independently.

If the paddle moved on its own, you would need its direction too, and then it
would be four. Following is what saves the number.

## README: Check your understanding

1. **Two numbers: position and direction.**
2. **Because a still picture records where something is, not where it is going.**
   A ball at column 12 looks identical whether it is heading left or right.
   Direction has to be remembered; it cannot be recovered from the frame.
3. **Because a character on the display cannot be modified once sent.** It stays
   until it scrolls off the top or the whole display is cleared. There is no
   erasing in place, so a frame cannot be made by removing the previous ball.
