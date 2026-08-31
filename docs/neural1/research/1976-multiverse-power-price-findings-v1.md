# 1976 MULTIVERSE Power-Regulator Price Findings v1

**Status:** source-backed partial power-section economic evidence  
**Cutoff:** pre-`DESIGN_1976_03_10`  
**Purpose:** improve Apple-1 and alternate-design cost coverage without silently treating a family/package price as the exact Apple production part price.

## Primary 1975 retail snapshot

The September 1975 first issue of *BYTE* contains a JAMES Electronics advertisement with a large linear-IC price table.

Primary scan:

https://vintageapple.org/byte/pdf/197509_Byte_Magazine_Vol_00-01_The_Worlds_Greatest_Toy.pdf

The visually verified advertisement includes:

- `LM323K-5` — **$14.00**;
- `LM320` negative-regulator family entries in K / other listed package forms;
- `LM340` positive-regulator family entries including 12 V forms;
- multiple TO/package variants with distinct prices.

The exact table must be transcribed package-by-package before importing every row into an authoritative machine-readable cost snapshot.

## PRICE-LM323K-1975-09

**Part:** National Semiconductor LM323K / 5 V, 3 A fixed regulator family  
**Apple-1 relation:** +5 V high-current regulator  
**Observed advertised price:** **$14.00**  
**Date:** September 1975  
**Economic regime:** R1 hobbyist retail  
**Source:** JAMES Electronics advertisement, *BYTE*, September 1975  
**Cutoff eligible:** yes for `DESIGN_1976_03_10`  

The Apple-1 reconstruction literature and surviving-board evidence identify National LM323K as the original-style +5 V regulator. National's 1975 linear data book documents LM323K as a 3 A TO-3 regulator.

### Use

This row is strong enough to enter the strict pre-cutoff retail snapshot as a price observation for the +5 V regulator family, while board-specific manufacturer/date-code/originality remains a separate production-realization field.

---

# Negative regulator package issue

The Apple-1 production-style part records identify:

- `LM320MP-5.0` — -5 V, TO-202 power package;
- `LM320MP-12` — -12 V, TO-202 power package.

National Semiconductor documentation confirms `MP` as the TO-202 power-package order family for LM320 negative regulators.

Period retail advertisements found so far clearly price several LM320 K/T-family variants, for example April 1975 listings around:

- LM320-5K — $2.90;
- LM320-5T — $2.50;
- LM320-12K — $2.90;
- LM320-12T — $2.50.

Source:

https://www.worldradiohistory.com/Archive-Radio-Electronics/70s/1975/Radio-Electronics-1975-04.pdf

### Policy

These values demonstrate the period market price scale of the LM320 family, but they are **not yet the exact Apple `MP` package price**.

Therefore:

- `LM320MP-5_EXACT_R1_PRICE = null`;
- `LM320MP-12_EXACT_R1_PRICE = null`;
- family/package-comparator records may retain the K/T observations;
- a candidate alternate design may use a K/T part only if its package/electrical/thermal integration is explicitly valid under the design contract.

Do not silently assign $2.50 or $2.90 to the Apple production `MP` row.

---

# Positive +12 V regulator package issue

Apple-1 reconstruction sources identify the production-style +12 V device as a National `LM340MP-12` / TO-220-class device, while period advertisements frequently list `LM340-12K` and `LM340T-12` forms.

Period evidence includes:

- December 1974: `LM340-12K` — **$2.60**;
- April 1975: `LM340-12K` — **$2.60**;
- September 1975 JAMES table: 12 V LM340 K/T-family entries around **$1.95 / $1.75** depending package.

Representative sources:

- https://www.worldradiohistory.com/Archive-Poptronics/70s/1974/Poptronics-1974-12.pdf
- https://www.worldradiohistory.com/Archive-Radio-Electronics/70s/1975/Radio-Electronics-1975-04.pdf
- https://vintageapple.org/byte/pdf/197509_Byte_Magazine_Vol_00-01_The_Worlds_Greatest_Toy.pdf

### Policy

As with the negative regulators, these are valid period family/package observations but do not yet establish one exact Apple production-package R1 price.

Keep the exact production-style row unresolved until the exact suffix/package price is sourced.

---

# Power-section cost coverage consequence

The current Apple-1 design baseline contains four major regulator packages:

- +5 V LM323K-class;
- -5 V LM320MP-5-class;
- -12 V LM320MP-12-class;
- +12 V LM340MP-12-class.

At present:

- +5 V LM323K has a strong exact-family pre-cutoff retail observation: **$14.00**;
- the remaining three have strong pre-cutoff family-level market-price evidence, but exact Apple package-price evidence remains incomplete.

This is enough to improve economic sensitivity modeling, but not enough to represent the complete Apple power-regulator subtotal as historically exact.

---

# Methodological lesson

Historical chip pricing must preserve at least:

```text
FUNCTION
FAMILY
EXACT ORDER NUMBER
PACKAGE
DATE
SELLER
PRICE
QUANTITY TIER
```

A regulator with the same output voltage but a different package/current/thermal profile is not automatically the same costed component.

MULTIVERSE should reward source completeness rather than hide uncertainty.

---

# Next power-section acquisition targets

1. Exact pre-March-1976 `LM320MP-5.0` retail or low-quantity price.
2. Exact pre-March-1976 `LM320MP-12` price.
3. Exact pre-March-1976 `LM340MP-12` price / clarification of early National package-order nomenclature.
4. MR500 rectifier period price.
5. 1N4001 period price.
6. Major electrolytic capacitor prices.
7. Board fuse/connector/passive prices if a complete motherboard-cost study requires them.
8. External transformer prices separately from the Apple motherboard BOM.

External transformers remain a customer-supplied power-package cost, not part of the $666.66 Apple motherboard cost unless the experiment explicitly constructs a fully powered interactive package.