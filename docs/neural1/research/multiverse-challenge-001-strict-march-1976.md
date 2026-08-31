# 1976 MULTIVERSE Challenge 001
## Blind March-10-1976 Apple-1-Capability Design Search

**Challenge ID:** `N1-MV-C001`  
**Status:** pre-registration / infrastructure pending  
**World cutoff:** `1976-03-10`  
**Execution target:** virtual only  
**Physical Replica:** out of scope  

## Research question

> Given only source-qualified components and engineering information plausibly available by March 10, 1976, can small local language models design a computer satisfying a capability target derived from the Apple-1 without seeing Apple's actual circuit, component choices, Monitor source, advertising, or later historical analysis?

A secondary question, asked only after candidate lock:

> Where does the real Apple-1 sit relative to the blinded candidate designs under functionality, package count, sourced economic coverage, complexity, and robustness metrics?

This experiment must not be framed as `AI beats Woz`. It is a constrained design-space experiment with a historical holdout design.

---

# 1. Blinding boundary

During candidate generation, the experimental model must not receive:

- Apple-1 schematic or PCB images;
- Apple-1 BOM;
- Apple-1 Operation Manual;
- Woz Monitor source/listing;
- Apple-1 advertisements;
- Apple-1 Registry material;
- modern replica schematics/BOMs;
- articles explaining Wozniak's Apple-1 design choices;
- candidate-specific hints derived from the real Apple-1.

The model may know generic pre-cutoff computing concepts through its pretrained weights; this cannot be erased. Therefore the experiment must record the model and treat potential pretrained Apple-1 knowledge as a threat to validity.

A stronger later variant should test retrieval-isolated/local models and explicit anti-recall controls.

---

# 2. Allowed experimental corpus

The runtime supplies only a curated component/engineering corpus whose authoritative records satisfy the historical lifecycle policy for the declared world.

Allowed material may include:

- period manufacturer datasheets;
- period manufacturer catalogs;
- period distributor advertisements/catalogs;
- period trade-publication product reports;
- generic engineering references dated on/before the cutoff;
- source-qualified component prices under the selected economic regime.

Every corpus record needs provenance and a cutoff/lifecycle decision.

No unsupported model-memory component fact may become an authoritative design input.

---

# 3. Capability target

The challenge target is inspired by source-backed Apple-1 capabilities but is expressed without identifying the Apple implementation.

A candidate must provide:

## Compute

- general-purpose programmable 8-bit-class microprocessor or source-qualified equivalent architecture;
- practical execution performance for interactive programming;
- at least 4,096 bytes of user-program/data memory available under normal operation.

## Human input

- direct interface for a period-appropriate ASCII keyboard or equivalent explicitly approved character-input device;
- no dependence on an external intelligent terminal or timesharing computer for normal programming interaction.

## Human output

- composite video output usable with a period raster-scan monitor/television interface;
- at least 40 character positions per line and 24 displayed lines, or an explicitly declared equivalent/better text capability under the scoring policy;
- automatic or software-managed progression through a usable text display.

## Programming/bootstrap interface

The machine must offer a resident or loadable low-level environment capable of the functional equivalents of:

- entering bytes/program material;
- examining stored state/memory;
- executing a user program;
- returning to or recovering the development environment under a declared mechanism.

ROM/PROM size is scored but not fixed to 256 bytes in this challenge. `256-BYTE UNIVERSE` handles the stricter firmware-budget experiment separately.

## Standalone boundary

External items may include:

- keyboard;
- video monitor/television;
- passive power transformers/supply hardware;
- cassette/storage peripheral only if the candidate explicitly includes it.

An external teletype, terminal computer, minicomputer, or modern host cannot provide the normal display/keyboard intelligence required by the target.

---

# 4. Historical procurement policies

Run at least two economic worlds when adequate source coverage exists.

## World A — `GENERAL_RETAIL_1976_03_10`

Use only components eligible under the lifecycle policy for ordinary small-quantity/general-market procurement and only R1-compatible price observations.

Unknown price stays unknown.

## World B — `SMALL_MANUFACTURER_1976_03_10`

Permit qualifying low-volume manufacturer/distributor tiers under R2 rules.

Do not mix R1 and R2 into one cost without a declared transformation.

## Apple-specific prototype components

`E3_APPLE_SPECIFIC` components such as a historically used but potentially withdrawn 6501 are **not** automatically available in the blind general-market worlds.

A separate `APPLE_PROTOTYPE_RECONSTRUCTION` world may use them.

---

# 5. Candidate representation

A model does not get to declare `my computer works`.

Each candidate must produce a structured design containing at least:

- component instances;
- part/family IDs resolving to the historical component registry;
- functional role;
- interconnection/net declarations;
- memory map;
- clock/timing description;
- keyboard path;
- display path;
- memory capacity calculation;
- firmware/bootstrap artifact or formal firmware requirement;
- power requirements;
- external dependencies;
- unresolved assumptions.

The runtime should reject malformed or historically ineligible components before scoring.

---

# 6. Validation levels

Candidate maturity must be explicit.

## `V0_PROPOSED`

Structured model output only.

## `V1_SCHEMA_VALID`

Design parses and all referenced component IDs exist.

## `V2_HISTORICALLY_ELIGIBLE`

Every required component passes the selected cutoff/procurement policy or is explicitly unresolved.

## `V3_STRUCTURALLY_VALIDATED`

Memory capacity, address conflicts, required interfaces, component connectivity constraints, and declared subsystem requirements pass deterministic checks available in the runtime.

## `V4_BEHAVIORALLY_SIMULATED`

A deterministic behavioral model demonstrates the required machine-level capability contract.

## `V5_ELECTRICALLY_VALIDATED`

Only use if timing/electrical validation is actually implemented to a defensible standard. Do not award this label from LLM reasoning.

No physical Apple-1 test is part of Challenge 001.

---

# 7. Primary metrics

Predeclare metrics before campaign execution.

## Functionality

- capability tests passed;
- bootstrap/development-interface tests passed;
- unsupported assumptions count.

## Complexity

- IC/package count;
- unique part-family count;
- estimated net/interconnect count where deterministically derived;
- firmware bytes;
- required regulated voltage rails;
- external required devices.

## Memory

- total RAM;
- user-available RAM;
- display-dedicated memory;
- ROM/PROM bytes.

## Historical robustness

- fraction of parts `E1_GENERAL_MARKET`;
- fraction `E2_PRODUCTION_QUANTITY`;
- unresolved lifecycle dependencies;
- number of single-source/single-vendor dependencies;
- substitution options supported by sourced equivalents.

## Economics

For every economic regime report:

- sourced cost subtotal;
- number of priced line items;
- fraction of required package cost positions covered;
- unpriced critical parts;
- complete cost only if the preregistered coverage rule is satisfied.

### Initial cost-publication rule

Until refined in a pilot, **do not rank candidates by 'total cost' unless at least 90% of required package positions have compatible price evidence in the same economic regime and no major high-cost category is wholly missing.**

Below that threshold report `SOURCED COST LOWER BOUND / COVERAGE`, not total cost.

---

# 8. Secondary metrics

Where source/model support exists:

- estimated power demand;
- timing margin;
- board implementation complexity proxy;
- ease of expansion;
- amount of custom/special-purpose logic;
- design sensitivity to component removal or price shock.

Do not fabricate unavailable engineering quantities.

---

# 9. Model campaign design

Initial model families should be those actually qualified by the NEURAL1 model runtime at campaign time.

For each family use matched:

- component corpus;
- world cutoff;
- prompt contract;
- token budget;
- number of design iterations;
- deterministic seed set where backend permits;
- critique/repair budget;
- validation feedback policy.

Record every attempted design, including invalid/extinct candidates.

---

# 10. Search conditions

Run multiple objective conditions rather than one vague `best computer` request.

At minimum:

### C1 — Minimize package count

Subject to capability validity.

### C2 — Minimize sourced cost

Only under an economic world with sufficient coverage.

### C3 — Maximize historical supply robustness

Prefer multiple sourced substitution paths and ordinary procurement.

### C4 — Balanced Pareto search

Seek non-dominated designs across functionality, package count, sourced cost/coverage, and supply robustness.

The objective presented to the model must match the metric used for selection.

---

# 11. Holdout reveal

The real Apple-1 design is introduced only after candidate generation/selection is locked and hashed.

The holdout comparison should use:

- `APPLE1-CAPABILITY-1976-V1`;
- `apple1-primary-package-inventory-v1.md`;
- declared `DRAWING_00101_REV_A` or `PRODUCTION_AS_BUILT_V1` topology;
- the same economic regime and price-coverage rules applied to candidates.

Do not give Apple a privileged hidden cost estimate unavailable to candidates.

---

# 12. Holdout comparison questions

The first analysis should answer:

1. Does any blinded candidate satisfy the target at lower package count?
2. Which candidates use materially different video-memory strategies?
3. Which CPU families dominate each objective condition?
4. Does any design repeatedly converge on shift-register display memory?
5. Does any design independently use a 6502-family CPU?
6. Where does Apple sit on the candidate Pareto frontier?
7. Which Apple choices appear difficult for models to improve simultaneously?
8. Which candidate advantages disappear after correcting price coverage or external-device assumptions?
9. Are candidate designs robust to month/channel changes in the historical price dataset?
10. Do model families converge on similar architectures independently?

---

# 13. Falsification / adversarial checks

META/1 should actively test apparently interesting findings.

Examples:

- If `models rediscover shift-register video`, rerun after removing one specific shift-register family while retaining period alternatives.
- If `6502 dominates`, rerun under CPU price perturbation and source-valid alternative CPUs.
- If `Apple is near Pareto-optimal`, test whether missing/unpriced Apple parts bias the frontier.
- If one model family dominates, match effective inference budget and perform cross-seed replication.
- If a candidate seems cheaper, normalize required external terminal/keyboard/video hardware before making the claim.

---

# 14. Threats to validity

Explicitly track:

- pretrained model may already know Apple-1 architecture;
- historical component corpus may be incomplete;
- price evidence is highly channel/date/quantity dependent;
- structural validation is weaker than real electrical validation;
- Apple design documentation contains known drawing-vs-as-built discrepancies;
- surviving-board evidence includes repairs/replacements;
- capability target itself is derived from the Apple-1 and may bias the design space;
- economic coverage may favor designs using easier-to-price commodity parts;
- model output quality may depend strongly on representation/schema design.

---

# 15. Pilot success criterion

Challenge 001 infrastructure is successful if it can produce, from at least two model families:

- multiple schema-valid candidate architectures;
- deterministic eligibility decisions;
- retained invalid candidates and reasons;
- reproducible scoring;
- cost coverage rather than fake totals;
- blinded candidate lock before Apple reveal;
- a holdout comparison report;
- at least one META-generated candidate hypothesis with a separately designed follow-up test.

A spectacular design is **not** required for infrastructure success.

---

# 16. Publication discipline

Permitted pilot wording:

> `In a blinded, source-constrained March-1976 design pilot, model family X produced candidate architecture Y under objective Z.`

Not permitted without stronger evidence:

> `AI designed a better Apple-1.`

Any eventual optimization claim must identify:

- exact metric;
- historical cutoff;
- procurement regime;
- validation level;
- price coverage;
- model/version;
- run IDs;
- proof capsule.

---

# 17. Required source bundles before execution

- component lifecycle ledger;
- component property records;
- price snapshot(s);
- generic period engineering references;
- explicit forbidden Apple-source list;
- Apple holdout package sealed/hash-recorded before candidate runs;
- challenge spec hash.

The holdout package must not enter the model context before candidate lock.