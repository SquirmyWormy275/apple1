# 0. Learn by predicting, running, and explaining

This book connects the project's existing Field Library to runnable examples.
You can start with no assembly experience. Basic familiarity with files and a
terminal helps; the first commands are given below. The physical computer is a
Replica 1 Plus, while the automatic worked labs run on an ordinary host.

## Your first session

From a checkout of this repository, with Python 3.12 or newer:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,textbook]'
python -m tools.textbook list
python -m tools.textbook run S03
python -m tools.textbook run C01
```

Windows PowerShell uses `python -m venv .venv` and
`.\.venv\Scripts\Activate.ps1` for the first two commands. The `textbook`
extra supplies Pillow for image generation. Running the examples themselves
needs the project runtime dependency, Py65, and a full checkout with `tools/`
and lesson resources. The standalone wheel is not the complete course.

## The four-step method

1. **Predict.** Write the output or machine state you expect before running.
2. **Run.** Use the lab ID's command and retain its actual output.
3. **Explain.** Connect each changed byte, flag, or classification to its cause.
4. **Vary.** Change one input or instruction, predict again, and compare.

A green check only says the authored checks passed. It cannot assess every
explanation you write. The original packets add activities and answer keys;
worked companions add executable demonstrations and captured results.

## Read the evidence label

| Label | What ran | What it does not establish |
|---|---|---|
| HOST_EXERCISE | A calculation or worked classification on the host | Independent historical verification or physical behavior |
| VIRTUAL_EXECUTION | Real instruction execution in the bounded Py65-based world or RAM harness | Electrical/cycle accuracy of the Replica |
| HOST_AND_VIRTUAL | A host analogue compared with a virtual machine result | A native BASIC interpreter run |
| SYNTHETIC_SOFTWARE | Actual project logic with authored fixtures | Real-model performance or scientific discovery |
| MOCK_TRANSPORT | The real adapter with an injected response | A connection to a local model server |
| DIRECT_CPU_MODEL | Direct stepping of Py65 with explicit memory/vectors | Physical reset, IRQ or cycle behavior |
| RETAINED_NATIVE_REEVALUATION | Verification/execution of retained actual model output | New inference during the automatic lab |
| RETAINED_RECORD | Reading an existing public evidence file | Fresh inference or a current hardware health check |

All captured images are readable renders of actual stdout. They are not
screenshots of the deployed Pi console. Each image is paired with raw text,
its example source, and a hash-verifiable capture manifest.

The [course guide](../course-guide.md) supplies a twelve-session route and
assessment prompts. The [native guide](../native/README.md) explains actual
inference recordings separately from the automatic deterministic runner.

## Keep a useful notebook

For each exercise record: objective, source revision, prediction, exact change,
command, actual result, discrepancy, and interpretation. Separate "I observed"
from "I think it means." Keep a failed attempt; it may explain a later result.

Work the original activity before opening its answers. In a group, exchange
predictions before running. A reviewer should be able to reproduce the observed
result without sharing your assumptions.

## Completion check

You are ready to continue when you can explain why 42 is `$2A`, run C01, locate
its instruction bytes, and distinguish its virtual result from a live-board
observation. The [coverage register](../coverage.md) records what the book
covers and which operations still require an identified operator environment.

[Textbook home](../README.md) · [Next chapter](01-the-machine.md)
