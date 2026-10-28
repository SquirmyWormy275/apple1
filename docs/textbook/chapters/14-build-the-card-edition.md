# 14. Build and inspect the card edition

Use the [card guide](../../../cf-card/README.md) to compile the 40x24 books,
build a new candidate from the preserved baseline and inspect the result.

Run K01–K04 first. They connect display constraints, real CFFA1 firmware,
the RAM reader and saved BASIC state without requiring the large baseline
image or a physical card. Then reproduce the full build with a hydrated
baseline and compare its inventory and preservation checks.

Explain three design choices: one directory level, scroll-based pages with
no assumed cursor positioning, and firmware-generated BA1 files. Show a
failed load or invalid-size case as well as the working pager.

The [build storyboard kit](../../hardware/build-storyboard/README.md) supplies
the next chapter's shot plan, evidence fields and integration checklist.
Its asset slots remain empty until the actual build arrives.

[Textbook home](../README.md) · [Previous chapter](13-run-integer-basic.md) · [Physical follow-through](../reference/physical-session.md)
