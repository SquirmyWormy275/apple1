# 1976 MULTIVERSE Source Findings 01

**Date:** 2026-08-30  
**Status:** source-upgrade note  
**Purpose:** record newly located period evidence that changes which component families can safely enter the strict `DESIGN_1976_03_10` world.

## Finding 1 — Apple-1 video-device families are documented years before 1976

The 1971 Signetics MOS data book indexed by Bitsavers contains explicit entries for:

- `2502/2503/2504` — 1024-bit-capacity multiplexed dynamic shift registers;
- `2513/2514` — high-speed character generator / ROM family;
- `2518/2519` — hex 32 / hex 40-bit static shift registers.

Source:

https://www.bitsavers.org/components/signetics/_dataBooks/1971_Signetics_MOS.pdf

The same book's extracted descriptions identify:

- 2513 as an ASCII-font character-generator configuration;
- 2519 as the hex 40-bit static shift-register member;
- 2504 as part of the 1024-bit multiplexed dynamic shift-register family.

### Consequence

Basic availability of the **2504, 2513, and 2519 families** does not need to rely on a late-1976 or 1977 Signetics data book.

They are eligible for the strict `DESIGN_1976_03_10` component universe, subject to:

1. extracting the exact model/variant properties required by the simulator;
2. distinguishing generic family documentation from the precise Apple-1-installed suffix/package/font variants;
3. using Apple-specific sources for the actual production configuration.

This materially strengthens the source basis for a blind reconstruction of the Apple-1 video subsystem.

---

## Finding 2 — period trade pricing exists for the 2519 family, but must not be treated as 1976 pricing

An *Electronic Design* item from January 1972 describes Signetics 2518B and 2519B shift registers and reports:

- price: **$6**;
- quantity basis: **250 to 999**;
- availability: **stock**.

Source:

https://www.worldradiohistory.com/Archive-Electronic-Design/1972/Electronic-Design-V20-N01-1972-0106.pdf

### Consequence

This is useful evidence that the device family was a commercial product well before the Apple-1.

It is **not** valid evidence for a March-1976 component price. The price must be stored with its 1972 date and quantity tier. A 1976 price remains a separate acquisition target.

---

## Finding 3 — Mostek MK4096 availability is directly supported before the Apple-1 design

Period *Electronic Design* material documents the Mostek MK4096 before 1976.

### November 22, 1974 advertisement

The ad explicitly promotes Mostek's 16-pin `MK4096` 4K RAM and compares its implementation/timing characteristics with 22-pin alternatives.

Source:

https://www.worldradiohistory.com/Archive-Electronic-Design/1974/Electronic-Design-V22-N24-1974-1122.pdf

### January 18, 1975 advertisement

A later Mostek ad again explicitly identifies the `MK4096`, including a comparative performance table. Extracted fields include approximately:

- 16-pin 4K RAM;
- 300 ns access time in the comparison;
- 425 ns read cycle;
- 425 ns write cycle;
- two TTL clock inputs in the comparison;
- direct compatibility claims with common logic families.

Source:

https://bitsavers.org/magazines/Electronic_Design/Electronic_Design_V23_N02_19750118.pdf

### Consequence

The MK4096 family is safely eligible for the strict `DESIGN_1976_03_10` world on availability grounds.

Exact Apple-1-installed speed-grade/package properties still require Apple-specific production evidence plus a qualifying period Mostek source where a simulator field depends on the precise suffix.

---

## Finding 4 — strict cutoff should distinguish availability from exact production variant

These findings expose an important schema requirement.

A component family may be demonstrably available before March 10, 1976 while the exact Apple-1 production suffix/date code/package may be documented only by surviving-board evidence.

The Multiverse corpus therefore needs separate concepts such as:

```text
family_available_by
family_source
variant_identity
variant_source
variant_observed_on_apple1
```

Do not collapse these into one `available=true` field.

---

## Updated acquisition priorities

### Now high confidence for strict-cutoff family availability

- MOS 6502;
- Motorola 6800 family;
- Signetics 2504 family;
- Signetics 2513 family;
- Signetics 2519 family;
- Mostek MK4096 family;
- many ordinary 74xx logic functions documented well before 1976.

### Still important to acquire precisely

1. exact period price evidence near March 1976;
2. exact 6820/compatible PIA pricing and availability near the design date;
3. manufacturer data for the precise MK4096 speed grades relevant to the Apple-1;
4. exact Apple-1 BOM/netlist extraction from the original drawings;
5. source-backed alternative memory-system costs including support logic;
6. comparable period video-design alternatives;
7. exact distributor or manufacturer quantity-price bases.

---

## Research-policy impact

The initial blind Multiverse can now be more ambitious than a CPU-only toy model.

A defensible first strict world can plausibly include real period families for:

- CPU;
- PIA/interface;
- dynamic RAM;
- character generation;
- video shift-register storage;
- TTL glue logic;
- keyboard encoding.

The remaining major weakness is **economic evidence**, not basic component existence.
