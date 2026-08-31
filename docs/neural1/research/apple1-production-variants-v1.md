# Apple-1 Production Variants v1

**Status:** observational production-model scaffold  
**Purpose:** prevent 1976 MULTIVERSE from treating every Apple-1 as though one immutable component-vendor BOM was populated on every board.

## Core distinction

MULTIVERSE needs at least two different historical objects:

1. **Design BOM / functional architecture** — what the schematic requires electrically and logically.
2. **Production realization** — which compatible manufacturer/package/date-code parts were actually populated in particular production batches/boards.

The first is primarily schematic/manual territory. The second requires surviving-board evidence, production records, photographs, and specialist registry work.

Do not use production variation to rewrite the underlying circuit topology unless evidence shows an actual revision.

---

# Evidence source

Apple-1 Registry / Achim Baqué:

https://www.apple1registry.com/en/theapple1.html

The Registry documents surviving boards, component manufacturers/packages/date codes, repairs, replacements, and batch characteristics. It is an important specialist observational source but is not a substitute for original Apple procurement records.

---

# Observed production variation

## Logic vendors

The Registry summarizes a strong batch tendency:

- first-batch Apple-1s: many logic ICs from Fairchild Semiconductor;
- second-batch Apple-1s: many logic ICs from Signetics, with some Signetics also present in first-batch machines.

### Consequence

A historical production simulator should represent logic *function* separately from compatible manufacturer/package realization.

A design candidate that requires, for example, a 74161 should not automatically imply one manufacturer unless the experiment fixes procurement/vendor constraints.

---

## CPU

Observed manufacturers across surviving Apple-1 history include:

- MOS Technology;
- Synertek;
- AMI-derived/other period-compatible production context where separately evidenced.

MOS 6502 is the dominant historical association and is explicitly present in Apple documentation/advertising.

### Consequence

Keep `CPU_ARCHITECTURE = 6502` separate from `CPU_VENDOR/PACKAGE/DATE_CODE` for production-realization studies.

---

## PIA

The Registry documents Apple-1s with compatible 6820/6520-family PIAs from multiple vendors, including:

- AMI;
- Motorola;
- Synertek;
- MOS-family replacements/compatible parts in the broader ecosystem.

Examples of surviving-board records include AMI S6820 and later Synertek/Motorola parts; replacement history must always be distinguished from original population.

### Consequence

The canonical architecture requires the interface function, not one immutable vendor label.

Production studies should record:

```text
FUNCTION = PIA
DEVICE_FAMILY = 6820/6520-compatible under declared timing/electrical contract
VENDOR = observed supplier
PACKAGE = ceramic/plastic/etc.
ORIGINALITY = original / suspected original / replacement / unknown
```

---

## DRAM

Apple-1 Registry identifies Mostek MK4096-11 as the important Apple-1 DRAM family and documents both:

- `MK4096N-11` — plastic/epoxy package;
- `MK4096P-11` — ceramic/gold side-brazed package.

The Registry notes that Apple used the `-11` speed class; other speed grades found on surviving machines may reflect later replacements/upgrades and must be evaluated board by board.

Examples in the Registry include both original 8K populations and machines originally associated with 4K configurations later expanded or altered.

### Consequence

The production model must separate:

- RAM capacity shipped;
- number of DRAM positions populated;
- device family;
- speed grade;
- package;
- date code;
- later expansion/replacement history.

Do not infer base 4K versus 8K shipment solely from the number of sockets on the PCB.

---

## Character generator / shift-register section

The Registry documents package/vendor differences in the 2513 character generator and related video devices across known machines.

For example, the board used in some early Apple advertising has a white ceramic character generator and a component combination the Registry considers unusual enough that it may have been prepared specifically for advertising.

### Consequence

Do not use a single advertisement photograph as the canonical production-population template.

The video architecture should be reconstructed from schematic/function first and production variants modeled separately.

---

## PROMs

The Apple-1 Monitor resides in two 256x4 PROM devices. Surviving boards can have ceramic or plastic devices and replacement histories.

### Consequence

For MULTIVERSE:

- firmware contents are one artifact;
- PROM function/organization is another;
- actual device vendor/package on a surviving board is a production-realization attribute.

---

# Example evidence that variation matters

## Registry board #3 — Apple advertisement board

https://www.apple1registry.com/en/3.html

Registry notes include:

- ceramic MOS 6502;
- ceramic AMI PIA;
- 8K ceramic Mostek MK4096-11;
- ceramic character generator;
- component/date-code combination unlike known surviving production boards.

The Registry explicitly cautions that it may have been built especially for advertising.

### Research lesson

Advertising imagery is primary evidence that *a board existed in that configuration*, but it is not automatically evidence that all customer boards used the same population.

---

## Registry board #23 — documented RAM evolution

https://www.apple1registry.com/en/23.html

Registry records the machine as originally having approximately 4K plastic DRAM plus an additional single chip, with later expansion to 8K and a mixed DRAM population.

### Research lesson

A current photograph can encode decades of modification. Production-state reconstruction must retain chronology.

---

## Registry board #105 / #106 — preserved 8K examples

Recent Registry entries document boards with original 8K Mostek MK4096-11 populations and AMI S6820 PIAs.

Sources:

- https://www.apple1registry.com/en/105.html
- https://www.apple1registry.com/en/106.html

### Research lesson

8K production realizations are real, but they do not invalidate Apple's own advertised/base 4K pricing statement.

---

# Production-realization schema proposal

A component placement should eventually support fields like:

```json
{
  "designator": "B5",
  "function": "quad_2_to_1_mux_tristate",
  "required_family": "74S257-compatible",
  "observed_part": "...",
  "manufacturer": "...",
  "package": "...",
  "date_code": "...",
  "board_id": "...",
  "batch_class": "first|second|unknown",
  "originality": "original|suspected_original|replacement|unknown",
  "source_id": "...",
  "confidence": "..."
}
```

This enables three different questions:

1. **Could the design be built?** — functional architecture.
2. **What would it cost using a given supplier universe?** — procurement realization.
3. **What did surviving Apple actually use?** — observed historical realization.

These must not be collapsed.

---

# New MULTIVERSE experiments enabled

## Supplier substitution robustness

Hold the Apple-1 architecture constant while changing the historically available supplier pool.

Measure whether the design remains electrically valid and how sourced cost changes.

## First-batch versus second-batch market reconstruction

Construct observational supplier profiles from surviving-board evidence and compare likely market availability/cost without claiming undocumented Apple invoice prices.

## Procurement-constrained redesign

Blind an agent to one component family or vendor and ask it to preserve the capability contract using only period-valid alternatives.

This tests whether the Apple-1 architecture was robust to 1976 supply constraints.

## Artifact archaeology

Give an agent a structured, partially modified surviving-board manifest and ask it to separate likely original design intent, original population, and later repair/replacement state.

This should be scored against curated human annotations rather than free-form model confidence.

---

# Limits

- Registry evidence is curated specialist evidence, not Apple factory paperwork.
- Surviving boards are subject to repairs and modifications.
- Date-correct does not automatically mean original.
- A vendor used on one board does not establish Apple's contractual supplier.
- Exact batch membership itself may be uncertain for some machines.
- No production-cost inference should be made solely from current collector-market part values.