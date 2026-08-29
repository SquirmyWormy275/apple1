# B01 Answer key

## Part A: five tasks

| # | Task | Language | Reason |
|---|---|---|---|
| 1 | Add twenty typed numbers | **BASIC** | `INPUT` and arithmetic are one line each. The assembly version needs digit-to-number conversion, multi-digit accumulation, and a loop. |
| 2 | Read a keyboard register bit | **Assembly** | BASIC has no way to reach `$D011` and test bit 7. This is exactly what assembly is for. |
| 3 | Print a multiplication table | **BASIC** | Nested loops and formatted output, all of which BASIC does in a few lines. |
| 4 | Fit in 26 bytes | **Assembly** | BASIC's interpreter alone is 4 KB. The question does not arise. |
| 5 | Five versions in an afternoon | **BASIC** | Edit a line, type `RUN`. Reassembling by hand five times is most of the afternoon. |

Items 2 and 4 are assembly for different reasons: 2 because BASIC *cannot*, 4
because BASIC *will not fit*. Worth separating.

## Part B: what BASIC hides

| BASIC | Hidden work |
|---|---|
| `10 PRINT "HI"` | Store the text somewhere; mark its end; point at it; loop through it; call the display routine per character; stop at the marker. |
| `20 A = B + C` | Decide where A, B, C live; load B; clear the carry; add C; store into A; handle the result exceeding one byte. |
| `30 INPUT "NAME", N$` | Print the prompt; print the question mark; poll the keyboard; store characters; detect Return; reserve the string's space; record its length. |
| `40 GOTO 10` | Almost nothing. This is the one that maps to a single instruction, a `JMP`. |

Row 4 is the useful one: not everything BASIC does is expensive. `GOTO` is a
jump with a friendlier name.

## Part C: Apple-1 BASIC facts

| # | Answer | Note |
|---|---|---|
| 1 | **False** | Integers only. |
| 2 | **True** | `MOD` gives the remainder. |
| 3 | **False** | Integer names are a letter or a letter and a digit; strings are a letter plus `$`. `NAME$` is too long. |
| 4 | **True** | `DIM` tells BASIC how many bytes to allocate. Maximum 255. |
| 5 | **False** | The question mark is automatic and cannot be turned off. |
| 6 | **True** | `PRINT 8+3` at the prompt answers 11 with no program. |

## Part D: cost and benefit

| | Assembly | BASIC |
|---|---|---|
| Speed of writing | Slow. Every detail is yours. | Fast. One line does a lot. |
| Speed of running | Fast. The instructions are the program. | Slower. Every line is interpreted as it runs. |
| Memory used | Small, and exactly what you chose. | Larger, and the interpreter must be resident. |
| Control over details | Total. | Limited to what the language exposes. |
| What must already be present | Nothing beyond the machine and a way to enter bytes. | BASIC itself, in ROM or loaded into RAM. |
| Ease of changing later | Hard. Addresses shift and byte lists must be re-derived. | Easy. Retype one line and run. |

A learner who left "speed of running" blank for BASIC, or "speed of writing"
blank for assembly, has not filled both columns. Every row has a real entry on
both sides.

## Part E: the unfair comparison

**It compares a program against a language.**

The assembly `PRINT` equivalent is a few instructions *for one fixed string*. To
match what BASIC's `PRINT` does, you would need it to handle any string, any
length, numbers as well as text, and formatting, at which point you have written
a chunk of an interpreter yourself.

The honest comparison is either program against program, one string against one
string, where assembly is indeed much smaller; or capability against capability,
where BASIC's 4 KB is doing far more.

Comparing your specific solution against their general one is the most common
unfair comparison in programming arguments, and it works in both directions.

## Part F: the third option

**Krusader sits between them.** It lets you write mnemonics rather than hex, and
it works out opcodes, addresses, and branch offsets for you.

**What it improves over hand entry:** no hand-assembly. You write `BNE LOOP` and
the assembler computes the offset, which removes an entire class of the errors
A03 was about. Labels mean inserting an instruction no longer requires
recalculating every address after it.

**What it does not change:** the program is still assembly. It runs at the same
speed, uses the same memory, requires the same understanding of registers and
addressing, and can reach the hardware just as directly. An assembler changes how
you *write* the program, not what the program *is*.

## Try a variation: `line-input-0300.hex` against `INPUT`

**Three things the assembly version can do that `INPUT` cannot:**

1. Store the characters at an address of your choosing, `$0400`.
2. React to each character as it arrives rather than waiting for the whole line.
3. Run without BASIC being present at all.

**Two things `INPUT` does that the assembly version does not:**

1. Prints a prompt, and the automatic question mark.
2. Makes the result available as a named string variable that later lines can use
   directly, with its length tracked.

A learner may also note that `INPUT` gives no way to reach the raw bytes, which
is a difference in both directions depending on what you want.

## README: Check your understanding

1. **Any of:** locating the text, walking through it, knowing where it ends,
   calling the display routine, returning afterwards.
2. **Because "better" has no meaning without a job.** Every difference between
   them is a trade, and which side of a trade you want depends entirely on what
   you are doing. The answerable question is "better for this."
3. **No.** It is integer division, working as documented. `MOD` supplies the
   remainder. A bug is behavior that contradicts what the thing claims to do;
   this is a documented limit, and the language tells you about it.
