# 6. Express the same idea at different levels

Machine code exposes operations that higher-level languages package together.
A BASIC interpreter handles parsing, variables, arithmetic, and output. The
original B-series companions use marked Python analogues. The new
[BASIC chapter](../reference/basic.md) and U01–U06 execute the identified
Apple-1 interpreter on a modeled NMOS 6502. Compare both modes deliberately;
a Python calculation does not validate BASIC syntax or representation.

## Compare a task rather than ranking languages

Storing the constant 42 is not the same task as computing 6 times 7 for arbitrary
inputs. B01 compares the represented result and explicitly states that boundary.
An honest comparison accounts for interpreter/runtime storage, development time,
execution cost, and the control the task requires.

B02 separates input, state, computation, and output. Before translating its flow
into any language, define the accepted numeric range and error behavior.
Python's numbers and strings do not establish Apple-1 BASIC syntax, integer
limits, or allocation rules. Use the original lesson's source notes for those.

## Make an algorithm executable in your head

An algorithm needs a definite next step and stopping rule. B03 replaces an
ambiguous sum with a finite item-by-item trace. B04 compares adjacent items,
swaps out-of-order pairs, and stops after a pass without swaps. The final
no-swap pass still performs work.

Before optimizing a sort, test an empty sequence, one item, already-sorted and
reverse-sorted inputs, and repeated values. State whether preserving the order
of equal items matters. A sorted final list alone does not reveal the algorithm
or its comparison cost.

## Creative work is also state and rules

- R01 uses a fixed-width grid and checks printable characters.
- R02 represents animation with position and direction; it does not implement
  physical frame timing or cursor addressing.
- R03 generates a triangle from a rule and lets you compare code size with a
  stored picture.
- R04 makes rooms, exits, and inventory state explicit; an invalid action has a
  defined result.
- R05 interprets bits as clap/rest slots. Tempo and sound generation are extra
  parameters and hardware mechanisms, not properties of the bit pattern alone.

Each example has a recorded host result. These patterns make good later assembly
projects once you can state memory layout, input contract, stop conditions, and
tests. A host prototype is a design aid, not evidence that the same feature is
already implemented on the Replica.

## Practice

Choose a two-room story. Draw the transition graph, include one unavailable exit,
and trace three actions. Then write a design card for its assembly implementation:
state bytes, program range, input interpretation, display routine, and exit.
Use A06 and R04 as starting points. Keep an honest list of features you have not
implemented; it is part of a good project explanation.

[Textbook home](../README.md) · [Previous chapter](05-input-output-and-debugging.md) · [Next chapter](07-local-models.md)
