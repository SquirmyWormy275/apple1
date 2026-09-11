# Local Codex handoff: ready the Propeller measurements

Updated: the bounded live capture runner is now implemented. Follow the
[unattended capture setup](propeller-unattended-capture.md) to deploy and rehearse
it on P1/Pi, perform the first attended checkout, and then launch one qualified
unattended job. Hardware qualification has not happened in the cloud session.

Run this task in local Codex on **strathex-P1**, in the existing Apple1 checkout.
Repository: https://github.com/SquirmyWormy275/apple1
Preparation PR: https://github.com/SquirmyWormy275/apple1/pull/6
Branch: work/propeller-overnight-preparation-2026-09-11

## First instruction

Read the current PR and fetch its branch, preserving all local changes and using
an isolated worktree if necessary. Read this handoff, the completed
[preparation report](propeller-overnight-report-2026-09-11.md), the
[reset/power reference](propeller-reset-power-reference.md), and the
[next-session card](../captures/propeller-reset-power-next-session.md).
Complete host-side readiness now, then identify exactly which physical checks
need Alex. Do not repeat the completed research or the old two-channel test.

## Host-side work that can run unattended

- Verify repository head and the new helpers. Use the established Python
  environment or a project-local virtual environment. Rehearse using a fresh
  output directory with the command below. Nothing needs to be attached.
- If the analyzer is attached to the P1, inspect its USB descriptors, driver,
  permissions, sigrok-cli version, and reported capabilities. The prior unit was
  SparkFun TOL-18627 / 0925:3881 / fx2lafw. Inspect only that analyzer; a broad
  scan that could open serial adapters is inappropriate. Do not start a physical
  capture while probe placement is unknown.
- Verify existing configured SSH access to the intended Pi only if available.
  Record host identity, project path, and versions without exposing credentials
  or reconfiguring NEURAL1 services. On the confirmed Pi, inspect serial symlinks
  and use the existing serial_owner.py **probe** command if its source still
  confirms that it never opens the device.
- Compare by-id and by-path to the historical record. Serial 00000000 is not
  unique. Report any changed topology; do not silently substitute ttyUSB0 or
  change the recorded binding.
- Save concise readiness results and the exact missing physical evidence to
  the task branch. Preserve concurrent changes. No live session or automatic
  retry is part of unattended readiness.

From the repository root (choose a fresh output path for each run):

```bash
python -m tools.propeller_rehearsal --out out/propeller-local-rehearsal
python -m tools.propeller_capture_job rehearse --out out/propeller-controller-rehearsal
```

The first command runs six original synthetic scenarios with the real
SerialOwner class and a fake transport. The second runs ten scenarios through
the production capture controller and synthetic subprocesses. Neither constructs
a live serial backend. A successful
rehearsal does not validate host USB throughput, SSH timing, physical probes,
power, or the board's behavior.

## Physical work with Alex

The first concrete task is to match the board/breakout to the newly located
Revision 0 drawing, then locate a secure **Propeller RST/RESn** probe point.
The drawing shows U7 pin 11/Q1 collector on RST, and a distinct RESET net for
the 6502/6821. It depicts DTR coupling through C9/Q1; the previous observation
of four installed conductors needs to be checked against this drawing.

Ask for current top/bottom breakout and U7/Q1/C9/R10 photos and power-off
continuity checks. Resolve what the voltage selector actually switches.
Do not instruct Alex to move it solely because the old record and generic
manufacturer instructions disagree.

Keep the analyzer USB on the P1 and Replica FT232R USB on the Pi for the initial
comparison. Establish real rail/ground/probe suitability before a new attended
no-transmit open. The prepared card supplies acquisition and recovery steps;
only proceed to that live action with Alex present and the setup verified.

## Expected handback

Provide current repository commit, P1/analyzer/Pi readiness, verified physical
mapping versus unresolved candidates, selector/supply findings, and the exact
next action. If physical access is missing, complete all host-side work and
stop at that specific dependency. No firmware load or EEPROM write is included.
