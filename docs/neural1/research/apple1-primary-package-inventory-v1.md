# Apple-1 Primary Package Inventory v1

**Status:** high-confidence design/package inventory; topology discrepancies tracked separately  
**Purpose:** replace a modern-replica-only quantity baseline with a package inventory reconciled against Apple Drawing `00101 Rev A`, while keeping as-built net differences explicit.

## Method

Package families and counts were reconciled using:

1. Apple Computer Company Drawing `00101 Rev A`, sheets 1–3;
2. the Apple-1 Operation Manual's supplied-4K / onboard-8K statements;
3. a component-location reconstruction of an original-style Apple-1 as a secondary cross-check;
4. surviving-board / Apple-1 Registry evidence where relevant.

The drawing remains the primary **design** source. Known drawing-vs-PCB net discrepancies are stored separately in `apple1-drawing-vs-as-built-v1.md`.

The inventory below is therefore suitable as the initial design-component-count contract, but it is not a claim that every production board used the same manufacturer, package material, date code, or RAM population.

---

# Processor / memory section

| Function / family | Qty | Population rule | Design evidence / notes |
|---|---:|---|---|
| MOS 6502-class CPU | 1 | supplied configuration | Drawing sheet 2 note specifies 6502 supplied; dotted 6800/6501 option circuitry omitted in supplied 6502 configuration |
| 6820 PIA | 1 | supplied | Drawing sheet 2 / manual interface documentation |
| 256x4 PROM | 2 | supplied | A1/A2; drawing permits Signetics 82S129, Harris H1024, Intel/MMI 3601 |
| 4096x1 DRAM | 8 | base supplied 4K | manual states 4K supplied |
| 4096x1 DRAM | +8 | optional/full 8K onboard | manual states board sockets/capacity for 8K |
| 74S257-class address multiplexers | 4 | supplied | B5-B8; drawing sheet 2 note 13 explicitly identifies all four positions |
| 74154 decoder | 1 | supplied | processor-section address decode |
| 8T97-class tri-state buffer | 2 | supplied | processor/bus buffering |
| 74123 monostable | 1 | supplied | DRAM timing / refresh-related processor section |
| 7400 NAND | 1 of total 3 | supplied | B1 package in processor-section cross-check |
| 7410 NAND | 1 of total 2 | supplied | B2 package in processor-section cross-check |

## RAM profiles

The authoritative experiment profiles are:

- `APPLE1_4K_SUPPLIED` = 8 x 4096x1 DRAM;
- `APPLE1_8K_FULL` = 16 x 4096x1 DRAM.

Do not price all 16 DRAM positions when reconstructing the documented base 4K machine.

---

# Terminal / video section

| Family | Qty | Principal board-location cross-check | Function |
|---|---:|---|---|
| 2504 | 7 | C11B, D4A/B, D5A/B, D14A/B | dynamic shift-register display storage |
| 2513 | 1 | D2 | character generator |
| 2519 | 1 | C3 | static shift register |
| DS0025 | 1 | C11A | two-phase MOS clock driver |
| 555 | 1 | D13 | cursor/timing function |
| 74160 | 1 | D6 | counter |
| 74161 | 5 | D7, D8, D9, D11, D15 | counters / terminal timing |
| 74166 | 1 | D1 | parallel-load shift register |
| 74157 | 2 | C4, C14 | selector/multiplexer |
| 74174 | 1 | C7 | latch / display-control logic |
| 74175 | 1 | C13 | cursor/control logic |
| 7404 | 1 | D12 | inverter |
| 7408 | 1 | C12 | AND logic |
| 7402 | 1 | C10 | NOR logic |
| 7427 | 1 | C5 | 3-input NOR logic |
| 7432 | 1 | C9 | OR logic |
| 7450/compatible function | 1 | C8 | AND-OR-invert function; surviving first-batch evidence may use functionally compatible Fairchild 7451-style part |
| 7410 | 1 of total 2 | C6 | NAND logic |
| 7400 | 2 of total 3 | C15, D10 | NAND logic |

The secondary board-location mapping above agrees with the package families/counts visible in the original terminal-section drawing. Manufacturer/vendor/package realization is not encoded in this design table.

---

# Consolidated digital/terminal semiconductor counts

Excluding power regulators, discrete transistor(s), diodes, and passive components:

| Family | Qty with base 4K | Qty with full 8K |
|---|---:|---:|
| 6502 | 1 | 1 |
| 6820 PIA | 1 | 1 |
| 256x4 PROM | 2 | 2 |
| 4096x1 DRAM | 8 | 16 |
| 7400 | 3 | 3 |
| 7402 | 1 | 1 |
| 7404 | 1 | 1 |
| 7408 | 1 | 1 |
| 7410 | 2 | 2 |
| 7427 | 1 | 1 |
| 7432 | 1 | 1 |
| 7450/compatible | 1 | 1 |
| 74123 | 1 | 1 |
| 74154 | 1 | 1 |
| 74157 | 2 | 2 |
| 74160 | 1 | 1 |
| 74161 | 5 | 5 |
| 74166 | 1 | 1 |
| 74174 | 1 | 1 |
| 74175 | 1 | 1 |
| 74S257 | 4 | 4 |
| 2504 | 7 | 7 |
| 2513 | 1 | 1 |
| 2519 | 1 | 1 |
| 8T97 | 2 | 2 |
| 555 | 1 | 1 |
| DS0025 | 1 | 1 |

**Digital/terminal package count, base 4K:** 53 packages.  
**Digital/terminal package count, full 8K:** 61 packages.

These totals are a defined package-count metric, not the total number of board components.

---

# Power section packages / major semiconductors

Drawing `00101`, sheet 3, explicitly shows:

| Part / function | Qty | Notes |
|---|---:|---|
| LM323 | 1 | +5V regulator |
| LM320 MP-5 | 1 | -5V regulator |
| LM320 MP-12 | 1 | -12V regulator |
| LM340-12 | 1 | +12V regulator |
| MR500 rectifier | 4 | +5V raw supply rectifier path |
| 1N4001 rectifier | 4 | +/-12V supply path |

The board also contains filter/output capacitors, connectors, fusing, and other passive/support parts that belong in the full BOM but not the digital-package count above.

---

# Important schematic notes affecting BOM interpretation

## 6800/6501 option circuitry

The original processor drawing contains a dotted optional section for 6800/6501-style clock requirements. Drawing note 7 says these components are omitted in the supplied 6502 configuration.

Therefore they must not be included in the normal production-6502 BOM cost unless the experiment explicitly studies the prototype/6501/6800 configuration.

## PROM substitution

The original drawing explicitly permits multiple compatible 256x4 PROM families. MULTIVERSE may therefore treat PROM vendor selection as a historically documented substitution choice where timing/electrical constraints are met.

## RAM population

Physical 16-chip capacity does not imply 16 chips in the base advertised machine.

## Logic-vendor substitution

Package function/count is more stable than manufacturer realization. Surviving original boards show Fairchild/Signetics and other vendor variation.

---

# Confidence classes

- `P1_DRAWING_DIRECT` — part/count directly visible or explicitly noted on Apple drawing.
- `P1_MANUAL_DIRECT` — population/capacity directly stated by Apple manual.
- `RECONCILED` — drawing count agrees with serious board reconstruction / surviving-board evidence.
- `VARIANT` — function is stable but manufacturer/part-family details vary in production.

The consolidated counts above are intended to be `P1_DRAWING_DIRECT` or `RECONCILED`; production vendor identity is generally `VARIANT` unless a named board is being modeled.

---

# Sources

Primary:

- Apple Computer Company Drawing No. `00101`, Rev A, sheets 1–3.
- Apple Computer Company, *Apple-1 Operation Manual*, 1976.
- The Henry Ford, *Apple 1 Schematic Diagram, March 10, 1976*.

Secondary cross-checks:

- Mike Willegal, Apple 1 hardware/netlist reconstruction: https://www.willegal.net/appleii/apple1-hardware.htm
- A1 Mimeo original-style component-position record: https://www.applefritter.com/node/24536
- Jean-David Gadina / XS-Computer-One BOM: modern reconstruction, quantity cross-check only.
- Apple-1 Registry: surviving-board population and production-variant evidence.

Known drawing-vs-board wiring discrepancies are intentionally not 'fixed' here; see `apple1-drawing-vs-as-built-v1.md`.