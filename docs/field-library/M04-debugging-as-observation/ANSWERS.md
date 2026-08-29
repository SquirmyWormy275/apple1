# M04 Answer key

## Part A: the sheet

**Expected**, from M03's recorded table:

> `screen_text` = `HI` CR, `buffer_text` = `HI` CR, `returned_to_monitor` =
> true, `instructions` = 30.

**Observed:**

> `screen_text` = `HI` CR, `buffer_text` = empty, `returned_to_monitor` = true.

**The difference is one field.** Everything else matched. That is a strong
result, because it rules out most of the program: the keyboard read worked, the
echo worked, the comparison against carriage return worked, and the exit worked.
Only the store misbehaved.

**A good hypothesis:**

> I think the cause is a wrong address in the `STA` instruction. If I am right,
> then examining the three bytes at offset 10 in the listing should show
> something other than `99 00 04`, and correcting it should restore the buffer
> field, and nothing else should change.

Accept any hypothesis that names a specific cause, predicts a specific
observation, and could be shown false.

## Part B: is it a hypothesis?

| # | Usable? | Why |
|---|---|---|
| 1 | **Not usable** | Names no cause and predicts nothing. It restates the symptom. |
| 2 | **Usable** | Specific, checkable, and falsifiable by reading three bytes. |
| 3 | **Not usable** as stated | Might be true, but it predicts nothing and is unfalsifiable in this form. It becomes usable as "the harness writes to the wrong buffer offset, so the same bytes on another 6502 simulator would store correctly." |
| 4 | **Usable** | Specific and checkable. Note it also predicts a *second* symptom, a wrong instruction count, which the observation contradicts. So it is usable and probably already refuted, which is exactly what a good hypothesis does for you. |
| 5 | **Not usable** | And in this case impossible: no hardware was involved in the run. |
| 6 | **Usable** | Specific and checkable, and it would explain the count but not the empty buffer. |

The instructive pair is 4 and 6: both are usable, and both are partly refuted by
evidence already in hand. Noticing that before testing saves the test.

## Part C: how many things changed

| # | Things changed | Interpretable? |
|---|---|---|
| 1 | Zero | **Yes.** Reproduces or fails to reproduce, which is real information. |
| 2 | One | **Yes.** The best case. |
| 3 | Three | **No.** If it works you cannot say which change mattered, and you may have masked one fault with another. |
| 4 | One | **Yes.** Same as 2, and the phrasing makes explicit that input and machine were held constant. |

## Part D: STOP or continue

| # | Answer | Rule |
|---|---|---|
| 1 | **Continue** | Software discrepancy in an emulator. Record it as a software issue and investigate. No machine state exists. |
| 2 | **STOP** | "If the display changes." |
| 3 | **STOP** | "Or bytes mismatch." |
| 4 | **STOP** | "A reset occurs." |
| 5 | **STOP** | "Identities drift." |
| 6 | **Continue** | Your model was wrong, which is a finding, not an incident. Consistent behavior is the good case. |

The line between 1 and the rest is whether a physical machine is in a state
somebody has to recover. Emulator surprises are puzzles. Machine surprises are
incidents.

## Part E: the worked STOP

1. **Opening the FT232R serial device from the host garbled the display.**
2. **"If the display changes."** The first condition in the rule.
3. **It was recorded, and the session ended.** Further opened serial sessions and
   transmit tests were blocked pending a measurement test card and an explicit
   operator start.
4. **Any two of:** opening it again to see whether it reproduced; swapping the
   cable and retrying; changing baud rate and retrying; power-cycling and
   carrying on with the planned test sequence. Each replaces a clean single
   observation with a muddle.
5. **Because it was recorded intact at the time,** with what was done and what
   was seen, and nothing was changed afterwards that would make the record
   ambiguous. A preserved observation stays evidence. A disturbed one becomes an
   anecdote.

## Part F: rewrite a bad bug report

One version:

> **Expected:** [not recorded]
> **Observed:** On an unrecorded date, the display showed unexpected output at
> some point during or after connecting an unspecified device.
> **Hypothesis:** None stated. "Might be the cable" names no mechanism.
> **Next step:** None possible from this report.

**Missing and unrecoverable:** the date and time; what exactly was connected and
in what order; what was on the display before; what "goes weird" means
specifically; how many things were swapped and which; whether the current
apparently-working state is the original configuration or a different one.

The last item is the worst. After "swapped a couple of things around," nobody
knows what the machine is now, so even the working state is not a known state.

## Try a variation

The smallest test for the address hypothesis is to **read the bytes**, not to
change anything: look at the three bytes where the `STA` should be. That costs
nothing and cannot break anything.

**What would make you abandon it:** finding `99 00 04` exactly as expected. Then
the store instruction is right and the fault is elsewhere.

## README: Check your understanding

1. **Because memory reshapes itself around what you saw.** After the fact you
   will sincerely believe you expected something closer to the result than you
   did. Writing first is the only way to hold the two apart.
2. **It is a conclusion, not an observation, and it is not specific enough to
   rule anything out.** "The buffer field was empty while the screen field was
   correct" eliminates most of the program in one sentence. "It does not work"
   eliminates nothing.
3. **That changing that byte changes that symptom.** Not that you have found the
   cause, and not that the program is now correct. Those need separate arguments.
   A change that makes a symptom vanish can also be masking it.
