# B04 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Almost nothing here is an Apple-1 claim

Bubble sort, selection sort, comparison counting, and the growth argument are
general computing science. They are not attributable to any source in this
project's collection and are not cited.

All comparison and swap counts in `ANSWERS.md` were derived by working the
procedure through by hand. They are arithmetic, and a reader can check any of
them with five cards in under a minute. Part A's pass-by-pass walk-through is
included in the answer key precisely so the counts can be verified rather than
taken on trust.

## The one Apple-1-adjacent claim

The README states that sorting a hundred items with this rule would be
"around ten thousand comparisons, each of which is several instructions," and
that this would be "a visible wait" on a machine of this era.

**The comparison count is arithmetic** (9,900, from Part C). **The "several
instructions" estimate is reasoning**, based on a comparison requiring at minimum
a load, a compare, and a branch. **The "visible wait" claim is qualitative and
uncited.**

This library makes no timing claims about any machine, and this one deliberately
stops short of a number. It says a wait would be visible, not how long. Recorded
as **V-22**: the visible-wait claim is qualitative reasoning, not a measurement,
and no source in this project supports a timing figure. If a future editor wants
to state a duration, it needs a source.

The `$0400` buffer address in Part G is this repository's (E-RAMONLY), used only
as a familiar location for a sketch. No program is written.

## Deliberate simplifications

1. **No asymptotic notation.** The curriculum brief for B04 asks for efficiency
   introduced intuitively rather than with notation, and "roughly quadruples when
   the list doubles" is the intuitive form.
2. **"Growth class" is used informally** in the Part F answer without defining
   it.
3. **Only two sorting rules appear.** Faster algorithms exist and are not
   mentioned, because the lesson's point is the contrast between constant-factor
   improvement and scaling, which two rules are enough to make.
4. **Stability, memory use, and worst-case analysis** are not covered.

## Claims needing verification

- **V-22 (new).** The "visible wait" claim is qualitative reasoning. No timing
  figure is given anywhere and none should be added without a source.
- **V-8 applies trivially.** No claim in this lesson concerns this board.

## What this lesson does not establish

No sorting program was written or run, on hardware or off. Part G explicitly asks
for English rather than bytes. This packet authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification.
