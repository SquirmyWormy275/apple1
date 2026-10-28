# Teach or study the course

Start with [chapter 0](chapters/00-how-to-use-this-book.md). You can finish the
core course on an ordinary computer, without a model download or a connected
Replica. The native recordings let you inspect real local inference separately.
A complete study pass takes multiple sessions; the estimates below include
exercises and discussion, not just reading time.

## Choose your first route

| Your starting point | First route | First observable result |
|---|---|---|
| New to programming | Chapters 0–3, S03, C01 | The program stores 42 and you find `$2A` in memory |
| Comfortable with Python, new to assembly | Chapter 4, T01–T12, A01–A06 | Copy `HELLO` and prove the destination bounds |
| Interested in local models | Chapter 7, L01–L08, N01 | Distinguish an actual generated response from its independently checked result |
| Reviewing the engineering | Chapters 8–10, F03–F16, F23–F25 | Reproduce a checkpoint/resume or export-integrity demonstration |
| Teaching or visiting a collection | Chapters 1, 11–12, H/SP/X packets | Explain what the exhibit establishes and show a sourced, bounded demo |

## A twelve-session sequence

Allow roughly 90–120 minutes per session plus independent practice. Treat the
B/R/H packet routes as additional seminars when teaching the whole library;
forty-two complete original packets take longer than twelve short meetings.
Each session has one thing a learner should be able to show without reciting
an answer key.

| Session | Reading / labs | Observable assessment |
|---|---|---|
| 1 | Chapters 0–1; S01–S04; C01 | Explain CPU, memory, program, replica and model host; run C01 |
| 2 | Chapter 2; C02–C04; X01 | Convert `$C8`, decode a character, find an operand boundary |
| 3 | Chapter 3; M01–M05; C05 | Deposit/read/run in the modeled Monitor and explain the exit |
| 4 | Chapter 4.1–4.5; T01/T02/T09; A01–A03 | Predict an indexed copy and compute a branch displacement |
| 5 | Chapter 4.6–4.8; T03–T06 | Explain C versus V and preserve a two-byte carry |
| 6 | Chapter 4.9–4.11; T07/T08/T10/T12; A04/A06 | Trace the stack, follow a pointer, and expose a boundary bug |
| 7 | Chapter 5; A05; T11; X02 | Explain empty input, 127/128-character cases and a failing sentinel |
| 8 | Chapters 6 and 13; B01–B05; U01–U06; selected R packets | Express an algorithm at two levels run real BASIC, compare it with the earlier host analogues |
| 9 | Chapter 7; L01–L08; N01; native guide | Trace prompt → parser → virtual program → verifier; explain a negative result |
| 10 | Chapters 8–9; F03/F05/F06/F08–F15/F23 | Recover a run and detect an altered exported byte |
| 11 | Chapters 10–11; F16/F24/F25/F30; H03/H04/SP01 | Explain deployment identity, storage guards and the physical boundary |
| 12 | Chapter 12; X03–X05 | Present a reproducible capstone, evidence package and limitations |

The [coverage register](coverage.md) links every original lesson and all 36
feature demonstrations. Use it for optional projects instead of implying that
one twelve-session route exhausts the library.

For the card/build extension, add chapter 14 and K01–K04 after the core route.
Use the [storyboard kit](../hardware/build-storyboard/README.md) to prepare the
physical exhibit without presenting planned photos as completed work.

## Keep prediction separate from explanation

Give learners the source and the question first. Have them write their expected
memory, stop reason or counterexample before opening the captured result. Then
run the command. A discrepancy becomes a small debugging task: identify the
first state transition that differs, change one thing, and retain both outputs.

Ask for explanations in plain language. “BNE loops” is incomplete; “CPY set Z
because Y reached five, so BNE falls through” identifies the cause. For a model
lab, “the model said it worked” is not an execution result. Ask the learner to
point to the memory readback, stop reason and boundary checks.

## Three useful assessment prompts

1. **Instruction reasoning:** A is `$7F`, C=0 and D=0. ADC #$01 gives what A,
   C and V? Answer: `$80`, C=0, V=1. Explain the signed and unsigned meanings.
2. **Boundary reasoning:** A routine writes the right five letters and returns,
   but the upper sentinel changes. Has it met the copy contract? Answer: no;
   an extra write violates an explicit requirement.
3. **Evidence reasoning:** A real local model produces no accepted Monitor
   commands under a 192-token limit. What can you conclude? Answer: this
   recorded configuration failed this task. It says nothing universal about
   that model family and does not establish physical Replica behavior.

Use the [capstone rubric](chapters/12-capstone.md#rubric-02-points-each) for a
review conversation. Scores organize feedback; a peer should also reproduce a
result from a clean checkout. No automated check can certify that a learner
understands a historical source or has explained a result correctly.

## Make the work presentable

A capstone README should state the problem, your contribution, an observed
result, a runnable first step, the important engineering decision and one
limitation. Show raw evidence beside a readable image. Give source credit and
identify whether a capture is host execution, real inference on the Pi, or a
physical measurement. A prospective employer should be able to follow the same
route as a classmate.

[Textbook home](README.md) · [Technical review](review.md) · [Native walkthrough](native/README.md)
