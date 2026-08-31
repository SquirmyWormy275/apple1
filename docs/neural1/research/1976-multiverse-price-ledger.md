# 1976 MULTIVERSE Price Ledger v1

**Status:** reconciled economic-evidence ledger  
**Purpose:** prevent incompatible, anachronistic, or unsupported component prices from entering 1976 MULTIVERSE scoring.

## Core rule

A component can be historically available without having a usable historical price. A market price can be real without being comparable to another price from a different quantity tier, seller, package, or date.

When qualifying price evidence is absent, the authoritative field remains unavailable. NEURAL1 must not ask an LLM to estimate it.

Every authoritative price record retains:

- part/family and exact order number where known;
- price and currency;
- publication/transaction date;
- seller/channel;
- quantity tier;
- package/variant;
- economic regime;
- source;
- cutoff eligibility;
- limitations.

See also:

- `1976-multiverse-economic-regimes.md`
- `1976-multiverse-component-lifecycle-policy.md`
- `1976-multiverse-price-snapshot-1976-01.json`
- `1976-multiverse-power-price-findings-v1.md`

---

# A. Strict pre-March-10-1976 records

## CPUs / PIA

| Part | Price | Date | Basis | Notes |
|---|---:|---|---|---|
| MOS 6502 | $25.00 | 1975-09 | introductory individual-sale advertisement | strict-cutoff eligible |
| Motorola MC6800 | $69.00 | 1975-10-30 | manufacturer advertisement, qty 1 | comparator CPU |
| Motorola MC6820 | $28.00 | 1974-12 / 1975-04 | small quantity / 1–24 trade listing | strict-cutoff eligible |

The MOS 6502 primary-artifact trail is the September 1975 WESCON advertisement. Motorola's MC6800 $69 quantity-one reduction is documented by the October 30, 1975 advertisement. MC6820 has two independent pre-cutoff low-quantity records.

---

# B. January 1976 hobbyist-retail snapshot

A single January 1976 *BYTE* market snapshot supplies an unusually coherent pre-cutoff retail comparison set. Machine-readable authoritative rows are in `1976-multiverse-price-snapshot-1976-01.json`.

Representative Apple-1-relevant rows:

| Part | Jan-1976 advertised price | Apple-1 relation |
|---|---:|---|
| Signetics 2504 | $9.00 | installed family |
| Signetics 2513 | $11.00 | installed family; font/suffix remains explicit |
| Signetics 2519 | $4.00 | installed family |
| 2102 SRAM | $2.95 | alternate design candidate |
| 2107 4096x1 DRAM | $19.95 | alternate DRAM candidate; not MK4096 price |
| 8T97B | $1.49 | installed-family comparator |
| NE555 | $0.49 | installed-function comparator |
| 82S129 256x4 PROM | $2.95 | explicitly drawing-permitted Apple PROM family |

Standard TTL retail rows from the same issue include:

| Part | Price |
|---|---:|
| 7400 | $0.14 |
| 7402 | $0.15 |
| 7404 | $0.19 |
| 7408 | $0.18 |
| 7410 | $0.16 |
| 7427 | $0.29 |
| 7432 | $0.23 |
| 7450 | $0.17 |
| 74123 | $0.85 |
| 74154 | $1.25 |
| 74157 | $0.99 |
| 74160 | $1.39 |
| 74161 | $1.25 |
| 74166 | $1.49 |
| 74174 | $1.62 |
| 74175 | $1.39 |

For the Apple Drawing `00101 Rev A` quantities, these standard TTL rows total **$18.17**, excluding the separately priced 74S257 positions.

Primary source set: January 1976 *BYTE* advertisements from JAMES Electronics, International Electronics Unlimited, and S.D. Sales.

---

# C. 74S257 resolved

## PRICE-74S257N-1975

**Part:** 74S257N  
**Price:** **$2.40 each**  
**Date:** documented in late-1975 retail listings, including December 1975  
**Economic regime:** R1 hobbyist/electronics retail  
**Cutoff eligible:** yes  
**Apple Drawing quantity:** 4  
**Extended Apple design-position cost:** **$9.60**

Representative source:

https://www.worldradiohistory.com/Archive-Radio-Electronics/70s/1975/Radio-Electronics-1975-12.pdf

The source lists `74S257N 2.40` among Schottky TTL parts. This closes the previously unresolved Apple 74S257 price position for strict pre-cutoff market studies.

---

# D. Power-regulator evidence

## LM323K-5

**Price:** **$14.00**  
**Date:** September 1975  
**Source:** JAMES Electronics advertisement, first issue of *BYTE*  
**Cutoff eligible:** yes

Primary scan:

https://vintageapple.org/byte/pdf/197509_Byte_Magazine_Vol_00-01_The_Worlds_Greatest_Toy.pdf

This is a strong exact-family observation for the Apple-1's high-current +5 V regulator position.

## LM320 / LM340 family observations

Period retail advertisements establish the market scale for related regulator packages before the cutoff, including records such as:

- LM320-5K — $2.90;
- LM320-5T — $2.50;
- LM320-12K — $2.90;
- LM320-12T — $2.50;
- LM340-12K — $2.60;
- September 1975 JAMES listings for LM340 12 V forms around $1.75–$1.95 depending package.

However, the exact Apple production-style `MP` suffix/package rows remain unresolved. Family-level observations may be used for alternative-design sensitivity studies but must not be silently assigned to the exact Apple production package.

See `1976-multiverse-power-price-findings-v1.md`.

---

# E. Mostek MK4096 DRAM

The MK4096 is firmly documented as commercially available before the Apple-1 design date, but a clean strict-R1 hobbyist-retail exact MK4096 price remains unresolved.

A 1975 NASA semiconductor-memory comparison records approximate Q1-1975 vendor-book tiers:

- 25-piece: $42 each;
- 100-piece: $28 each;
- 1,000-piece: $22 each.

These are **production/vendor-book regime observations**, not hobbyist-retail prices.

For sensitivity only:

| Apple memory profile | 25-piece tier | 100-piece tier | 1,000-piece tier |
|---|---:|---:|---:|
| 4K / 8 DRAMs | $336 | $224 | $176 |
| 8K / 16 DRAMs | $672 | $448 | $352 |

Do not infer Apple's actual memory procurement cost from this table.

January 1976 retail evidence for Intel 2107 at $19.95 provides an alternate-design DRAM market observation, not an MK4096 substitute price.

---

# F. Signetics family historical context

A 1971 Signetics MOS data book establishes that 2504, 2513/2514, and 2518/2519 families were commercial product families years before the Apple-1.

A January 1972 *Electronic Design* record lists 2518B/2519B at **$6 in quantities 250–999**, useful as early commercialization evidence but **not** as a March-1976 price.

The January 1976 retail snapshot supersedes that old quantity-tier observation for strict R1 comparison of the 2519 family.

---

# G. DS0025

National Semiconductor's 1975 Interface Integrated Circuits data book directly documents the `DS0025/DS0025C` two-phase MOS clock-driver family and its electrical/package properties.

Source:

https://www.bitsavers.org/components/national/_dataBooks/1975_National_Interface_Integrated_Circuits.pdf

**Strict pre-cutoff market price:** **UNRESOLVED**.

Repeated targeted searches have located the product documentation but not a sufficiently clear period low-quantity/retail price. Keep the price null rather than estimating it.

---

# H. Product / commercial records — separate from component cost

These belong to R4/R5 commercial analysis, not the strict component-price table:

- Apple-1 advertised/invoiced retail baseline: **$666.66 / 4K**;
- Apple Cassette Interface: **$75** on surviving December 1976 invoice;
- Byte Shop: **50 assembled units x $500 wholesale = $25,000 PO value**;
- July 15, 1976 Kierulff payment: **$3,430 for Apple-1 parts**, line items unknown;
- July 1, 1976 Santa Clara Circuits payment: **$673.36**, production-PCB context, quantity unknown;
- March 1976 Ramlor payment: **$116.97**, PCB-related context, quantity unknown.

See `apple1-commercial-economics-ledger-v1.md` and `apple1-procurement-cashflow-v1.json`.

---

# I. Late-1976 records — later cutoff only

Example November 1976 Motorola commercial-temperature family prices:

- MC6800CL — $49;
- MC6820CL — $23;
- MC6850CL — $24;
- MC6810ACL — $9.25.

These are useful for `YEAR_END_1976_12_31` but must never leak into the strict March-10 world.

---

# J. Current strict-cutoff status

## Resolved / usable price families relevant to Apple design

- 6502;
- MC6820;
- 2504;
- 2513;
- 2519;
- standard 74xx TTL set;
- 74S257;
- 8T97B comparator;
- NE555;
- drawing-permitted 82S129 PROM configuration;
- LM323K-5;
- several LM320/LM340 family/package comparators.

## Still unresolved as exact Apple design/procurement prices

| Component/category | Status |
|---|---|
| MK4096 exact strict-R1 retail / actual Apple procurement | UNRESOLVED |
| Intel/MMI 3601 exact pre-cutoff price | UNRESOLVED; drawing-permitted 82S129 is priced separately |
| DS0025 exact pre-cutoff price | UNRESOLVED |
| exact Apple LM320MP-5 package price | UNRESOLVED |
| exact Apple LM320MP-12 package price | UNRESOLVED |
| exact Apple LM340MP-12 package price | UNRESOLVED |
| 14.31818 MHz crystal before 1976-03-10 | UNRESOLVED |
| rectifiers / exact passives / sockets / connectors | PARTIAL OR UNRESOLVED |
| PCB per-unit fabrication | UNRESOLVED despite surviving aggregate payments |
| assembly labor per unit | UNRESOLVED |

---

# K. Scoring policy

1976 MULTIVERSE must not produce a fake complete dollar cost while required rows remain unsupported.

Default reporting:

```text
SOURCED COMPONENT COST: $X
COST-COVERED PACKAGE POSITIONS: N / TOTAL
COST COVERAGE: Y%
ECONOMIC REGIME: R1 / R2 / ...
COMPLETE BOM COST: UNAVAILABLE
```

If a candidate has unsupported cost rows, report a **partial sourced cost / lower bound** rather than assigning LLM-estimated values.

Market prices are identified by **date + seller/channel + quantity tier + package/configuration**. Price comparisons across regimes require a preregistered normalization method or separate Pareto frontiers.
