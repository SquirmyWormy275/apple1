# What is NEURAL1?

NEURAL1 is a lab for studying what small language models can do with a very
limited computer interface. Instead of receiving a modern shell or a large
software library, an experimental agent uses modeled Apple-1 Monitor commands
to inspect memory, deposit bytes, and run programs.

The models run on a modern host, such as the Raspberry Pi. Their programs run
in a virtual Apple-1 world. An ordinary Apple-1 does not run the language model.

## A small example

A model might propose bytes that store a number in memory. The runtime executes
the bytes and records what happened. If the model says it succeeded but the
memory or execution result disagrees, the execution record determines the result.

The [first demonstration](../docs/neural1/getting-started.md) makes this concrete:
a fixed test program stores 42, and a second participant reads `2A`, its
hexadecimal representation. Fixed responses make that demo repeatable without
downloading a model.

## Four parts of the project

| Name | Meaning |
|---|---|
| COMPUTER | Ordinary Apple-1 computing, independent of AI or a required Pi |
| Field Library | Lessons, activities, sources, and explanations |
| NEURAL1 | The virtual experimental runtime and its five experiment families |
| META/1 | A persistent record of claims, their evidence, and review work |

## Words you will see

- A **run** is one recorded execution; a **campaign** groups experiment settings and cells.
- A **transcript** contains commands, model responses, and recorded observations.
- A **snapshot** records virtual machine state; a **checkpoint** records progress for resuming work.
- A **provider** connects the runtime to a real model, fixed test responses, or an exact recording.
- A **bundle** packages evidence with hashes so later inspection can detect changes.

## What has been demonstrated?

The runtime, console, and five experiment paths are implemented. The
[Pi closeout](../docs/neural1/operations/pi-closeout-2026-09-10.md) records native
local inference and recoverable operation. The
[experiment guide](Experiments-and-Discoveries.md) explains the results separately
from the research ambitions. Scientific discovery, a complete replacement
Monitor, and physical Replica qualification are not established by these runs.

For the detailed description, see the [NEURAL1 overview](../docs/neural1/README.md).
The [initial methods report](../docs/neural1/publications/technical-report.md)
is a dated foundation document, not a current deployment report.

[Wiki home](Home.md) · [Previous: first demonstration](../docs/neural1/getting-started.md) · [Next: architecture](Architecture.md)
