# R01 Answer key

## Part A: draw one

Acceptance: no line exceeds 40 columns, every character is upper-case printable
ASCII, the word is legible from a normal reading distance, and the learner
counted rather than estimated.

The most common failure is a banner that is beautiful and 43 columns wide.

## Part B: measure the examples

| Example | Widest line | Fits? |
|---|---:|---|
| One, block letters | 32 | Yes |
| Two, border and title | 34 | Yes |
| Three, shading | 20 | Yes |

All three were built inside the limit deliberately, with margin. Designing to
exactly 40 leaves no room for a later change.

## Part C: the width arithmetic

Total = letters x columns + gaps x (letters - 1).

| Letters | Each | Gap | Total | Fits? |
|---:|---:|---:|---:|---|
| 4 | 5 | 2 | 26 | Yes |
| 5 | 5 | 2 | 33 | Yes |
| 6 | 5 | 2 | 40 | Yes, exactly |
| 7 | 5 | 2 | 47 | **No** |
| 8 | 4 | 1 | 39 | Yes, but the letters are cramped |

The last row is the real trade: eight letters fit only by making each one four
columns wide with a single column of gap, at which point legibility suffers.
There is no arrangement that gives you eight readable five-column letters.

## Part D: rank the weights

Lightest to heaviest, roughly:

`'` `,` `.` `=` `+` `O` `*` `#` `@`

Reasonable people will order the middle differently, and that is the point.

**How many can you reliably tell apart? About three.** Maybe four. Beyond that
the ranking stops being obvious to a viewer who is not thinking about it, and the
picture reads as texture rather than as shading. This is why the examples sheet
says three weights and no more.

## Part E: what would the formatter do

| In | Out |
|---|---|
| `Apple-1` | `APPLE-1` |
| `HELLO` | `HELLO`, unchanged |
| `caf` + e-acute | `CAF?` |
| A 45-character line | Wrapped into a 40-character line and a 5-character line |
| An em-dash | Replaced with `?` |

The last two are the ones that catch people. **An em-dash is not ASCII**, so it
becomes a `?`. And a long line is not truncated, it is wrapped, so nothing is
lost but the layout changes.

## Part F: the overrun

1. **It wraps.** The 41st character appears at the start of the next line, and
   everything below is displaced by one line.
2. **No.** Once a character is on the display it cannot be modified. It leaves by
   scrolling off the top or by clearing the whole display.
3. **On paper, before drawing.** Counting a line costs seconds. This is why the
   grid has a ruler across the top.

## Part G: design challenge

No single answer. Acceptance criteria:

- Every line 40 columns or fewer, counted.
- 12 rows or fewer.
- Upper-case printable ASCII throughout, so it would pass the formatter
  unchanged.
- At most three weights.
- Contains `APPLE-1`.

A worked example that meets all five, at 34 columns and 7 rows:

```text
++++++++++++++++++++++++++++++++++
+                                +
+   A P P L E - 1                +
+   ....................         +
+   F I E L D   L I B R A R Y    +
+                                +
++++++++++++++++++++++++++++++++++
```

Three weights: `+` for the frame, letters for the text, `.` for the rule.

## Try a variation: a word that does not fit

**Narrower letters:** shrink to four or three columns each. Three-column letters
are possible but several become ambiguous, notably `M` and `W`, which need width
to be distinguishable from each other and from `N`.

**Two lines:** split the word, using full-size letters on both. This almost
always reads better, because legibility per letter matters more to a reader than
the word being on one line.

The general finding: when you run out of width, spend height. It is the cheaper
resource on a display that scrolls.

## README: Check your understanding

1. **Because its video section is text only.** It stores a character's ASCII code
   and looks the shape up in a small ROM, so only characters present in that ROM
   can appear. There is no bitmapped graphics mode.
2. **Six.** 6 x 5 + 5 x 2 = 40 exactly. Seven needs 47.
3. **Because a character on the display cannot be modified.** It stays until it
   scrolls off the top or the whole display is cleared. There is no editing in
   place.
