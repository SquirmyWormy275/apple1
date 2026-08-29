# R01 Activity: draw a banner

**Status:** OFF-DEVICE. Paper and pencil. Nothing is displayed on any machine.

## Part A: draw one (this is the first result)

Choose a word of five letters or fewer and draw it on `assets/grid-40.txt`,
counting columns against the ruler.

Rules: upper case only, printable ASCII only, 40 columns maximum, no wrapping.

## Part B: measure the examples

Using the ruler, measure the three worked banners.

| Example | Widest line | Fits in 40? |
|---|---:|---|
| One, block letters | | |
| Two, border and title | | |
| Three, shading | | |

## Part C: the width arithmetic

| Letters | Columns each | Gaps | Total | Fits? |
|---:|---:|---:|---:|---|
| 4 | 5 | 2 | | |
| 5 | 5 | 2 | | |
| 6 | 5 | 2 | | |
| 7 | 5 | 2 | | |
| 8 | 4 | 1 | | |

## Part D: rank the weights

Put these in order from lightest to heaviest, then say how many distinct weights
you can reliably tell apart at a glance.

`.` &nbsp; `#` &nbsp; `+` &nbsp; `'` &nbsp; `@` &nbsp; `=` &nbsp; `,` &nbsp;
`*` &nbsp; `O`

## Part E: what would the formatter do

The repository's text formatter upper-cases input and replaces unsupported
characters with a visible `?`. For each line, say what comes out.

| In | Out |
|---|---|
| `Apple-1` | |
| `HELLO` | |
| `caf` followed by an e-acute | |
| A line 45 characters long | |
| An em-dash between two words | |

## Part F: the overrun

You draw a banner and one line comes out 41 columns wide.

1. What happens on a 40-column display?
2. Can you fix it after it has been displayed?
3. What is the cheapest place to have caught it?

## Part G (optional): design challenge

Design a title screen for this library. Constraints: 40 columns, at most 12
rows, upper case, three weights at most, and it must include the word
`APPLE-1`. Count every line.

## What this activity does not do

It draws on paper. Nothing is displayed on a machine and no hardware action is
authorized.
