# Negative results and lessons learned

Failures help define what the system and experiments can establish. This page
points to concrete records so an unsuccessful candidate or interrupted run is
not hidden behind a successful software launch.

## Two records worth reading

| Record | What happened | What to learn from it |
|---|---|---|
| [Pilot 001 negative results](../docs/neural1/research/pilot-001/negative-results.md) | Zero strict-parser acceptances across 156 recorded turns; a thermal stop left most planned cells incomplete | Prompt/provider/model configurations and resource limits matter; an incomplete matrix cannot establish the planned broad comparison |
| [Pi family outcomes](../docs/neural1/operations/pi-closeout-2026-09-10.md#limits-and-preserved-history) | Native operation included rejected historical designs, a negative shared-memory ending, and 256-byte coverage/behavior failures | Correct operation of an evaluator includes rejecting a candidate that fails its task |

The Pi closeout also retains earlier failed attempts, network/name-resolution
limitations, and the distinction between operational acceptance and scientific
success. Its later results do not erase the pilot.

## Record a failure so someone else can use it

Preserve the run ID, exact configuration, relevant transcript, error or result
classification, stopping reason, and available artifacts. Explain whether a
retry changes an experimental factor or simply repeats the same conditions.
Keep provider errors, parser rejections, valid negative outcomes, and unavailable
data distinguishable.

The [negative-results policy](../docs/neural1/research/negative-results.md)
defines the recording expectations. The
[researcher guide](For-Researchers.md) explains how controls and uncertainty
limit the conclusion you can draw.

[Wiki home](Home.md) · [Previous: researcher guide](For-Researchers.md) · [Next: development journal](Development-Journal.md)
