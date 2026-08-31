# 1975–1976 Contemporary System Comparators v1

**Status:** source-backed partial R5 market ledger  
**Purpose:** compare Apple-1 capability/economics with complete or near-complete microcomputer offerings visible to hobbyists around the strict March 1976 design world.

These are **system-level market comparators**, not substitute BOM prices.

A system's advertised price is not directly comparable to an Apple-1 bare-board retail price unless included features are explicitly normalized.

---

## SYS-001 — MITS Altair 8800

**Primary price-list date:** 1975-04-01  
**CPU:** Intel 8080  
**Computer kit:** $439  
**Assembled:** $621  
**4K dynamic memory board:** $264 kit / $338 assembled  
**RS-232 serial interface:** $119 kit / $138 assembled  

Primary price list:

https://www.bitsavers.org/pdf/mits/8800/Altair_PriceList_19750401.pdf

### Comparison caveat

The base Altair price is not equivalent to the Apple-1's integrated keyboard/display electronics. A functionally interactive configuration needs memory plus an I/O path and an external terminal/TTY.

A simple period price sum for kit Altair + 4K memory + RS-232 interface is $822 before an external terminal, software, shipping, or other accessories.

This arithmetic is a package comparison, not a claim about equivalent functionality.

---

## SYS-002 — JOLT 6502

**Period source:** January 1976 BYTE  
**CPU:** MOS Technology 6502  
**Basic JOLT CPU kit:** $249  
**JOLTS I/O kit:** $96  

Primary period advertisement:

https://www.worldradiohistory.com/Archive-Byte/70s/Byte-1976-01.pdf

The advertisement describes JOLT as a fully tested microcomputer with an onboard DEMON debug monitor and identifies the basic CPU card as using the MOS Technology 6502.

### Comparison caveat

JOLT's architecture, included RAM, I/O, and display requirements differ materially from the Apple-1. It is especially useful as a same-CPU contemporary comparator, not as a direct feature-for-feature price comparison.

---

## SYS-003 — SWTPC 6800

**Period source:** February 1976 BYTE  
**CPU:** Motorola 6800  
**Computer system kit:** $450  
**Included:** serial interface and 2,048 words of memory  
**4,096-word expansion:** $125  
**Serial or parallel interface card:** $35  

Primary period source:

https://www.worldradiohistory.com/Archive-Byte/70s/Byte-1976-02.pdf

The SWTPC advertisement emphasizes that its base system still expects an external TTY or video terminal for human interaction.

### Comparison caveat

Unlike the Apple-1, the SWTPC base computer did not itself provide the Apple-1-style integrated composite-video terminal electronics and ASCII-keyboard interface as part of the board. Terminal cost must be modeled separately when comparing an interactive package.

---

## SYS-004 — MITS Altair 680

**Period source:** February 1976 BYTE  
**CPU:** Motorola 6800  
**Advertised introductory kit price through 1975-12-31:** $293  
**Contemporary normal context:** the February article describes the model after that introductory window  
**Included on CPU board:** 1,024 words RAM, configurable terminal interface, provisions for 1,024 words ROM/PROM  

Primary period source:

https://www.worldradiohistory.com/Archive-Byte/70s/Byte-1976-02.pdf

### Comparison caveat

The $293 value is explicitly an introductory offer ending December 31, 1975. Preserve it as a dated market offer, not an assumed February/March 1976 purchase price.

---

## SYS-005 — Apple-1

**Retail baseline:** $666.66  
**Base RAM:** 4K  
**Integrated human interface electronics:** ASCII keyboard input plus composite video generation  
**Case, keyboard, power transformers, monitor:** not included as a finished consumer appliance  

Primary/reputable evidence:

- Apple-1 Operation Manual / advertising;
- Computer History Museum;
- surviving 1976 Apple invoices.

### Commercial distinction

The Apple-1 was sold as a fully assembled motherboard rather than a solder-it-yourself computer kit. The Byte Shop wholesale order required assembled computers.

---

# Normalization dimensions

MULTIVERSE should not rank these systems using sticker price alone. System comparisons need explicit dimensions such as:

- CPU architecture;
- RAM included;
- resident monitor/debug software;
- keyboard interface included;
- video generation included;
- serial interface included;
- external terminal required;
- enclosure included;
- power supply included;
- assembled versus kit;
- expansion capacity;
- software ecosystem;
- cutoff date.

A useful comparison object should therefore look conceptually like:

```text
SYSTEM PRICE: $X
INTERACTIVE PACKAGE PRICE: $Y OR UNKNOWN
INCLUDED RAM: N
DISPLAY ELECTRONICS: YES/NO
KEYBOARD INTERFACE: YES/NO
SERIAL: YES/NO
ASSEMBLY: KIT/ASSEMBLED
SOURCE DATE: YYYY-MM-DD
```

No missing feature price should be silently imputed.

# First useful research question

Rather than asking which computer was cheapest, ask:

> At March-1976 market prices, what was the lowest documented expenditure required to obtain a programmable microcomputer with at least 4K memory, human-readable output, practical keyboard input, and a resident or loadable low-level development interface?

The answer is not yet established by this ledger. The ledger exists so that question can eventually be answered without apples-to-oranges pricing.