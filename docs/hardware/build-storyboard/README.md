# Physical build storyboard and evidence kit

The finished enclosure and Replica setup are still being made. This kit prepares
the story and evidence slots now, without inventing completed work or finished
hardware photographs. The [R04 enclosure record](../enclosure/README.md) remains
the design reference; this plan changes no geometry, materials or joinery.

[Shot manifest](shots.json) · [Measurement template](measurements.template.json) ·
[Caption template](caption-template.md) · [Physical acceptance chapter](../../textbook/reference/physical-session.md)

## Tell the story in this order

| Sequence | Story question | Evidence to add |
|---|---|---|
| 1. Purpose and design | What is being built, and why? | R04 reference beside the actual finished assembly |
| 2. Parts and craft | What did the maker actually use and change? | Identified parts, material/finish, construction photos and maker's account |
| 3. Fit and service | Does the assembled layout fit and remain serviceable? | Measured clearances, keyboard fit, supports, ventilation and unpowered CF access |
| 4. First accepted operation | What did the finished system actually do? | Qualified power/reset observation, one key, known program, expected/actual result |
| 5. Complete exhibit | How do the historical machine and modern host relate? | Physical reader/BASIC output beside separately labeled Pi inference and verification |
| 6. Reflection | What worked, failed or remains uncertain? | Preserved failures, changes, limitations and a source-linked final exhibit |

The manifest assigns stable shot IDs. Filenames should begin with those IDs,
but retain camera originals unchanged in preservation storage. Keep a derived
web image beside a record of its original hash, crop, resize and caption.
Do not substitute a diagram, emulator screenshot or generated illustration for
an empty physical-photo slot.

## Capture details that make the story useful

Record date/time and timezone, photographer/maker credit, permission to publish,
actual component identity, revision, orientation and the claim supported.
Use a scale in a measurement photograph, and record units, tool and uncertainty.
A wide view establishes context; a close view supports the measurement. A
photograph alone does not establish installed firmware, electrical safety or
serial qualification.

Ask the maker for the actual build sequence, selected material, finish and
joinery when those facts are available. Until then those fields remain null.
Do not turn a proposed R04 dimension into an as-built measurement.

The [measurement template](measurements.template.json) includes the CF/card
stack, under-shelf gap, motherboard rise, keyboard fit, shelf support,
ventilation/cable clearance, and installed assembly envelopes. It intentionally
has no invented values or pass marks.

## Keep a physical session inspectable

Use the existing instrumented physical test cards and stop conditions. This
storyboard is a documentation plan, not permission to open serial, change
wiring, flash firmware or energize an unqualified assembly. The historical
serial-open display fault stays visible until a measured session resolves it.

For an accepted reader/BASIC trial, retain:

1. Identified ROM and card-image records, test/payload version and expected result.
2. Camera view of the physical keyboard and screen, raw observation and timestamps.
3. Device logs and reset/control-line evidence where the qualified test requires them.
4. Actual result, interpretation and any mismatch, with the failing trial retained.

Use the [caption template](caption-template.md) to separate observation from
interpretation. The Pi's proposal and independent verifier belong to a separate
evidence chain until physical transport is demonstrated.

## Integrate the finished chapter

When the setup arrives, copy the templates into a new dated session directory.
Populate the manifest with real original and derivative assets; verify their
hashes and local links. Add the as-built measurements without overwriting R04.
Create a concise build narrative using the maker's recorded facts.

Then replace the planned slots with credited photographs, add the accepted
physical reader/BASIC captures next to their existing host counterparts,
and update README/wiki status from the new evidence. Preserve earlier
failures and candidate receipts so a prospective employer can see the
engineering decisions and verification, not just a polished final photograph.
