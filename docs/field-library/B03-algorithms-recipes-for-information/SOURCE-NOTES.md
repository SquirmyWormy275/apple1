# B03 Source notes

Keys refer to the shared pool in `../SOURCES.md`.

## Not an Apple-1 lesson

Most of this packet carries no Apple-1-specific claim. The four properties of an
algorithm (finite, definite, effective, general) are standard computing-science
definitions, long predating this machine and not attributable to any source in
this project's collection. They are stated as general background, not as cited
fact.

The sandwich, the shuffled steps, and the rewriting exercises are constructed for
this lesson.

## The Apple-1-specific parts

| Claim | Key |
|---|---|
| `line-input-0300.hex` stops after a carriage return | REPO `software/ram-only/README.md`; A05 |
| It also stops when Y reaches `$80`, after 128 characters | A05, derived by inspection; **V-18** |
| It behaved identically across four different recorded inputs | `../EMULATOR-RUNS.md` |
| Machine instructions have exactly one meaning to the processor | OWAD Appendix D, the instruction reference, which assigns one operation per opcode |

The generality claim in Part E is supported by, not proven by, the four recorded
runs. Four inputs behaving the same way is evidence of generality, not a proof of
it. The answer key says "the recorded runs used four different inputs and all
behaved the same way" rather than claiming the program is proven general.

## The finiteness argument depends on V-18

Part E's finiteness answer relies on both exits terminating, and the second exit
is the one A05 recorded as an open question. The answer key states this
explicitly rather than quietly relying on it: the program is finite whichever way
the intent question is settled, but a reader should know the argument uses a
finding that is not fully closed.

## Deliberate simplifications

1. **"Effective" is given the informal reading** of "each step can actually be
   done." The formal computability sense is not raised.
2. **Complexity and efficiency are not mentioned.** B04 introduces efficiency
   intuitively.
3. **Correctness is not distinguished from termination.** A procedure can be
   finite, definite, effective, general, and wrong. That distinction belongs with
   X02.

## Claims needing verification

- Page numbers inherit **V-1**.
- **V-18 carried forward** in the Part E finiteness argument.
- **V-8 applies.** Nothing here concerns this board's state.

## What this lesson does not establish

Nothing about this project's machine. It authorizes no firmware load, EEPROM
write, CFFA1 write, serial-port open, or physical modification.
