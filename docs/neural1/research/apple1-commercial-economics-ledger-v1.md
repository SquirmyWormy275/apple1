# Apple-1 Commercial Economics Ledger v1

**Status:** source-backed commercial-context ledger  
**Purpose:** separate the March 10, 1976 design universe from Apple's later commercialization, wholesale, and retail economics.

## Why this is separate from the strict design cutoff

`DESIGN_1976_03_10` asks what an engineer could have designed using information available by Steve Wozniak's schematic design date.

Commercial events immediately after that date answer different questions:

- what it cost Apple to convert the schematic into a manufacturable PCB;
- what the Byte Shop agreed to pay;
- what Apple/retailers charged customers;
- what additional RAM and peripherals cost.

These records must not leak backwards into blind design-world knowledge unless an experiment explicitly uses a later cutoff.

---

## COM-001 — Apple check No. 1 / PCB layout

**Date:** 1976-03-16  
**Amount:** $500  
**Payee:** Howard Cantin  
**Purpose:** Apple-1 printed-circuit-board design/layout services  
**Evidence class:** surviving primary financial artifact; auction-house catalog record  

Source:

https://www.rrauction.com/auctions/lot-detail/350879307346000-steve-jobs-and-steve-wozniak-historic-signed-1976-apple-computer-check-no-1-to-howard-cantin-designer-of-the-apple-1-printed-circuit-board-psa-mint-9/

The artifact is a Wells Fargo check numbered 1, dated March 16, 1976, payable to Howard Cantin for $500 and signed by Steve Jobs and Steve Wozniak. The catalog identifies the payment as compensation for the Apple-1 PCB design/layout.

### Use

This is a real Apple development cost, not a per-unit PCB fabrication price. It belongs in commercialization/development-cost analysis and must not be divided across an arbitrary production quantity without explicitly declaring that allocation assumption.

---

## COM-002 — Byte Shop purchase order

**Order:** 50 assembled Apple-1 computers  
**Unit price to Apple:** $500  
**Purchase-order value:** $25,000  
**Terms:** cash on delivery / assembled machines  
**Evidence class:** reputable museum history plus direct later oral testimony by Paul Terrell

Computer History Museum:

https://www.computerhistory.org/revolution/personal-computers/17/300/1052

CHM records that Jobs and Wozniak obtained parts to fill an order from Palo Alto's Byte Shop for 50 Apple-1 computers at $500 each.

A 2026 oral history published by Fast Company quotes Paul Terrell directly: he ordered 50 units, offered $500 per unit, and describes the purchase order as $25,000 cash on delivery.

### Use

This supplies a strong R4 commercial constraint:

`APPLE_WHOLESALE_REVENUE_PER_BYTE_SHOP_UNIT = $500`

It does **not** directly establish Apple's component cost or gross margin.

---

## COM-003 — Retail price / base memory

**Retail price:** $666.66  
**Base RAM:** 4K  
**Evidence class:** Apple advertisement / museum records

Computer History Museum records the Apple-1 at $666.66 with 4K memory.

Later 1976 Apple advertising explicitly states that $666.66 includes 4K bytes RAM while the board supports 8K.

### Use

The historical retail baseline is therefore:

`APPLE1_4K_RETAIL = $666.66`

Do not represent the base retail product as necessarily populated with all 16 DRAM positions.

---

## COM-004 — Additional 4K / $120

**Claim:** additional 4K RAM cost $120  
**Status:** secondary-corroborated / primary price sheet still sought

Multiple modern Apple-1 software-history references independently state that expanding the base 4K machine to 8K cost an additional $120.

This produces an implied 8K board price of $786.66 before peripherals if accurate.

### Use

Do **not** promote this to the authoritative R4 ledger until a period Apple price sheet, advertisement footnote, invoice, or similarly qualifying primary source is acquired.

---

## COM-005 — Apple Cassette Interface

**Retail price:** $75  
**Evidence class:** surviving invoice / historical documentation

A surviving December 7, 1976 Apple invoice described in the Christie's lot record totals $741.66 for an Apple-1 plus Apple Cassette Interface, consistent with $666.66 + $75.

### Use

The ACI is a peripheral and should remain outside the Apple-1 baseboard BOM comparison unless an experiment explicitly defines a complete BASIC-capable package.

---

## Commercialization timeline fields for MULTIVERSE

The research system should distinguish at least:

- `DESIGN_1976_03_10` — blind architecture/design knowledge cutoff;
- `PCB_LAYOUT_1976_03_16` — documented $500 layout expenditure;
- `BYTE_SHOP_ORDER_1976_SPRING` — 50 units x $500 wholesale;
- `APPLE1_RETAIL_1976` — $666.66 / 4K configuration;
- `YEAR_END_1976_12_31` — later-1976 component and market comparison world.

The exact Byte Shop purchase-order date remains an acquisition target if a surviving document can be identified.

## Derived commercial metrics permitted now

These arithmetic statements are directly derived from source-backed values:

- Byte Shop PO nominal value: 50 x $500 = $25,000.
- Dealer gross spread before dealer costs: $666.66 - $500 = $166.66 per base unit.
- Retail/wholesale ratio: $666.66 / $500 = 1.33332.

These are **not** Apple's margins.

Apple's actual per-unit manufacturing cost remains unknown until procurement, PCB fabrication, labor, and other cost records are adequately sourced.

## Research questions enabled

1. Could a blind period-valid design meet the Apple-1 capability contract while leaving plausible room under a $500 wholesale ceiling?
2. How much of the design frontier changes when optimizing for $500 wholesale rather than theoretical component minimum?
3. Does Wozniak's design sit near a Pareto frontier for retail-visible capability, chip count, and plausible production economics?
4. How sensitive is the answer to 4K versus 8K population?
5. Which architectural features consume the greatest share of sourced component cost under each economic regime?

## Open acquisition targets

- original Byte Shop purchase order, if surviving/accessibly archived;
- Apple component supplier invoices / Cramer or Kierulff records;
- Apple PCB fabrication invoice(s);
- Apple labor/assembly records;
- period Apple evidence for $120 additional 4K;
- period dealer price sheets;
- production-quantity component purchase terms.