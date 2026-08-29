# M01 Status

**Mode: OFF-DEVICE**

No runnable artifact. The Monitor commands in this packet are quoted from a
manual and read on paper.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/three-jobs.txt` | Plain-text reference card, 40 columns | No |

**No command in this packet is an instruction to type anything on a machine.**
The examples are documentation quoted for reading. `ACTIVITY.md` states this at
the top.

## Expected result

A learner names three jobs and reads six documented commands. All items keyed.

## Known limitations

- The value `E1` in the inspect and change examples is from the manual's own
  worked example. It is illustrative and is not a claim about the contents of
  `$0300` on any board. A learner who takes it as a fact about this machine has
  misread it, and the answer key and source notes both flag this.
- Line-editing behavior (backspace, escape) is omitted.
- The command syntax is documented replica behavior and has not been observed on
  this project's board.

## Stop condition

Not applicable. No device interaction.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No automated control of the machine. Nothing here
authorizes powering on or typing at the Replica 1 Plus.
