# Experiments and results

Each family poses a question under a different constraint. Their names describe
research directions; the implemented tests and recorded outcomes define what
has actually been demonstrated.

## The five questions

| Family | In everyday language | Detailed guide |
|---|---|---|
| 4K MIND | What can an agent preserve in a small RAM world when its conversational context resets? | [Memory and inheritance](../docs/neural1/experiments/4k-mind.md) |
| 1976 MULTIVERSE | Does a proposed machine design satisfy the historical constraints supported by reviewed sources? | [Historical design](../docs/neural1/experiments/1976-multiverse.md) |
| SELFHOST/1 | Can constructed artifacts retain ancestry and be rebuilt to the exact recorded bytes? | [Tool construction](../docs/neural1/experiments/selfhost1.md) |
| 256-BYTE UNIVERSE | Can a program meet an executable task within an exact 256-byte candidate budget? | [Small-program evaluation](../docs/neural1/experiments/256-byte-universe.md) |
| RAM REPUBLIC | How do isolated participants interact through shared memory? | [Shared-memory interaction](../docs/neural1/experiments/ram-republic.md) |

## Start with two different evidence records

| Record | Observed result | What it supports |
|---|---|---|
| [Historical Pilot 001](../docs/neural1/research/pilot-001/README.md) | Six of 45 cells completed; 156 turns produced zero strict-parser acceptances; a thermal stop left the matrix incomplete | A bounded negative result for those prompt/provider/model configurations, plus a limited resume observation |
| [September 10 Pi closeout](../docs/neural1/operations/pi-closeout-2026-09-10.md) | All five family paths were exercised; a separate post-boot run accepted eight commands across three responses | Recorded local operation and bounded family evaluations, including rejected and negative outcomes |

These records describe different runs, configurations, and purposes. Later
acceptance does not replace the historical pilot's failures.

## How to read an outcome

**COMPLETED** describes execution state. Inspect the family result to learn
whether a candidate passed its task. Parser rejection, provider failure,
insufficient historical data, and a valid negative result have different meanings.
None by itself establishes autonomous discovery or general model capability.

SELFHOST's bounded rebuild evidence does not establish compiler discovery.
A 256-byte candidate is not a complete replacement Monitor. RAM interactions
do not establish protocol emergence. The console's reviewed year-end-1976 CPU/RAM
records do not establish complete historical machine designs, missing prices,
or electrical compatibility.

Continue with [negative results](Negative-Results.md), or use the
[researcher guide](For-Researchers.md) before planning a comparison.

[Wiki home](Home.md) · [Previous: architecture](Architecture.md) · [Next: reproducing results](Reproducing-Results.md)
