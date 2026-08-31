# 1976 MULTIVERSE Price Ledger v1

**Status:** initial economic-evidence ledger  
**Purpose:** prevent incompatible or anachronistic component prices from entering 1976 MULTIVERSE scoring.  

## Rule

A component can be historically available without having a usable historical price.

When price evidence is absent or not comparable, the authoritative field remains unavailable. NEURAL1 must not ask an LLM to estimate the missing value.

Every price record must retain:

- part/family;
- price;
- currency;
- publication/transaction date;
- quantity tier;
- price basis;
- source;
- cutoff eligibility;
- limitations.

---

# Confirmed / high-confidence period records

## PRICE-MOS6502-1975-09

**Part:** MOS Technology 6502  
**Price:** USD $25  
**Date:** September 1975  
**Context:** introductory MOS advertisement / WESCON sale offering  
**Quantity basis:** individual sale / advertisement context; preserve exact ad wording during final transcription  
**Price basis:** P1/P2 pending direct final transcription classification  
**Eligible cutoffs:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  

**Primary-artifact provenance record:**  
https://commons.wikimedia.org/wiki/File:MOS_6501_6502_Ad_Sept_1975.jpg

The Commons record identifies the source as a MOS Technology advertisement appearing in the September 1975 issue of *IEEE Computer*, pp. 38–39, for the September 16–19, 1975 WESCON.

**Secondary corroboration:** IEEE Spectrum and Computer History Museum histories identify the 6502's $25 introductory price.

**Rights note:** the Commons record marks this advertisement image public domain based on lack of a copyright notice. Preserve that rights record if the image is ever redistributed.

---

## PRICE-MC6800-1975-10-30

**Part:** Motorola MC6800  
**Price:** USD $69  
**Date:** 1975-10-30  
**Quantity basis:** quantity one  
**Prior price stated in source history:** $175 quantity one; $125 for 50–99 before the reduction  
**Price basis:** P1 — manufacturer advertisement  
**Eligible cutoffs:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  

**Primary citation identity:** Motorola advertisement, “All this and unbundled $69 microprocessor,” *Electronics*, Vol. 48 No. 22, 1975-10-30, p. 11.

**Current accessible source trail:**  
https://www.swtpc.com/mholley/microprocessors/microprocessor_history.html

The source index explicitly identifies the period advertisement and the quantity-one price reduction.

**Acquisition note:** retain the direct period magazine scan or independently archived advertisement image in the final evidence package before marking the machine-readable price row fully ingested.

---

## PRICE-MC6820-1974-12-26

**Part:** Motorola MC6820 Peripheral Interface Adapter  
**Price:** USD $28  
**Date:** 1974-12-26  
**Quantity basis:** small quantities  
**Price basis:** P2 — period trade publication product report  
**Eligible cutoffs:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  

**Primary period source:** *Electronics*, 1974-12-26, p. 114.  
https://www.worldradiohistory.com/Archive-Electronics/70s/74/Electronics-1974-12-26.pdf

The period text describes the MC6820 PIA, its 40-pin ceramic DIP packaging, and states that it cost **$28 each in small quantities**.

---

## PRICE-MC6820-1975-04-26

**Part:** Motorola MC6820 Peripheral Interface Adapter  
**Price:** USD $28  
**Date:** 1975-04-26  
**Quantity basis:** 1–24  
**Price basis:** P2 — period trade publication product listing  
**Eligible cutoffs:** `DESIGN_1976_03_10`, `YEAR_END_1976_12_31`  

**Primary period source:** *Electronic Design*, Vol. 23 No. 9, 1975-04-26.  
https://www.worldradiohistory.com/Archive-Electronic-Design/1975/Electronic-Design-V23-N09-1975-0426.pdf

The listing gives Motorola Semiconductor Products' MC6820 PIA at **$28 (1–24)**.

### Significance

This is an unusually useful strict-cutoff record because it establishes a price and an explicit low-quantity tier well before the Apple-1 design date.

---

## PRICE-SIG2519B-1972

**Part:** Signetics 2519B / 2518B shift-register family  
**Price:** USD $6  
**Date:** January 1972 period source  
**Quantity basis:** 250–999  
**Availability:** stock  
**Price basis:** P2 — period trade product listing  
**Cutoff use:** proves early commercialization and provides historical economic context; **do not use as a March-1976 price without a study explicitly permitting older price observations**.  

**Primary period source:** *Electronic Design*, January 1972 issue record located during source acquisition.  
https://www.worldradiohistory.com/Archive-Electronic-Design/1972/Electronic-Design-V20-N01-1972-0106.pdf

### Limitation

This quantity tier is radically different from single-unit hobbyist purchasing. It must not be compared directly against a quantity-one CPU price in an assembled BOM without an explicit price-normalization methodology.

---

# Late-1976 records — useful only for later cutoff worlds

## PRICE-MOTOROLA-FAMILY-1976-11

**Date:** November 1976  
**Source:** *Microcomputer Digest*, Vol. 3 No. 5  
**URL:** https://bitsavers.org/magazines/Microcomputer_Digest/Microcomputer_Digest_v03n05_Nov76.pdf  
**Price basis:** P2  
**Eligible cutoff:** `YEAR_END_1976_12_31` only  

Reported commercial-temperature family prices include:

- MC6800CL — $49
- MC6820CL — $23
- MC6850CL — $24
- MC6810ACL — $9.25

The issue describes availability as off the shelf.

These values must **not** be projected backward into the March-1976 design world.

---

# Product-level transaction records — not component cost

## PRICE-APPLE1-INVOICE-1976-12-07

**Product:** Apple-1  
**Price:** USD $666.66  
**Date:** 1976-12-07  
**Additional ACI:** $75  
**Basis:** P4 if underlying invoice image is directly inspected  
**Locator:** Apple-1 Registry Frank Anderson system record  
https://www.apple1registry.com/en/41.html

**Use:** Apple-1 retail/product history only.

**Prohibited inference:** do not derive Apple's component procurement cost or margin from this invoice without separate cost evidence.

---

## PRICE-APPLE1-RICKETTS-1976

**Product:** Apple-1 transaction  
**Recorded payment:** USD $600 for Apple-1 in the Registry description; separate later payment associated with software/programming  
**Date:** July/August 1976 according to artifact history  
**Basis:** P4 only after underlying check is directly verified  
**Locator:**  
https://www.apple1registry.com/en/30.html

**Use:** product transaction history, not BOM cost.

---

# Important missing price evidence

These remain priority targets:

| Component/family | Strict March-1976 price status |
|---|---|
| Mostek MK4096 / exact Apple-1 DRAM grade | MISSING |
| Signetics 2504 | MISSING |
| Signetics 2513 | MISSING |
| Signetics 2519 near 1975/early-1976 | MISSING; only older quantity-tier evidence currently recorded |
| Common Apple-1 TTL parts | MISSING as a coherent comparable price set |
| PROM/ROM alternatives in Apple schematic | MISSING |
| Keyboard encoders | MISSING |
| Power regulators / analog support | MISSING |
| Connectors / sockets / board fabrication | MISSING |

---

# Pricing methodology decisions still required

1976 MULTIVERSE must not produce a fake single-dollar cost score until these questions are explicitly resolved:

1. **Quantity basis:** are candidate machines priced at quantity one, hobbyist retail, or a documented production tier?
2. **Date basis:** use latest qualifying price before cutoff, nearest qualifying observation, or a declared price window?
3. **Distributor versus manufacturer:** should these be separate frontiers rather than normalized together?
4. **Missing price:** exclude the candidate, mark cost incomplete, or compute a partial-cost lower bound?
5. **Board/support costs:** how are PCB, connectors, sockets, transformers, and passives treated?
6. **Alternative designs:** must support logic and refresh circuitry be priced alongside the primary memory/video chip?

Recommended initial policy:

> Use only directly sourced component prices at their declared quantity/date basis. Report **partial sourced cost** plus **coverage percentage**, rather than pretending the complete BOM cost is known.

Example:

```text
SOURCED COMPONENT COST: $X
COST-COVERED REQUIRED LINE ITEMS: 18 / 31
COST COVERAGE: 58%
COMPLETE BOM COST: UNAVAILABLE
```

This is less visually satisfying than a fake total and far more scientifically defensible.
