# C01 Answer key

## Part A

| Instruction | English |
|---|---|
| `LDA #$00` | Load the accumulator with the number zero. |
| `LDA $D011` | Load the accumulator with the contents of address `$D011`. |
| `STA $0400` | Store the accumulator into address `$0400`. |

## Part B: hash or no hash

| A | B | Difference |
|---|---|---|
| `LDA #$10` | `LDA $10` | A loads the number sixteen. B goes to address `$0010` and loads whatever is there. |
| `LDY #$FF` | `LDY $FF` | A loads 255 into Y. B loads the contents of address `$00FF` into Y. |

The `#` is the whole difference. Without it, the number is a place.

## Part C: name the register

| Register | Job |
|---|---|
| A | The accumulator. The main working byte; most data and arithmetic passes through it. |
| X | An index register. Counting and stepping through memory. |
| Y | An index register, same idea as X. Both RAM-only programs in this repository use Y to step through a buffer. |
| Program counter | Holds the *address* of the next instruction. The CPU's place in the program. |

## Part D: the real program's first six bytes

1. **`LDY #$00`** sets Y to zero. It is the count-from-the-start setup.
2. **`LDA $D011`** loads the contents of `$D011`, which is the keyboard control
   register. It holds the flag saying whether a key is waiting.
3. **`BPL $0302`** branches back to the instruction that just ran. Taken
   together, the three lines are: start the counter at zero, then check the
   keyboard flag over and over until it changes. This is the polling loop from
   S02, written out in bytes.

A learner who says "it is waiting for a key" has the answer.

## Part E: how many bytes

| Instruction | Bytes | How you know |
|---|---:|---|
| `LDY #$00` | 2 | `A0 00`. Opcode plus a one-byte value. Also: the next instruction starts at `$0302`, two past `$0300`. |
| `LDA $D011` | 3 | `AD 11 D0`. Opcode plus a two-byte address. `$0305` minus `$0302` is 3. |
| `BPL $0302` | 2 | `10 FB`. Opcode plus a one-byte offset. |

The address column in a listing is the reliable way to count instruction length:
subtract one address from the next.

Notice `AD 11 D0` stores the address `$D011` as `11 D0`, low byte first. That
ordering has a name and is covered in C02.

## Part F: the fetch-decide-act trap

A program "finishing" means control passed somewhere else, not that the CPU
stopped. `line-input-0300.hex` ends with `JMP $FF1F`, which hands control to the
Monitor, and the Monitor then runs its own loop waiting for you to type. The CPU
has not paused for an instant.

## README: Check your understanding

1. **`LDA #$41` loads the number 65. `LDA $41` loads the contents of address
   `$0041`.** The `#` means the value itself.
2. **Because it names a place, not data.** Adding one to the program counter
   moves to the next byte of program; adding one to a register changes a value.
   Confusing the two is confusing the map for the territory.
3. **It runs a loop that goes nowhere,** typically a jump to itself, or it sits
   in a polling loop waiting for input that has not come. The fetch-decide-act
   cycle continues either way.
