# For builders and collection visitors

Choose the part of the project you want to explore. Reading the collection
records and running the virtual examples are useful starting points before any
physical integration work.

## Start with the software

1. Follow the [first demonstration](../docs/neural1/getting-started.md).
2. Read [Architecture](Architecture.md) to find the relevant modules.
3. Use the [development checks](../README.md#development-and-validation) when changing code.

The [RAM-only software library](../docs/apple1-software-library.md) and
[emulator guide](../docs/emulator-demo-guide.md) explain the small example
programs. [The CF-card library](CF-Card-Library.md) now has a verified media installation: 50 main books, six saved BASIC programs, full supplemental readings and the original six files. The [loading guide](../cf-card/DEPLOYMENT.md) explains the `$0800` main reader and `$1000` supplements. The [dated receipt](../cf-card/AUDIT-2026-10-28.md) records the storage checks; physical Replica display/keyboard acceptance remains pending.

## Explore the enclosure and collection

| Interest | Guide | What is established |
|---|---|---|
| Wooden enclosure | [R04 record](../docs/hardware/enclosure/README.md) and [drawing](../docs/hardware/enclosure/Apple1_Wooden_Enclosure_R04.pdf) | Design reference with an inclined keyboard deck and flat rear shelf; fitting and assembly checks remain |
| The Replica and preserved artifacts | [Preservation dossier](../docs/preservation-dossier.md) | Inventory, provenance, and the distinction between a replica and an original Apple-1 |
| Displays and the Sanyo monitor | [Display history](../docs/peripherals/displays/README.md) and [collection accession](../docs/collection/sanyo-vm-4209-1979/README.md) | Sourced historical research and collection-specific verification fields |
| Showing the project to someone | [Visitor materials](../docs/field-library/visitor-mode/README.md) | Two-, five-, and fifteen-minute tours with unpowered-hardware routes |

## Understand the physical integration boundary

The Replica serial fault remains unresolved. Start with the
[bounded repair plan](../docs/hardware/replica-repair-plan.md), its
[history and recovered photographs](../docs/hardware/repair-context-2026-10-28/README.md),
and [repair issue #17](https://github.com/SquirmyWormy275/apple1/issues/17).
The [troubleshooting record](../docs/troubleshooting.md) preserves the measured
observations. Basic power checks and a preserved-original/spare-EEPROM recovery
route precede a firm stopping point for vendor repair or replacement. The
[recovery package](../firmware/recovery/110REV03-2026-10-28/README.md) is built
off-device, with images, laptop tools, hashes and loading/rollback instructions;
physical recovery remains pending. Software tests and preparation documents do
not qualify the physical adapter. Read the
[physical boundary](../docs/neural1/architecture/physical-boundary.md) before
planning any adapter or hardware procedure.

For normal operation on the already commissioned Pi, use the
[operator guide](../docs/neural1/operations/terminal-application.md) and its
version notes. Source publication does not reinstall that machine.

[Wiki home](Home.md) · [Related: engineering highlights](Project-Highlights.md) · [Next: artwork and attribution](Artwork-and-Attribution.md)
