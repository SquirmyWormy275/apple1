# B02 Answer key

## Part A: choose a job and draw it

Worked example for job 1, inches to centimetres:

| Box | Content |
|---|---|
| ASK | Print "HOW MANY INCHES" |
| GET | Read a number into `I` |
| WORK | Multiply by 254, divide by 100 |
| TELL | Print the result with a label |

Variable name `I`, a number.

The `WORK` box is worth a comment. Apple-1 BASIC has integers only, so
multiplying by 2.54 is not available. Multiplying by 254 and dividing by 100
keeps everything integer and loses the fractional part, which is the honest
consequence of the language's limits rather than a workaround to be embarrassed
about.

A learner who wrote `I * 2.54` should be shown that it cannot work here, and
asked what they want to happen to the fraction.

## Part B: legal names

| Name | Legal? | Why |
|---|---|---|
| `A` | **Yes** | A letter. |
| `A1` | **Yes** | A letter and a digit. |
| `SUM` | **No** | Too long. Integer names are one letter or a letter and a digit. |
| `N$` | **Yes** | A letter and a dollar sign. |
| `NAME$` | **No** | Too long for a string name. |
| `Z9` | **Yes** | |
| `1A` | **No** | Starts with a digit, not a letter. |
| `B$` | **Yes** | |

## Part C: predict the output

| Line | Output |
|---|---|
| `PRINT N$` | `TOM` |
| `PRINT "N$"` | `N$` |
| `PRINT "HELLO "; N$` | `HELLO TOM` |
| `PRINT A` | `5` |
| `PRINT "A"` | `A` |
| `PRINT A*2` | `10` |

The pattern: quotation marks mean "print these characters." No quotation marks
means "print what is in this."

## Part D: write the lines

Job 2, a greeting:

```text
10 DIM N$(20)
20 INPUT "WHAT IS YOUR NAME", N$
30 PRINT "HELLO "; N$
40 END
```

Job 1, inches to centimetres:

```text
10 INPUT "HOW MANY INCHES", I
20 PRINT I; " INCHES IS "; I*254/100; " CM"
30 END
```

Accept any version with the four boxes present, a legal variable name, and a
`DIM` where a string is used.

## Part E: what the user sees

For the greeting program:

```text
WHAT IS YOUR NAME?TOM
HELLO TOM
```

**The question mark is automatic and cannot be removed.** Notice there is no
space between it and the typed answer either. A prompt written as
`"WHAT IS YOUR NAME?"` would produce `WHAT IS YOUR NAME??`, which is the sort of
thing that only becomes obvious when you write the exchange out.

That is why Part E exists. Reading the interaction aloud catches things reading
the code does not.

## Part F: the missing DIM

1. **How many bytes to set aside for the string.** BASIC needs to reserve the
   space before anything is stored in it.
2. **Because a string has a length and an integer does not.** An integer is a
   fixed size whatever its value. A string could be one character or two hundred,
   and BASIC cannot guess which.
3. **255 characters**, which is 255 bytes, one per character.

## Part G: two inputs

Redrawing gives five boxes: ask, get, ask, get, work, tell, or the two asks and
gets interleaved.

**New ways to go wrong**, at least: the two inputs arriving in the wrong order;
the second overwriting the first if the same variable name is reused; a prompt
that does not make clear which value is wanted; and a `WORK` box that uses one
variable twice instead of using both.

The last one is the sneaky one and it produces plausible wrong answers rather
than obvious failures.

## Try a variation: the one-question quiz

The boxes stay four, but their contents change:

| Box | Quiz version |
|---|---|
| ASK | Print the question |
| GET | Read the answer |
| WORK | **Compare** against the correct answer rather than calculate |
| TELL | Print one of two messages depending on the comparison |

**What changes in `TELL`:** it is no longer a single output. It is a choice
between two, which means the program now contains a decision. In BASIC that is an
`IF`; in assembly it is A04's compare-and-branch. The four-box shape does not
show the fork, which is a limitation of the diagram worth noticing.

## README: Check your understanding

1. **Legal: `A`, `A1`, `N$`, `Z9`. Not legal: `SUM`, `NAME$`.** Both illegal ones
   are too long.
2. **So BASIC knows how many bytes to reserve.** A string's length varies and
   cannot be inferred; an integer's does not.
3. **`PRINT N$` prints the contents of the variable. `PRINT "N$"` prints the two
   characters `N` and `$`.** The quotation marks are the difference.
