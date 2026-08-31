# Apple-1 BOM / Cost Crosswalk v1

**Status:** source-backed partial historical reconstruction  
**Cutoff:** `DESIGN_1976_03_10` unless otherwise stated  
**Purpose:** create a source-disciplined Apple-1 baseline for 1976 MULTIVERSE comparisons without treating a modern replica BOM as primary historical evidence.

## Authority order

1. 1976 Apple Computer Company schematic / operation manual.
2. Period manufacturer, distributor, trade-journal, and hobbyist-retail records.
3. Surviving-board / registry evidence where provenance is explicit.
4. Modern replica BOMs only as a component-count cross-check.

The package inventory has been reconciled against Apple Drawing `00101 Rev A`; see `apple1-primary-package-inventory-v1.md`. Known drawing-vs-as-built net differences remain separate in `apple1-drawing-vs-as-built-v1.md`.

## Memory population profiles

Apple's 1976 manual states that the Apple-1 was supplied with 4K RAM and supported 8K onboard:

- `APPLE1_4K_SUPPLIED`: 8 x 4096x1 DRAM devices.
- `APPLE1_8K_FULL`: 16 x 4096x1 DRAM devices.

Do not price all 16 DRAM sockets as the historical base $666.66 configuration.

## Core semiconductor crosswalk

| Family / function | Qty, full board | Qty, 4K supplied | Historical source status | Pre-cutoff price status |
|---|---:|---:|---|---|
| MOS 6502 CPU | 1 | 1 | primary schematic/manual | $25 introductory 1975 individual-sale record |
| Motorola MC6820 PIA | 1 | 1 | primary schematic + period PIA records | $28 low-quantity 1974/75 record |
| MK4096-family 4Kx1 DRAM | 16 | 8 | primary manual + surviving-board evidence | exact strict-R1 price open; Q1-1975 vendor-book tiers available |
| 256x4 bipolar PROM | 2 | 2 | primary drawing permits 82S129 / H1024 / 3601 | Jan-1976 82S129 $2.95; exact 3601 price open |
| 2504 shift register | 7 | 7 | primary schematic + Signetics documentation | Jan-1976 retail $9 each |
| 2513 character generator | 1 | 1 | primary schematic + Signetics documentation | Jan-1976 retail $11 |
| 2519 shift register | 1 | 1 | primary schematic + Signetics documentation | Jan-1976 retail $4 |
| 8T97-family tri-state buffer | 2 | 2 | primary drawing / reconciled inventory | Jan-1976 8T97B $1.49 each; suffix caveat |
| 555 timer | 1 | 1 | primary terminal drawing | Jan-1976 NE555 $0.49 comparator |
| DS0025 two-phase MOS clock driver | 1 | 1 | primary schematic + 1975 National data book | price unresolved |

## TTL population — primary drawing reconciled

| Part | Qty | Pre-cutoff price each | Extended |
|---|---:|---:|---:|
| 7400 | 3 | $0.14 | $0.42 |
| 7402 | 1 | $0.15 | $0.15 |
| 7404 | 1 | $0.19 | $0.19 |
| 7408 | 1 | $0.18 | $0.18 |
| 7410 | 2 | $0.16 | $0.32 |
| 7427 | 1 | $0.29 | $0.29 |
| 7432 | 1 | $0.23 | $0.23 |
| 7450/compatible function | 1 | $0.17 | $0.17 |
| 74123 | 1 | $0.85 | $0.85 |
| 74154 | 1 | $1.25 | $1.25 |
| 74157 | 2 | $0.99 | $1.98 |
| 74160 | 1 | $1.39 | $1.39 |
| 74161 | 5 | $1.25 | $6.25 |
| 74166 | 1 | $1.49 | $1.49 |
| 74174 | 1 | $1.62 | $1.62 |
| 74175 | 1 | $1.39 | $1.39 |
| 74S257 | 4 | $2.40 | $9.60 |

**Pre-cutoff TTL subtotal including 74S257: $27.77.**

The 74S257 price is supported by late-1975 retail advertising, including a December 1975 *Radio-Electronics* listing at $2.40 each.

## Pre-cutoff digital/terminal semiconductor partial

Using price-supported rows and excluding DRAM, DS0025, power regulators, passives, PCB, sockets/connectors and assembly:

- 6502: $25.00
- MC6820: $28.00
- TTL including four 74S257: $27.77
- 7 x 2504: $63.00
- 1 x 2513: $11.00
- 1 x 2519: $4.00
- 2 x 8T97B: $2.98
- 1 x NE555: $0.49

**Partial matched subtotal excluding PROMs: $162.24.**

Using the drawing-permitted Signetics 82S129 PROM configuration:

- 2 x 82S129 at $2.95 = $5.90.

**Drawing-permitted digital/terminal partial: $168.14.**

This is not a complete Apple-1 BOM cost and is not a claim about the exact PROMs on a particular production board.

### Package-position price coverage

The reconciled base-4K digital/terminal inventory contains **53 IC packages**.

Under the current strict pre-cutoff evidence set and the drawing-permitted 82S129 PROM choice:

- directly price-supported package positions: **44**;
- unresolved positions: **9** = 8 base DRAMs + 1 DS0025;
- package-position coverage: **44 / 53 = 83.0%**.

This high package-count coverage must not be confused with economic coverage: the eight unresolved DRAM positions are economically dominant.

## Power-section increment

A September 1975 JAMES Electronics advertisement lists `LM323K-5` at **$14.00**. This is a strong pre-cutoff market observation for the Apple-1's high-current +5 V regulator family.

Adding only this sourced regulator to the drawing-permitted digital/terminal partial gives:

**Current expanded price-supported partial: $182.14.**

This still excludes:

- 8 x MK4096 base DRAMs;
- DS0025;
- exact LM320MP-5 and LM320MP-12 package prices;
- exact LM340MP-12 package price;
- crystal;
- rectifiers and remaining analog/support parts;
- passives;
- sockets/connectors;
- PCB fabrication;
- assembly labor.

See `1976-multiverse-power-price-findings-v1.md` for the package-specific regulator policy.

## DRAM economic evidence

A 1975 NASA comparative memory study reports Q1-1975 vendor-book prices for Mostek MK4096 of approximately:

- 25-piece: $42 each;
- 100-piece: $28 each;
- 1,000-piece: $22 each.

These are production/vendor-book observations, not hobbyist retail and not Apple's procurement cost.

Sensitivity only:

| Profile | 25-piece tier | 100-piece tier | 1,000-piece tier |
|---|---:|---:|---:|
| 4K / 8 chips | $336 | $224 | $176 |
| 8K / 16 chips | $672 | $448 | $352 |

This tier sensitivity is why MULTIVERSE preserves economic regimes rather than collapsing them into one cost.

## Drawing-permitted alternatives versus production observations

Distinguish:

1. **Drawing-permitted alternative** — explicitly allowed by Apple Drawing `00101`.
2. **Historically market-available alternative** — eligible under a declared cutoff/procurement policy.
3. **Observed production part** — documented on a specific surviving original board/batch.

Examples:

- 82S129 is explicitly permitted by Apple's processor drawing and has a January-1976 $2.95 retail observation; it is not thereby proven to be the PROM installed on a named production board.
- Intel 2107 at $19.95 in January 1976 is an alternate DRAM-market observation, not proof of MK4096 price or drop-in compatibility.
- 2102 SRAM is useful for alternate 1976 architecture experiments, not as historical Apple RAM.

## Remaining high-priority evidence gaps

1. MK4096 exact strict-R1 market price and/or Apple procurement price.
2. DS0025 pre-cutoff price.
3. Exact 3601 PROM pre-cutoff price for production-style configurations.
4. Exact Apple production-package prices for LM320MP-5, LM320MP-12, LM340MP-12.
5. 14.31818 MHz crystal price before March 10, 1976.
6. Apple supplier line-item invoices / statements.
7. PCB per-unit fabrication cost.
8. Sockets/connectors/passives and assembly labor.
9. Full as-built PCB netlist reconciliation against published-drawing discrepancies.

## Sources / cross-checks

Primary / period:

- Apple Computer Company Drawing `00101 Rev A`, sheets 1–3.
- Apple Computer Company, *Apple-1 Operation Manual*, 1976.
- January 1976 *BYTE* retail advertisements.
- September 1975 *BYTE* JAMES Electronics linear-IC advertisement.
- late-1975 74S257 retail advertisements.
- Motorola MC6820 pricing records in period trade publications.
- MOS Technology 6501/6502 1975 advertisement.
- NASA 1975 semiconductor-memory comparison, NTRS `19750020659`.

Secondary / observational cross-checks:

- Mike Willegal Apple-1 reconstruction.
- Applefritter A1 Mimeo records.
- Apple-1 Registry production evidence.
- Jean-David Gadina (`macmade`), `XS-Computer-One/BOM.md`, quantity consistency only.

All machine-readable rows derived from this document must retain source IDs, lifecycle eligibility, topology layer, package/variant information, and economic regime.
