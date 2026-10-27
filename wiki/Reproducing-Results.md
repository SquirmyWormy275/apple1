# Reproducing results

There are three different activities here: running a software demonstration,
checking a saved evidence package, and repeating a model experiment. Choose the
one that matches your goal.

## 1. Try the repeatable software demonstration

Follow the [setup walkthrough](../docs/neural1/getting-started.md). With its
virtual environment active, run this from the checkout root:

```bash
python -m neural1.demos --out out/my-first-demo
```

Read `summary.json` in that folder. It records `serial_opened: false` and labels
itself a deterministic prototype demonstration. Choose a new folder for a
separate demo. Fixed responses exercise the software without running a model.

## 2. Verify a saved evidence bundle

For a bundle you already have, replace `BUNDLE_PATH` with its directory:

```bash
neural1 verify-bundle BUNDLE_PATH
```

Inspect the returned validity and errors. Verification checks recorded file
hashes and bundle structure; it does not rerun the model or prove a research
claim. Keep the exact source revision and reproduction instructions with the
package. Raw private Pi logs and model weights are not included in this repo.

## 3. Repeat a real-model experiment

A real campaign requires a qualified local provider and model registry. Preserve
its exact model identity, generation settings, seed, prompts, runtime revision,
snapshots, and analysis version. A template registry intentionally lacks the
metadata needed to execute a real campaign.

Begin with the [reproducibility procedure](../docs/neural1/research/reproducibility.md)
and [model qualification](../docs/neural1/research/pilot-001/reproducibility.md).
Review the [experimental controls](../docs/neural1/research/experimental-controls.md)
before making changes. Exact replay uses recorded prompt/agent/seed tuples;
missing recordings must fail rather than invent a replacement response.

The Pi's [acceptance record](../docs/neural1/operations/pi-closeout-2026-09-10.md)
identifies its installed release. A fresh source checkout does not include the
private deployment configuration, SSD state, or model store and is not a request
to repeat commissioning.

[Wiki home](Home.md) · [Previous: experiments](Experiments-and-Discoveries.md) · [Next: researcher guide](For-Researchers.md)
