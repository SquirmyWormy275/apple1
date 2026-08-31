# 1976 MULTIVERSE Source Findings 02

**Date:** 2026-08-30  
**Status:** source-upgrade note  
**Purpose:** record newly located pre-cutoff retail and whole-system evidence relevant to March-1976 MULTIVERSE experiments.

## Finding 1 — January 1976 BYTE provides a strong hobbyist-retail component snapshot

A James Electronics advertisement in *BYTE*, January 1976, visibly lists period retail prices for several parts central to alternate Apple-1 designs.

Selected directly visible entries include:

- Signetics 2504, 1024 dynamic shift register: **$9.00**;
- Signetics 2519, hex 40-bit shift register: **$4.00**;
- Signetics 2513 character generator: **$11.00**;
- Intel 2102, 1024x1 static RAM: **$2.95**;
- Intel 1702A FAMOS PROM/EPROM family: **$15.95**;
- 8080 / 8080A-class advertised CPU pricing around **$39.95** in the same market context.

Source:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

### Consequence

The strict `DESIGN_1976_03_10` universe now has a source-backed **R1 hobbyist retail** basis for comparing at least some competing display-memory and boot-storage strategies.

This does not establish Apple's procurement cost.

---

## Finding 2 — January 1976 BYTE also supplies broad glue-logic retail pricing

A separate International Electronics Unlimited advertisement in the same issue lists a broad TTL catalog.

Selected prices include:

- 7400: **$0.14**;
- 7404: **$0.19**;
- 7410: **$0.16**;
- 7474: **$0.35**;
- 7489: **$2.48**;
- 7490: **$0.59**.

Source:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

### Consequence

MULTIVERSE does not need an arbitrary flat "TTL chip cost" assumption. Candidate machines can eventually be scored from actual period retail prices for many glue-logic choices, provided each chip used by the candidate has a sourced row.

---

## Finding 3 — March 1976 BYTE supplies a contemporaneous complete-system comparator

The March 1976 issue advertises the Southwest Technical Products 6800 computer system.

The advertisement states:

- Motorola M6800 processor;
- Mikbug ROM operating system;
- 2,048 words of memory in the advertised $395 system;
- complete system with serial interface and 2,048 words of memory: **$395**;
- full 4K static-memory board: **$125**;
- serial or parallel interface: **$35**.

Source:

https://vintageapple.org/byte/pdf/197603_Byte_Magazine_Vol_00-07_Cassette_Interfaces.pdf

### Consequence

This should be stored as economic regime **R5 — whole-system contemporary market comparison**, not decomposed into unsupported component prices.

It gives MULTIVERSE a period reference point for what a complete 6800-based system with monitor/serial infrastructure and memory cost immediately around the Apple-1 design date.

---

## Finding 4 — the March-10 cutoff should remain strict

The Henry Ford holds an Apple 1 schematic explicitly dated **10 March 1976**.

Source record:

https://www.thehenryford.org/collections/explore/artifact/473962

This reinforces the need to distinguish:

- `DESIGN_1976_03_10`;
- later 1976 availability/pricing;
- year-end 1976 comparisons.

A later-1976 component may be useful in a `YEAR_END_1976_12_31` search while remaining prohibited in a blind strict-design reconstruction.

---

## Next acquisition targets

Highest priority:

1. period MK4096 / compatible 4096-family pricing before 1976-03-10;
2. Apple-1 schematic/BOM transcription into a provenance-aware component-count baseline;
3. period crystal / timing-component prices;
4. PROM parts used by the Apple-1 and equivalent boot-storage alternatives;
5. sockets, connectors, regulators, transistors, and passive-component pricing sufficient to quantify cost coverage honestly;
6. documented Apple procurement evidence where available;
7. additional pre-cutoff supplier snapshots to estimate supplier sensitivity rather than relying on a single retail ad.

Do not fill these gaps from modern collector pricing or LLM estimates.
