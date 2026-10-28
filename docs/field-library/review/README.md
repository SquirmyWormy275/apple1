# Pre-hardware packet review

This review applies the structural part of the curriculum gate to **all 42
original packets**, with targeted editorial corrections and a local-scan
quotation-location check. It supports the **host reading candidate**. It does
not certify every historical statement, third-party rights, physical acceptance
or a learner's understanding.

[Packet-by-packet record](packets.json) · [Source-location ledger](source-ledger.json) ·
[Current verification register](../README.md#open-verification-items) ·
[Card edition](../../../cf-card/README.md)

## What was checked

| Gate | Evidence and result |
|---|---|
| Objective and first visible result | Every packet has the required learner sections and a first-result path of one to three listed actions; SP01 uses its explicit First result list |
| Activity and answers | Every labeled activity part maps to an answer, worked example, explicit criteria, or a documented self-check/drill |
| Source links | All shared source keys referenced in packet notes resolve; original packet/source/asset inputs are hashed |
| Evidence mode | The original worksheets remain OFF-DEVICE; each has a separately labeled executable host companion |
| Programs and boundaries | Existing companions exercise the teaching results; U01–U06 and K01–K04 add real interpreter/firmware execution and negative cases |
| Card representation | Complete packet readings, activities, text assets and answers compile within declared page/file/RAM bounds; all atlas plates retain their layout using display-safe borders |
| Claim limits | Source-location checks, historical interpretation, rights and installed-hardware observations remain separate |

`tools.field_library_review.review_packets()` reproduces the structural record.
Tests compare it against `packets.json`, so editing an input requires another
review. Source-key resolution is a coverage check; it is not an automated proof
that every claim is true.

## Corrections made in this pass

- **B02:** Bound the integer converter to 0–129 before multiplication. Record
  actual overflow at 130, integer truncation, immediate INPUT rejection, the
  successful greeting and the double-question-mark prompt.
- **B04:** Reverse sorting makes 10 swaps over 20 comparisons; it does not swap
  on every comparison. The real BASIC sort reproduces the paper trace.
- **C04:** A single AND converts an already-known lowercase letter. General
  input needs range checks; blindly clearing bit 5 also changes digits.
- **H01:** Attribute Owad's undefined “first of its kind” comparison instead of
  presenting it as a settled historical-priority result.
- **Shared source pool:** Correct the Monitor-ROM quotation spanning pp. 216–217,
  BASIC entry at Briel p. 22, and quotations that had silently included paraphrase
  or omitted intervening text. Keep the reset/stack/range errata visible.
- **Primary BASIC source:** Visually inspect the original Apple BASIC manual's
  printed p. 1 / PDF p. 3 for cassette loading and cold/warm entry.
- **Flash-card presentation:** Spell out lowercase character examples, retain
  diagrams with safe vertical borders, and handle exact 40-column wrap.

Earlier corrections and preserved failures remain in the
[textbook technical review](../../textbook/review.md).

## Source-location method and limits

The ledger matches **73 quoted fragments** to cited pages in the identified
local Owad/Briel scans. Comparison removes whitespace and punctuation to handle
PDF line breaks and typographic quotes. It records the fragments and matching
pages so this is inspectable. It does not claim a byte-exact text extraction
or independent corroboration of the historical assertion.

Tables are recorded as tables rather than fabricated continuous quotations.
Selected critical pages were visually reviewed in the earlier textbook pass;
the new original BASIC-loading page was also visually checked. The retained
manual SHA-256 records identify the scans. A correct page reference does not
correct an error printed on that page.

V-36 now has an applied gate and a per-packet disposition; V-1's quoted-text
location issue has an explicit ledger. Made/sold counts, replica distinctions,
unknown author intent, rights and the display-history dossier retain their
qualified treatment. A candidate can teach those uncertainties directly rather
than quietly replacing them with confident guesses.

## Reproduce the structural record

```python
import json
from tools.field_library_review import review_packets

result = review_packets()
assert len(result["records"]) == 42
print(json.dumps(result, indent=2))
```

After an editorial change, inspect the new record before replacing the retained
JSON, regenerate the card edition and textbook captures, and run the tests.
Physical acceptance and credited build photographs belong in their own records.
