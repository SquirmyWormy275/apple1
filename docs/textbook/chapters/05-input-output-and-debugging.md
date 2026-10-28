# 5. Connect input, memory, and visible output

The line-input lesson is an end-to-end program small enough to trace completely.
Its 26-byte artifact reads a high-bit keyboard stream, saves each byte in an
indexed buffer, echoes it, and reaches Monitor warm entry on the defined exit.

## Read the pipeline

1. Initialize Y, the buffer index.
2. Poll the keyboard status convention represented by the harness.
3. Read a character when ready.
4. Store it at `$0400,Y`.
5. Call the Monitor ECHO stub.
6. Compare with high-bit carriage return and either exit or advance Y.

Read [A05's original activity](../../field-library/A05-keyboard-to-screen/ACTIVITY.md)
and the [program annotations](../../field-library/program-annotations/README.md).
The host harness supplies readiness/input bytes; it does not measure a physical
keyboard, PIA, Propeller, USB serial connection, or display timing.

## A complete test case

For `HI` plus Return, predict the screen and buffer before running M03.
The recorded output contains `"HI\r"` for both fields, `returned_to_monitor`
true, and 30 instructions in this harness. The carriage return is stored because
the store occurs before the exit comparison.

The empty line still contains Return. Treat it as a real case, not the absence
of an input event. A05 runs both cases. To investigate long input, derive the
index and branch limits from the listing and compare actual harness results;
do not assume unrestricted buffer growth.

## Display output and an output log

The CPU produces a character through the modeled ECHO entry point. The harness
records the character as text. Its `screen_text` is a log of emitted characters,
not a full terminal emulator supporting arbitrary cursor motion, scrolling, or
screen editing. The `buffer_text` is read from the modeled data area.

The longer echo variant has different observed control flow. Keep it a separate
artifact and do not silently "fix" it during a lesson. Its behavior and intended
purpose are separate questions in the existing verification register.

## Build a useful bug report

Write the exact input, source artifact/hash, load address, expected output,
actual output, stop reason, instruction bound, and minimal changed bytes.
Include a negative case. A clean Monitor return does not prove that every byte
was written to the correct location.

## Practice

Predict `A` plus Return, then run a scratch variation of M03. Explain the change
in work from the additional ordinary character. A timing claim would require
more than an instruction count: the physical implementation and measurement
procedure would also matter.

For a different output exercise, R01 constructs a 40-column banner; R02 treats
animation as state transitions. Neither activity assumes a physical video driver
or a working serial connection.

[Textbook home](../README.md) · [Previous chapter](04-assembly-and-control-flow.md) · [Next chapter](06-algorithms-basic-and-creative-computing.md)
