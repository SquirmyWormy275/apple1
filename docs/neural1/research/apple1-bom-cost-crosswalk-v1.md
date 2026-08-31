# Apple-1 BOM / Cost Crosswalk v1

**Status:** research scaffold / partial historical reconstruction  
**Cutoff:** `DESIGN_1976_03_10` unless otherwise stated  
**Purpose:** create a source-disciplined Apple-1 baseline for 1976 MULTIVERSE comparisons without treating a modern replica BOM as primary historical evidence.

## Authority order

1. 1976 Apple Computer Company schematic / operation manual.
2. Period manufacturer, distributor, trade-journal, and hobbyist-retail records.
3. Surviving-board / registry evidence where provenance is explicit.
4. Modern replica BOMs only as a component-count cross-check.

The modern `macmade/XS-Computer-One` BOM is useful for checking designators and quantities, but it is **not** proof of what Apple actually procured, populated, paid, or shipped on a particular 1976 board.

## Memory population profiles

Apple's 1976 manual states that the Apple-1 was supplied with 4K RAM and supported 8K onboard. Therefore two separate profiles are required:

- `APPLE1_4K_SUPPLIED`: 8 x 4096x1 DRAM devices.
- `APPLE1_8K_FULL`: 16 x 4096x1 DRAM devices.

A modern replica BOM that lists all 16 DRAM positions corresponds to full onboard population, not automatically the historical $666.66 supplied configuration.

## Core semiconductor crosswalk

| Family / function | Qty, full board | Qty, 4K supplied | Historical source status | Pre-cutoff price status |
|---|---:|---:|---|---|
| MOS 6502 CPU | 1 | 1 | primary schematic/manual | $25 introductory 1975 record |
| Motorola MC6820 PIA | 1 | 1 | primary schematic + period PIA records | $28 low-quantity 1974/75 record |
| MK4096-family 4Kx1 DRAM | 16 | 8 | primary manual identifies 4096-family RAM; exact production suffix requires board evidence | Q1-1975 vendor-book tiers found; hobbyist-retail exact MK4096 price still open |
| 3601 256x4 bipolar PROM | 2 | 2 | primary schematic / reconstruction cross-check | exact price open |
| 2504 shift register | 7 | 7 | primary schematic + Signetics period documentation | Jan-1976 retail $9 each |
| 2513 character generator | 1 | 1 | primary schematic + Signetics period documentation | Jan-1976 retail $11 |
| 2519 shift register | 1 | 1 | primary schematic + Signetics period documentation | Jan-1976 retail $4 |
| 8T97-family tri-state buffer | 2 | 2 | schematic / reconstruction; exact suffix to preserve | Jan-1976 retail 8T97B $1.49 each; variant caveat |
| 555 timer | 1 | 1 | primary schematic / reconstruction | Jan-1976 retail NE555 $0.49 |
| DS0025 two-phase MOS clock driver | 1 | 1 | primary schematic + 1975 National data book | price open |

## TTL population cross-check

The modern replica BOM gives the following counts, which must continue to be reconciled against the original schematic before being promoted to authoritative historical BOM data:

| Part | Qty | Jan-1976 hobbyist price each | Extended |
|---|---:|---:|---:|
| 7400 | 3 | $0.14 | $0.42 |
| 7402 | 1 | $0.15 | $0.15 |
| 7404 | 1 | $0.19 | $0.19 |
| 7408 | 1 | $0.18 | $0.18 |
| 7410 | 2 | $0.16 | $0.32 |
| 7427 | 1 | $0.29 | $0.29 |
| 7432 | 1 | $0.23 | $0.23 |
| 7450 | 1 | $0.17 | $0.17 |
| 74123 | 1 | $0.85 | $0.85 |
| 74154 | 1 | $1.25 | $1.25 |
| 74157 | 2 | $0.99 | $1.98 |
| 74160 | 1 | $1.39 | $1.39 |
| 74161 | 5 | $1.25 | $6.25 |
| 74166 | 1 | $1.49 | $1.49 |
| 74174 | 1 | $1.62 | $1.62 |
| 74175 | 1 | $1.39 | $1.39 |
| 74S257 | 4 | unavailable in current pre-cutoff retail snapshot | unavailable |

**Sourced subtotal for standard TTL rows above, excluding 74S257:** **$18.17**.

The 74S257 family is documented as commercially available by Signetics before 1976, but a qualifying pre-March-1976 price has not yet been established.

## Jan-1976 sourced semiconductor subtotal

Using only rows for which a qualifying retail/small-quantity price has been found, and excluding DRAM, exact 3601 PROM price, 74S257, DS0025, regulators, transformers, passives, PCB, sockets, connectors, and assembly:

- 6502: $25.00 (1975 introductory record; not Jan-1976 ad)
- MC6820: $28.00 (period low-quantity record)
- standard TTL subtotal excluding 74S257: $18.17
- 7 x 2504: $63.00
- 1 x 2513: $11.00
- 1 x 2519: $4.00
- 2 x 8T97B retail reference: $2.98
- 1 x NE555: $0.49

**Partial matched subtotal:** **$152.64**.

This is **not** an Apple-1 BOM cost. It is a partial sum of price-supported semiconductor rows under mixed but declared pre-cutoff R1/R2 evidence. It deliberately excludes major missing categories.

## DRAM economic evidence

A 1975 NASA comparative memory study reports Q1-1975 vendor-book prices for Mostek MK4096 as approximately:

- 25-piece quantity: $42 each;
- 100-piece quantity: $28 each;
- 1,000-piece quantity: $22 each.

These values belong to a production/vendor-book regime, **not hobbyist retail**.

Applied mechanically only to illustrate sensitivity—not to claim Apple's procurement cost—the memory silicon alone would be:

| Profile | 25-piece tier | 100-piece tier | 1,000-piece tier |
|---|---:|---:|---:|
| 4K / 8 chips | $336 | $224 | $176 |
| 8K / 16 chips | $672 | $448 | $352 |

This enormous tier sensitivity is precisely why MULTIVERSE must preserve economic regimes and must not infer Apple's cost from retail or volume-book prices.

## Compatible / alternative parts are separate records

Examples:

- Signetics 82S129 is a functional alternative cited by modern replica builders for the 3601 PROM. A January-1976 hobbyist ad lists 82S129 at $2.95. This must **not** be substituted into the historical Apple BOM cost unless the experiment explicitly allows alternate components.
- January-1976 ads list 2107 4096x1 dynamic RAM at $19.95, useful for alternate 1976 designs but not proof of MK4096 price.
- January-1976 ads list 2102 SRAM at several retail prices, useful when testing SRAM-based alternate architectures.

## Remaining high-priority BOM evidence gaps

1. Exact original schematic reconciliation for every TTL count.
2. Exact 3601 PROM pre-cutoff price.
3. 74S257 pre-cutoff price.
4. DS0025 pre-cutoff price.
5. Apple-specific MK4096 suffix/population evidence by board batch.
6. Apple actual procurement quantities/prices, if any surviving record can be sourced.
7. PCB fabrication cost / Byte Shop production economics.
8. Regulator and power-supply component prices.
9. Crystal price before March 10, 1976.
10. Sockets/connectors/passives and assembly labor.

## Sources / cross-checks

- Apple Computer Company, *Apple-1 Operation Manual* and schematic, 1976.
- January 1976 *BYTE*, JAMES Electronics and International Electronics Unlimited / S.D. Sales advertisements.
- Motorola MC6820 period pricing records in *Electronics* / *Electronic Design*.
- MOS Technology 6502 September 1975 introductory advertisement.
- NASA 1975 semiconductor-memory comparison, NTRS citation 19750020659.
- Jean-David Gadina (`macmade`), `XS-Computer-One/BOM.md`, modern replica reconstruction used only as a cross-check.

All machine-readable MULTIVERSE rows derived from this document must retain their own source IDs and economic regime.