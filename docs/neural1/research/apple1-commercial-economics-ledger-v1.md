# Apple-1 Commercial Economics Ledger v1

**Status:** source-backed commercial-context ledger  
**Purpose:** separate the March 10, 1976 design universe from Apple's later commercialization, wholesale, procurement, and retail economics.

## Why this is separate from the strict design cutoff

`DESIGN_1976_03_10` asks what an engineer could have designed using information available by Steve Wozniak's schematic design date.

Commercial events immediately after that date answer different questions:

- what it cost Apple to convert the schematic into a manufacturable PCB;
- what the Byte Shop agreed to pay;
- what Apple paid suppliers after production began;
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

### Use

This supplies a strong commercial constraint:

`APPLE_WHOLESALE_REVENUE_PER_BYTE_SHOP_UNIT = $500`

It does **not** directly establish Apple's component cost or gross margin.

---

## COM-003 — Retail price / base memory

**Retail price:** $666.66  
**Base RAM:** 4K  
**Evidence class:** Apple advertisement / museum records

Computer History Museum records the Apple-1 at $666.66 with 4K memory. Later 1976 Apple advertising states that $666.66 includes 4K bytes RAM while the board supports 8K.

### Use

`APPLE1_4K_RETAIL = $666.66`

Do not represent the base retail product as necessarily populated with all 16 DRAM positions.

---

## COM-004 — Additional 4K / $120

**Claim:** additional 4K RAM cost $120  
**Status:** secondary-corroborated / primary price sheet still sought

Do **not** promote this to the authoritative commercial ledger until a period Apple price sheet, advertisement footnote, invoice, or similarly qualifying primary source is acquired.

---

## COM-005 — Apple Cassette Interface

**Retail price:** $75  
**Evidence class:** surviving invoice / historical documentation

A surviving December 7, 1976 Apple invoice described in the Christie's lot record totals $741.66 for an Apple-1 plus Apple Cassette Interface, consistent with $666.66 + $75. Apple-1 Registry board #41 independently records the same invoice.

Sources:

- https://www.apple1registry.com/en/41.html
- Christie's provenance record for the Frank Anderson Apple-1 set

The ACI remains outside the Apple-1 baseboard BOM comparison unless an experiment explicitly defines a complete BASIC-capable package.

---

## COM-006 — Kierulff Electronics parts payment

**Date:** 1976-07-15  
**Amount:** $3,430  
**Payee:** Kierulff Electronics  
**Purpose:** Apple-1 parts  
**Evidence class:** surviving primary Apple financial artifact; auction-house catalog record

Source:

https://www.rrauction.com/auctions/lot-detail/345625006328020-steve-jobs-and-steve-wozniak-signed-1976-apple-computer-check/

The catalog explicitly identifies this payment as for Apple-1 parts. It also reports historical context that Kierulff extended Apple roughly $20,000 of parts on net-30 terms.

### Use

This establishes a real production-era electronics-distributor expenditure. It does **not** establish exact line items, quantities, unit prices, or a per-board manufacturing cost.

---

## COM-007 — Ricketts direct Apple transaction

**Date:** 1976-07-27  
**Payment:** $600 to Apple Computer  
**Evidence class:** surviving customer cancelled check documented by Christie's / Steve Jobs archive provenance

Source:

https://www.christies.com/lot/lot-5855175

This is evidence of a real direct Apple-1-era transaction, but must not replace the advertised $666.66 retail baseline because the exact bundle/discount terms are not fully established here.

---

## COM-008 — March 1976 Apple bank statement / prototype-business spending

**Statement period:** March 1976  
**Evidence class:** surviving Apple Wells Fargo account statement; auction-house catalog record

Source:

https://www.rrauction.com/auctions/lot-detail/351019507346002-steve-jobs-march-1976-wells-fargo-account-statement-for-apple-computer-co-apples-first-financial-record/

The statement reports:

- deposits totaling **$840**;
- debits totaling **$697.45**;
- **$500** to Howard Cantin;
- **$116.97** to PCB maker Ramlor, Inc.;
- **$13.86** to Elmar Electronics;
- **$4.95** to Zack Electronics;
- **$13.25** to University Art Center;
- **$47.50** to Pacific Telephone.

### Use

This is a rare primary snapshot of Apple's prototype/startup cash flow immediately after the March 10 design date. The **$116.97 Ramlor payment is PCB-related spending**, but the record does not state board quantity, fabrication specification, whether it covered prototypes versus a larger lot, or unit cost. It therefore cannot be divided into a per-board PCB cost without additional evidence.

The small electronics-distributor payments demonstrate real March procurement activity but likewise do not expose purchased line items.

---

## COM-009 — Santa Clara Circuits production PCB payment

**Date:** 1976-07-01  
**Amount:** $673.36  
**Payee:** Santa Clara Circuits  
**Evidence class:** surviving Apple check; auction-house catalog record

Source:

https://www.rrauction.com/auctions/lot-detail/351630507484001-steve-jobs-signed-1976-apple-computer-company-check-to-santa-clara-circuits-linked-to-the-first-apple-1-boards/

The catalog identifies Santa Clara Circuits as a contract PCB manufacturer believed to have produced the first Apple-1 boards assembled for the Byte Shop order.

### Use

This is stronger evidence for **production PCB expenditure** than the earlier Ramlor prototype-era payment, but still does not establish an exact per-board price because the check itself does not specify quantity or invoice line items.

It creates a high-value archival target: the corresponding Santa Clara Circuits invoice/order.

---

## COM-010 — July 1976 Apple bank statement / production cash-flow map

**Statement period:** July 1976  
**Total checking-account debits:** $6,756.14  
**Evidence class:** surviving Apple Wells Fargo statements; auction-house catalog record

Source:

https://www.rrauction.com/auctions/lot-detail/351630707484005-steve-jobs-july-1976-wells-fargo-account-statements-for-apple-computer-co-tracing-the-funds-behind-early-apple-1-production/

The surviving statement enumerates approximately 48 checks during July, including:

- **$3,430** to Kierulff Electronics;
- **$10.52** to Elmar Electronics;
- **$4.01** to Radio Shack;
- **$9.18** to Tektronix;
- **$47.70** to IBM;
- **$125** to Elmer Baum;
- **$17** to bookkeeper Elizabeth Holmes.

The statement provides an unusually strong period cash-flow map but not enough line-item detail to classify every payment as Apple-1 manufacturing cost.

### Use

Preserve individual checks as vendor-payment observations. Do **not** sum every July debit into an Apple-1 production-cost estimate; several payments were clearly administrative, financing, or otherwise non-component expenditures.

---

## COM-011 — Elmar Electronics production-era payment

**Date:** 1976-07-16  
**Amount:** $10.52  
**Payee:** Elmar Electronics  
**Evidence class:** surviving Apple check

Source:

https://www.rrauction.com/auctions/lot-detail/349143007005088-steve-jobs-filled-out-and-signed-apple-computer-company-check-to-elmar-electronics-july-16-1976/

The payee was an electronics distributor. The auction catalog reasonably associates the timing with early Apple-1 production, but the exact purchased parts are unknown.

Classification: **electronics-vendor payment / component use plausible, line items unknown**.

---

## COM-012 — Quement Electronics production-era payment

**Date:** 1976-07-16  
**Amount:** $24.75  
**Payee:** Quement Electronics  
**Evidence class:** surviving Apple check

Source:

https://www.rrauction.com/auctions/lot-detail/349145707050156-steve-jobs-signed-1976-apple-computer-check-to-quement-electronics/

Quement was an electronics warehouse. The exact purchased items are not specified by the check.

Classification: **electronics-vendor payment / component use plausible, line items unknown**.

---

# Commercialization timeline fields for MULTIVERSE

The research system should distinguish at least:

- `DESIGN_1976_03_10` — blind architecture/design knowledge cutoff;
- `STARTUP_FINANCE_1976_03` — primary bank-statement evidence including Cantin, Ramlor, Elmar, Zack;
- `PCB_LAYOUT_1976_03_16` — documented $500 layout expenditure;
- `BYTE_SHOP_ORDER_1976_SPRING` — 50 units x $500 wholesale;
- `PRODUCTION_PCB_1976_07_01` — $673.36 Santa Clara Circuits payment;
- `PRODUCTION_1976_07_15` — $3,430 Kierulff parts payment;
- `PRODUCTION_CASHFLOW_1976_07` — July bank-statement vendor map;
- `APPLE1_RETAIL_1976` — $666.66 / 4K configuration;
- `YEAR_END_1976_12_31` — later-1976 component and market comparison world.

# Derived commercial metrics permitted now

These arithmetic statements are directly derived from source-backed values:

- Byte Shop PO nominal value: 50 x $500 = $25,000.
- Dealer gross spread before dealer costs: $666.66 - $500 = $166.66 per base unit.
- Retail/wholesale ratio: $666.66 / $500 = 1.33332.

These are **not** Apple's margins.

Apple's actual per-unit manufacturing cost remains unknown until procurement, PCB fabrication, labor, and other cost records are adequately sourced.

# Research questions enabled

1. Could a blind period-valid design meet the Apple-1 capability contract while leaving plausible room under a $500 wholesale ceiling?
2. How much of the design frontier changes when optimizing for $500 wholesale rather than theoretical component minimum?
3. Does Wozniak's design sit near a Pareto frontier for retail-visible capability, chip count, and plausible production economics?
4. How sensitive is the answer to 4K versus 8K population?
5. Which architectural features consume the greatest share of sourced component cost under each economic regime?
6. Can Apple supplier-payment records constrain a plausible production-cost interval without inventing line-item prices?
7. Can Ramlor and Santa Clara Circuits records eventually distinguish prototype PCB cost from production PCB cost?
8. How much procurement-channel dependence is visible between local distributors and larger credit suppliers?

# Open acquisition targets

- original Byte Shop purchase order, if surviving/accessibly archived;
- corresponding Kierulff Electronics invoice / statement for the July 15, 1976 $3,430 payment;
- corresponding Santa Clara Circuits invoice/order for the July 1, 1976 $673.36 payment;
- Ramlor invoice/order corresponding to the March $116.97 payment;
- Elmar, Quement, Cramer, Zack, or other supplier line-item records;
- Apple labor/assembly records;
- period Apple evidence for $120 additional 4K;
- production-quantity component purchase terms;
- Stanford Apple Computer archival material relevant to 1976 procurement and sales.
