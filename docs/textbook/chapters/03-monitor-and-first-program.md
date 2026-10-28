# 3. Use the Monitor and execute your first program

Here "Monitor" means a small resident machine-control program, not the video
display. Its core operations are to examine bytes, deposit bytes, and transfer
control. It is not a shell, a filesystem, or a language-model assistant.

## An inspectable task

Store 42 at `$0400`, then return to the Monitor. In assembly:

```text
LDA #$2A
STA $0400
JMP $FF1F
```

The modeled Monitor accepts encoded bytes. The worked lab uses these virtual
commands:

```text
0300: A9 2A 8D 00 04 4C 1F FF
0300.0307
0300R
0400
```

The first line deposits eight bytes. The second inspects that inclusive range.
The third requests execution from `$0300`. The fourth inspects the stored byte.
Run [M01](../../field-library/M01-meet-the-monitor/WORKED.md) and compare your
prediction with each recorded reply. These are host-only virtual commands,
not an instruction to enter bytes on the blocked physical unit.

## Why the origin matters

The origin is where the first byte is placed. It determines instruction and
label addresses. Absolute operands still name explicit destinations. A source
file consisting only of byte values does not by itself identify where it must
be loaded. Read the program's contract before interpreting it.

[M02](../../field-library/M02-addresses-and-byte-entry/WORKED.md) displays the
address of every encoded byte. Draw boxes around opcode and operand fields.
Then explain why `00 04` inside a store names `$0400`.

## Exit deliberately

A final `JMP $FF1F` selects the modeled Monitor warm-entry stop. `RTS` removes
a return address from the stack; it is valid only when the entry path created
a compatible call frame. A Monitor run transfer must not be assumed to provide
one. [M05](../../field-library/M05-why-jmp-ff1f-matters/WORKED.md) separates
`JSR ECHO` returning from the program's own final jump.

The generic world treats BRK as a bounded stop without reproducing a full
hardware interrupt sequence. A `STOP=BRK` result in a lab therefore does not
teach the complete physical BRK/IRQ behavior. Inspect the explicit stop reason.

## Handle a wrong result

Write your expected value before running. If memory contains 43, distinguish
whether the immediate operand is wrong, the destination is wrong, or the
expectation is wrong. [M04](../../field-library/M04-debugging-as-observation/WORKED.md)
provides a deliberate mismatch. Preserve the failed observation and change one
factor for the next test.

## Practice

Modify a scratch copy to store `$5A` at `$0402`. Before running, state the changed
operand bytes, expected memory result, and unchanged exit. Use the helper-based
[A02 lab](../../field-library/A02-variables-in-memory/WORKED.md) to check it.

[Textbook home](../README.md) · [Previous chapter](02-numbers-and-characters.md) · [Next chapter](04-assembly-and-control-flow.md)
