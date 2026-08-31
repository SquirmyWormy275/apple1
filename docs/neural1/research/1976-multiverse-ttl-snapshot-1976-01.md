# 1976 MULTIVERSE TTL Retail Snapshot — January 1976

**Status:** source-backed period retail snapshot  
**Cutoff eligibility:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  
**Economic regime:** R1 — hobbyist advertised retail

## Source

International Electronics Unlimited advertisement, *BYTE*, January 1976.

Archive copy:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

The scanned advertisement states that shipping would be by first-class mail in the U.S., Canada, and Mexico and presents a broad retail logic catalog, making it useful as a dated hobbyist-market price snapshot.

## Selected standard TTL prices visibly listed

| Part | Price (USD) |
|---|---:|
| 7400 | 0.14 |
| 7401 | 0.16 |
| 7402 | 0.15 |
| 7403 | 0.16 |
| 7404 | 0.19 |
| 7405 | 0.19 |
| 7406 | 0.35 |
| 7407 | 0.35 |
| 7408 | 0.18 |
| 7409 | 0.19 |
| 7410 | 0.16 |
| 7411 | 0.25 |
| 7413 | 0.55 |
| 7420 | 0.16 |
| 7427 | 0.29 |
| 7430 | 0.20 |
| 7432 | 0.23 |
| 7437 | 0.35 |
| 7438 | 0.35 |
| 7440 | 0.17 |
| 7473 | 0.35 |
| 7474 | 0.35 |
| 7475 | 0.57 |
| 7476 | 0.39 |
| 7483 | 0.79 |
| 7485 | 1.10 |
| 7486 | 0.40 |
| 7489 | 2.48 |
| 7490 | 0.59 |
| 7491 | 0.97 |

The advertisement contains many additional 74xx, low-power TTL, high-speed TTL, CMOS, memory, linear, display, and support-device prices. The table above is intentionally a bounded transcription, not a claim that these are the only available parts.

## Use in MULTIVERSE

This source can support:

- period-correct glue-logic cost estimation for candidate machines;
- comparison of alternative decode/counter/register strategies;
- validation that a candidate design's economic score is sensitive to actual chip count rather than an arbitrary per-chip constant.

## Rules

1. Do not treat this supplier's price as Apple's procurement price.
2. Do not mix these R1 retail prices with manufacturer volume prices without explicit regime conversion/reporting.
3. Exact Apple-1 BOM use requires a separately sourced component/netlist mapping; this file only supplies a market price snapshot.
4. Parts not transcribed here may be added only after direct verification against the source scan.
5. Preserve the January 1976 date with every derived economic result.
