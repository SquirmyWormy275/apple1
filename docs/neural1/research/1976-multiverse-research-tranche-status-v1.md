# 1976 MULTIVERSE Historical Research Tranche — Status v1

**Branch:** `research/neural1-agenda-1976-sources`  
**Status:** ready for integration review after the active NEURAL1 implementation branch settles  
**Scope:** off-device historical/economic research only

## What this tranche establishes

The project now has a source-disciplined basis for a strict `DESIGN_1976_03_10` world rather than a generic "1976" bucket.

### Historical cutoff

The strict blind-design world uses March 10, 1976 as the default Apple-1 design cutoff. Later-1976 prices, commercial outcomes, Apple sales records, and production observations are retained in separate worlds/timelines and must not leak backward into the blinded design corpus.

### Apple-1 capability target

`apple1-capability-contract-v1.json` provides a source-backed comparison target based on the Apple-1 Operation Manual rather than a model-authored description.

### Apple package inventory

The primary package inventory is reconciled against Apple Drawing `00101 Rev A`:

- base 4K digital/terminal configuration: 53 IC packages;
- fully populated 8K digital/terminal configuration: 61 IC packages;
- optional 6501/6800-support circuitry is modeled separately rather than treated as standard population.

The drawing is **not** treated as perfect as-built physical truth. Known drawing-vs-production-net discrepancies have a separate ledger.

### Production variability

The project distinguishes:

1. design/drawing-permitted part;
2. period-market-available candidate;
3. observed production part on a particular batch/board;
4. later repair/replacement.

Vendor/package variation across surviving boards is preserved rather than collapsed into a fake canonical production BOM.

### Component availability

Strong pre-cutoff evidence now exists for major Apple-1 families including:

- MOS 6502;
- MC6820 PIA;
- MK4096 family;
- Signetics 2504;
- Signetics 2513;
- Signetics 2519;
- common 74xx logic;
- 74S257;
- DS0025 family;
- LM320 / LM323 / LM340 regulator families.

Availability and price remain distinct evidence dimensions.

## Economic evidence status

### Strict small-quantity / hobbyist-market price support

Strong price observations now exist for:

- 6502 — $25 introductory 1975 individual-sale record;
- MC6820 — $28 low-quantity period record;
- 2504 — $9 January 1976 retail;
- 2513 — $11 January 1976 retail;
- 2519 — $4 January 1976 retail;
- broad Apple 74xx logic set — January 1976 retail;
- 74S257N — $2.40 late-1975 retail;
- 8T97B — $1.49 January 1976 retail comparator;
- NE555 — $0.49 January 1976 retail comparator;
- drawing-permitted 82S129 PROM — $2.95 January 1976 retail;
- LM323K-5 — $14 September 1975 retail;
- multiple pre-cutoff LM320/LM340 family/package observations.

### Current Apple digital/terminal coverage

Using the drawing-permitted 82S129 PROM variant:

- price-supported digital/terminal package positions: 44 / 53;
- package-position coverage: 83.0%;
- unresolved digital/terminal positions: 8 base DRAM packages + DS0025.

This does **not** mean 83% economic-cost coverage because DRAM dominates the missing cost.

### Current partial sourced Apple configuration

Digital/terminal partial with drawing-permitted 82S129:

`$168.14`

Add the source-backed LM323K-5 regulator observation:

`$182.14`

This remains explicitly a **partial sourced configuration**, not a complete Apple-1 BOM cost and not Apple's manufacturing cost.

### DRAM

A Q1-1975 NASA vendor-book comparison gives MK4096 approximate tiers of:

- $42 at 25 pieces;
- $28 at 100 pieces;
- $22 at 1,000 pieces.

These are retained as R2/R3 vendor/production-regime observations. They are not collapsed into the R1 hobbyist-retail frontier and are not claimed as Apple procurement prices.

### Remaining exact high-impact price gaps

The following remain intentionally unresolved after targeted searching:

1. strict-R1 exact MK4096 market price or Apple procurement price;
2. DS0025 strict pre-cutoff low-quantity price;
3. exact production-style Intel/MMI 3601 pre-cutoff price;
4. exact Apple `LM320MP-5` package price;
5. exact Apple `LM320MP-12` package price;
6. exact Apple `LM340MP-12` package price;
7. 14.31818 MHz crystal price before March 10, 1976;
8. several exact passives/sockets/connectors;
9. per-unit PCB fabrication cost;
10. per-unit assembly labor.

These remain null. No LLM estimate is permitted to fill them.

## Apple commercial/procurement evidence

The commercial ledger and machine-readable cash-flow ledger now preserve primary surviving financial records including:

- March 16, 1976: $500 to Howard Cantin for PCB layout;
- March 1976: $116.97 to Ramlor, Inc. in the first Apple bank statement;
- spring 1976: Byte Shop order for 50 assembled machines at $500 each / $25,000 nominal PO value;
- July 1, 1976: $673.36 to Santa Clara Circuits, production-PCB context;
- July 15, 1976: $3,430 to Kierulff Electronics for Apple-1 parts;
- July 16, 1976: $10.52 to Elmar Electronics;
- July 16, 1976: $24.75 to Quement Electronics;
- July 1976 bank statement: $6,756.14 total debits with multiple electronics-vendor payments;
- Apple-1 retail baseline: $666.66 / 4K;
- Apple Cassette Interface: $75 on surviving invoice.

These observations are not converted into unsupported per-board costs.

## Key methodological decisions now locked

### Date is part of price identity

A price is not just `part -> dollars`. It includes date, seller/channel, quantity, package, and evidence source.

### Economic regimes remain separate

At minimum:

- R1 hobbyist/small-quantity retail;
- R2 low-quantity manufacturer/trade;
- R3 production/volume;
- R4 documented Apple transactions/procurement;
- R5 complete contemporary systems.

### Lifecycle matters

A part can be documented historically yet not be a valid procurement choice at a given cutoff because it may have been withdrawn, superseded, limited to volume availability, or only available as legacy stock.

### Missing price remains missing

Cost comparisons report partial sourced cost and coverage. No implicit interpolation, inflation adjustment, or LLM estimate is allowed without a separately preregistered methodology.

## Blind experiment readiness

`N1-MV-C001` is preregistered as the first strict March-10-1976 blind MULTIVERSE challenge.

The model receives:

- a source-backed capability target;
- a dated component universe;
- explicit procurement/lifecycle eligibility;
- experiment-declared cost regime;
- no Apple-specific solution topology.

The Apple-1 drawing/BOM/Monitor solution remains hidden until candidate designs are locked and hashed.

## Highest-value archival acquisition targets

Further progress is more likely to come from archives than broad web search.

Priority targets:

1. Kierulff Electronics invoice/statement corresponding to the July 15 $3,430 Apple payment;
2. Santa Clara Circuits invoice/order corresponding to the July 1 $673.36 check;
3. Ramlor invoice/order corresponding to the March $116.97 payment;
4. Cramer Electronics Apple purchase-order / net-30 records;
5. original Byte Shop purchase order;
6. Apple supplier line-item invoices in Stanford's Apple Computer records;
7. period Apple price sheet or primary ad confirming the reported $120 additional 4K option;
8. manufacturer/distributor catalogs capable of closing exact MK4096 and DS0025 price rows.

## Integration policy

Do not merge this branch into active implementation work blindly.

After the current Codex NEURAL1 completion branch lands:

1. rebase or recreate these research commits against current `main`;
2. reconcile any schemas Codex created for MULTIVERSE historical sources;
3. import the machine-readable capability/price/cash-flow records through the new validated schemas;
4. preserve source IDs and provenance;
5. run documentation/provenance tests;
6. review the preregistration against the implemented experiment contract before executing real models.

## Bottom line

The historical basis is now sufficient to run a scientifically meaningful first blind MULTIVERSE campaign even though a complete Apple-1 dollar BOM is not established.

The unresolved rows are documented limits, not blockers to architecture search. Candidate designs can be compared using capability, component count, sourced partial cost, price coverage, and separate economic-regime frontiers without inventing missing facts.
