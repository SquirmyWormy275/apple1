# Firmware baseline and recovery boundary

## Candidate source

`firmware/vendor/110REV03/` is an unchanged copy of the manufacturer-hosted
Replica 1 archive. Its provenance and per-file SHA-256 values are in
`provenance.json` beside the source.

This is a **candidate source baseline**, not an EEPROM readback from this
Replica 1 Plus. It may be compiled for analysis, but it is not a recovery
artifact and does not authorize a RAM load or EEPROM write.

## Observed candidate properties

- Serial RX is P31 and serial TX is P30 at 9600 baud.
- P9 is the CLEAR input and P15 supplies the 1 MHz clock.
- Serial injection holds its strobe for 7 ms and discards bytes outside its
  `serdata < 96` filter.
- The bundled full-duplex serial driver has a 16-byte receive ring.
- PS/2 and serial paths independently drive the keyboard bus in this source;
  that is a characterization finding, not a compliance result.

## Recovery gate

Before any persistent write, retain a revision-compatible recovery image with
its own provenance and hash, rehearse its RAM load and restore path, and keep
two copies. Until then, the only allowed firmware outcome is compile-only.
