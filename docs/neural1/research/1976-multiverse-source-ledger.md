# 1976 MULTIVERSE Source Ledger v1

**Status:** initial source acquisition / provenance ledger  
**Purpose:** establish what historical facts NEURAL1 may treat as authoritative when generating or scoring period-constrained computer designs.  

## Non-negotiable rule

A model's internal knowledge is never an authoritative historical source for 1976 MULTIVERSE.

A component, price, availability date, electrical specification, architecture fact, or Apple-1 comparison field may enter the authoritative dataset only when supported by a qualifying source record.

---

# 1. Temporal methodology

## 1.1 "1976" is not one technology bucket

The Apple-1 processor schematic reproduced by the Computer History Museum carries:

- **Design engineer:** S. Wozniak — **1976-03-10**
- **Project engineer:** S. Jobs — **1976-03-10**
- **Drawn by:** R. Wayne — **1976-04-02**

Source:

- Computer History Museum reproduction of the Apple-1 schematic / *The Computer Museum Report*, Vol. 17:  
  https://archive.computerhistory.org/resources/access/text/2011/12/102659144-05-01-acc.pdf

Therefore a blind reconstruction intended to represent the design world available to Wozniak must not silently use a part merely because it existed by December 1976.

## 1.2 Initial cutoff modes

### `DESIGN_1976_03_10`

Strict Apple-1 design-date world.

A part must be evidenced as available or publicly documented on or before **1976-03-10**.

A 1976 catalog with no sufficiently precise publication/availability evidence is not automatically acceptable for this cutoff.

### `YEAR_END_1976_12_31`

Technology documented as available by the end of 1976.

This is useful for studying how rapidly the design landscape changed during the same calendar year.

### Additional cutoffs

Additional dates may be added only with a declared research purpose and source policy.

Never move a cutoff merely to admit a desired component.

---

# 2. Evidence classes

## Historical fact evidence

| Class | Meaning |
|---|---|
| H0 | model memory / unsourced statement — prohibited as authoritative data |
| H1 | modern secondary account |
| H2 | reputable curator/archive description of a primary artifact |
| H3 | period trade publication / period advertisement / period manual |
| H4 | manufacturer period datasheet/catalog/manual or original Apple documentation |
| H5 | dated transactional artifact or directly inspected original artifact with provenance |

Prefer H4/H5 for authoritative machine records.

H2/H3 can establish fields where the underlying primary artifact is identifiable and the limitation is recorded.

## Price evidence

Prices are especially easy to misuse. Keep different price concepts separate.

| Code | Price basis |
|---|---|
| P0 | no qualifying price evidence |
| P1 | manufacturer list price / published manufacturer price |
| P2 | period trade-press quoted price |
| P3 | period distributor / dealer retail price |
| P4 | documented real transaction / invoice / cancelled check |
| P5 | inferred procurement cost — **not permitted** unless methodology is separately justified |

Never compare a P1 manufacturer quantity price against a P4 retail transaction as though they were the same economic quantity.

Every cost field must record:

- currency;
- date;
- quantity basis if known;
- source type;
- price basis code;
- uncertainty.

---

# 3. Source ledger

## A76-001 — Apple-1 Operation Manual

**Title:** *Apple-1 Operation Manual*  
**Date:** 1976  
**Source owner:** Apple Computer Company  
**Archive:** Computer History Museum  
**URL:** https://archive.computerhistory.org/resources/text/Apple/Apple.AppleI.1976.102646518.pdf  
**Evidence class:** H4 scan curated by CHM  
**Ingestion status:** READY / fields require page-level extraction  

### Directly supported fields observed in the scan

- CPU: MOS Technology 6502.
- Microprocessor clock frequency: 1.023 MHz.
- Effective cycle frequency including refresh waits: 0.960 MHz.
- Composite video output.
- Display: 40 characters per line, 24 lines, automatic scrolling.
- Display memory described as dynamic shift registers, 1K x 7.
- On-board RAM sockets: 8 KB capacity; 4 KB supplied.
- RAM described as 16-pin 4K dynamic type 4096 (2104 also appears as an equivalent notation in the scan).
- Dynamic RAM refresh is built into the system; four out of every 65 clock cycles are dedicated to refresh according to the expansion section.
- Expansion to 65K via the edge connector is described.
- Keyboard/display software interface and PIA register addresses are documented.
- Recommended power transformers and supply requirements are documented.
- The complete Woz Monitor listing is included.

### Why this source matters

This is the primary baseline for the capability contract that candidate 1976 MULTIVERSE machines may be asked to satisfy.

### Rights note

Use as cited historical source. Do not assume scan redistribution rights beyond the archive's terms.

---

## A76-002 — Apple-1 processor schematic / drawing 00101

**Title:** Apple Computer Company schematic diagram, Apple-1 processor section, Drawing 00101 Rev A  
**Original dates visible:** design/project engineering 1976-03-10; drawing 1976-04-02  
**Archive reproduction:** Computer History Museum  
**URL:** https://archive.computerhistory.org/resources/access/text/2011/12/102659144-05-01-acc.pdf  
**Evidence class:** H4 content reproduced by a museum source  
**Ingestion status:** READY for structural Apple-1 baseline; net-level extraction should be independently checked against the high-quality manual scan before machine ingestion  

### Supported fields observed

- the production unit as supplied used a 6502;
- the drawing explicitly provides a 6800 substitution path requiring additional components and jumper changes;
- user-selectable 4K chip-select blocks are documented;
- PROM alternatives are listed in schematic notes;
- expansion/DMA notes are documented;
- engineering dates establish a defensible strict historical cutoff.

### Research significance

The 6800 is not an arbitrary modern counterfactual. The Apple schematic itself contemplated it. The first CPU-substitution experiment should therefore prioritize **6502 versus 6800** before adding later or less directly relevant CPU families.

---

## A76-003 — Computer History Museum Apple-1 object record

**Title:** Apple-1 operation manual — CHM Revolution  
**URL:** https://www.computerhistory.org/revolution/personal-computers/17/300/1051  
**Evidence class:** H2 curator description  
**Status:** READY as provenance/identity support, not as component electrical data  

CHM identifies the manual as a 1976 Apple Computer Company artifact and notes that it contains the complete wiring diagram and monitor source.

---

## MOS-001 — MCS6500 Hardware Manual

**Title:** `6500-10A_MCS6500hwMan_Jan76.pdf`  
**Date:** January 1976  
**Manufacturer:** MOS Technology  
**Archive:** Bitsavers  
**Index:** https://bitsavers.org/components/mosTechnology/  
**Evidence class:** H4  
**Status:** HIGH PRIORITY ACQUISITION / extraction pending  

### Intended supported fields

- 6502 bus/timing/electrical architecture;
- clock requirements;
- memory/peripheral interface constraints;
- DMA/RDY behavior relevant to Apple-1 expansion.

### Cutoff

Eligible in principle for `DESIGN_1976_03_10` because the manual is dated January 1976, subject to exact field extraction.

---

## MOS-002 — MCS6500 Programming Manual

**Title:** *MCS6500 Microcomputer Family Programming Manual*, Publication 6500-50A, Second Edition  
**Date:** January 1976  
**Manufacturer:** MOS Technology  
**URL:** https://www.bitsavers.org/components/mosTechnology/6500-50A_MCS6500pgmManJan76.pdf  
**Evidence class:** H4  
**Status:** READY for instruction-set/programming-model extraction  

The scan identifies itself as MOS Technology copyright 1976, January 1976, Revision A.

---

## MOS-003 — MOS 6501/6502 introductory advertisement

**Artifact:** MOS Technology advertisement from *IEEE Computer*, September 1975  
**Period:** September 1975 / WESCON introduction  
**Source image provenance:** Wikimedia Commons record identifies the original as an advertisement appearing in September 1975 *IEEE Computer*, pp. 38–39  
**URL:** https://commons.wikimedia.org/wiki/File:MOS_6501_6502_Ad_Sept_1975.jpg  
**Evidence class:** H3 primary advertisement with documented provenance  
**Price basis:** P1/P2 depending on exact wording extracted from the ad  
**Status:** READY for price/availability extraction after direct image transcription is verified  

### Secondary corroboration

Computer History Museum states that the MOS 6502 was introduced in 1975 at a cost of $25:
https://www.computerhistory.org/timeline/1975/

### Rights

The Commons record marks this particular 1975 advertisement image as public domain based on the absence of a copyright notice. Preserve the Commons rights record if the image itself is ever reused.

---

## MOT-001 — M6800 Microprocessor Applications Manual

**Title:** `M6800_Microprocessor_Applications_Manual_1975.pdf`  
**Date:** 1975  
**Manufacturer:** Motorola  
**Archive index:** https://www.bitsavers.org/components/motorola/6800/  
**Evidence class:** H4  
**Status:** HIGH PRIORITY ACQUISITION / field extraction pending  

Eligible for strict March-1976 experiments once relevant fields are extracted.

---

## MOT-002 — MC6800 Microcomputer System Design Data

**Title:** *MC6800 Microcomputer System Design Data*  
**Date:** 1976  
**Manufacturer:** Motorola  
**URL:** https://www.bitsavers.org/components/motorola/6800/MC6800_Microcomputer_System_Design_Data_1976.pdf  
**Evidence class:** H4  
**Status:** READY for year-end 1976 data; publication timing must be resolved before strict March cutoff use  

Contains system-family technical data including clock, memory, PIA and interface material.

---

## MOT-003 — November 1976 M6800-family commercial pricing

**Title:** *Microcomputer Digest*, Vol. 3 No. 5, November 1976  
**URL:** https://bitsavers.org/magazines/Microcomputer_Digest/Microcomputer_Digest_v03n05_Nov76.pdf  
**Evidence class:** H3 period trade publication  
**Price basis:** P2  
**Status:** READY for `YEAR_END_1976_12_31`; not eligible for March cutoff pricing  

The issue reports commercial-temperature Motorola family pricing and says availability is off the shelf, including:

- MC6800CL: $49
- MC6820CL: $23
- MC6850CL: $24
- MC6810ACL: $9.25

These are November-1976 data and must not be projected backward to March without additional evidence.

---

## INTEL-001 — Intel Data Catalog 1975

**Title:** *Intel Data Catalog*  
**Date:** 1975  
**URL:** https://www.bitsavers.org/components/intel/_dataBooks/1975_Intel_Data_Catalog.pdf  
**Evidence class:** H4  
**Status:** READY / extraction pending  

Observed catalog coverage includes the 2101 and 2102 static RAM families plus ROM/PROM and logic devices. This is a useful source for period memory alternatives.

---

## INTEL-002 — Intel Data Catalog 1976

**Title:** *Intel Data Catalog*  
**Date:** 1976  
**URL:** https://www.bitsavers.org/components/intel/_dataBooks/1976_Intel_Data_Catalog.pdf  
**Evidence class:** H4  
**Status:** READY for year-end candidate records; exact publication date must be resolved for strict cutoff use  

The catalog describes the 8080A family and 1976 Intel memory products.

---

## SIG-001 — Signetics 2513/2514 character generator documentation

**Source:** Signetics MOS data literature scan  
**Archive URL:** https://www.bitsavers.org/components/signetics/_dataBooks/1971_Signetics_MOS.pdf  
**Evidence class:** H4  
**Status:** READY  

The document describes the 2513/2514 static character generator/ROM family, including the 2513 ASCII-font configuration and electrical/interface properties.

### Historical significance

This establishes that the 2513 family predates the Apple-1 design by several years; exact Apple-specific configuration still comes from Apple/board sources.

---

## SIG-002 — Signetics Data Manual 1976

**Title:** `1976_Signetics_Data_Manual.pdf`  
**Archive index:** https://www.bitsavers.org/components/signetics/_dataBooks/  
**Evidence class:** H4  
**Status:** HIGH PRIORITY ACQUISITION  

Target extraction:

- 2504 family;
- 2513;
- 2519;
- relevant TTL/logic data if present;
- exact electrical/timing properties.

Do not assume every device in a 1976 manual was available by March 10 without independent dating where necessary.

---

## TI-001 — TI Semiconductor Memory Data Book

**Title:** *The Semiconductor Memory Data Book*  
**Date:** 1975  
**Archive index:** https://www.bitsavers.org/components/ti/_dataBooks/  
**Evidence class:** H4  
**Status:** HIGH PRIORITY for alternate-memory records  

---

## TI-002 — TI TTL Data Book, 2nd edition

**Title:** *The TTL Data Book*, second edition  
**Date:** 1976  
**Archive index:** https://www.bitsavers.org/components/ti/_dataBooks/  
**Evidence class:** H4  
**Status:** HIGH PRIORITY for logic-device constraints  

Publication timing must be resolved before using a device as evidence of March-10 availability solely from this book.

---

## NS-001 — National Semiconductor Memory Databook

**Date:** 1976  
**Archive index:** https://www.bitsavers.org/components/national/_dataBooks/  
**Evidence class:** H4  
**Status:** source candidate / cutoff dating required  

---

## NS-002 — National Semiconductor TTL Databook

**Date:** 1976  
**Archive index:** https://www.bitsavers.org/components/national/_dataBooks/  
**Evidence class:** H4  
**Status:** source candidate / cutoff dating required  

---

## FAIR-001 — Fairchild F8 source set

**Primary archive:** https://www.bitsavers.org/components/fairchild/f8/  
**Relevant period documents include:**

- `F8_prelimUM_Jan75.pdf`
- `F8_FORMULATOR_1975.pdf`
- `F8S_Development_Module_Users_Manual_Aug75.pdf`
- `Fairchild_Semiconductor_-_F8_Microprocessor_brochure_-_1975.pdf`
- `67095665A_F8_Users_Guide_Feb76.pdf`

**Evidence class:** H4  
**Status:** READY as a period alternative architecture family, but inclusion in a given experiment must follow the experiment's capability contract rather than assuming F8 interchangeability with 6502/6800 systems.

---

## TI-003 — TMS1000 series

**Archive:** https://www.bitsavers.org/components/ti/TMS1000/  
**Relevant documents:** 1975 and February 1976 data/programming manuals  
**Evidence class:** H4  
**Status:** period-valid architecture family, but likely a poor fit for general Apple-1-like capability because it is a one-chip microcomputer architecture; retain for broader Multiverse studies, not the first direct Apple-1 substitute search.

---

## EA-001 — Electronic Arrays keyboard encoders

**Archive:** https://www.bitsavers.org/components/electronicArrays/  
**Documents:**

- `EA2007A_2030_197507_Keyboard_Encoder_197507.pdf`
- `EA2000_Keyboard_Encoder_197509.pdf`

**Evidence class:** H4  
**Status:** useful for period-valid keyboard-interface alternative studies.

---

## A1REG-001 — Apple-1 Registry component evidence

**Site:** Apple-1 Registry  
**Document/software index:** https://www.apple1registry.com/en/soft.html  
**Evidence class:** H2/H1 depending on page; modern specialist registry, often describing photographed primary artifacts  
**Status:** SECONDARY SUPPORT / physical-production evidence  

Useful for:

- observed component families and date codes on surviving boards;
- manual/ad/invoice identities;
- distinguishing production variation from schematic allowance;
- locating primary artifacts for follow-up.

Do not use a Registry component list as a substitute for manufacturer electrical specifications.

Examples currently observed in Registry records include original/period Apple-1 boards using MOS 6502 CPUs, AMI/Motorola-family 6820 PIAs, Mostek MK4096 DRAM, Signetics/GI 2513-family character generators, 2519 and 2504 video chips, and period TTL families.

---

## A1REG-002 — Apple-1 transaction evidence

The Apple-1 Registry records several primary transaction artifacts, including:

- a December 7, 1976 Apple Computer invoice listing an Apple-1 at $666.66 and ACI at $75 on the Frank Anderson system page;
- two July/August 1976 cancelled checks associated with the Ricketts Apple-1, including a $600 Apple-1 payment.

Example URLs:

- https://www.apple1registry.com/en/41.html
- https://www.apple1registry.com/en/30.html

**Evidence class:** H2 transcription/description of H5 artifacts unless the artifact image itself is independently inspected  
**Price basis:** P4 when the underlying artifact is directly verified  
**Status:** useful for product transaction history, not component procurement cost.

Never infer Apple's component cost from retail Apple-1 transaction prices.

---

# 4. Apple-1 baseline fields currently supportable

These fields can already be populated from the original Apple manual/schematic with high confidence once page/diagram extraction is formalized:

| Field | Current evidence |
|---|---|
| CPU | MOS Technology 6502 |
| Nominal CPU clock | 1.023 MHz |
| Effective cycle rate incl. refresh waits | 0.960 MHz |
| Display | composite video |
| Geometry | 40 columns x 24 lines, auto-scroll |
| Display memory concept | dynamic shift registers, 1K x 7 |
| On-board RAM capacity | 8 KB sockets |
| RAM supplied | 4 KB |
| RAM technology | 16-pin 4K dynamic RAM, type 4096 family |
| Expansion | up to 65K via edge connector described |
| Refresh | 4 of every 65 clock cycles used for refresh |
| User interface | keyboard + integrated display; Woz Monitor |
| Optional CPU path | 6800 substitution explicitly documented in schematic |
| Design date anchor | 1976-03-10 on schematic |

Do not yet populate a complete bill-of-materials cost for the Apple-1.

---

# 5. Major blocked evidence

The following are **not yet adequately established** for authoritative Multiverse scoring:

1. exact March-1976 single-unit/street prices for most Apple-1 components;
2. Apple's actual procurement prices for most components;
3. precise availability dates for every speed grade/manufacturer variant;
4. a fully machine-readable verified Apple-1 BOM tied net-by-net to the original drawing;
5. comparable period prices for all plausible alternative video architectures;
6. comparable period prices for dynamic versus static RAM systems including required support logic;
7. construction-time or labor-cost metrics that can be compared objectively;
8. defensible power numbers for complete candidate systems, rather than isolated typical chip values;
9. an exact period-valid component substitution set for every TTL position.

META/1 and the Multiverse scorer must represent these as unavailable rather than estimate them silently.

---

# 6. Acquisition priorities

## Priority 1 — exact Apple-1 baseline

- extract all three original schematic sheets at sufficient resolution;
- create a source-linked component/net inventory;
- distinguish required, optional, and 6800-only components;
- map each part to a manufacturer-neutral functional role;
- preserve drawing note numbers and source locations.

## Priority 2 — video subsystem

Acquire/extract period Signetics documentation for:

- 2504;
- 2513;
- 2519.

This is essential because Woz's video architecture is one of the most interesting parts of the Multiverse search.

## Priority 3 — memory alternatives

Build dated records for:

- Mostek MK4096/4096-family DRAM;
- Intel 2102 static RAM;
- period 4K dynamic alternatives;
- support/refresh requirements.

## Priority 4 — CPU/peripheral alternatives

First direct comparison:

- MOS 6502/6500 family;
- Motorola 6800/6820 family.

Then consider:

- Intel 8080A;
- Fairchild F8;
- Zilog Z80 only in cutoffs where availability is independently established;
- other architectures only with explicit research justification.

## Priority 5 — period pricing

Search period:

- manufacturer price lists;
- distributor catalogs;
- trade-magazine advertisements;
- dated invoices;
- electronics supplier ads.

Record quantity tiers and never back-project late-1976 price cuts into March.

---

# 7. Ingestion rule for the future machine-readable corpus

A component record should not become `authoritative=true` until it contains at minimum:

```text
component_id
manufacturer
part_number
functional_class
source_id
source_date
available_by
available_by_confidence
electrical_fields_supported
unsupported_fields
rights_status
```

If price is present:

```text
price_amount
price_currency
price_date
price_basis
price_quantity
price_source_id
```

If `available_by` is uncertain, the record must not pass a strict historical cutoff automatically.

---

# 8. Source repositories currently judged useful

- Computer History Museum — original Apple-1 documentation and curated history:  
  https://www.computerhistory.org/
- Bitsavers — period manufacturer manuals/catalogs and period technical publications:  
  https://bitsavers.org/
- Apple-1 Registry — specialist secondary registry and locator for primary artifacts:  
  https://www.apple1registry.com/
- Wikimedia Commons — only for specific artifacts with independently reviewed source/rights metadata, such as the 1975 MOS advertisement; never treat Commons generally as authoritative technical evidence.

---

# 9. Immediate research conclusion

The first scientifically defensible 1976 MULTIVERSE should **not** attempt a giant all-1976 parts universe immediately.

Start with a narrow, high-confidence world:

1. Apple-1 capability contract from original Apple documentation;
2. strict `1976-03-10` cutoff;
3. MOS 6502 and Motorola 6800 families;
4. source-backed period RAM, ROM, PIA, TTL, keyboard, and video components;
5. metrics limited to fields with qualifying evidence.

Then expand the universe as the ledger improves.

This avoids the most dangerous failure mode: producing an impressive-looking alternate-1976 design space contaminated by later components, inconsistent prices, or model memory.
