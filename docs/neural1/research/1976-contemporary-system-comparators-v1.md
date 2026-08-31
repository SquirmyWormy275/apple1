# 1975–1976 Contemporary System Comparators v1

**Status:** source-backed partial R5 market ledger  
**Purpose:** compare Apple-1 capability/economics with complete or near-complete microcomputer offerings visible to hobbyists around the strict March 1976 design world.

These are **system-level market comparators**, not substitute BOM prices.

A system's advertised price is not directly comparable to an Apple-1 bare-board retail price unless included features are explicitly normalized.

A second important rule emerged during source collection: **market prices can move materially month to month and can differ by sales channel.** Preserve the exact publication date, seller, and channel for every comparison.

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
**Direct manufacturer CPU kit:** $249  
**Direct manufacturer 4K RAM kit:** $265  
**Direct manufacturer I/O kit:** $96  
**Direct manufacturer power-supply kit:** $145  
**Assembled CPU:** $348  

Primary period advertisement:

https://vintageapple.org/byte/pdf/197601_Byte_Magazine_Vol_00-05_Build_a_Light_Pen.pdf

The direct JOLT advertisement describes the CPU card as using a MOS Technology 6502 and containing 512 bytes of user RAM, 64 bytes interrupt-vector RAM, 1K monitor/debug ROM, terminal I/O, interrupts, timer, and DEMON debug monitor. The same ad separately prices a 4K RAM card, I/O card, and power supply.

### Same-issue reseller evidence

A JAMES Electronics advertisement in the same January 1976 issue lists JOLT modules at materially different prices, including approximately:

- JOLT CPU kit — $159.95;
- JOLT RAM kit — $199.95;
- JOLT I/O kit — $95.50;
- JOLT power-supply kit — $99.95.

This is a valuable warning: **seller/channel is part of the historical price identity.** Do not average these figures or silently select the lower quote. The exact configuration, promotion, and fulfillment terms must remain attached to each source record.

### Comparison caveat

JOLT's architecture, included RAM, I/O, and display requirements differ materially from the Apple-1. It is especially useful as a same-CPU contemporary comparator, not as a direct feature-for-feature price comparison.

---

## SYS-003 — SWTPC 6800

**CPU:** Motorola 6800  
**Included:** serial interface and 2,048 words of memory  
**4,096-word expansion:** $125  
**Serial or parallel interface card:** $35  

### February 1976 snapshot

**Advertised kit price:** $450

Source:

https://vintageapple.org/byte/pdf/197602_Byte_Magazine_Vol_00-06_Color_Graphics.pdf

### March 1976 snapshot

**Advertised kit price:** $395

Source:

https://vintageapple.org/byte/pdf/197603_Byte_Magazine_Vol_00-07_Cassette_Interfaces.pdf

The March advertisement explicitly prices the computer system with serial interface and 2,048 words at $395, while retaining $125 per full 4K memory board and $35 serial/parallel interface pricing.

### Consequence

The nominal SWTPC base-system price fell $55, or about 12.2%, between adjacent BYTE issues. MULTIVERSE therefore must not treat `1976 price` as a timeless scalar.

### Comparison caveat

Unlike the Apple-1, the SWTPC base computer expected an external TTY or video terminal for human interaction. Terminal cost must be modeled separately when comparing an interactive package.

---

## SYS-004 — MITS Altair 680

**Period source:** February 1976 BYTE  
**CPU:** Motorola 6800  
**Advertised introductory kit price through 1975-12-31:** $293  
**Included on CPU board:** 1,024 words RAM, configurable terminal interface, provisions for 1,024 words ROM/PROM  

Primary period source:

https://vintageapple.org/byte/pdf/197602_Byte_Magazine_Vol_00-06_Color_Graphics.pdf

### Comparison caveat

The $293 value is explicitly an introductory offer ending December 31, 1975. Preserve it as a dated market offer, not an assumed February/March 1976 purchase price.

---

## SYS-005 — Apple-1

**Retail baseline:** $666.66  
**Base RAM:** 4K  
**Integrated human interface electronics:** ASCII keyboard input plus composite video generation  
**Case, keyboard, power transformers, monitor:** not included as a finished consumer appliance  
**Assembly state:** assembled/tested motherboard, not a solder-it-yourself computer kit  

Primary/reputable evidence:

- Apple-1 Operation Manual / 1976 Apple advertising;
- Computer History Museum;
- surviving 1976 Apple invoices.

### Commercial distinction

The Byte Shop wholesale order required assembled computers. Apple advertising later in 1976 explicitly described the board as including 4K RAM, complete video terminal electronics, keyboard interface, firmware monitor, and onboard regulated supplies.

---

## SYS-006 — Micro-Sphere 200

**Period source:** March 1976 BYTE  
**Processor:** described in advertisement as a 6800-type microcomputer  
**Price:** $860  
**Assembly:** completely assembled and tested  
**RAM:** 4K, expandable to 8K  
**Human interface:** full alphanumeric keyboard; standard TV display  
**Storage:** cassette loader / cassette interface  
**Software:** Sphere Cassette Operating System; games package  
**Display:** 16 lines x 21 characters alphanumeric and 128 x 128 B&W dot-matrix graphics  
**Case:** included  

Primary period source:

https://vintageapple.org/byte/pdf/197603_Byte_Magazine_Vol_00-07_Cassette_Interfaces.pdf

### Comparison significance

This is a much closer *complete interactive computer* comparator than a bare Altair chassis. It costs more than the Apple-1 motherboard but includes keyboard, case, cassette system, and graphics capability that Apple-1 customers had to source separately or did not receive.

It demonstrates why normalized capability vectors are necessary.

---

# Normalization dimensions

MULTIVERSE should not rank these systems using sticker price alone. System comparisons need explicit dimensions such as:

- CPU architecture;
- RAM included;
- resident monitor/debug software;
- keyboard interface included;
- physical keyboard included;
- video generation included;
- graphics capability;
- serial interface included;
- cassette interface included;
- external terminal required;
- enclosure included;
- power supply included;
- assembled versus kit;
- expansion capacity;
- software ecosystem;
- seller/channel;
- source date.

A useful comparison object should therefore look conceptually like:

```text
SYSTEM PRICE: $X
SELLER: ...
SOURCE DATE: YYYY-MM-DD
INTERACTIVE PACKAGE PRICE: $Y OR UNKNOWN
INCLUDED RAM: N
DISPLAY ELECTRONICS: YES/NO
PHYSICAL KEYBOARD: YES/NO
KEYBOARD INTERFACE: YES/NO
SERIAL: YES/NO
CASSETTE: YES/NO
ENCLOSURE: YES/NO
ASSEMBLY: KIT/ASSEMBLED
```

No missing feature price should be silently imputed.

# First useful research question

Rather than asking which computer was cheapest, ask:

> At the exact March-1976 market snapshot, what was the lowest documented expenditure required to obtain a programmable microcomputer with at least 4K memory, human-readable output, practical keyboard input, and a resident or loadable low-level development interface?

The answer is not yet established by this ledger. The ledger exists so that question can eventually be answered without apples-to-oranges pricing.

# Second useful research question

> Does the Apple-1 remain unusually cost-efficient after interactive capability, assembly state, external terminal requirements, and sales channel are normalized?

This must be tested, not assumed.