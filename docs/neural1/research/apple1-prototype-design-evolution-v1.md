# Apple-1 Prototype / Design Evolution v1

**Status:** historical design-evolution scaffold  
**Purpose:** represent the Apple-1's documented prototype/CPU-selection path as a real MULTIVERSE branch rather than an invented counterfactual.

## Why this matters

The production Apple-1 schematic contains a dotted optional clock-driver area usually described as the `6800` section. Historical specialist evidence and a later direct statement from Steve Wozniak indicate that this area also reflects the MOS 6501 option he considered because the 6501 was initially cheaper than the 6502.

The surviving/photographically documented production prototype known as **Apple Computer A** has this extra area populated and is identified by the Apple-1 Registry as using a MOS 6501.

This means a `6501 Apple-1` is not merely a modern thought experiment. It belongs to the documented design/prototype history.

---

# PEV-001 — supplied production drawing supports alternate 6800-class clock circuitry

Apple Drawing `00101 Rev A`, processor-section note 7, states that the supplied unit uses a 6502, has solder jumpers at the points marked for the 6502, and omits the components in the dotted box. If a 6800 is substituted, those components are installed and the relevant bridges are broken.

### Interpretation

The production drawing therefore intentionally retains an alternate processor/clock implementation even though the normal shipped configuration is the 6502.

This is a primary design-source fact.

---

# PEV-002 — production prototype `Apple Computer A`

Apple-1 Registry entry #2 documents a pre-production mainboard significantly different from later production boards:

- hand-soldered / pre-production status;
- board marked `Apple Computer A © 76` rather than the later production legend;
- different trace layout;
- the 6800/6501 auxiliary clock-driver area populated;
- 4K ceramic Mostek DRAM;
- MOS MCS6501 CPU identified in the surviving partial board/provenance record.

Source:

https://www.apple1registry.com/en/2.html

The Registry notes that only the left portion of the surviving board remains today and that some historical details cannot be fully resolved.

---

# PEV-003 — Wozniak's reported 6501 / 6502 cost reasoning

The Apple-1 Registry preserves a 2012 response attributed directly to Steve Wozniak after he was shown a photograph of the prototype. In substance, Wozniak explained that:

- he retained the 6800-style area because the pin-compatible 6501 needed the stronger clock-driver circuitry;
- the 6501 was about $20 while the 6502 was about $25 at that point;
- a few early boards were built with the 6501;
- by production time Apple could obtain the 6502 for the same cost.

Source:

https://www.apple1registry.com/en/prototypes.html

### Evidence classification

`DIRECT_LATER_RECOLLECTION_PRESERVED_BY_SPECIALIST_REGISTRY`

This is valuable evidence, but it is not the same evidentiary class as a surviving 1976 purchase invoice.

### Economic consequence

Do not encode `$20 6501` or `same cost by production` as a universal market price. Encode them as Wozniak's reported Apple/design-choice context.

---

# PEV-004 — Woz Monitor compatibility

The Registry reports that the Woz Monitor PROMs work with the 6501 prototype configuration without modification.

### Research consequence

A controlled MULTIVERSE branch can hold firmware constant while changing:

- 6501 vs 6502;
- clock-driver component set;
- cost/supply assumptions;
- board complexity.

This creates an unusually clean historical counterfactual because the alternate CPU path was actually represented in the original hardware design trajectory.

---

# Proposed historical worlds

## `APPLE1_PROTOTYPE_6501`

- CPU: MOS 6501;
- 6800/6501 clock-driver option populated;
- 4K base RAM unless experiment declares another observed prototype configuration;
- Woz Monitor behavior target held constant where source-supported;
- prototype trace/layout differences represented only where evidence exists.

## `APPLE1_PRODUCTION_6502`

- CPU: MOS 6502-class;
- dotted 6800/6501 option omitted per drawing note 7;
- production-board topology selector;
- 4K supplied / 8K full profiles.

## `BLIND_1976_CPU_SELECTION`

An experimental agent receives only the source-qualified pre-cutoff CPU/component market universe and Apple-1 capability target. It does not see Apple's final processor choice.

Possible candidates may include 6501, 6502, 6800, and other genuinely cutoff-eligible processors if all required support components and prices are sourced.

---

# Flagship experiments enabled

## 1. Would the 6501 still win under its apparent $5 CPU advantage?

Measure complete implementation cost rather than CPU sticker price alone.

The 6501/6800-compatible option requires extra high-voltage/strong clock-driver circuitry absent from the supplied 6502 configuration. A cheaper CPU may therefore fail to produce a cheaper complete machine.

Required evidence before result publication:

- period-valid 6501 market/Apple price evidence;
- source-backed additional option-component list;
- source-backed option-component prices or explicit incomplete-cost coverage;
- equivalent functional test target.

## 2. Did the 6502 reduce complexity enough to dominate the Pareto frontier?

Compare:

- sourced component cost;
- package count;
- power requirements where source data permits;
- board complexity proxy;
- firmware compatibility;
- timing margin.

Do not assume the answer.

## 3. Can small LLMs independently rediscover the 6502 choice?

Blind models to the Apple-1 final design and give them the historically constrained processor/component universe.

Measure which processor families they choose under different objective functions:

- minimum complete implementation cost;
- minimum chip count;
- maximum software simplicity;
- minimum development risk;
- robustness to supply-price changes.

## 4. Path dependence

Start identical agent populations before the CPU decision, then fork the world:

```text
                PRE-PRODUCTION WORLD
                       |
             +---------+---------+
             |                   |
          6501 PATH           6502 PATH
             |                   |
       EXTRA CLOCK HW        OMITTED OPTION
             |                   |
       SOFTWARE CULTURE      SOFTWARE CULTURE
```

Feed each resulting machine into later 256-BYTE / SELFHOST / 4K MIND studies where technically meaningful.

Question:

> Can an apparently small hardware procurement decision measurably alter downstream firmware/software evolution under constrained agents?

---

# Important limits

- The Registry states that not all prototype details can be reconstructed.
- The surviving production prototype is incomplete/damaged today.
- Wozniak's later recollection is valuable but not contemporaneous accounting paperwork.
- `6501 Apple-1` should refer only to a clearly defined prototype/experimental world, not to the normal retail Apple-1.
- Do not turn the `$20` and `$25` recollection into generic 1976 market prices without separate period sources.

# Sources

- Apple Computer Company Drawing No. `00101`, Rev A, Processor Section note 7.
- Apple-1 Registry, production prototype #2: https://www.apple1registry.com/en/2.html
- Apple-1 Registry prototype history: https://www.apple1registry.com/en/prototypes.html
- Apple-1 Registry press/research material on `Apple Computer A`.

Use source-specific rights/attribution before redistributing Registry imagery; the Registry's site terms explicitly restrict reproduction except where separate CC BY-SA press materials are provided.