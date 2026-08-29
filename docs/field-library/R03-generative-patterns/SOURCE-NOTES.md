# R03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Display material is 40 columns of upper-case printable ASCII | E-WIDTH |
| Unsupported characters become a visible `?` | E-SUBST |
| The 6502 instruction set contains add, subtract, compare, and shift instructions | OWAD Appendix D pp. 249 to 255 |
| The 6502 has **no** divide instruction | OWAD Appendix D, "Instructions by Category", which lists no division operation in any category |

## The patterns were generated, not drawn

Every pattern in `assets/pattern-rules.txt` was produced during authoring by
applying the stated rule mechanically, not by drawing. Specifically:

- **Rule one**, `#` where the number divides by 3, over 36 columns.
- **Rule two**, `#` where the column divides by the row number, rows 1 to 8 over
  32 columns.
- **Rule three**, Pascal's triangle over 16 rows with odd values marked `#` and
  even values left blank.

This matters for the lesson's credibility: the claim "nobody drew that shape" is
true of the asset itself, not just of the idea.

The asset was checked against `tools/apple1_text.format_for_apple1` during
authoring and passes unchanged: upper case, printable ASCII, no line over 40
columns, no substitutions.

## The no-divide claim

The statement that the 6502 has no divide instruction is an argument from absence:
OWAD's instruction reference organizes the whole instruction set by category and
lists none. That is reasonably strong evidence for a complete reference, but it is
absence rather than a positive statement.

Recorded as **V-26**: the "no divide instruction" claim rests on its absence from
OWAD's instruction categories, not on a source stating it. A reviewer can confirm
against any 6502 reference.

The related claim that division must be built from repeated subtraction or
shifting is standard practice and is not cited.

## Pascal's triangle and Sierpinski

Neither is Apple-1 material and neither is cited. Both are general mathematics,
long predating the machine. The lesson names the nested triangle as "sometimes
called a Sierpinski triangle" rather than asserting the attribution as a fact
about the pattern's origin.

## Deliberate simplifications

1. **"Divides exactly" is used rather than "modulo,"** to keep S03 as the only
   prerequisite arithmetic.
2. **No program is supplied**, even for the optional extension. The learner
   writes their own, in any language, on an ordinary computer.
3. **No claim is made about generating these on the Apple-1.** Part F discusses
   what would be cheap in principle; nothing states that any of it has been done
   or would work.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-26 (new).** The absence of a 6502 divide instruction is inferred from
  OWAD's instruction categories rather than positively stated.
- **V-7 and V-24 apply** as in R01 for the character canvas.
- **V-8 applies.** Nothing here has been generated on or displayed by this
  machine.

## What this lesson does not establish

No pattern here has been produced on or displayed by this project's board, and no
timing claim is made. It authorizes no firmware load, EEPROM write, CFFA1 write,
serial-port open, or physical modification, and the optional extension explicitly
directs the learner to an ordinary computer.
