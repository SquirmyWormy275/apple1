# B02 Status

> **Current host evidence (October 28, 2026):** The original paper activity
> remains available. [The BASIC chapter](../../textbook/reference/basic.md)
> now runs the preserved interpreter on a modeled NMOS 6502. U01–U06 retain
> actual sessions; U02 checks conversion bounds and U04 checks one-based arrays.
> V-20 and V-21 are resolved for these identified host sessions. Older "not run"
> notes below describe the earlier edition; they do not describe current host
> capability. Physical installation and execution remain unverified.

**Mode: OFF-DEVICE**

The worksheet remains OFF-DEVICE. U01/U02 provide runnable host counterparts
using the preserved BASIC interpreter; see the current evidence notice above.

## Artifacts

| File | Type | Runnable |
|---|---|---|
| `README.md` | Learner text | No |
| `ACTIVITY.md` | Worksheet | No |
| `ANSWERS.md` | Answer key | No |
| `SOURCE-NOTES.md` | Citations | No |
| `assets/flow-diagram.txt` | Plain-text flow diagram, 40 columns | No |

The BASIC listings in `ANSWERS.md` were constructed for this lesson from
documented syntax. They are project-authored examples. U01 executes the greeting and U02 executes
the revised, guarded conversion.

## Expected result

A completed four-box diagram with a legal variable name. Parts B, C, and F have
single correct answers; Parts A, D, E, and G are keyed with worked examples and
acceptance criteria.

## Known limitations

- Selected BASIC programs now execute in the host interpreter labs (U01–U06).
- U01 now observes the double-question-mark behavior; installed hardware remains untested.
- The host tests observe arithmetic precedence and the intermediate overflow
  boundary for this exact interpreter; that is not evidence of installed ROM identity.
- The four-box diagram cannot represent a decision, which the answer key states.

## Stop condition

The paper activity has no execution. Host sessions stop at the input poll or
a declared instruction limit; no physical device is involved.

## What this status does not authorize

No firmware load. No EEPROM write. No CFFA1 write. No serial-port open. No
physical modification. No typing of any BASIC line on hardware.
