# Apple-1 Drawing vs. As-Built Topology v1

**Status:** source-backed discrepancy ledger / research architecture decision  
**Purpose:** keep the published Apple drawing, production PCB, surviving component population, and later repair state distinct inside 1976 MULTIVERSE.

## Core rule

The Apple Computer Company drawing `00101 Rev A` is a primary historical design artifact. It is **not automatically a perfect netlist of the production PCB**.

MULTIVERSE must therefore preserve at least four layers:

1. `DRAWING_00101_REV_A` — what Apple's published schematic shows.
2. `PRODUCTION_AS_BUILT` — topology reconstructed from the production PCB / high-confidence board evidence.
3. `PRODUCTION_POPULATION` — vendor/package/date-code realization on a specific original board or batch.
4. `LATER_STATE` — repairs, replacements, upgrades, or collector-era changes.

Do not silently 'correct' the primary drawing. Record a discrepancy object instead.

---

# Primary drawing identity

Apple Computer Company, Drawing No. `00101`, Rev A:

- Sheet 1 of 3 — Terminal Section;
- Sheet 2 of 3 — Processor Section;
- Sheet 3 of 3 — Power Supply.

Title-block evidence:

- design engineer: S. Wozniak — 3-10-76;
- project engineer: S. Jobs — 3-10-76;
- drawn by R. Wayne — 4-2-76 on production drawing sheets;
- Rev A / released for production on the large schematic sheets.

The Henry Ford preserves the Apple-1 schematic as a March 10, 1976 artifact.

Sources:

- https://www.thehenryford.org/collections/explore/artifact/473962
- Apple-1 Operation Manual / schematic scans.

---

# Documented drawing / board discrepancies

Mike Willegal's Apple-1 hardware reconstruction records differences found while laying out a board and comparing his netlist with Apple's published schematics:

Source:

https://www.willegal.net/appleii/apple1-hardware.htm

## DVA-001 — A2 PROM address A7

Willegal reports that address line 7 is connected to pin 15 of the PROM at location A2 on the actual board.

**Layer affected:** processor section netlist.  
**Policy:** preserve the original drawing connection separately from the reconstructed as-built connection.

## DVA-002 — A2 PROM address A1

Willegal reports that address line 1 is connected to pin 6 of PROM A2 on the actual board.

**Layer affected:** processor section netlist.

## DVA-003 — counter inputs are not all bussed as drawing implies

Willegal reports floating/unbussed inputs on the actual board at:

- D6 pins 3 and 5;
- D7 pins 3, 6, and 11;
- D8 pin 1;
- D9 pin 1.

**Layer affected:** terminal timing logic.

This is especially important for simulation because replacing a floating TTL input with an explicit logic level can change timing/behavior.

## DVA-004 — VINH naming inconsistency

The drawing uses `/VINH` in one location and `VINH` in another for what Willegal identifies as the same signal.

**Layer affected:** drawing nomenclature / terminal timing.

The authoritative source record should retain the labels exactly as drawn, plus a normalized-net identity used by the simulator.

## DVA-005 through DVA-009 — 6800/6501 option area

Willegal reports several differences between the published 6800 option circuit and the actual board, including:

- C8/C9 digital connections exchanged with C10/C11;
- R16/R18 connected to ground;
- R17/R19 connected to +5V;
- R22/R23 connected to phase-1 rather than DBE;
- R20/R21 connected to DBE rather than phase-1.

**Layer affected:** optional 6800/6501 clock-driver section.

These differences are historically interesting even though normal production 6502 operation omits the dotted-box option components.

---

# Primary sheet-2 notes that constrain interpretation

The Apple drawing itself states, in substance:

- the supplied unit includes a 6502 and omits components in the dotted 6800/6501 option box;
- PROMs are 256 x 4 and may be Signetics 82S129, Harris H1024, or Intel/MMI 3601;
- if DMA is required, the jumper is broken and 74S257 devices at B5-B8 are used; the note marks these positions as supplied;
- configurable chip-select jumpers map 4K blocks;
- +12/-12 edge-connector voltages are unregulated filtered DC.

These notes are part of the design contract and should be represented independently of the observed supplier/vendor population.

---

# Additional as-built behaviors worth preserving

Willegal also documents physical implementation traits not obvious from a simple logical netlist:

- +12V distribution to DRAM rows uses DRAM power pins at A15/B15 as board-layer feedthrough paths;
- terminal-section video can exhibit crosstalk-related spurious pixels from adjacent board traces;
- D8 74161 timing is unusually tight and can behave differently with faster `A`-suffix devices;
- -5V distribution can exhibit substantial switching noise across the DRAM/video MOS load.

These should **not** automatically be modeled in the baseline logical simulator. They belong in an optional `PHYSICAL_REALIZATION` model for experiments about historical implementation quirks or emulator-versus-hardware fidelity.

---

# Schematic intellectual-property note

Some surviving scans reproduce Apple's original drawing notice restricting reproduction/use of the drawing. The project should cite and analyze the schematic but should not assume that an online scan is freely redistributable.

Do not vendor third-party schematic scans into public release bundles without a separate rights review.

---

# Required MULTIVERSE data objects

## Drawing net

```json
{
  "drawing_id": "00101_REV_A",
  "sheet": 2,
  "source_label": "VINH",
  "normalized_net": "VINH",
  "source_id": "..."
}
```

## Discrepancy

```json
{
  "discrepancy_id": "DVA-001",
  "drawing_object": "...",
  "drawing_state": "...",
  "as_built_state": "...",
  "evidence": ["..."],
  "confidence": "...",
  "simulation_impact": "..."
}
```

## Experiment selector

Every topology-sensitive experiment should declare one of:

- `DRAWING_00101_REV_A`;
- `PRODUCTION_AS_BUILT_V1`;
- a named surviving-board state where adequate evidence exists.

A run that does not declare its topology source is invalid for historical-result publication.

---

# Research opportunities created by the discrepancy model

## Drawing-versus-board validation benchmark

Give a model the drawing plus a curated set of measured/observed board facts and ask it to identify the smallest discrepancy set explaining the observations.

## Emulator fidelity study

Compare logical behavior under the published drawing and the reconstructed production topology for known edge conditions.

## Historical engineering-error analysis

Ask which published-drawing discrepancies are behaviorally irrelevant under normal supplied-6502 use and which materially alter simulation.

## Artifact reconstruction challenge

Give an agent incomplete evidence from a surviving board and require it to classify each statement as:

- drawing fact;
- as-built observation;
- production-population observation;
- later modification;
- unresolved.

This directly fits META/1's evidence/claim model.