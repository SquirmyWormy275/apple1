# Current project status

Updated **September 16, 2026 (Pacific time)** for the source integration and
repository cleanup. Operational statements below describe retained acceptance
records, not a new live health check.

[Project home](../README.md) · [Full project map](PROJECT-MAP.md)

## At a glance

| Workstream | Current state | Remaining work |
|---|---|---|
| NEURAL1 software | The repository includes the native Pi application, shared virtual runtime, five family paths, META/1, lifecycle controls, storage guards, and tests. | Continue bounded virtual research; distinguish operational acceptance from scientific success. |
| Commissioned Pi | September 10 closeout records usable local inference, persistent SSD state, and automatic mount/provider startup after operator SSD activation. | No reinstallation is required for this repository update. USB 2 connection speed and intermittent network/name resolution remain recorded limitations. |
| Physical Replica / FT232R | September 2 no-transmit open reproduced display corruption; root cause remains inconclusive. | Resolve reset and analog power/ground evidence through an approved instrumented procedure. |
| Propeller diagnostic preparation | PR #6 holds the bounded capture/worker preparation. | It remains separate from Pi operation and is not physical qualification. |
| Field Library | 42 existing lesson packets, including SP01, are present. The prior 41-entry index omitted the special lesson. | Keep the catalog synchronized; the earlier corpus-review and CF-card approval gates remain open. |
| Historical research | The broad March-1976 index remains research staging. The console has two separately reviewed year-end-1976 CPU/RAM records. | Do not extrapolate those bounded records into complete-board, price, electrical, or March-1976 claims. |

## NEURAL1 on the Pi

From a normal login on the already commissioned Pi:

```text
neural1
```

Use the [terminal operator guide](neural1/operations/terminal-application.md)
for commands and the [native Pi closeout](neural1/operations/pi-closeout-2026-09-10.md)
for deployment identity, startup, recovery, outcomes, and retained evidence.
The public [evidence extracts](neural1/operations/evidence/pi-closeout-2026-09-10/README.md)
remain separate from the private original records.

The closeout's post-boot run `N1-P-5898735E8998CC35` produced three responses
and eight accepted commands. It began September 10 at 20:45:39 PDT, or September
11 at 03:45:39 UTC. Those are the same run, not two power tests.

All five family paths were exercised; their scientific results were not all
positive. Rejected MULTIVERSE genomes, a negative RAM REPUBLIC ending, and
256-BYTE UNIVERSE coverage/behavior failures remain in the record. SELFHOST/1
establishes its bounded archive/rebuild result, not compiler discovery.

### Source publication is not deployment

The recorded installed application remains
`4f06e6d10bcbffca47c0f7554800972555085c78`; applied late-SSD startup wiring came
from installer revision `462ec40fdb41a5f009574b84b824442ebabd9be6`.
The source integration preserves those identities rather than claiming that
GitHub's current head has been installed on the Pi.

A fresh checkout lacks the Pi's private configuration, qualified model store,
and commissioned SSD. Do not repeat installation, formatting, model downloads,
or successful power tests solely because the source and documentation were
merged. Ordinary development uses the off-device tests and demo.

## Physical Replica and Propeller

The [troubleshooting record](troubleshooting.md) and
[September 2 packet](captures/2026-09-02-ft232r-open-analyzer/README.md) remain the
basis for the investigation. Display corruption occurred while both measured
UART channels stayed digitally high. The capture did not settle reset or analog
power/ground behavior.

[PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) is diagnostic preparation,
not evidence of a repaired board. A source merge cannot observe the display,
measure rails, qualify probe points, or authorize an unattended hardware run.
No new multimeter reading, reset trace, firmware repair, or physical acceptance
is claimed by this update.

## Research, lessons, and collection

[Historical Pilot 001](neural1/research/pilot-001/README.md) retains 45 planned
cells, six completed, 156 turns, the 102°C cooperative stop, zero strict-parser
acceptances, and zero automatic findings. The later Pi run is a separate result.

The [Field Library index](field-library/README.md) is the lesson directory and
review register. SP01, [Two Boards, One Computer](field-library/SP01-two-boards-one-computer/README.md),
was already present in the inspected main tree; the discrepancy was navigation,
not lost work. Listing all 42 lessons does not close the original corpus-review
gate or approve physical CF deployment.

The [source-ingestion policy](neural1/history/source-ingestion.md) and
[console-corpus review](neural1/history/console-corpus-review.md) retain separate
historical scopes. [Display research](peripherals/displays/README.md), the
[Sanyo accession](collection/sanyo-vm-4209-1979/README.md), and
[preservation dossier](preservation-dossier.md) retain their existing provenance
and rights qualifications.

## Repository history

[PR #8](https://github.com/SquirmyWormy275/apple1/pull/8) provides the polished
navigation; [PR #7](https://github.com/SquirmyWormy275/apple1/pull/7) integrates the
previously separate native Pi source and commissioning evidence. The earlier
[review record](repository/review-2026-09-16.md) is a dated pre-integration
snapshot, not a live list of unmerged work. Original commits and evidence remain
preserved through merge ancestry; no installed hardware state changes here.
