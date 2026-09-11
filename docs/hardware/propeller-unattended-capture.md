# Propeller capture job: local setup and unattended operation

Status: IMPLEMENTED AND SOFTWARE-TESTED; NOT YET QUALIFIED ON ALEX'S HARDWARE.
This follow-on implements Alex's request to prepare testing while he sleeps.
The cloud session has not connected to P1/Pi or launched a hardware test.

The job performs one 12-second passive baseline and one 30-second event capture
at 4 MS/s. It invokes the existing serial owner once, with no transmit. It saves
raw samples, derived sigrok files, owner evidence, and a report, then exits.
There is no overnight loop, scheduled duplicate, automatic retry, firmware load
to the Replica, or remote reset operation.

## Connections and physical prerequisites

| Item | Connection |
|---|---|
| Analyzer USB | strathex-P1 |
| CH0 / D0 | Verified FT232R TX-O point |
| CH1 / D1 | Verified FT232R RX-I point |
| CH2 / D2 | Verified Propeller RST/RESn point |
| Analyzer ground | Verified board ground and analyzer ground contact |
| Replica FT232R USB | Existing Pi host connection |
| P1 to Pi | Existing verified SSH connection |

This runner deliberately uses the three required channels only. Optional DTR
and PHI0 measurements need a separately reviewed configuration change; do not
add them and assume the qualification still applies. The binary layout is one
byte per sample, with D0/D1/D2 in bits 0/1/2; other bits are not interpreted.

Before the first live cycle, complete the
[physical reference](propeller-reset-power-reference.md) and
[attended card](../captures/propeller-reset-power-next-session.md). Record actual
board/breakout identification, power topology, selector function and measured
rails, secure probe locations, ground continuity, RST continuity, DTR routing
finding, display state, and the physical Reset recovery in a setup record.
Include paths/hashes for the supporting photos and measurements. Do not fill
these from the generic schematic as though they were observations.

The runner cannot inspect the display, establish probe contact, measure rail
amplitude, press Reset, or power the board off. A constant digital high is not
proof of a correctly connected probe. The first live cycle therefore remains
attended. If it corrupts the display, it does not qualify an unattended open.

## Work local Codex can complete now

1. Fetch [PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) into an isolated
   worktree if the existing checkout has local changes. Read this file and the
   actual helpers. Preserve NEURAL1 deployment and services.
2. Confirm Python 3.12+ on both machines. The Pi needs pyserial 3.5. The optional
   dependency is `.[hardware]`; install it in a dedicated project environment if
   needed, rather than altering a running NEURAL1 environment. Both machines
   need the same `serial_owner.py` and `propeller_remote_owner.py` bytes. The
   worker checks them before opening. Commands run from the checkout root.
3. Verify the intended Pi's existing SSH alias and hostname, GNU `timeout`,
   actual checkout/Python paths, and the two serial symlinks. Read-only checks
   must not open the serial device. Never guess a new SSH host or accept an
   unfamiliar host key automatically.
4. On P1, identify the analyzer's USB sysfs location and confirm exactly one
   0925:3881 unit. Check sigrok-cli, eight-channel D0-D7 reporting, storage,
   systemd-run/systemd-inhibit, and the existing SSH agent. The launcher uses
   `--expand-environment=no`, requiring systemd 254 or later. Do not scan serial
   adapters. Normal fx2lafw initialization can load firmware into analyzer RAM;
   it does not program the Replica.
5. Run the new simulator below. It uses the production controller and separate
   synthetic capture/owner processes, without sigrok, SSH, or physical devices.
6. Copy the [configuration example](propeller-capture-config.example.json) to
   an untracked local path such as `out/propeller-config.json`. Populate actual
   absolute paths and host identities. Its placeholders are deliberately
   rejected. Complete the physical setup record with Alex before a live launch.

```bash
python -m tools.propeller_capture_job rehearse --out out/propeller-controller-rehearsal
python -m tools.propeller_capture_job plan --config out/propeller-config.json --out out/propeller-runs/attended-20260911-a
```

The first command takes seconds, using synthetic 1 kHz samples and compressed
test time. It checks ten outcomes: stable, missing analyzer, unstable idle,
capture not ready, partial capture, reset during open, owner failure, SSH loss
after open, owner timeout, and unexpected startup bytes. Each outcome is labelled
TEST_FIXTURE. It cannot create a hardware qualification.

`plan` reads files and prints exact Pi command arguments and capture limits.
It does not access USB, SSH, or serial. Inspect the configuration and printed
arguments. It is not a physical readiness certificate.

## First attended checkout

Use the same service launcher that will be used unattended. Keep Alex present
with the display visible and physical recovery available. This verifies the
service environment, sleep inhibitor, SSH agent, real USB throughput, and the
three-channel recording together. Start it only after physical setup is verified.

```bash
python -m tools.propeller_capture_job launch --config out/propeller-config.json --out out/propeller-runs/attended-20260911-a --mode attended
journalctl --user -u propeller-attended-20260911-a.service --no-pager
```

Launch means a service start was requested, not that the experiment succeeded.
Check the job's `result.json`, `report.md`, raw captures, and journal. If the
inhibitor or SSH authentication fails, fix host readiness; do not assume an open
occurred or start another job without inspecting the attempt/remote evidence.
Keep P1 connected to power and logged in; leave the lid open for the initial
checkout. Closing a terminal does not own the service lifetime. Logging out,
forcing sleep, or removing power is not supported by this qualification.

After `COMPLETE_DIGITAL_QUIET`, and only if Alex observed the display remain
stable throughout the cycle, record that observation:

```bash
python -m tools.propeller_capture_job qualify --run-dir out/propeller-runs/attended-20260911-a --display-stable
```

This creates `qualification.json` beside the attended evidence. It binds the
configuration, setup-record hash, helper hashes, and measured host/software
identity. It is an operator observation, not automated visual analysis. Stopped,
unconfirmed, synthetic, altered, or older-than-24-hour runs cannot qualify.
The same-day requirement keeps the unattended run tied to the current bench
setup; changes to wiring, power, host, code, or dependencies need a new checkout.

## Start one unattended job

With the qualified setup still connected and unchanged:

```bash
python -m tools.propeller_capture_job launch --config out/propeller-config.json --out out/propeller-runs/night-20260911-a --mode unattended --qualification out/propeller-runs/attended-20260911-a/qualification.json
```

The service requests a sleep inhibitor, has `Restart=no`, and a 180-second
outer runtime limit. Capture commands, stalls, and the Pi session have shorter
internal deadlines. A per-user kernel lock prevents concurrent launches from
controlling the analyzer. The qualification must match the current setup/code
and be less than 24 hours old; runtime versions and Pi identity are rechecked
before any recording or session.

The P1 controller waits for at least five seconds of actual sample bytes and
five seconds of local observation before invoking SSH. It requires at least
five seconds of samples and wall time after receiving the completed owner log.
It checks the raw stream for low UART/RESn samples and stops on any such sample.
Detection follows host buffering/polling and is not a hardware trigger or a
guaranteed instantaneous reset detector.

The Pi worker is independently bounded by GNU timeout: TERM after five seconds,
KILL after two more if needed. Its run directory and attempt marker are created
before an open, and the same run ID cannot be opened again. The shared existing
serial-owner lock still applies. A timeout or SSH loss can leave the physical
outcome unknown; it is never interpreted as permission to repeat.

To stop the service deliberately:

```bash
systemctl --user stop propeller-night-20260911-a.service
```

The controller handles TERM/HUP and attempts to save partial evidence. Hard
power loss, disk failure, or SIGKILL may prevent a final report; retained files
and the Pi attempt marker must then be inspected. Never delete an attempt
directory to make a used run ID appear unused.

## Results and recovery

Each local run keeps `baseline.bin` and `event.bin` as original raw capture
bytes, plus derived `.sr`/summary files where data exists. A stopped run may
have partial files or no event file. `events.jsonl` records P1 timestamps and
received-sample counts; `owner.jsonl` contains the returned Pi evidence when
available. The unmodified remote worker result and stderr are also retained.
`hashes.json` covers files present at completion, before an optional qualification
receipt is added. Host provenance and configuration are retained with the job.

`COMPLETE_DIGITAL_QUIET` means this single cycle completed with the monitored
bits high and one confirmed open/drain/close. It does not mean the display was
stable, the board was repaired, or the root cause was established. Every job
reports display UNOBSERVED and scientific result INCONCLUSIVE_ROOT_CAUSE.
The report is a capture-job bundle, not an automatic upgrade to the existing
trace-packet protocol's complete display-evidence status.

On STOP, local Codex should analyze saved files and leave a precise handback.
If the SSH reply was lost, use the read-only `pi_collect_argv` from `plan` for
that same run ID to retrieve `<pi_output_root>/<run-id>/result.json` if it exists.
If only `attempt.json` or a partial owner log remains, report the uncertainty;
do not rerun `session`. Physical Reset remains Alex's action when needed.

The inherited September 2 raw packet and its external videos remain untouched.
No precise shared clock, absence of upstream sample loss, or analog rail
stability is inferred from the new controller's timestamps and byte counts.

## Implementation sources and validation scope

The [sigrok-cli manual](https://sigrok.org/wiki/Sigrok-cli) documents explicit
USB selection, sample limits, binary output, and channel selection. The upstream
[binary output module](https://github.com/sigrokproject/libsigrok/blob/master/src/output/binary.c)
copies logic bytes without channel repacking; the
[fx2lafw driver](https://github.com/sigrokproject/libsigrok/blob/master/src/hardware/fx2lafw/api.c)
defines the D0-D7 layout used here. Source reviewed 2026-09-11; the installed
driver/layout still requires the attended checkout. The derived export states
the requested rate rather than claiming an independent frequency measurement.

Service/inhibitor options were checked against the upstream manuals distributed
by Debian: [systemd-run](https://manpages.debian.org/trixie/systemd/systemd-run.1.en.html)
and [systemd-inhibit](https://manpages.debian.org/trixie/systemd/systemd-inhibit.1.en.html).
The launcher is tested as constructed arguments; this cloud environment has
not qualified P1's user service manager, inhibitor permissions, or SSH agent.

Regression tests exercise real child-process lifecycle, stalled/partial
acquisition, stop-on-level behavior, SSH ambiguity, single-use remote IDs,
cleanup on device disappearance, post-event coverage, evidence hashes,
qualification checks, and service argument construction. Local validation passed:
**168 tests**, Ruff, mypy (35 source files), repository/link validation, and the
deterministic off-device demo. All ten expected simulator outcomes passed.
See the [executed validation record](../captures/2026-09-11-propeller-controller-validation.json)
for helper hashes and scenario results, and PR #6 for the published revision's CI.
