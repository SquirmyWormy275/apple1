# SP01 Answer key

## Part A

- 6502: **A7**.
- 6820 PIA: **A4**.
- RAM bank X: **row B**, B11–B18.
- RAM bank W: **row A**, A11–A18.
- Video-dense rows: **C and D**.

## Part B

1. **P8X32A-D40 Propeller**.
2. **62256 SRAM**.
3. The **ASCII keyboard input** is retained alongside PS/2.

## Part C

`A=2 B=3 C=1 D=4 E=5`.

The most visually dramatic reduction is the video/I/O subsystem: many original
terminal IC packages are replaced by a much denser modern implementation.

## Part D

The display/video implementation changes most. The overall conceptual route—
keyboard input, PIA-visible I/O, 6502/Monitor processing, output to a display
system—remains related.

## Part E

A program is written against software-visible addresses and behavior. If the
Replica preserves the relevant I/O contract, the physical circuitry behind that
contract can change without requiring the program to know the component-level
implementation.

## Part F

1. **Supported by manufacturer design documentation.**
2. **Observed on this project unit.**
3. **Not established.**
4. **False for the recorded test:** a no-transmit open disturbed the display and
   required physical Reset.
5. **No.** The atlas is an educational identification map, not a service or
   probing diagram.
