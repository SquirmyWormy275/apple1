# Apple-1 display rules and animation

- Maximum line width: 40; machine assets: upper-case printable ASCII.
- Default page maximum: 23 lines where a 40x23 master is intended.
- Rendering and pagination must be deterministic.
- Animation is a sequence of valid complete frames; one key skips to the final
  frame. It never gates Monitor recovery or COMPUTER entry.
- A host preview establishes formatting only, not physical appearance/timing.

The validator and paginator live in `neural1/visualization.py`.
