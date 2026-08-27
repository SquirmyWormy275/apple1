# Replica 1 Plus preservation dossier

This dossier protects the collection record while the serial fault remains under investigation. **No firmware load, EEPROM write, or physical modification is authorized by this document.** It deliberately excludes enclosure and other design work.

## Chain-of-custody record

Complete one row before changing the setup or collecting a live capture. Keep
original images and instrument files unchanged; this document is an index, not
a substitute for source evidence.

| UTC time | Operator | Activity | Power source | USB topology | Physical change | Evidence location | Result |
|---|---|---|---|---|---|---|---|
| | | | | | `none` unless stated | | PASS / STOP / INCONCLUSIVE |

## Baseline inventory checklist

Record observed values, photographs, and any uncertainty. Do not infer a
component's installed firmware from a source archive.

- Replica label, board revision, and board serial (if present)
- CPU, ROM, PIA, Propeller, CFFA1, FT232R, display, keyboard, Pi, and power
  supplies: maker/part/serial, condition, and photo filename
- Jumper and DIP state while powered down only; record a photo before and after
  any intentional change
- Cable make/model, both USB endpoints, and the Pi's recorded by-id and by-path
  identities
- Monitor prompt/ROM-dump evidence and reset recovery procedure
- Packaging, signed box, manuals, and separately stored recovery media

## Evidence rules

1. Record facts separately from hypotheses and vendor claims.
2. Hash every copied source, capture, binary, and photo manifest with SHA-256.
3. Preserve the original filename, source URL or physical origin, retrieval
   date, and any license/permission note.
4. Store a read-only duplicate of raw captures before annotation.
5. Use the support-bundle tool only with explicitly named files. It does not
   inspect or open serial hardware.
6. If the display changes, a reset occurs, identities drift, or bytes mismatch,
   record `STOP`, recover to the known monitor state, and do not continue a
   test sequence.

## Current boundaries

- The FT232R host open has already produced a display-garbling STOP result.
  Do not run an opened serial session or transmit test until the measurement
  test card is ready and an operator explicitly starts that single step.
- The vendor `110REV03` source is immutable candidate evidence, not the
  EEPROM image installed in this machine.
- No temporary CA2 wiring, soldering, resistor installation, uploader use, RAM
  load, or EEPROM action belongs in ordinary development work.
