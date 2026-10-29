# Replica 1 Plus: restore dependable operation

**Current plan — October 28, 2026.** Start with basic power and interface checks,
then try a compatible firmware/spare-EEPROM recovery while preserving the
original EEPROM. Cap the effort; use vendor repair or board replacement if it
fails. A complete electrical root-cause investigation is optional.

[Repair issue #17](https://github.com/SquirmyWormy275/apple1/issues/17) ·
[History, corrections and eight recovered photographs](repair-context-2026-10-28/README.md) ·
[Separate CF acceptance #15](https://github.com/SquirmyWormy275/apple1/issues/15)

## Why this is the next step

Opening the FT232R without transmitting reproduced display corruption on
August 27 and September 2. Physical Reset restored Monitor operation/cursor.
The September 2 trace found **no digital UART threshold crossings**; it did
not measure Propeller RESn or analog power/ground. Reset, supply/interface
behavior and installed firmware remain candidates. **No failed component or
corrupt firmware has been demonstrated.**

The September 12–13 **Build Shopping List** conversation revised the earlier
measurement-first strategy: one further bench session, roughly **60–90 minutes**
and **$60 additional troubleshooting tools/parts before shipping/tax**, with
**no oscilloscope purchase**. These are historical planning bounds, not current
prices or an instruction to buy. The user accepted that approach and said they
would get a multimeter and DIP puller. Inventory them before proposing purchases.

The practical aim is a usable computer. A successful bounded recovery does not
require reconstructing every cause of the old failure. The older September 2
scope-first sequence is retained as history and an optional diagnostic route;
it does not impose an endless prerequisite before a repair attempt.

## What already exists, and what does not

| Item | Verified state | Consequence |
|---|---|---|
| [September 2 experiment](../captures/2026-09-02-ft232r-open-analyzer/README.md) | Complete, root cause inconclusive; external video is hash-identified. TX-O/RX-I were digitally quiet over 120 million samples at 4 MS/s. | Freeze it. The original one-open event is spent; do not repeat it for bookkeeping. |
| [Historical photographs](repair-context-2026-10-28/README.md#recovered-hardware-photographs) | Eight supplied JPEGs recovered. Revision 0, ReActiveMicro branding and P8X32A-D40 markings are visible. | Use these before requesting more pictures. They are not continuity or voltage measurements. |
| [PR #6](https://github.com/SquirmyWormy275/apple1/pull/6) | Capture runner, simulations and P1/Pi preparation exist. September 11 eventually detected the analyzer. | Preparation is real; a completed reset capture or unattended qualification is not. Initial readiness prose is stale. |
| Firmware | [Recovery package built off-device](../../firmware/recovery/110REV03-2026-10-28/README.md): program/EEPROM images, pinned tools, hashes, offline rebuild and loading procedure. | Physical interface/power compatibility, installed-image identity and on-board recovery remain unverified. |
| [Pi commissioning](../neural1/operations/pi-closeout-2026-09-10.md) | Complete for the recorded installed revision. | Preserve it; do not reimage/reinstall NEURAL1 to repair the Replica. |
| [CF installation](../../cf-card/AUDIT-2026-10-28.md) | 386 files fully read back; six originals preserved unchanged. | Preserve the card/receipts. Physical reader/BASIC acceptance remains open in #15. |

## 1. Prepare the repair package off-device

The [off-device package](../../firmware/recovery/110REV03-2026-10-28/README.md)
and [loading/rollback procedure](../../firmware/recovery/110REV03-2026-10-28/LOADING.md)
are now built and staged. Verify those files before the limited bench session;
rebuild only when needed for another host or an actual change. The steps below
remain the compatibility and evidence checklist; they do not require repeating
successful software preparation.

1. Match the recovered Revision 0/ReActiveMicro/P8X32A-D40 photographs to the
   present board. Identify the exact USB breakout and its programming/reset
   connections. The [vendor guide](https://wiki.reactivemicro.com/Replica_1)
   specifies a 5V switch setting for its documented programming arrangement;
   the old capture recorded 3.3V. Establish what this actual selector switches
   and the revision-compatible arrangement before moving it.
2. Locate revision-compatible vendor firmware or build the identified candidate
   with a documented, versioned compiler. Keep source URL/revision, tool versions,
   exact build command, output binary, size, SHA-256 and uploader command. Keep
   two independently checked copies. A successful compile alone does not prove
   compatibility or that the same image is currently installed.
3. Prefer a compatible **24LC256 DIP-8 spare EEPROM**. Preserve the original
   physically, labeled with orientation/date and stored safely. If a verified
   readback is already practical, retain it, but obtaining an installed-image
   readback or proving root cause is not a prerequisite to this preserved-original
   repair route. Do not overwrite the original EEPROM to simplify the exercise.
4. Specify the exact temporary RAM load, spare-EEPROM programming/verification,
   cold-start test and physical rollback. Confirm which chip is being changed:
   Propeller EEPROM, 6502 EPROM and CFFA1 firmware are different artifacts.
5. Record the current USB identity/path and exclusive port owner. The historical
   serial is nonunique (`00000000`), so rediscover both by-id and by-path. The
   September 11 path differed from the earlier capture. Reuse working host/Pi
   tooling; do not reopen the previous generic analyzer-cable troubleshooting loop.

If compatible firmware, a reliable programming connection or the spare cannot
be prepared within the bounded approach, go directly to vendor support or
replacement. Do not convert preparation into another equipment campaign.
This document is a repair plan; it performs no device load or physical action.

## 2. Use the first part of the bench session for simple checks

With serial closed, record the present power arrangement, breakout selector,
CFFA1 position, display and recovery sequence. Compare the historical photos
with what is actually fitted. Keep one intentional power source and change
connections only with power disconnected.

Use the meter to establish ground and check the board's nominal **5V and 3.3V**
rails at identified points against revision-compatible specifications. Record
readings, points, supply and meter; a healthy DC reading does **not** rule out
fast disturbances. Do not select a clip point from a photograph alone.

Confirm a normal standalone start: the expected power-on display, physical
Reset to Monitor, keyboard input, a tiny RAM write/read and BASIC where the
installed ROM supports it. Preserve any existing user program first. This
establishes which parts work before changing the Propeller subsystem.

| Finding | Next action |
|---|---|
| Wrong external supply, cable fault or demonstrably wrong selector configuration | Correct the verified external problem, then recheck. Do not blindly flip the selector from its label. |
| Abnormal rails persist | One unpowered CFFA1 removal/base-board comparison can separate accessory loading if justified. Persistent on-board abnormal power goes to vendor repair/replacement. Do not load firmware into an electrically abnormal setup. |
| Basic power is acceptable and the compatible recovery package/interface is ready | Proceed to the controlled recovery below. A scope capture or complete reset diagnosis is **not** required first. |
| No stable standalone Monitor/keyboard baseline | Record that broader fault and use vendor repair/replacement unless a simple verified external correction resolves it. |

Do not buy a scope, bench supply, programmer, soldering station, random
regulator/capacitors, 6502 or 6821 just to keep the investigation moving.

## 3. Try the firmware/EEPROM route while preserving the original

Follow the reviewed, artifact-specific procedure prepared in step 1, with an
operator observing the display and able to recover the board. Start with a
compatible temporary RAM image where the programming arrangement permits it.
Retain its loader log and exact binary hash; assess video, PS/2 and serial paths.

**Account for reset before interpreting the result.** Propeller RAM code is lost
on Propeller reset. If opening the serial port resets it, a subsequent test may
silently boot the old EEPROM image. Record which image is actually active;
power-cycle recovery to the old EEPROM is not evidence that the RAM image passed.
A normal 6502 Reset and Propeller RESn are different signals.

If the RAM trial passes, program and verify the **spare** EEPROM and test a true
cold boot from it. If reset makes a meaningful RAM comparison impossible, decide
from the verified programming procedure whether a spare-EEPROM cold-boot trial
is the clearer controlled comparison. Preserve the original throughout; do not
keep repeating RAM loads against the same reset trap.

Retain one result per deliberate change, including failures. A programming
failure or uncertain image identity is a stop for review, not a reason to retry
indefinitely. Returning the untouched original to its documented orientation is
the hardware rollback; it restores the old boot path, not proof of a healthy board.

If the compatible spare EEPROM resolves the symptom and acceptance passes,
stop. Describe it as successful firmware/EEPROM-path recovery; it does not prove
that the original image was corrupt rather than a different marginal condition.

## 4. Make at most one further justified substitution, then stop

If power is acceptable and the known-compatible spare-EEPROM trial fails, the
later chat allowed a compatible **P8X32A-D40 DIP-40** substitution if an inexpensive
known-good spare is available and the total time/cost limit still fits. Document
orientation and preserve the original. Do not substitute a different package or
near-matching part number.

A replacement breakout/cable is another possible targeted choice if evidence
specifically points there; it is not an additional list of mandatory purchases.
Choose the one justified comparison. If it does not restore dependable operation,
or if preparing it consumes the budget, stop and use vendor repair or a complete
board replacement. Do not move on to replacing arbitrary logic ICs.

**Vendor handoff:** provide the eight photographs, board markings, supply/selector
readings, [September 2 summary](../captures/2026-09-02-ft232r-open-analyzer/README.md),
no-transmit symptom, physical-Reset recovery and the exact recovery/substitution
results. Ask for the revision-compatible breakout/selector arrangement, firmware,
and repair/replacement options. No service availability or price quote is verified.
The agent can prepare this packet; contacting the vendor is a separate user action
unless explicitly requested.

## 5. Pass a finite acceptance sequence

After a selected repair, record:

- **Three successful cold boots**, using the documented normal Reset/Clear startup
  sequence. Normal documented startup garbage is distinct from unexpected corruption.
- **Five normal serial connection cycles** on the accepted topology, without
  unexpected corruption. A failure ends that acceptance attempt; it is not five
  additional attempts to recreate the same failure.
- Working local keyboard, host-to-Replica **and** Replica-to-host bytes. Start
  payload testing at the [protocol's](../serial-test-protocol.md) 9600 8N1,
  no flow control and `TEST` + CR at 500 ms/character. Screen echo alone does not
  establish both serial directions. Follow with a tiny Monitor RAM write/read.
- A short read-only CFFA1 operation after unpowered reinstallation, then the
  [CF reader/saved-BASIC handoff](../../cf-card/HARDWARE-HANDOFF.md) for #15.

A deliberately managed initial reset and one persistent port may be a usable
workflow if firmware/vendor behavior supports it. That is a separately labeled
operating workaround requiring acceptance, not proof of an electrical repair.
The current `serial_owner.py session` settles/drains for about 0.2 seconds and
closes; it does not implement an interactive persistent connection.

Keep before/after setup, exact changed part/image, logs, observations and rollback
in a new dated capture/session record. Update #17, troubleshooting, status and
Wiki from those results. Close #17 only for a demonstrated repair or an explicitly
accepted operating workaround with limits. Keep CF acceptance #15 distinct.
Once these finite checks pass, stop investigating the historical cause unless
new symptoms justify it.

## Optional: a bounded measurement branch

Use this only if the owner chooses further diagnosis, compatible recovery is
unavailable, or vendor support asks for a specific measurement. It is not a
scope-purchase prerequisite to the repair route above.

The [PR #6 reset/power reference](https://github.com/SquirmyWormy275/apple1/blob/6d644d26425e8f62e48b9627b1c56430be144cbc/docs/hardware/propeller-reset-power-reference.md)
and [next-session card](https://github.com/SquirmyWormy275/apple1/blob/6d644d26425e8f62e48b9627b1c56430be144cbc/docs/captures/propeller-reset-power-next-session.md)
provide the prepared procedure. The drawing identifies U7 pin 11/Q1 collector
as RST/RESn and a DTR→C9→Q1 path; the 6502/6821 RESET button net is separate.
Confirm actual continuity, Q1 pin order and the full breakout connection with
power disconnected. Reconcile the photographed multi-position mounting and
schematic with the September 2 four-conductor finding; neither proves the
present DTR path on its own.

The existing digital runner plans TX-O, RX-I and verified RESn at 4 MS/s, a
12-second baseline and a 30-second event, with one exclusive owner and no
automatic retry. It cannot measure analog rails, press Reset or observe display
stability. Analyzer enumeration and simulator passes do not qualify unattended
operation. A new card/setup and operator qualification are needed.

A RESn transition correlates with reset; DC-good rails or flat digital traces do
not exclude an analog disturbance. A borrowed scope could characterize VDD, 5V,
RESn and UART behavior if suitable grounding/probes are available. Record probe
points, bandwidth and time base. Use [SparkFun's ground guidance](https://www.sparkfun.com/usb-logic-analyzer-24mhz-8-channel.html)
and the [Parallax-authored D40 datasheet](https://tecnoedu.com/Download/Propeller-P8X32A-Datasheet-v1.4.0.pdf).
Do not apply the vendor's published pull-up/capacitor noise remedies without
matching the actual revision and symptom. Stop at the agreed session limit.
