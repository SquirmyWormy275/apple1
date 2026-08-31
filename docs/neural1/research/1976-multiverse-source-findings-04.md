# 1976 MULTIVERSE Source Findings 04

**Date:** 2026-08-30  
**Status:** source-upgrade note  
**Purpose:** record evidence that changes how MULTIVERSE must model market prices, sales channels, and Apple production economics.

## Finding 1 — market price is time-dependent even across adjacent months

SWTPC advertisements in consecutive BYTE issues show a material change in the advertised price of the 6800 system:

- February 1976: $450 for the computer system with serial interface and 2,048 words of memory;
- March 1976: $395 for the same advertised base description.

The March ad continues to list:

- 4,096-word static memory expansion: $125;
- serial or parallel interface: $35.

Sources:

- https://vintageapple.org/byte/pdf/197602_Byte_Magazine_Vol_00-06_Color_Graphics.pdf
- https://vintageapple.org/byte/pdf/197603_Byte_Magazine_Vol_00-07_Cassette_Interfaces.pdf

### Consequence

A generic `1976 price` field is methodologically invalid for fast-moving products.

Every MULTIVERSE market-price observation must retain at least:

- source date / issue;
- seller;
- channel;
- kit versus assembled state;
- included configuration;
- promotion window where present.

For systems and rapidly falling semiconductors, exact monthly cutoff can materially affect design rankings.

---

## Finding 2 — sales channel can differ dramatically in the same month

The January 1976 BYTE issue contains both a direct JOLT manufacturer advertisement and a JAMES Electronics reseller advertisement.

The direct JOLT advertisement lists roughly:

- CPU kit: $249;
- 4K RAM kit: $265;
- I/O kit: $96;
- power supply kit: $145.

The JAMES advertisement in the same issue lists JOLT modules at roughly:

- CPU kit: $159.95;
- RAM kit: $199.95;
- I/O kit: $95.50;
- power supply kit: $99.95.

Source:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

### Consequence

Do not average these quotes and do not automatically choose the lowest price.

The discrepancy may reflect promotion, reseller pricing, exact configuration differences, stale copy, or other commercial terms. Until reconciled, both are valid observations with distinct source/channel identities.

MULTIVERSE should be able to run channel-sensitive worlds rather than pretending the market exposes one canonical price.

---

## Finding 3 — a close March-1976 complete-system comparator exists

The March 1976 BYTE issue advertises the Micro-Sphere 200 at $860, completely assembled and tested, with:

- 4K RAM expandable to 8K;
- full alphanumeric keyboard;
- standard-TV display;
- cassette loader/interface;
- Sphere Cassette Operating System;
- 16 x 21 alphanumeric display;
- 128 x 128 B&W graphics;
- case.

Source:

https://vintageapple.org/byte/pdf/197603_Byte_Magazine_Vol_00-07_Cassette_Interfaces.pdf

### Consequence

Micro-Sphere is a useful reminder that Apple's $666.66 board price cannot be compared directly with every system sticker price. The Sphere price includes several physical and software components that Apple customers had to provide separately or that the Apple-1 did not offer.

A capability-vector normalization layer is mandatory for R5 comparisons.

---

## Finding 4 — Apple-specific supplier cash-flow evidence exists

A surviving Apple Computer Company check dated July 15, 1976 is payable to Kierulff Electronics for $3,430 and signed by Steve Jobs and Steve Wozniak. The auction catalog identifies the payment as being for Apple-1 parts.

Source:

https://www.rrauction.com/auctions/lot-detail/345625006328020-steve-jobs-and-steve-wozniak-signed-1976-apple-computer-check/

### Consequence

This is a real R4 Apple procurement datum.

It does **not** reveal the line items or quantities, so dividing $3,430 by an assumed board count would manufacture a false per-unit BOM cost.

The correct next target is the associated Kierulff invoice/statement/purchase order.

---

## Finding 5 — Cramer and Kierulff need to be modeled separately

Apple-1 Registry historical material states that Jobs obtained the original production components from Cramer Electronics on net-30 terms backed by the Byte Shop order.

Separately, the July 1976 surviving check documents a later Apple payment to Kierulff Electronics.

Sources:

- https://www.apple1registry.com/en/theapple1.html
- https://www.rrauction.com/auctions/lot-detail/345625006328020-steve-jobs-and-steve-wozniak-signed-1976-apple-computer-check/

### Consequence

Do not collapse `Apple supplier` into one vendor or assume the $3,430 Kierulff payment describes the first Byte Shop batch.

The commercial ledger should preserve distinct supplier events and evidence classes.

---

## Finding 6 — primary Apple advertising confirms the base configuration, but not yet the $120 RAM upgrade

1976 Apple advertising explicitly gives:

- Apple-1 price: $666.66;
- includes 4K bytes RAM;
- 8K onboard RAM capacity;
- integrated video terminal electronics;
- ASCII keyboard interface;
- 6502;
- firmware in PROMs;
- regulated supplies.

Representative source trail:

- Apple-1 Registry advertising archive: https://www.apple1registry.com/en/soft.html
- period Interface Age ad scans and surviving auction material.

The current primary advertising evidence reviewed in this pass does **not** visibly state the commonly repeated $120 price for the second 4K.

### Consequence

Keep the $120 upgrade price as secondary-corroborated until a qualifying period Apple price sheet/invoice/advertisement is located.

---

## New methodological requirement

Historical economic records need at least this identity tuple:

```text
DATE
SELLER
CHANNEL
PART_OR_SYSTEM
CONFIGURATION
ASSEMBLY_STATE
QUANTITY_TIER
PRICE
ECONOMIC_REGIME
SOURCE_ID
```

A price without this context is not sufficient for authoritative MULTIVERSE scoring.