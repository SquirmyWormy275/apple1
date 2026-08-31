# 1976 MULTIVERSE Component Lifecycle Policy

**Status:** methodology / authoritative eligibility rule  
**Purpose:** prevent anachronistic use of components that merely existed before a cutoff but were not plausibly procurable or appropriate at that cutoff.

## Core principle

`FIRST_KNOWN_DATE <= EXPERIMENT_CUTOFF` is necessary but **not sufficient** for historical component eligibility.

A component record must distinguish invention/documentation from actual market lifecycle.

This matters immediately for the MOS 6501: it was advertised and sold in 1975, Apple used it in a prototype path, but MOS withdrew it from the market following Motorola litigation. A model running in a March-1976 procurement world must not automatically treat the 6501 as an ordinary fresh-purchase option just because a 1975 advertisement exists.

---

# Lifecycle states

A component/source record should support dated events such as:

- `ANNOUNCED`
- `DOCUMENTED`
- `SAMPLED`
- `ORDERABLE`
- `STOCK_ADVERTISED`
- `SHIPPING`
- `PRICE_OBSERVED`
- `WITHDRAWAL_ANNOUNCED`
- `WITHDRAWN`
- `DISCONTINUED`
- `REPLACED_BY`
- `APPLE_SPECIFIC_ON_HAND`
- `APPLE_SPECIFIC_USED`
- `UNKNOWN`

Events are observations, not one timeless status field.

---

# Procurement eligibility classes

For a given experiment cutoff, derive one of:

## `E1_GENERAL_MARKET`

Strong evidence that a technically competent US buyer could obtain/order the part at the cutoff.

Examples of qualifying evidence:

- contemporary distributor advertisement;
- manufacturer price list/order information;
- contemporary product report saying stock/shipping;
- dated distributor catalog.

## `E2_PRODUCTION_QUANTITY`

Orderable, but the qualifying evidence is a manufacturer/volume tier rather than hobbyist-unit retail.

The part may be technically eligible but cannot be given an R1 hobbyist price without separate evidence.

## `E3_APPLE_SPECIFIC`

Evidence that Apple/Woz/Jobs possessed or used the component even when general market procurement at that date is uncertain.

This is appropriate for reconstructing a documented Apple prototype, not automatically for a blind general-market design contest.

## `E4_LEGACY_STOCK_POSSIBLE`

A withdrawn/discontinued component could physically remain in inventory, surplus, or private possession, but no strong evidence establishes general current ordering.

Use only in experiments that explicitly allow surplus/legacy stock.

## `E5_NOT_ELIGIBLE`

Evidence indicates the component did not yet exist, was not yet available, or had already been withdrawn under a world that permits only current ordinary procurement.

## `E0_UNKNOWN`

Evidence is inadequate.

Unknown is not equivalent to eligible.

---

# Example — MOS 6501

## 1975 market evidence

MOS Technology advertised the pin-compatible MCS6501 for $20 in August/September 1975. The contemporary November 1975 BYTE article describes it at $20 in single quantities.

Sources:

- MOS Technology August 1975 advertisement, preserved at Wikimedia Commons: https://commons.wikimedia.org/wiki/File:MOS_6501_Ad_August_1975.jpg
- November 1975 BYTE, `Son of Motorola (or, the $20 CPU Chip)`: https://www.worldradiohistory.com/Archive-Byte/70s/Byte-1975-11.pdf

## Withdrawal

Historical records document Motorola's litigation against MOS Technology and MOS's withdrawal of the 6501.

## Apple-specific evidence

The Apple-1 Registry preserves Wozniak's later explanation that the 6501 motivated the retained 6800-compatible clock-driver area and that a few early boards used the 6501. The production prototype `Apple Computer A` is identified with an MCS6501.

### March-10-1976 classification

For a strict **general-market ordinary-procurement** world:

`MOS_6501 = E0_UNKNOWN or E5_NOT_ELIGIBLE pending a dated withdrawal/availability boundary strong enough for exact classification.`

For an **Apple prototype reconstruction** world:

`MOS_6501 = E3_APPLE_SPECIFIC`.

Do not conflate these worlds.

---

# Example — Signetics 2504 / 2513 / 2519

Documentation from the 1971 Signetics MOS data book establishes the families years before the Apple-1. January 1976 retail advertisements establish current market sale close to the March cutoff.

Thus the specific qualifying variants can reach `E1_GENERAL_MARKET` when properties/variant identity are adequately reconciled.

---

# Example — Mostek MK4096

1974/1975 Mostek advertisements establish commercial availability. Q1-1975 vendor-book pricing establishes quantity-tier procurement.

Until a hobbyist/single-unit retail record is found, the part can be:

- `E2_PRODUCTION_QUANTITY` with the documented vendor tiers;
- potentially `E1_GENERAL_MARKET` on availability if a qualifying ordinary-order source is acquired;
- but R1 hobbyist price remains unavailable.

---

# Experiment rules

Every historical experiment must declare a procurement policy.

Examples:

## `PROCUREMENT_GENERAL_RETAIL`

Permit only `E1_GENERAL_MARKET` components with a compatible retail/small-quantity evidence profile.

## `PROCUREMENT_SMALL_MANUFACTURER`

Permit `E1_GENERAL_MARKET` and qualifying `E2_PRODUCTION_QUANTITY` parts using declared low-volume tiers.

## `PROCUREMENT_APPLE_REALIZATION`

Permit documented `E3_APPLE_SPECIFIC` parts when reconstructing an actual Apple prototype/production state.

## `PROCUREMENT_SURPLUS_ALLOWED`

May permit `E4_LEGACY_STOCK_POSSIBLE`, but the experiment must explicitly model uncertain supply rather than treating stock as unlimited.

---

# Required source fields

A component lifecycle record should eventually include:

```json
{
  "part_id": "...",
  "event": "ORDERABLE",
  "date": "YYYY-MM-DD",
  "date_precision": "day|month|quarter|year",
  "market": "US",
  "channel": "manufacturer|distributor|retail|apple_specific",
  "quantity_tier": "...",
  "source_id": "...",
  "confidence": "...",
  "notes": "..."
}
```

Eligibility at an experiment cutoff should be derived from event history, not manually asserted without evidence.

---

# META/1 integration

META should be able to answer:

- `WHY WAS PART X ELIGIBLE?`
- `WHAT SOURCE MAKES X ORDERABLE?`
- `WHAT CHANGED BETWEEN JAN AND MAR 1976?`
- `SHOW WITHDRAWN COMPONENTS`
- `RERUN WITHOUT LEGACY STOCK`

A design result depending on an `E0_UNKNOWN` component should be classified as historically unresolved rather than silently accepted.