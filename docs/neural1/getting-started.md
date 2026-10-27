# Your first five minutes with NEURAL1

NEURAL1 lets you explore a virtual Apple-1 and study how small language models
work within its limits. Start with a recorded, repeatable demonstration. You
need Python 3.12 or newer and a checkout of this repository; you do not need a
Pi, model download, or physical Apple-1 connection.

[Project home](../../README.md) · [Current status](../STATUS.md) ·
[Full operator guide](operations/terminal-application.md)

## 1. Prepare a development checkout

Open a terminal in the repository root, where `pyproject.toml` lives. On Linux
or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate the environment with
`.\.venv\Scripts\Activate.ps1` instead of `source .venv/bin/activate`.
If this checkout already has an installed development environment, activate it
and skip creating another one.

Use the checkout and editable installation for this walkthrough. The standalone
wheel does not include the lesson documents, historical data, or emulator helper
needed by all features.

## 2. Run the demonstration

From the same repository root:

```bash
python -m neural1.demos --out out/my-first-demo
```

The command prints a run ID, a path ending in `summary.json`, and
`"serial_opened": false`. It creates files under `out/my-first-demo`. Choose a
new output folder when you want to retain a separate demonstration.

This uses fixed test responses in place of a language model. It exercises the
software and virtual execution; its results are labeled **DETERMINISTIC
PROTOTYPE DEMO - NOT A RESEARCH FINDING**.

## 3. Read one result

Open `out/my-first-demo/summary.json` in your text editor. Start with these fields:

| Field | What to look for |
|---|---|
| `4k_mind.transcript` | One participant deposits and runs bytes; another reads the result at `0300`. The value `2A` is hexadecimal for 42. |
| `field_library.deterministic_evidence` | The virtual program echoes `HI`, uses 30 instructions, and returns to the modeled Monitor. |
| `serial_opened` | `false`: this demonstration did not open a physical serial connection. |
| `label` | The evidence class. A passing software demonstration is not a model research finding. |

A **transcript** records commands and replies. A **checkpoint** saves progress
so a run can continue. A **campaign** groups experiment runs with their settings.
**META/1** connects claims to their evidence and records what still needs review.

## 4. Explore a first lesson

Read [What is an Apple-1?](../field-library/S01-what-is-an-apple-1/README.md),
then [Your first hex number](../field-library/S03-your-first-hex-number/README.md).
The [Field Library index](../field-library/README.md) lists lesson levels,
estimated times, and prerequisites. You can read these files without running a
model or configuring the Pi.

## If you are using the already commissioned Pi

The Pi console uses its installed deployment configuration and SSD. Launch it
with `neural1`; do not repeat installation to follow this guide.

Start by exploring without launching an experiment:

```text
HELP 1
STATUS
LESSONS
SOURCE S01
```

When ready, enter `1` to select 4K MIND and `START` to begin its bounded preset.
Use `RUNS` to find its run ID, then replace `run-id` below with that exact ID:

```text
SHOW run-id
TRANSCRIPT run-id
```

Read the family evaluation as well as the run state: **COMPLETED** means the
execution finished, and may include a rejected candidate or negative result.
`STOP run-id` requests cancellation. `QUIT` closes the console while an active
run continues in its user service.

Interactive results use readable labels and adapt to the terminal width.
`neural1 console --retro` uses 40-column prose; IDs, hashes, and paths stay whole
for copying. `neural1 console --json` shows raw JSON. One-shot
`neural1 console --command STATUS` continues to return JSON for scripts.

## If something goes wrong

- **No deployment configuration:** use the model-free demonstration above on a
  development checkout. The interactive console expects a configured Pi. For
  an existing deployment with a different config location, use
  `neural1 console --config /path/to/config.json`.
- **File or directory not found:** check the filename and your working directory.
  Run the demonstration from the repository root.
- **Unrecognized console command:** type `HELP`, or `HELP START` for an example.
  Commands with missing or extra arguments are rejected before execution.
- **Need troubleshooting details:** add `--debug`, for example
  `neural1 console --debug`, to retain the exception traceback.

For further work, use the [operator guide](operations/terminal-application.md)
or [experiment overview](README.md). Physical Replica testing has its own
[troubleshooting record and evidence requirements](../troubleshooting.md).
