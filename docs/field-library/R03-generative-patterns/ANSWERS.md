# R03 Answer key

## Part A: four rows by hand

Columns 1 to 12. `#` where the column divides exactly by the row number.

| Row | Output |
|---:|---|
| 1 | `############` |
| 2 | `.#.#.#.#.#.#` |
| 3 | `..#..#..#..#` |
| 4 | `...#...#...#` |

**Row 3 has four `#`**, at columns 3, 6, 9, and 12.

**Row 1 has no dots because every number divides exactly by 1.** The condition is
true at every column, so the row is solid. A learner who expected some variation
in row 1 has not yet read the rule as a question asked at every position.

## Part B: the triangle

The numbers:

```text
            1
           1 1
          1 2 1
         1 3 3 1
        1 4 6 4 1
       1 5 10 10 5 1
```

Odd marked with `#`, even with space:

```text
            #
           ##
          # #
         ####
        #   #
       ##  ##
```

**The shape is a nested triangle**, sometimes called a Sierpinski triangle: a
large triangle made of smaller triangles, each made of smaller ones again. The
larger version on `assets/pattern-rules.txt` shows it more clearly over sixteen
rows.

**Did anyone draw that shape? No.** The rule says "add the two above" and "mark
the odd ones." Neither sentence mentions triangles, symmetry, or nesting. All
three are consequences.

## Part C: predict the rule from the output

| # | Output | Rule |
|---|---|---|
| 1 | `#.#.#.#.#.#.` | `#` at odd columns, or: `#` where the column does not divide by 2. |
| 2 | `#..#..#..#..` | `#` where the column leaves a remainder of 1 when divided by 3. |
| 3 | `#.#..#...#..` | Gaps grow: `#` at columns 1, 3, 6, 10. Those are the triangular numbers, each gap one longer than the last. |
| 4 | `............` | **Two possible answers**, among others: "never print `#`," or "`#` where the column divides by 13," which is true of no column in the first twelve. |

Line 4 is the useful one. **Two different rules produce identical output over a
short sample.** You cannot recover a rule from output with certainty; you can
only find rules consistent with what you have seen. Extending the sample to
thirteen columns would separate these two.

That is the S04 habit again: the output is evidence for a rule, not proof of one.

## Part D: characters change everything

| Characters | How it reads |
|---|---|
| `#` and `.` | Texture. The dots fill the background and the eye sees a grid. |
| `#` and space | Shape. The eye sees form against nothing. |
| `*` and `-` | Somewhere between. The dashes read as lines, which introduces a horizontal grain that was not in the pattern. |

**Title screen: `#` and space.** **Texture: `#` and `.`.**

The `*` and `-` case is worth noting: the choice of background character added an
apparent structure that the rule did not produce. Characters are not neutral.

## Part E: the cost comparison

| | As a picture | As a rule |
|---|---|---|
| 40 by 20 | 800 characters | One sentence, or a few instructions |
| 40 by 100 | 4,000 characters | **The same sentence.** Unchanged. |
| To change | Redraw everything affected | Change the rule; everything follows |
| To understand later | Immediate. You can see it. | Hard. You must run the rule in your head to know what it produces. |

**The last row is the argument the other way**, and it is a real one. A picture is
self-documenting and a rule is not. A rule you wrote six months ago may take
longer to understand than the picture would have taken to redraw.

The honest summary: rules win on size and on flexibility, and lose on
legibility.

## Part F: what the machine can do cheaply

Cheapest to most expensive:

1. **`ADD ONE`** and **`SUBTRACT`**, single instructions.
2. **`COMPARE`**, a single instruction.
3. **`MULTIPLY BY TWO`**, a single shift instruction.
4. **`DIVIDE`**, which the 6502 has no instruction for at all. It must be built
   from repeated subtraction or shifting.

**What that makes practical:** rules based on counting and resetting a counter.
"Every third column" is cheap if you keep a counter that counts 1, 2, 3, resets,
and print when it resets. The same rule stated as "where the column divides by 3"
sounds like division and is not, once you write it that way.

The lesson: restate a rule in terms of counting before deciding it is expensive.

## Part G: the extension

Acceptance: the learner worked three rows by hand *before* running the program,
and compared. A program checked against a hand-computed expectation is the M04
habit; a program admired after the fact is not.

Confirm nothing was attempted on the Replica 1 Plus.

## Try a variation: remainder of 1

**Prediction:** the pattern shifts. Instead of marking columns 3, 6, 9, it marks
1, 4, 7, 10.

Worked, for row 3, columns 1 to 12: `#..#..#..#..`

The shape is identical and its position has moved by one. Changing the target
remainder slides the pattern; changing the divisor changes its spacing. Two
independent controls, from one small rule.

## README: Check your understanding

1. **Because every number divides exactly by 1**, so the condition is true at
   every column and the row is solid.
2. **800 characters against one sentence.** And the gap widens as the pattern
   grows, because the rule does not get longer.
3. **From the arithmetic.** Adding the two numbers above, then asking whether the
   result is odd, produces the nesting as a consequence. The rule contains no
   triangle; the triangle is what that arithmetic does.
