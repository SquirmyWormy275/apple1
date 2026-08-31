# 1976 MULTIVERSE Retail Price Snapshot — January 1976

**Status:** source-backed period retail snapshot  
**Cutoff eligibility:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  
**Source type:** period hobbyist supplier advertisement  

## Source

James Electronics advertisement, *BYTE*, January 1976, p. 79/80 scan region in the restored issue.

Archive copy:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

The scanned advertisement visibly lists retail prices for microprocessor, shift-register, ROM, RAM, PROM, and support parts. This snapshot is valuable because it is both **pre-March-10-1976** and oriented toward the electronic hobbyist / small-quantity market rather than only manufacturer volume pricing.

## Directly visible prices

| Part | Description in ad | Price (USD) |
|---|---|---:|
| 8080 | `SUPER 8008` | 39.95 |
| 8080A | advertised headline price | 39.95 |
| 2504 | `1024 DYNAMIC` shift register | 9.00 |
| 2518 | `HEX 32 BIT` | 7.00 |
| 2519 | `HEX 40 BIT` | 4.00 |
| 2524 | `512 DYNAMIC` | 3.50 |
| 2525 | `1024 DYNAMIC` | 6.00 |
| 2533 | `1024 STATIC` | 7.95 |
| 2513 | `CHAR. GEN.` | 11.00 |
| 7488 | `RANDOM BITS` | 3.50 |
| 1101 | 256x1 static RAM | 2.25 |
| 1103 | 1024x1 dynamic RAM | 5.95 |
| 2101 | 256x1 static RAM | 6.95 |
| 2102 | 1024x1 static RAM | 2.95 |
| 2107 | 4096x1 dynamic RAM | 19.95 |
| 2111 | 256x4 static RAM | 7.95 |
| 7489 | 16x4 static RAM | 2.49 |
| 1702A | 2048-bit FAMOS PROM/EPROM family | 15.95 |
| 5203 | 2048-bit FAMOS | 14.95 |
| 8223 | 32x8 bipolar PROM | 3.00 |
| 74S287 | PROM / static entry as advertised | 7.95 |

## Interpretation rules

1. Treat these as **January 1976 advertised retail prices from one supplier**, not universal market prices.
2. Do not substitute these values for manufacturer quantity pricing or Apple procurement cost.
3. Preserve exact date and source identity with every derived economic comparison.
4. Where the advertisement does not explicitly state a quantity tier, classify the value as `RETAIL_ADVERTISED_PRICE` rather than inventing `quantity_one`.
5. Use this snapshot as one economic regime in MULTIVERSE rather than the sole regime.

## Why this matters

This single source establishes that, before the Apple-1 design cutoff, hobbyist buyers could see contemporaneous advertised prices for several architectural alternatives central to the MULTIVERSE search space:

- shift-register versus static-RAM display storage;
- character-generator ROM versus other display approaches;
- 8080-class CPU alternatives;
- small static RAM and dynamic RAM;
- erasable PROM/EPROM boot storage.

It therefore enables genuinely date-bounded cost comparisons without asking an LLM to guess period prices.

## Important limitation

This snapshot does **not** include a visible MK4096 listing. The Apple-1 DRAM-family cost remains an independent evidence target. A complete Apple-1 BOM cost must remain unavailable until sufficiently comparable coverage exists.
