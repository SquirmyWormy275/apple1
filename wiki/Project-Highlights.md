# Project highlights: engineering and evidence

**Project by [Alex Kaper](https://github.com/SquirmyWormy275).** This page is a
short technical review of the problem, the implemented work, and the evidence
available to inspect. Start with the [demonstration](../docs/neural1/getting-started.md)
if you want to run an example first.

## The problem

A language model can describe a successful program without producing one.
NEURAL1 makes that distinction inspectable: models work through a constrained
virtual Apple-1 interface, and deterministic execution and family evaluators
check their proposals. The surrounding collection and lesson material make
the historical computer understandable to readers as well as to experimenters.

## Project scope and contribution

The work combines a shared Python runtime, local-model adapters, experiment
policies, recoverable campaign execution, a persistent evidence system,
Linux/Pi deployment tooling, and a source-grounded educational library.
Collection preservation, display research, and the R04 enclosure design form
related workstreams with their own records.

The virtual execution harness uses the third-party Py65 6502 emulator. The
project's constrained world, campaign/application logic, evidence layer, and
lesson integration sit around that dependency. Original Apple-1 architecture,
preserved manuals, model weights, and reference artwork are not claimed as
original project inventions.

## Decisions you can inspect in the code

| Engineering problem | Approach | Implementation and checks |
|---|---|---|
| Model text can claim success without valid execution | Restrict the command surface; evaluate actual machine behavior separately | [Virtual world](../neural1/world.py), [family evaluator](../neural1/family_runner.py), [runtime tests](../tests/test_neural1_runtime.py) |
| Model work may be interrupted or restarted | Save atomic checkpoints, retain transcripts and snapshots, and resume with the recorded effective registry | [Campaign engine](../neural1/campaign.py), [resume regression tests](../tests/test_neural1_resume_protocol.py) |
| A deployment can lose its storage or exhaust resources | Verify storage identity and paths, supervise bounded workers, and refuse fallback writes | [Deployment checks](../neural1/deployment.py), [application](../neural1/application.py), [storage tests](../tests/test_deployment_storage.py) |
| A result needs a traceable basis | Link claims to evidence, retain content hashes, and verify export contents | [META persistence](../neural1/meta_store.py), [bundles](../neural1/bundle.py), [bundle tests](../tests/test_neural1_campaign_bundle.py) |
| New readers need an approachable first step | Provide a model-free walkthrough, ordered lesson packets, contextual help, and readable console output | [Walkthrough](../docs/neural1/getting-started.md), [Field Library](../docs/field-library/README.md), [console tests](../tests/test_neural1_console_usability.py) |

The [architecture guide](Architecture.md) connects these modules into one flow.
The [off-device CI workflow](../.github/workflows/ci.yml) checks lint, types,
tests, repository links/schemas/provenance, a deterministic demo, and tracked-file
cleanliness. [GitHub Actions](https://github.com/SquirmyWormy275/apple1/actions/workflows/ci.yml)
provides the run-specific results.

## Recorded outcomes

- **Native local inference:** the September 10 Pi closeout records a post-boot
  Phi4-mini run with three responses and eight accepted commands. Independent
  replay matched its recorded program output. See the
  [run evidence](../docs/neural1/operations/pi-closeout-2026-09-10.md#post-boot-run-and-hashes).
- **Recovery and startup:** the closeout records cancellation/same-ID resume,
  persistent META/export reopening, refusal when the expected SSD was absent,
  and provider startup after the operator connected the SSD. See
  [storage and recovery](../docs/neural1/operations/pi-closeout-2026-09-10.md#storage-startup-and-recovery).
- **Honest negative results:** Pilot 001 retained six completed cells out of 45,
  a thermal stop, and zero strict-parser acceptances across 156 turns. See
  [the report and its interpretation](../docs/neural1/research/pilot-001/README.md).
- **Educational material:** the [Field Library](../docs/field-library/README.md)
  contains 42 packets with source notes, activities, answers, and review status.
  Catalog presence does not imply all packets passed review or physical deployment.

These are bounded observations from retained records, not a current hardware
health check or a broad scientific-discovery claim. Public extracts omit private
configuration and raw private logs; their
[evidence index](../docs/neural1/operations/evidence/pi-closeout-2026-09-10/README.md)
explains the relationship to retained originals.

## Remaining work and tradeoffs

The Apple-1 execution target remains virtual, and the physical Replica serial
fault is unresolved. Checkout-based installation supplies resources omitted by
the standalone wheel. Reviewed historical CPU/RAM records are intentionally
small; missing historical prices stay unknown. The R04 design retains fitting
checks. Source usability improvements require separate deployment before they
exist on the commissioned Pi.

The [current-status page](../docs/STATUS.md) distinguishes these workstreams.
[Negative results](Negative-Results.md) and the
[researcher guide](For-Researchers.md) explain why successful execution alone
does not establish a scientific finding.

[Wiki home](Home.md) · [Next: architecture and source tour](Architecture.md) · [Try the demonstration](../docs/neural1/getting-started.md)

## Teaching backed by execution

The expanded [textbook](../docs/textbook/README.md) includes 100 runnable labs,
raw captures, exercises and worked answers. Its [technical review](../docs/textbook/review.md)
records assembler, retrieval and teaching corrections discovered during use.
[Native Pi verification](../docs/textbook/validation/README.md) reproduced every
lab and passed the full 439-test suite. Fresh model records retain successful
tutoring, rejected proposals and the source changes behind a corrected answer.
