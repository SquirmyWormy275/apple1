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

## Recovery routes

The October 28 [bounded repair plan](hardware/replica-repair-plan.md) records
the later user-accepted route: acceptable basic power, a compatible recovery
package and programming arrangement, the **original EEPROM physically preserved**,
then temporary RAM and/or a controlled **spare-EEPROM** comparison. Installed-image
readback and a complete reset/scope diagnosis are not prerequisites for that
route. It does not authorize overwriting the original. The verified compiled
package and physical acceptance remain missing. See the
[updated recovery ledger](recovery-evidence-ledger.md).

### Earlier persistent-write gate

The earlier rule below remains applicable to overwriting an existing EEPROM;
it does not block preparation or proposal of the preserved-original repair route.

Before any persistent write, retain a revision-compatible recovery image with
its own provenance and hash, rehearse its RAM load and restore path, and keep
two copies. Until then, the only allowed firmware outcome is compile-only.
