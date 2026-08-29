# B02 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

| Claim | Key |
|---|---|
| Integer variables are named with a letter or a letter and a digit (`A`, `N`, `A1`, `B8`) | B-VARNAMES |
| String variables are a letter plus `$` (`A$`, `R$`, `Z$`) | B-VARNAMES |
| Strings must be dimensioned; one byte per character; maximum 255 | B-DIM |
| `INPUT` automatically inserts a question mark and it cannot be turned off | B-INPUT-Q |
| The worked exchange `WHAT IS YOUR NAME?TOM` with no space before the typed answer | OWAD ch. 5 p. 130, the quoted `>RUN` transcript |
| `PRINT N$` prints the string; `PRINT "N$"` prints the literal characters | OWAD ch. 5 p. 131, the worked `DIM N$(2)` example |
| A semicolon joins items on one output line | OWAD ch. 5 p. 130, `PRINT "YOUR NAME IS "; N$` |
| Apple-1 BASIC supports integers only | B-INTEGER |
| Arithmetic expressions such as `(8+3)*4` work | B-IMMEDIATE |
| A colon places two statements on one line | B-COLON |

## The example programs are constructed, not quoted

The two programs in `ANSWERS.md` Part D were written for this lesson using the
syntax documented in OWAD chapter 5. They are **not** quoted from a source and
**have not been run**, because this repository packages no BASIC environment
(V-20, from B01).

The `WHAT IS YOUR NAME?TOM` exchange in Part E is patterned on the transcript
OWAD prints on p. 130, which shows exactly that spacing.

The double-question-mark warning in Part E follows from B-INPUT-Q by reasoning:
if the question mark is automatic and the prompt already ends in one, two appear.
This has not been observed and is stated as a consequence rather than a
transcript. Recorded as **V-21**.

## The inches conversion

`I*254/100` uses integer arithmetic deliberately, per B-INTEGER. The answer key
states that the fractional part is lost rather than presenting the expression as
exact. No claim is made about how Apple-1 BASIC orders multiplication and
division in that expression, and a learner writing `I/100*254` would get a
different and much worse answer, which is a good discussion but not a documented
fact in any source here.

## Deliberate simplifications

1. **`IF` is not taught**, only mentioned in the Try a variation answer as where
   a decision would go.
2. **The four-box diagram cannot express a fork**, which the answer key points
   out rather than hiding.
3. **Operator precedence in BASIC is not documented here** and is not relied on
   by any answer.
4. **Variable storage location is not discussed.** BASIC chooses; the lesson says
   only that.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-20 applies.** No BASIC in this library has been executed.
- **V-21 (new).** The double-question-mark consequence in Part E is reasoned from
  B-INPUT-Q, not observed in a transcript.
- **V-8 applies.** Nothing here concerns this machine.

## What this lesson does not establish

It does not establish that any program here would run, or that BASIC is present
on this project's board. It authorizes no firmware load, EEPROM write, CFFA1
write, serial-port open, or physical modification.
