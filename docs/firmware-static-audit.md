# Firmware static audit and toolchain preflight

These tools inspect the immutable `110REV03` vendor candidate. They do not
compile Spin, invoke an uploader, open a serial device, or identify the
EEPROM installed in the Replica.

## Static source facts

```powershell
python .\tools\firmware_static_audit.py .\firmware\vendor\110REV03
```

The report provides a repeatable reference to the candidate's P31 RX, P30 TX,
P15 clock, 7 ms serial strobe, and the two source routines that directly write
the keyboard data/strobe path: `ps2` and `serial`. Those are characterization
findings only, not a conclusion about the live board or a repair instruction.

## Propeller toolchain preflight

```powershell
python .\tools\propeller_preflight.py .\firmware\vendor\110REV03
```

The preflight records the archive's original `Propeller Tool version 1.3.2`
claim and lists the evidence required before a future compiler is even run. A
present tool executable may be recorded with `--tool`, but this tool never
executes it. A compile remains blocked until its exact executable version and
hash, the candidate-source hash, and an isolated output directory are retained.

No compile result is a recovery image. No preflight result authorizes RAM load,
EEPROM programming, or a programming lease.
