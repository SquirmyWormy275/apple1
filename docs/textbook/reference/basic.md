# Run real Apple-1 Integer BASIC

The course now executes the preserved Apple-1 interpreter on a modeled NMOS
6502. This validates actual interpreter behavior for an identified binary.
Python provides the CPU and I/O harness; it does not evaluate the BASIC
expressions.

Start from a checkout with the usual Python environment active:

```bash
python -m tools.apple1_basic software/basic/HELLO.session
python -m tools.textbook run U01
```

You should see the numbered lines entered, `RUN`, the automatic INPUT question
mark, and `HELLO TOM`. The final record gives the stop reason, instruction count
and interpreter SHA-256. The host stops when the interpreter is waiting for
another line; it does not invent a successful END result.

## Predict and observe a greeting

The program in [HELLO.bas](../../../software/basic/HELLO.bas) is:

```text
10 DIM N$(20)
20 INPUT "WHAT IS YOUR NAME",N$
30 PRINT "HELLO ";N$
40 END
```

Predict the exchange before opening [U01](../features/U01.md). `DIM` reserves
string capacity. INPUT prints its prompt and adds `?`. A semicolon in PRINT
joins the message to the variable's contents. `RUN` is a command that executes
stored numbered statements; `INPUT` is not accepted as an immediate command
by this interpreter.

Try adding `?` to the prompt itself. The captured second U01 session shows
`NAME??TOM`. The extra question mark is actual interpreter output. Neither the
prompt nor the input routine inserts a space before TOM.

## Integers impose intermediate limits

[U02](../features/U02.md) runs the conversion and the boundaries 0, 129, 130 and
−1. The accepted domain is **nonnegative integers 0–129**. Integer division
truncates: `5*254/100` reports 12, not 12.7. `129*254` is 32766, within the
interpreter's 32767 maximum. `130*254` overflows before division happens.

The [guarded program](../../../software/basic/CONVERT.bas) checks that domain
before calculating. A number outside it gets a helpful message. Fractional
input is outside this contract; this program is not a floating-point converter.
The raw failing unguarded expression is retained in U02.

The tests also execute `38/9` → 4, `38 MOD 9` → 2, `1+2*3` → 7,
`(1+2)*3` → 9 and the signed endpoints. `−32768` is rejected by this
interpreter; do not infer its domain from a modern signed 16-bit type alone.

## Follow the state, then the algorithm

| Lab | Program | Prediction to make first |
|---|---|---|
| [U03](../features/U03.md) | Running sum | Write each index and total before the next iteration |
| [U04](../features/U04.md) | Bubble sort | Reproduce B04's four passes and final no-swap result |
| [U05](../features/U05.md) | Quiz | Predict both matching and nonmatching answers |
| [U06](../features/U06.md) | Pattern | Count rows and stars without running |

BASIC arrays in this interpreter are **one-based**. `DIM A(5)` gives indices
1 through 5. Index 0 raises `RANGE ERR`. U04 retains that failure alongside
the successful sort. A Python list's indexing rules do not validate BASIC.

The source programs, exact sessions, executable examples, transcript images,
practice questions and answers are all linked from these labs.

## Understand the saved program

The BASIC ROM is 4096 bytes at `$E000–$EFFF`, SHA-256
`5d8a3fe3c20c42903b226d67430c840ea5119557f88774c069e2e4dd80ad2c67`.
Its [preservation record](../../../preservation/software/apple1-reference/provenance.json)
traces it to `/UTILITIES/BASIC` in the original card image.

A cold host session starts at `$E000`. The identified interpreter initializes
`LOMEM` at `$4A/$4B` to `$0800` and `HIMEM` at `$4C/$4D` to `$1000`.
Warm entry at `$E2B3` preserves a loaded program. The original Apple BASIC
manual describes cold and preserved-program entry on printed p. 1 / PDF p. 3;
the [source pool](../../field-library/SOURCES.md#pre-hardware-source-additions-october-28-2026)
records the scan.

CFFA1 BA1 (`$F1`) files begin with `A1` and format version 0. The first
512-byte block carries a header and saved zero-page state; subsequent data
cover LOMEM through HIMEM. The actual firmware constructs this format.
[K04](../features/K04.md) saves a tokenized program, clears program RAM and
BASIC state, reloads it, and runs the restored greeting. Renaming a text file
does not create this state.

The candidate's `BASICLABS` directory contains six real BA1 files generated
this way. The [card guide](../../../cf-card/README.md) gives the intended
transition between reader and BASIC.

## Model boundaries

The keyboard model presents high-bit input. The display is always ready and
collects writes at `$D012`. It has no analog signal, serial transport, scan
timing or physical keyboard. Sessions have an instruction bound; an infinite
program reaches that bound and reports it. Script input is queued one complete
line at the blocking `$E003` input poll, so runtime break checks cannot eat
future commands.

The preserved binary's identity is known. The finished board's installed
interpreter, character set and hardware timing remain to be measured.
These host sessions require no serial connection or firmware change.

[Textbook home](../README.md) · [Card edition](../../../cf-card/README.md) · [Program sources](../../../software/basic/README.md)
