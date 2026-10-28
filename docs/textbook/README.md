# Apple-1, Replica 1 Plus, and local models: a worked textbook

Learn the machine, write and debug small 6502 programs, and understand how
NEURAL1 connects local-model proposals to independently checked execution.
Start without assembly experience; build toward a reproducible capstone.

**This edition:** 13 teaching chapters, all 42 existing Field Library packets
with worked companions, eight new local-model labs, and 36 feature walkthroughs.
Twelve extended CPU labs add pointers, flags, multi-byte arithmetic, calls,
branch limits and original-program boundary cases. Native evidence labs
connect actual local inference to independently checked execution.
All 100 catalog examples have executable source, actual stdout, checks,
a captured image, a practice variation, and a worked answer.

[Course and teaching guide](course-guide.md) · [Fresh native walkthrough](native/README.md) · [6502 desk reference](reference/6502.md) · [Technical review](review.md) · [Pi verification](validation/README.md)

[Begin chapter 0](chapters/00-how-to-use-this-book.md) · [Coverage and evidence modes](coverage.md) · [Original lesson index](../field-library/README.md) · [Project home](../../README.md)

## Start with one observable result

From the checkout root with your Python environment active:

```bash
python -m pip install -e '.[dev,textbook]'
python -m tools.textbook run C01
python -m tools.textbook run L04
```

C01 executes a known program that stores 42. L04 shows which parts of a model-like
response the real parser accepts. The latter is an authored fixture, not real
inference. [Setup and evidence labels](chapters/00-how-to-use-this-book.md)
explain how to read every capture.

## Read in order

| Chapter | What you will be able to do |
|---|---|
| [0. Learn by predicting, running, and explaining](chapters/00-how-to-use-this-book.md) | Set up, predict, run, explain, and label evidence |
| [1. Build a mental model of the machine](chapters/01-the-machine.md) | Separate the CPU, memory, I/O, replica, and virtual world |
| [2. Numbers, bits, and characters](chapters/02-numbers-and-characters.md) | Read bytes, signed offsets, characters, and arithmetic flags |
| [3. Use the Monitor and execute your first program](chapters/03-monitor-and-first-program.md) | Deposit, inspect, execute, and exit a modeled program |
| [4. Write assembly as controlled state changes](chapters/04-assembly-and-control-flow.md) | Use addressing modes, branches, loops, calls, and traces |
| [5. Connect input, memory, and visible output](chapters/05-input-output-and-debugging.md) | Follow keyboard input through a buffer to visible output |
| [6. Express the same idea at different levels](chapters/06-algorithms-basic-and-creative-computing.md) | Design algorithms, compare language levels, and model creative programs |
| [7. Understand a local language model before connecting it](chapters/07-local-models.md) | Explain tokens, weights, context, identity, providers, and bounded generation |
| [8. Ask questions the evaluator can answer](chapters/08-experiments-and-controls.md) | Define tasks, negative controls, and proportional conclusions |
| [9. Make a run recoverable and a claim inspectable](chapters/09-campaigns-evidence-and-recovery.md) | Checkpoint, resume, export, verify, and trace claims to evidence |
| [10. Understand deployment without confusing it with a lab](chapters/10-pi-operation-and-feature-reference.md) | Understand installed Pi lifecycle, storage, guards, and operator boundaries |
| [11. Preserve the evidence and teach it accurately](chapters/11-preservation-and-teaching.md) | Preserve sources, interpret historical claims, and teach accurately |
| [12. Build an inspectable constrained-computing exhibit](chapters/12-capstone.md) | Build and assess an inspectable capstone |

## Use the book as a course

Follow the original lesson prerequisites inside each topic, rather than treating
alphabetical filename order as a dependency order. For example, C05 assumes C01, C02, and C03; its arithmetic exercise builds on
those earlier representations and state concepts. The routes below group the
material, and capstones come after their required skills.

| Route | Lesson order |
|---|---|
| Foundations | S01, S02, S03, S04, C01, C02, C03, C04, C05 |
| Monitor and assembly | M01, M02, M03, M04, M05, A01, A02, A03, A04, A05, A06 |
| Algorithms and creative work | B01–B05, R01–R05; follow each packet's prerequisites |
| History and collection | H01–H06, then SP01 after its CPU/Monitor prerequisites |
| Local models | L01–L08, supported by F03/F04/F13/F15/F21/F28 |
| Capstone | X01–X05 after their stated prerequisites; chapter 12 supplies a review rubric |

The [full coverage register](coverage.md) links every original packet, companion,
local-model lab, feature lab, public command surface, and operator-only procedure.

## Capture, verify, and extend

```bash
python -m tools.textbook list
python -m tools.textbook capture --out out/my-textbook-captures --images
python -m tools.textbook verify out/my-textbook-captures --rerun
```

Use a new output directory. The tool refuses to overwrite existing captures.
The [committed manifest](captures/manifest.json) records source identities and
stdout/image hashes. `verify --rerun` checks every catalog example against their
captured text. `build-pages` regenerates worked guides from the reviewed catalog,
example source, and committed outputs; it is an authoring command, not a learner
prerequisite.

## What completion means here

The host book covers every original lesson and the implemented feature surface.
Its modes include real bounded virtual execution, authored fixtures, direct CPU
semantics and offline inspection of actual local-model output. The separate
[native chapter](native/README.md) retains fresh observations, including failed
proposals, rather than treating generated text as proof of success.

A native BASIC interpreter, physical Replica acceptance, historical source
clearance and the unfinished physical launcher are not established by these
captures. Their status stays explicit in the [review record](review.md), the
[coverage boundaries](coverage.md#operator-and-environment-dependent-work) and
the [physical-session chapter](reference/physical-session.md). The course is
usable without waiting for the physical setup; a measured hardware chapter can
be added when that setup is available.
