# M04 Activity: expected, observed, one hypothesis

**Status:** OFF-DEVICE. Paper, plus optionally the M03 emulator on an ordinary
computer. **No step of this activity involves the Replica 1 Plus.**

## Part A: the sheet (this is the first result)

The situation: `line-input-0300.hex` run in the emulator with input `HI` + CR
returns an empty `buffer_text`, while `screen_text` shows `HI` and a carriage
return, and `returned_to_monitor` is true.

Fill `assets/observation-sheet.txt`:

1. Expected column, from M03's recorded table.
2. Observed column, from the situation above.
3. One hypothesis in the given form.

## Part B: is it a hypothesis?

Mark each **usable** or **not usable**, and say why.

| # | Statement | Usable? |
|---|---|---|
| 1 | Something is wrong with the buffer. | |
| 2 | The store instruction targets `$4000` instead of `$0400`. | |
| 3 | The emulator is buggy. | |
| 4 | The `8D` comparison byte was mistyped, so the loop never ends. | |
| 5 | It is a hardware problem. | |
| 6 | The input string is missing its carriage return. | |

## Part C: how many things changed

For each, say how many things changed and whether the result is interpretable.

| # | What was done | Things changed | Interpretable? |
|---|---|---|---|
| 1 | Reran the same command. | | |
| 2 | Fixed one byte and reran. | | |
| 3 | Fixed one byte, changed the input, and reran on a different computer. | | |
| 4 | Fixed one byte and reran with the same input on the same machine. | | |

## Part D: STOP or continue

For each observation, decide **STOP** or **continue**, and give the rule.

| # | Observation | STOP or continue |
|---|---|---|
| 1 | An emulator run gives an unexpected instruction count. | |
| 2 | The machine's display garbles during a test. | |
| 3 | A byte list you transcribed does not match the source. | |
| 4 | The machine resets by itself mid-test. | |
| 5 | The serial device identity is not the one recorded. | |
| 6 | Your prediction was wrong but the program behaved consistently. | |

## Part E: the worked STOP

Read the FT232R account in the README.

1. What was the observation?
2. Which STOP condition did it meet?
3. What was done immediately after?
4. Name two things somebody might have done instead that would have destroyed
   the evidence.
5. Why is this still usable as evidence months later?

## Part F (optional): rewrite a bad bug report

> "Tried it again today and it's still broken, the screen goes weird sometimes
> when I plug things in. Might be the cable, I swapped a couple of things around
> and now it seems ok but I'm not sure."

Rewrite as: expected, observed, one hypothesis, and one proposed next step. List
what information is missing and cannot be recovered.

## What this activity does not do

It practices writing observations. Any testing happens in the emulator. It
authorizes no hardware action, and the FT232R account is history, not a
procedure.
