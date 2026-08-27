# RAM-only Monitor programs

The `.hex` files contain address-free, space-separated byte lists for entry at
the address shown in their filename. They are retained from the confirmed
learning exercises in the project handover; this folder is not an assembler,
uploader, or deployment path.

## Safety boundary

- Start only from a photographed Monitor prompt with a reset recovery plan.
- Run one program at a time and retain the exact byte list used.
- Exit via `JMP $FF1F`. Do not replace it with `RTS`: the Monitor's `R` command
  jumps to the address and leaves no return address on the stack.
- Do not combine a program run with an open serial session, firmware action,
  ROM-bank change, or CFFA1 write.

## Expected behavior

`line-input-0300.hex` reads a key when `$D011` indicates ready, stores it at
`$0400,Y`, echoes through `$FFEF`, stops after CR, and returns to the Monitor.
`line-input-echo-0300.hex` then reads that buffer back through `$FFEF` before
starting over. The latter is a display-path exercise, not proof of serial TX.
