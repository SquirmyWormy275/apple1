# Recorded card-reader gallery

Download [index.html](index.html) and open it locally for an offline, keyboard-
accessible viewer of all 50 books. N/P change recorded pages, A jumps to
answers, and the book menu selects a lesson. The browser selects retained
observations; it does not run a new emulator or connect to the board.

[Raw reader screens](screens.json) contain all 1,468 observed pages. Their
SHA-256 is recorded in the [build receipt](../validation/card-build.json).
The individual PNGs show each book's first page; [the atlas map](BOARDATLAS-map.png)
shows a full-width plate. [The short tour](reader-tour.gif) uses those same
actual observations.

These are output from the real RAM pager and identified CFFA1 ROM running
against behavioral CPU/I/O models. They are not photographs of the finished
hardware. Exact source and case-sensitive host commands remain in the repository.

[Card guide](../../../cf-card/README.md) · [Textbook](../README.md)
