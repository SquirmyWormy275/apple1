# Future bench procedure: RAM trial and preserved-original EEPROM recovery

**Staged instructions; no board was loaded or qualified.** The software is built.
Physical setup/power/reset checks remain for the next bounded repair session.
Use the [repair plan](https://github.com/SquirmyWormy275/apple1/blob/main/docs/hardware/replica-repair-plan.md)
for decision branches and the [recovered photographs](https://github.com/SquirmyWormy275/apple1/tree/main/docs/hardware/repair-context-2026-10-28/photos)
for identification. Inventory the existing meter/puller/spare before buying more.

## 1. Record the setup before running a loader

Copy `bench-session-template.json` into a **new dated session directory** under
`out/replica-recovery/`; keep originals of all logs and later publish a sanitized
session record under `docs/captures/`. Record timezone, current board/breakout,
USB topology, sole intended power arrangement, selector function, identified
5V/3.3V measurement points/readings, standalone Monitor/keyboard baseline and
operator recovery sequence. The old 3.3V observation and vendor 5V programming
instruction must be reconciled for the fitted module; do not guess a switch
setting. No serial application should open the port during these checks.

The staged profile uses **USB UART DTR reset**, ROM loading at **115200 baud**,
and terminal operation at the firmware's **9600 baud**, not GPIO reset or a fast
RAM loader. Verify that this board's complete fitted interface supplies the
required programming reset route. The old four-wire UART finding is not proof
that the full programming connection exists. If it does not, document the
specific missing interface/vendor-supported connection; do not improvise wiring
or repeatedly retry the same upload.

Keep the original Propeller EEPROM unchanged. If proceeding to persistent
recovery, disconnect power, document orientation, remove/label/store the original,
and install the verified-compatible **spare 24LC256 DIP-8** under the board's
service procedure. The 6502 EPROM and CFFA1 firmware are separate. Do not change
wiring or chips while powered. Wrong/persistent abnormal power takes the repair
plan's external-correction or vendor route before any load.

## 2. Verify files and bind the intended port without opening it

From repository/bundle root:

```bash
python3 tools/replica_recovery.py verify
ls -l /dev/serial/by-id/ /dev/serial/by-path/
```

Use the **present** by-id and by-path links for the same FT232R. Its historical
serial `00000000` is nonunique; do not copy an old physical path. Confirm USB
VID/PID `0403:6001` and actual topology with metadata, for example
`udevadm info --query=property --name /dev/serial/by-id/CURRENT_LINK`.
Check for existing port owners (`fuser -v` on the resolved device) without opening
it. Stop/quiesce any intended serial service deliberately; the loader itself uses
`TIOCEXCL`, which does not evict an application that already has the port open.

Generate commands using actual links and review the resulting `binding_precheck`
and `loader_command` / `recording_command`:

```bash
python3 tools/replica_recovery.py commands \
  --by-id /dev/serial/by-id/REPLACE_WITH_CURRENT_LINK \
  --by-path /dev/serial/by-path/REPLACE_WITH_CURRENT_LINK \
  --mode ram \
  --session-dir out/replica-recovery/REPLACE_WITH_NEW_SESSION
```

This prints JSON **without checking/opening those ports or running the loader**.
The printed binding check resolves both links and confirms the same character
device without opening it. Metadata and current physical setup must also match.
Never omit `-p` or fall back to automatic port selection.

## 3. One attended RAM trial, with the port kept open

After the preceding checks, run the printed binding check and the reviewed RAM
loader command from a real interactive terminal. The command has this shape:

```text
<PACKAGE>/bin/linux-x86_64/proploader -I <PACKAGE>/config -b replica1 \
  -s -p <CURRENT_BY_ID_LINK> -r -t <PACKAGE>/images/replica-110REV03.binary
```

Use the **printed shell-quoted command**, not the angle-bracket example. Capture
it and all output in the new session directory. On this Linux laptop, the
installed `script` utility can record a real terminal session:

```text
script -qef --log-out <NEW_SESSION>/ram.typescript --command '<PRINTED_LOADER_COMMAND>'
```

The tool also prints a complete shell-quoted `recording_command` for the supplied
`--session-dir`; use that directly after creating a fresh session directory.
Do not overwrite earlier transcripts. Record the exact image hash,
command, return status, acknowledgments and synchronized display observations.
No initial identification-only open is needed: loading includes a reset,
handshake and Propeller-version check.

`-t` retains the same connection after loading and switches it to 9600 baud.
**Escape exits terminal mode.** Observe normal video/startup, then use the normal
6502 Reset/Clear procedure to reach Monitor. Check local keyboard and initial
serial behavior without reopening. Terminal mode does not add character pacing;
follow the serial protocol for actual paced payload qualification later.

**Do not misidentify the active image:** a Propeller reset discards the RAM load
and can boot the old EEPROM. The 6502 Reset button is a different net. Closing
terminal, reopening a port or an unexpected reset can invalidate a RAM comparison.
Record uncertainty; use the preserved-original/spare cold-boot comparison when
that is the clearer bounded test. Do not call an old-EEPROM reboot a RAM pass.

On handshake, programming or observation failure, retain the log and stop for
review. The ROM loader polls for acknowledgments within an attempt; there is no
outer automatic reflash/retry loop in the staged procedure.

## 4. Program only the spare EEPROM

With the original labeled/stored and compatible spare installed, use the same
verified setup and a new recorded attempt:

```bash
python3 tools/replica_recovery.py commands \
  --by-id /dev/serial/by-id/REPLACE_WITH_CURRENT_LINK \
  --by-path /dev/serial/by-path/REPLACE_WITH_CURRENT_LINK \
  --mode spare-eeprom \
  --session-dir out/replica-recovery/REPLACE_WITH_NEW_SESSION
```

The printed loader command adds **`-e`** to the RAM command and retains `-r -t`.
It still takes the **`.binary`** input. The staged profile fixes candidate header
clock settings at 80 MHz / `0x6f`; it does not borrow an unrelated board profile.
ROM loading checks Propeller version, RAM acknowledgment, EEPROM programming
acknowledgment and EEPROM verification acknowledgment. Capture the complete log.
These acknowledgments are not an independent exported readback of every EEPROM
byte. A real cold boot and functional acceptance are still required.

If a RAM test was inconclusive specifically because reset replaced the active
image, the compatible spare cold-boot route can be chosen directly under the
reviewed plan. A full electrical root-cause diagnosis is not a prerequisite.

## 5. Cold boot, acceptance, rollback and stop

Exit the loader terminal deliberately, power down, then cold boot the **spare**
EEPROM. Record normal startup/Reset behavior and the active candidate provenance.
Pass three cold boots, five normal serial connection cycles, local keyboard,
actual bytes in both directions, a small Monitor RAM transaction and read-only
CFFA1 operation. Expected startup garbage is separate from unexpected corruption.
A failure ends acceptance; preserve it rather than repeating until a pass.

Then use the [CF hardware handoff](https://github.com/SquirmyWormy275/apple1/blob/main/cf-card/HARDWARE-HANDOFF.md)
for reader/saved-BASIC acceptance under issue #15. Do not rewrite the installed
CF edition to troubleshoot this recovery.

For rollback: power off, restore the labeled original EEPROM in its documented
orientation, restore the recorded original setup and cold-start procedure, then
record the result. This restores the original boot path, not proof that the old
image or board was healthy. Preserve the spare/image/logs as well.

Observe the agreed 60–90 minute/~$60 additional-parts bounds. After a failed
compatible spare trial, at most one justified substitution fits the plan; then
vendor repair/replacement. Optional reset/rail diagnosis remains available if
chosen, with no mandatory oscilloscope purchase. Keep issue #17 open until a
repair or explicitly accepted workaround passes its documented acceptance.
