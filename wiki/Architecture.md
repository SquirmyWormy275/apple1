# How the software fits together

The key design choice is to check execution independently of model-generated
claims. Model output is a proposal; the virtual world and experiment evaluator
produce the result that can be inspected.

```text
Experiment settings + model identity + seed
                    |
                    v
          Model proposes commands
                    |
                    v
          Parser checks the response
                    |
                    v
       Bounded virtual Apple-1 executes
                    |
                    v
     Family evaluator checks the outcome
                    |
                    v
  Transcripts + checkpoints + evidence records
                    |
                    v
          META/1 and verified exports
```

## Follow the implementation

| Layer | Responsibility | Read the code |
|---|---|---|
| Model adapters | Bound requests and support local, fixed-response, and replay providers | [models.py](../neural1/models.py), [provider_factory.py](../neural1/provider_factory.py) |
| Virtual world | Enforce the modeled memory and execution interface | [world.py](../neural1/world.py) |
| Experiment logic | Define family objectives and deterministic evaluations | [family_runner.py](../neural1/family_runner.py), [experiments.py](../neural1/experiments.py) |
| Runtime and campaigns | Identify runs, preserve snapshots, checkpoint progress, and resume | [runtime.py](../neural1/runtime.py), [campaign.py](../neural1/campaign.py) |
| Evidence and export | Persist claim relationships and verify bundled files | [meta_store.py](../neural1/meta_store.py), [bundle.py](../neural1/bundle.py) |
| Operator application | Select models, manage workers, check resources, and inspect results | [application.py](../neural1/application.py), [deployment.py](../neural1/deployment.py) |

The execution harness builds on [Py65](https://github.com/mnaberez/py65).
The project adds its constrained world, experiment controls, application,
evidence system, and lesson tooling. It does not claim electrical or
cycle-accurate emulation of the Replica.

## Why one shared runtime?

All five experiment families use common model records, snapshots, manifests,
and evidence conventions. That makes comparisons and recovery easier to inspect
than maintaining unrelated implementations for each experiment.
The [shared-runtime decision](../docs/neural1/decisions/ADR-0001-shared-virtual-runtime.md)
records the rationale.

For a deeper review, use the [system overview](../docs/neural1/architecture/system-overview.md),
[repository architecture](../docs/repository/architecture.md), and
[engineering highlights](Project-Highlights.md). For the commissioned Pi's actual
storage and startup behavior, use the
[deployment closeout](../docs/neural1/operations/pi-closeout-2026-09-10.md).

[Wiki home](Home.md) · [Previous: what is NEURAL1?](What-is-NEURAL1.md) · [Next: experiments](Experiments-and-Discoveries.md)
