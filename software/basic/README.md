# Apple-1 Integer BASIC programs

These six project-authored programs execute on the identified preserved
interpreter. The host uses an NMOS 6502, a ready display and a high-bit keyboard
model. It does not translate BASIC into Python.

```bash
python -m tools.apple1_basic software/basic/HELLO.session
python -m tools.textbook run U04
```

| Source | Learn | Expected run result |
|---|---|---|
| [HELLO.bas](HELLO.bas) | DIM, string INPUT, PRINT punctuation | `HELLO TOM` |
| [CONVERT.bas](CONVERT.bas) | Integer arithmetic and intermediate bounds | 5 inches reports 12 cm; rejects integers outside 0–129 |
| [SUM.bas](SUM.bas) | FOR/NEXT and accumulated state | Final sum 15 |
| [SORT.bas](SORT.bas) | One-based arrays, comparisons and swaps | 16 comparisons, 7 swaps |
| [QUIZ.bas](QUIZ.bas) | Both outcomes of IF | 42 succeeds; 41 receives a hint |
| [PATTERN.bas](PATTERN.bas) | Nested loops and text generation | Six rows, 21 stars |

A `.bas` file contains the numbered source. A `.session` contains that source,
`RUN` and any INPUT replies. An empty line inside a session is a submitted
Return, not a comment. Use uppercase printable input. Later script lines are
released only at this ROM's blocking input poll, so break-key checks during
execution cannot consume the next command.

Plain source is not a saved CFFA1 BASIC file. The host image builder feeds the
source to the interpreter, uses CFFA1's real `SaveBASICFile` API, then clears RAM,
loads the saved BA1 and executes it again. `BASICLABS` in the candidate image
contains those generated `$F1` files. No physical card is written.

[Full BASIC chapter](../../docs/textbook/reference/basic.md) · [Card guide](../../cf-card/README.md)
