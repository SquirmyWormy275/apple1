# 1976 MULTIVERSE Economic Regimes

**Status:** methodology / preregistration support  
**Purpose:** prevent economically invalid comparisons between period designs.

## Principle

There is no single historically meaningful number called "the 1976 price" of a component.

A price is only comparable when its acquisition context is preserved.

MULTIVERSE must therefore score candidate machines under explicitly selected economic regimes rather than collapsing every period price into one table.

## Regime R1 — Hobbyist advertised retail

Use period advertisements and catalogs aimed at individual builders or small buyers.

Examples:

- January 1976 James Electronics BYTE advertisement;
- contemporary mail-order electronics advertisements;
- period hobbyist distributor catalogs.

Required fields:

- publication/catalog date;
- supplier;
- advertised unit price;
- stated quantity tier if any;
- stock/delivery statement if present;
- source artifact.

Use case:

> What might an individual technically capable builder have had to pay in the contemporaneous hobbyist market?

Do not silently infer that Steve Wozniak or Apple actually paid these prices.

## Regime R2 — Manufacturer low-quantity list price

Use manufacturer advertisements, price announcements, and data-book price tables where the quantity tier is approximately one to tens of units.

Use case:

> Compare component families using contemporary manufacturer pricing at modest quantities.

## Regime R3 — Production / volume pricing

Use explicitly stated manufacturer/distributor quantity tiers such as 100, 250, 1000, etc.

Use case:

> What happens to the design frontier if the machine is intended for repeated production rather than one-off construction?

Never compare R3 directly to R1 without labeling the difference.

## Regime R4 — Documented Apple procurement

Use only evidence of what Apple/Wozniak/Jobs/Byte Shop actually paid or were quoted for specific components.

This is the highest-value regime for reconstructing real Apple economics but is expected to have sparse coverage.

Unknown values remain null.

## Regime R5 — Whole-system contemporary market comparison

Use contemporary complete systems, kits, boards, terminals, and memory products as context rather than component-BOM input.

Examples already identified:

- January 1976 JOLT system advertisement;
- March 1976 Southwest Technical Products 6800 system advertisement.

These records can answer questions such as:

- how much did an integrated competing computer cost?
- what premium accompanied RAM, serial interfaces, monitors, power supplies, or complete packaging?

They must not be decomposed into unsupported component prices.

## Cost coverage

Every candidate-machine economic score must report coverage.

Example:

```text
SOURCED COST:        $83.40
SOURCED LINE ITEMS:  18 / 31
QUANTITY REGIME:     R1
COST COVERAGE:       58%
TOTAL BOM COST:      UNAVAILABLE
```

A design with incomplete cost coverage cannot be declared globally cheaper than another design merely because its known subtotal is lower.

## Cross-regime reporting

Where sufficient evidence exists, MULTIVERSE may report the same design under several regimes:

```text
DESIGN M-01842

R1 HOBBYIST RETAIL:     $...
R2 LOW-QTY MFR:         $...
R3 VOLUME 100+:         $...
R4 APPLE PROCUREMENT:   UNAVAILABLE
```

This is preferable to creating a synthetic blended price.

## Temporal rule

A price must satisfy both:

1. the experiment's historical cutoff; and
2. the chosen economic regime.

A 1972 Signetics 2519 volume quote demonstrates historical commercialization and can be useful context, but it is not a substitute for a March-1976 hobbyist retail price.

## Inflation

Primary MULTIVERSE optimization should operate in nominal period dollars.

Modern inflation-adjusted dollars may be reported as a secondary interpretive output, never substituted for period-dollar optimization.

## Missing data

Missing values remain missing.

Do not:

- interpolate from modern collector prices;
- ask an LLM to estimate a component price;
- use a later price as though it applied before the cutoff;
- infer one supplier's discount from another supplier;
- infer Apple procurement cost from retail advertisements.

## Initial source-backed anchors

Current research records include:

- MOS 6502 introductory price, September 1975;
- Motorola MC6800 quantity-one price, October 1975;
- Motorola MC6820 small-quantity pricing, 1974/1975;
- January 1976 hobbyist retail snapshot containing 2504, 2519, 2513, 2102, 1702A, and other parts;
- 1972 Signetics 2519-family production-quantity price for historical context.

See:

- `1976-multiverse-price-ledger.md`
- `1976-multiverse-retail-snapshot-1976-01.md`
- `1976-multiverse-source-ledger.md`
