# Apple-1 BOM / Cost Crosswalk v1

**Status:** research scaffold / partial historical reconstruction  
**Cutoff:** `DESIGN_1976_03_10` unless otherwise stated  
**Purpose:** create a source-disciplined Apple-1 baseline for 1976 MULTIVERSE comparisons without treating a modern replica BOM as primary historical evidence.

## Authority order

1. 1976 Apple Computer Company schematic / operation manual.
2. Period manufacturer, distributor, trade-journal, and hobbyist-retail records.
3. Surviving-board / registry evidence where provenance is explicit.
4. Modern replica BOMs only as a component-count cross-check.

The package inventory has now been reconciled against Apple Drawing `00101 Rev A`; see `apple1-primary-package-inventory-v1.md`. Known drawing-vs-as-built net differences are deliberately retained separately in `apple1-drawing-vs-as-built-v1.md`.

## Memory population profiles

Apple's 1976 manual states that the Apple-1 was supplied with 4K RAM and supported 8K onboard. Therefore two separate profiles are required:

- `APPLE1_4K_SUPPLIED`: 8 x 4096x1 DRAM devices.
- `APPLE1_8K_FULL`: 16 x 4096x1 DRAM devices.

A full 16-DRAM socket/population model corresponds to 8K capacity and must not automatically be used as the historical $666.66 supplied configuration.

## Core semiconductor crosswalk

| Family / function | Qty, full board | Qty, 4K supplied | Historical source status | Pre-cutoff price status |
|---|---:|---:|---|---|
| MOS 6502 CPU | 1 | 1 | primary schematic/manual | $25 introductory 1975 individual-sale record |
| Motorola MC6820 PIA | 1 | 1 | primary schematic + period PIA records | $28 low-quantity 1974/75 record |
| MK4096-family 4Kx1 DRAM | 16 | 8 | primary manual identifies 4096-family RAM; surviving-board evidence identifies MK4096-11 production family | Q1-1975 vendor-book tiers found; hobbyist-retail exact MK4096 price still open |
| 256x4 bipolar PROM | 2 | 2 | primary drawing explicitly permits Signetics 82S129, Harris H1024, or Intel/MMI 3601 | Jan-1976 retail 82S129 $2.95; exact 3601 cutoff price still open |
| 2504 shift register | 7 | 7 | primary schematic + Signetics period documentation | Jan-1976 retail $9 each |
| 2513 character generator | 1 | 1 | primary schematic + Signetics period documentation | Jan-1976 retail $11 |
| 2519 shift register | 1 | 1 | primary schematic + Signetics period documentation | Jan-1976 retail $4 |
| 8T97-family tri-state buffer | 2 | 2 | primary processor drawing / reconciled package inventory | Jan-1976 retail 8T97B $1.49 each; suffix/variant caveat |
| 555 timer | 1 | 1 | primary terminal drawing / reconciled package inventory | Jan-1976 retail NE555 $0.49 |
| DS0025 two-phase MOS clock driver | 1 | 1 | primary schematic + 1975 National data book | price open |

## TTL population — primary drawing reconciled

The following package counts are now reconciled with Apple Drawing `00101 Rev A`; the modern replica BOM remains only a secondary consistency check.

| Part | Qty | Pre-cutoff price each | Extended |
|---|---:|---:|---:|
| 7400 | 3 | $0.14 | $0.42 |
| 7402 | 1 | $0.15 | $0.15 |
| 7404 | 1 | $0.19 | $0.19 |
| 7408 | 1 | $0.18 | $0.18 |
| 7410 | 2 | $0.16 | $0.32 |
| 7427 | 1 | $0.29 | $0.29 |
| 7432 | 1 | $0.23 | $0.23 |
| 7450/compatible function | 1 | $0.17 retail 7450 reference | $0.17 |
| 74123 | 1 | $0.85 | $0.85 |
| 74154 | 1 | $1.25 | $1.25 |
| 74157 | 2 | $0.99 | $1.98 |
| 74160 | 1 | $1.39 | $1.39 |
| 74161 | 5 | $1.25 | $6.25 |
| 74166 | 1 | $1.49 | $1.49 |
| 74174 | 1 | $1.62 | $1.62 |
| 74175 | 1 | $1.39 | $1.39 |
| 74S257 | 4 | $2.40 | $9.60 |

**Pre-cutoff TTL subtotal including 74S257:** **$27.77**.

### 74S257 price evidence

A period component advertisement in *Popular Electronics*, August 1975, lists `74S257N` at **$2.40**. Additional late-1975 listings repeat the same $2.40 figure. This establishes a pre-March-1976 market price observation for the required Schottky multiplexer family.

Primary period source trail:

- `Popular Electronics`, August 1975, semiconductor advertisement: https://americanradiohistory.com/Archive-Poptronics/70s/1975/Poptronics-1975-08.pdf
- late-1975 Radio-Electronics listings provide corroboration.

The Apple drawing specifies 74S257 at B5-B8. Manufacturer/package realization on a particular surviving Apple board remains a separate production-history question.

### Production-vendor caveat

The design function is more stable than vendor/package realization. Surviving boards show Fairchild/Signetics and other supplier variation; at C8, for example, functionally compatible 7450/7451-style realization requires board-specific treatment. Do not turn the price rows above into claims about a specific original board's vendor marking.

## Pre-cutoff sourced semiconductor partials

Using rows for which qualifying retail/small-quantity price evidence has been found, and excluding DRAM, DS0025, regulators, transformers, passives, PCB, sockets, connectors, and assembly:

- 6502: $25.00 (1975 introductory individual-sale record)
- MC6820: $28.00 (period low-quantity record; economic-regime caveat)
- TTL including four 74S257: $27.77
- 7 x 2504: $63.00
- 1 x 2513: $11.00
- 1 x 2519: $4.00
- 2 x 8T97B retail reference: $2.98
- 1 x NE555: $0.49

**Partial matched subtotal excluding PROMs:** **$162.24**.

Apple's own processor drawing explicitly permits three 256x4 PROM families. If the historical design configuration selects the January-1976 retail-priced Signetics 82S129 option:

- 2 x 82S129 at $2.95 = $5.90.

**Drawing-permitted partial subtotal with 82S129 PROMs:** **$168.14**.

Neither figure is an Apple-1 BOM cost. Both are partial sums of price-supported semiconductor rows under declared pre-cutoff evidence. The second is a **drawing-permitted configuration**, not a claim that production Apple used 82S129s on a particular board.

### Package-position price coverage

Closing 74S257 pricing resolves four additional required package positions. The major unresolved digital-package concentration is now the eight base DRAM devices plus the DS0025 clock driver, with economic-regime treatment of the PIA still requiring care.

Despite improved package-position coverage, the missing DRAM price in the strict hobbyist-retail regime remains economically dominant. Therefore a total-cost ranking is still invalid.

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

## Drawing-permitted alternatives versus production observations

The project must distinguish three concepts:

1. **Drawing-permitted alternative** — explicitly allowed by Apple Drawing `00101`.
2. **Historically market-available alternative** — eligible for a blind MULTIVERSE candidate under the declared cutoff/procurement policy.
3. **Observed production part** — documented on a specific surviving original board/batch.

Examples:

- Signetics 82S129 is not merely a modern substitute: Apple's original processor drawing explicitly lists it as an allowed 256x4 PROM type. Its January-1976 $2.95 retail observation may therefore be used for a `DRAWING_ALLOWED_82S129` Apple design-cost variant. It must not be described as the actual PROM on a named board without board evidence.
- January-1976 ads list 2107 4096x1 dynamic RAM at $19.95. It is useful for alternate 1976 designs, but does not establish an MK4096 price or timing compatibility with the Apple-1 without validation.
- January-1976 ads list 2102 SRAM at several retail prices, useful when testing SRAM-based alternate architectures.

## Remaining high-priority BOM evidence gaps

1. Exact 3601 PROM pre-cutoff price for observed-production-style configurations.
2. DS0025 pre-cutoff price.
3. Apple-specific MK4096 procurement quantities/prices and/or strict R1 market price.
4. Apple actual supplier line-item invoices, if surviving records can be sourced.
5. PCB fabrication cost / Byte Shop production economics.
6. Exact production-package regulator prices where period family prices do not resolve the suffix/package.
7. 14.31818 MHz crystal price before March 10, 1976.
8. Sockets/connectors/passives and assembly labor.
9. Full as-built PCB netlist reconciliation against known published-drawing errors.

## Sources / cross-checks

Primary:

- Apple Computer Company, Drawing `00101 Rev A`, sheets 1–3.
- Apple Computer Company, *Apple-1 Operation Manual*, 1976.
- January 1976 *BYTE* period retail advertisements.
- *Popular Electronics*, August 1975 74S257 component advertisement.
- Motorola MC6820 period pricing records in *Electronics* / *Electronic Design*.
- MOS Technology 6501/6502 1975 advertisements.
- NASA 1975 semiconductor-memory comparison, NTRS citation `19750020659`.

Secondary / observational cross-checks:

- Mike Willegal Apple-1 hardware/netlist reconstruction.
- Applefritter A1 Mimeo original-style component record.
- Apple-1 Registry production-population evidence.
- Jean-David Gadina (`macmade`), `XS-Computer-One/BOM.md`, modern reconstruction used only as a consistency check.

All machine-readable MULTIVERSE rows derived from this document must retain their own source IDs, lifecycle eligibility, topology layer, and economic regime.