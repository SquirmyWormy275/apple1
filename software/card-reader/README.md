# RAM card reader

[reader.asm](reader.asm) is an NMOS 6502 pager at `$0800`. It uses CFFA1's
`$900C` API to locate and read a selected book from the `EDUCATION` prefix.
The filename table starts at `$0C00`; book data occupy `$1000–$7FFF`.
The program uses zero page `$60–$69` and exits with `JMP $FF1F`.

The host compiler assembles the reader, checks its size, appends 16-byte
length-prefixed filenames, and emits `READER` with ProDOS BIN type `$06`
and auxiliary address `$0800`. Book files are BIN containers, not plain TXT.

| Key | Action |
|---|---|
| N | Next page; stays at the end |
| P | Previous page; stays at the beginning |
| A | Jump to the answer key, when present |
| M | Choose a book by its two-digit index, 00–49 |
| Q | Return to Monitor |

A wrong prefix produces a visible CFFA error. Invalid signatures, page counts,
oversized loads and out-of-file page offsets are rejected. The host compiler
also validates every page, file offset and character. This small pager is
intended for the reviewed edition, not arbitrary untrusted disk content.

The display routine polls `$D012` and writes characters directly. Full-width
lines rely on automatic wrap; the binary encoder omits a redundant CR after
column 40. Ordinary prose leaves a margin for a footer. The original atlas
plates use the full display and retain the same navigation keys without a
footer. The reader scrolls 24 blank lines between pages.

Starting this reader overwrites BASIC program RAM. Save any program before
switching between the book and BASIC. The current candidate has been rehearsed
against identified firmware and behavioral I/O models. Installed ROM identity,
keys, glyphs, bus timing and physical media still need acceptance.

```bash
python -m tools.card_image rehearse
python -m tools.textbook run K03
```

[Card build and intended load sequence](../../cf-card/README.md) · [Physical follow-through](../../docs/textbook/reference/physical-session.md)
