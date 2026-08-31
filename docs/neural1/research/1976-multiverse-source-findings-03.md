# 1976 MULTIVERSE Source Findings 03

**Date:** 2026-08-30  
**Status:** source-upgrade note  
**Purpose:** record pre-March-1976 retail and vendor-book evidence that materially improves the Apple-1 economic baseline.

## Finding 1 — January 1976 hobbyist retail covers most standard Apple-1 TTL

The January 1976 issue of *BYTE* contains a full International Electronics Unlimited TTL price sheet. It lists all of the following standard TTL families used in the current Apple-1 BOM cross-check:

- 7400 — $0.14
- 7402 — $0.15
- 7404 — $0.19
- 7408 — $0.18
- 7410 — $0.16
- 7427 — $0.29
- 7432 — $0.23
- 7450 — $0.17
- 74123 — $0.85
- 74154 — $1.25
- 74157 — $0.99
- 74160 — $1.39
- 74161 — $1.25
- 74166 — $1.49
- 74174 — $1.62
- 74175 — $1.39

Source:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

The ad states that data sheets are available and identifies International Electronics Unlimited, Monterey, California.

### Consequence

The current modern-replica TTL quantity cross-check can be given a pre-cutoff hobbyist-retail price for every standard TTL row except the four 74S257 devices.

The sourced standard-TTL subtotal under that cross-check is $18.17, excluding 74S257.

This remains a retail reconstruction, not Apple's production cost.

---

## Finding 2 — January 1976 retail directly prices 8T97B and NE555

A separate S.D. Sales advertisement in the same issue lists:

- Signetics 8T97B tri-state hex buffer — $1.49;
- NE555 timer — $0.49.

It also lists Signetics 82S129 256x4 bipolar PROM at $2.95.

Source:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

### Consequence

The 8T97B and NE555 rows can enter the pre-cutoff retail universe, with an explicit suffix/variant note for the 8T97 family.

82S129 is useful as an experimentally allowed 3601-compatible PROM candidate. It must not be silently priced as though it were the actual Apple-installed 3601.

---

## Finding 3 — the Apple-1 historical baseline requires separate 4K and 8K profiles

The Apple-1 Operation Manual states that the board is supplied with 4K of RAM and can accommodate 8K onboard.

The modern `XS-Computer-One` BOM lists 16 x MK4096 positions, corresponding to full 8K population.

### Consequence

1976 MULTIVERSE now distinguishes:

- `APPLE1_4K_SUPPLIED`: 8 DRAMs;
- `APPLE1_8K_FULL`: 16 DRAMs.

A full 16-chip modern BOM must not be used to reconstruct the $666.66 base machine without this population distinction.

---

## Finding 4 — Q1-1975 vendor-book evidence gives a real MK4096 price ladder

NASA NTRS citation `19750020659` contains a comparative 4K DRAM table with Q1-1975 vendor-book price columns. For Mostek MK4096 it reports approximately:

- 25-piece quantity: $42;
- 100-piece quantity: $28;
- 1,000-piece quantity: $22.

Source identity:

https://ntrs.nasa.gov/citations/19750020659

The currently indexed copy exposes the table text but the direct PDF endpoint may require separate archive acquisition before machine ingestion.

### Consequence

This is the first strong source showing how violently the Apple-1 memory economics change with procurement scale.

For eight DRAMs, mechanically applying the published per-unit tiers gives $336 / $224 / $176. For sixteen it gives $672 / $448 / $352.

These are sensitivity calculations, not claims about Apple's actual procurement.

---

## Finding 5 — period evidence confirms 74S257 availability, price still unresolved pre-cutoff

A January 1973 Signetics advertisement in *Electronic Design* explicitly lists the 74S257 as a quad 2-line-to-1-line data selector/multiplexer with tri-state outputs and states that the firm's Schottky MSI devices were in volume availability.

Source:

https://www.worldradiohistory.com/Archive-Electronic-Design/1973/Electronic-Design-V21-N01-1973-0104.pdf

### Consequence

74S257 is safely available in the strict March-1976 component universe. A qualifying pre-March-1976 price remains open.

---

## Finding 6 — later $120 4K expansion claim is useful but not yet primary-source qualified

Multiple modern Apple-1 software/history references state that the base $666.66 machine included 4K and that an additional 4K cost $120.

This is plausible and useful for acquisition targeting, but it has not yet been promoted into the authoritative economic ledger because the current research pass has not located a qualifying period Apple price sheet/invoice explicitly supporting the $120 memory expansion.

### Consequence

Keep `$120 EXTRA 4K` as `SECONDARY_CORROBORATED / PRIMARY_SOURCE_OPEN` rather than using it as a direct component-cost fact.

---

## New acquisition priorities

1. Primary Apple invoice/price list showing the additional-4K price.
2. Direct period 3601 PROM price.
3. Pre-March-1976 74S257 price.
4. Pre-March-1976 DS0025 price.
5. Exact MK4096 suffixes and population patterns on early production boards.
6. Period 14.31818 MHz crystal price.
7. Power regulator/transformer price evidence.
8. PCB fabrication and assembly cost evidence.