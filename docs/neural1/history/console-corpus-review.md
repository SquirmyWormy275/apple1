# Console corpus review — 2026-09-10

The bounded console preset uses **YEAR_END_1976_12_31**, not the stricter March
research world. It exercises CPU/RAM selection, memory placement and structural
validation. It does not simulate a complete computer or prove electrical,
procurement, cost or performance feasibility.

The existing project scan `preservation/manuals/2026-08-28/files/Apple1 Manual.pdf`
was rehashed: `8f5e595ea6c0c91fdd4206a4b2c2333be8990178db2600392af185ec63f9a1c2`.
Its specification leaf (PDF page 2 of 15) was rendered and visually reviewed.
The [Computer History Museum catalogued scan](https://archive.computerhistory.org/resources/text/Apple/Apple.AppleI.1976.102646518.pdf)
independently identifies the manual as 1976; that different scan does **not** have
the project artifact's byte identity. December 31 is a conservative eligibility
bound for a year-only date, not an asserted publication day.

The reviewed leaf supports MOS Technology 6502 identification and a demonstrated
4K-byte supplied bank using 16-pin type 4096 (2104) dynamic RAM. The bank record
is an assembly abstraction, not a claim that one device stores 4096 bytes.
Manufacturer, exact suffix, price and maximum component clock remain unknown.
Dynamic RAM requires refresh; the candidate must explicitly acknowledge that
engineering obligation, whose implementation is outside this starting task.

`console-corpus.json` contains the two reviewed records and source identity.
Existing research staging and its zero promoted records remain historical,
separate records. Model prompts expose abstract component capabilities, never
the reference machine genome. No new copyrighted scan was added to Git.

The evaluator parses strict bounded JSON, rejects unknown/duplicate components,
missing provenance, invalid structure and wrong RAM spans, and records source
hashes with each result. Its declared task requires one CPU, one 4096-byte bank,
a CPU-to-bank connection and a contiguous 4096-byte range. Accepted structural
proposals remain hypotheses about a partial machine. Failures remain recorded
negative results. Known-good and rejected controls are software tests, not live
model evidence.
