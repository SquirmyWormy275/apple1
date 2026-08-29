# C04 Answer key

## Part A: the table

| Char | Dec | Hex | High-bit hex |
|---|---:|---|---|
| A | 65 | `$41` | `$C1` |
| B | 66 | `$42` | `$C2` |
| Z | 90 | `$5A` | `$DA` |
| 0 | 48 | `$30` | `$B0` |
| Space | 32 | `$20` | `$A0` |
| CR | 13 | `$0D` | `$8D` |

## Part B: decode the message

| Byte | Minus `$80` | Char |
|---|---|---|
| `C8` | `$48` | H |
| `C9` | `$49` | I |
| `A0` | `$20` | (space) |
| `D4` | `$54` | T |
| `C8` | `$48` | H |
| `C5` | `$45` | E |
| `D2` | `$52` | R |
| `C5` | `$45` | E |
| `8D` | `$0D` | (carriage return) |

**`HI THERE` followed by Enter.**

### Part 3 of the worksheet

Stripping the top bit comes first **because ASCII assigns nothing above 127.**
Looking up `$C8` in an ASCII table finds no entry at all. The top bit is not part
of the character; it is a marker added around it.

## Part C: encode a message

`APPLE` plus carriage return:

```text
C1  D0  D0  CC  C5  8D
```

Check: `A`=`$41`+`$80`=`$C1`, `P`=`$50`+`$80`=`$D0`, `L`=`$4C`+`$80`=`$CC`,
`E`=`$45`+`$80`=`$C5`.

## Part D: which layer is responsible

| # | Layer | Note |
|---|---|---|
| 1 | **ASCII** | Published standard. |
| 2 | **Apple-1 convention** | Documented in the Monitor listing. |
| 3 | **ASCII** | A property of how the standard assigns values. |
| 4 | **Emulator convention** | The harness accepts seven-bit text and applies the high bit itself. |
| 5 | **ASCII** | |
| 6 | **Apple-1 convention** | The comparison value is `$0D` plus the high bit. |

Items 2 and 6 are the same fact seen from two sides. Item 4 is the one learners
put in the wrong bin.

## Part E: spot the mistake

1. **They had `HELLO`.** `C8 C5 CC CC CF` strips to `48 45 4C 4C 4F`.
2. **They skipped stripping the top bit** before the lookup.
3. **In reverse:** writing `48 45 4C 4C 4F` into a byte list intended for the
   Monitor, without setting the top bit. The program comparing against `$8D` for
   Enter would never match, and a loop waiting for a carriage return would not
   stop.

The reverse case is worse, because it produces a program that runs and misbehaves
rather than a lookup that visibly fails.

## Part F: the case question

One line of reasoning. Handling a lower-case byte costs one instruction: clearing
bit 5 turns any lower-case letter into its upper-case equivalent, since they
differ by exactly that bit. Rejecting it costs a comparison and a decision about
what to do instead. Handling is cheaper and kinder, but it silently changes what
the user typed, which is a real trade rather than an obvious win.

Accept any answer that notices the one-bit relationship and weighs silent
correction against visible rejection. The repository's own firmware behavior
model takes the strict line: it rejects lower-case conversion until measured
rather than guessed.

## Try a variation: `$D4`

`$D4` minus `$80` is `$54`, which is **`T`**.

Someone reading a byte list without knowing the convention would see values from
`$80` upward, find them unassigned in ASCII, and reasonably conclude the machine
used an extended or non-standard character set. They would be wrong, but not
foolish. The correct move is the S04 one: treat "this machine uses a different
character set" as a claim, and look for what would establish it.

## README: Check your understanding

1. **`HI` is `C8 C9`.** `H` is `$48`, `I` is `$49`, each plus `$80`.
2. **Because the digits are consecutive and `0` is `$30`.** Subtracting `$30`
   from any digit character gives the number it represents: `$35` minus `$30` is
   5.
3. **Two possibilities:** the Apple-1 keyboard convention, which sets bit 7 on a
   character coming in; or the emulator harness, which applies that convention to
   the plain text you gave it on the command line. The transcript alone does not
   distinguish them.
