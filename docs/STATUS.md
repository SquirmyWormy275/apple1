# Current project status

Reviewed **September 16, 2026 (Pacific time)**. This page is the current reading
guide, not a new hardware test. Statements about operation below refer to the
recorded runs and closeouts, not a live health check of the Pi or Replica.

[Project home](../README.md) · [Full project map](PROJECT-MAP.md)

## At a glance

| Workstream | Recorded state | What remains |
|---|---|---|
| NEURAL1 virtual foundation on `main` | Runtime, five experiment prototypes, META/1, campaign tooling, deterministic demos, and tests are present. | Keep software evidence distinct from model and hardware evidence. |
| Native Pi application | September 10 closeout records usable Pi-hosted NEURAL1 with local inference, persistent SSD state, and all five family paths exercised and checked. | Review and integrate the preserved Pi branch; it was not on `main` at this review. |
| Physical Replica / FT232R | September 2 no-transmit open reproduced display corruption. Root cause remains inconclusive. | Resolve the reset/power evidence gap through a separately approved, instrumented procedure. |
| Propeller diagnostic preparation | PR #6 contains bounded capture/worker preparation and its reported software checks. | Review the implementation and qualify the actual setup before any unattended run. |
| Field Library and historical research | The existing library index says 41 lesson packets; the Pi closeout reports 42 lessons including SP01. The broad 1976 research index remains staging. | Reconcile the index count against the actual catalog, rather than assuming a branch-specific missing lesson. Preserve outstanding corpus review and CF-card approval boundaries. |

## NEURAL1 on the Pi

The [native Pi closeout at the reviewed revision](https://github.com/SquirmyWormy275/apple1/blob/32102a1ad46210c4792680293d136cf0719f8fe7/docs/neural1/operations/pi-closeout-2026-09-10.md)
is the operator and acceptance record. It reports:

- Normal launch with `neural1` from any directory on the commissioned Pi, using
  its local provider rather than a laptop daemon.
- Persistent models, runs, META/1, exports, and recovery material on the dedicated
  SSD; missing or wrong storage refuses work rather than falling back to microSD.
- Automatic mounting and provider startup after the operator connected/activated
  the SSD during the documented power test, without manual mount or service-start
  commands.
- A genuine post-boot run, `N1-P-5898735E8998CC35`, with three model responses and
  eight accepted commands. Execution and independent replay are described in the
  closeout; command acceptance alone is not a scientific-discovery claim.

That run began September 10 at 20:45:39 PDT, which is September 11 at 03:45:39 UTC.
The date difference is timezone conversion, not a second power test.

All five family paths were exercised, but their scientific outcomes are not
uniformly positive. The record retains rejected MULTIVERSE genomes, a negative
RAM REPUBLIC ending, and 256-BYTE UNIVERSE coverage/behavior failures. SELFHOST/1
establishes the bounded archive/rebuild result described there, not discovery
of an assembler or compiler.

### Source branch is not deployed release

| Role | Exact revision |
|---|---|
| `main` inspected for this review | `2c40f1c5c63a083184eb724df4500cd1427bd3d2` |
| Pi completion branch initially inspected | `32102a1ad46210c4792680293d136cf0719f8fe7` |
| Pi review head after the formatting-only CI fix | `63012aca3eadeac6ab401399cd51e2c99fe840f2` |
| Installed Pi application in the closeout | `4f06e6d10bcbffca47c0f7554800972555085c78` |
| Late-SSD startup installer change applied there | `462ec40fdb41a5f009574b84b824442ebabd9be6` |

At initial inspection, `neural1/pi-completion-r3` was **40 commits ahead and zero
behind** `main`, across 59 changed files. Its work is now exposed in
[draft PR #7](https://github.com/SquirmyWormy275/apple1/pull/7). One subsequent
commit removed an extra blank line in a test import block, bringing the branch
to 41 commits ahead without changing runtime or test semantics. The resulting
[Pi PR validation run](https://github.com/SquirmyWormy275/apple1/actions/runs/35183942893)
passed all steps. This is software validation, not a new device acceptance run
or a complete implementation review. The PR remains draft and unmerged.

Use the pinned closeout's terminal guide and recovery notes for the deployed
application. Do not repeat installation, model downloads, storage formatting,
or successful power tests merely because publication and integration lagged.

## Physical Replica and Propeller

The [troubleshooting record](troubleshooting.md) and
[September 2 evidence packet](captures/2026-09-02-ft232r-open-analyzer/README.md)
remain the basis for the physical investigation. Display corruption was
reproduced while the two recorded UART channels stayed digitally high. Reset
and analog power/ground behavior were not resolved by that capture.

[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) is preparation for a
bounded, better-instrumented diagnostic. It is not evidence that the proposed
procedure has been physically qualified or that the board has been repaired.
No new meter readings, reset capture, or successful firmware repair are claimed
by this documentation review.

A runnable Pi does not qualify the Replica link. Keep the virtual experiment
path usable while this separate hardware issue is resolved.

## Research and collection boundaries

[Historical Pilot 001](neural1/research/pilot-001/README.md) remains 45 planned
cells, six completed, 156 recorded turns, a 102°C cooperative stop, zero strict
parser acceptances, and zero automatic scientific findings. The later Pi run is
a separate result, not a correction to those observations.

The [1976 source-ingestion policy](neural1/history/source-ingestion.md) still
separates the broad staged corpus from reviewed runtime claims. The Pi branch's
console corpus must be reviewed on its own merits; it does not promote the
entire historical index. Unknown prices remain unknown.

[Display research](peripherals/displays/README.md), the
[Sanyo accession](collection/sanyo-vm-4209-1979/README.md), and
[preservation records](preservation-dossier.md) keep their existing evidence and
rights qualifications. This review does not establish new physical measurements,
photo custody, collection provenance, or artwork permissions.

## Next work, in order

1. Review the Pi implementation in PR #7, then integrate it only with merge
   authorization. Reconcile its README addition with the polished navigation
   rather than dropping either. Update this page after integration.
2. Keep PR #6 separate. Its next physical step needs the actual setup and an
   explicitly approved qualification procedure, not another uninstrumented open.
3. Continue learning, virtual experiments, and source review without waiting for
   physical Replica commissioning. Preserve raw evidence and negative outcomes.

The [repository review record](repository/review-2026-09-16.md) holds the audit
scope and preservation checks behind this summary.
