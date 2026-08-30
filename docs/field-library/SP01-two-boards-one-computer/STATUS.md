# SP01 Status

**Mode: OFF-DEVICE**

The project owner approved the expanded ASCII lesson for repository inclusion.
That approval is **not** authority to write a CF card or operate the live machine.

## Card-facing artifacts

All learner-facing screens are under `card/` and are validated as:

- printable 7-bit ASCII;
- uppercase;
- maximum 40 columns;
- maximum 24 lines.

See `CARD-MANIFEST.md` for the per-file dimensions.

## Runnable artifacts

None.

## Expected result

A learner can navigate the original Apple-1 and Replica 1 Plus physical atlases,
locate the principal CPU/PIA/memory/video regions, and explain how a software-
visible interface can remain familiar while the underlying hardware changes.

## Known limitations

- The original map is a component-location teaching atlas, not a dimensionally
  exact PCB drawing.
- The Replica map follows the manufacturer's labeled board photograph and is a
  relative-location teaching map, not board CAD.
- Manufacturer documentation describes the design, not the exact electrical
  state of this project's live unit.
- The project's recorded FT232R no-transmit open produced a STOP result and is
  not waived by this lesson.

## Stop condition

Not applicable to the lesson itself because it is OFF-DEVICE. If anyone starts
using a card page as a probing, wiring, serial, firmware, or live-execution
procedure, stop: the packet does not authorize that use.

## What this status does not authorize

No CFFA1/CF-card write. No serial-port open. No firmware load. No EEPROM write.
No jumper, power, or wiring change. No live program run.
