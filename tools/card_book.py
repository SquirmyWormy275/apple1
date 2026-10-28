"""Compile the uppercase 40x24 card reading edition and its RAM pager.

This command writes ordinary files to a NEW host directory. It does not open a
device. The separate card_image build uses CFFA1 firmware against a virtual ATA
image. Markdown and exact case-sensitive source remain authoritative on host.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import textwrap
import unicodedata
from pathlib import Path

from neural1.assembler import LessonAssembler

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "docs/textbook"
MAGIC = b"A1BK\x01"


def ascii_reading(text: str) -> str:
    replacements = {"\u2013": "-", "\u2014": " - ", "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                    "\u2192": " TO ", "\u2264": "<=", "\u2265": ">=", "\u00d7": "*", "\u00f7": "/", "\u2260": "<>", "\u2026": "..."}
    for original, replacement in replacements.items():
        text = text.replace(original, replacement)
    text = "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))
    text = text.encode("ascii", "replace").decode("ascii").upper()
    # 64-character display alphabet: SPACE through UNDERSCORE, plus CR/LF.
    for char, replacement in {"`": "", "|": " / ", "{": "(", "}": ")", "~": " APPROX "}.items():
        text = text.replace(char, replacement)
    if any(c not in "\r\n\t" and not 0x20 <= ord(c) <= 0x5F for c in text):
        raise ValueError("unmapped character in reading edition")
    return text


def reading_lines(markdown: str, *, preserve_layout: bool = False) -> list[str]:
    markdown = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"[FIGURE: \1; SEE HOST SOURCE]", markdown)
    markdown = re.sub(r"\[([^]]*)\]\([^)]*\)", r"\1", markdown)
    # A display that cannot show lowercase must not turn the statement
    # `a` = $61 into the false statement A = $61.
    markdown = re.sub(r"`([a-z])`", lambda m: "LOWERCASE " + m[1].upper(), markdown)
    lines: list[str] = []
    paragraph: list[str] = []
    code = preserve_layout

    def append(text: str, *, layout: bool = False) -> None:
        # Preserve diagrams and code coordinates, including their left margin.
        if layout:
            text = text.replace("|", "!")
        text = ascii_reading(text.replace("**", "").replace("`", ""))
        if re.fullmatch(r"[ /:\-]+", text):
            return
        if layout and len(text) <= 40:
            lines.append(text.rstrip())
        else:
            lines.extend(textwrap.wrap(text, width=38, break_long_words=True, break_on_hyphens=False) or [""])

    def flush() -> None:
        if paragraph:
            append(" ".join(paragraph))
            paragraph.clear()

    for raw in markdown.splitlines():
        if raw.startswith("```") and not preserve_layout:
            flush()
            code = not code
            continue
        if code:
            append(raw, layout=True)
        elif not raw.strip():
            flush()
            if lines and lines[-1]:
                lines.append("")
        elif raw.startswith("#"):
            flush()
            append(re.sub(r"^#+\s*", "", raw).strip())
        elif raw.startswith("|"):
            flush()
            append(raw.strip())
        elif re.match(r"^\s*(?:[-*]|\d+\.)\s", raw):
            flush()
            paragraph.append(raw.strip())
        else:
            paragraph.append(re.sub(r"^>\s*", "", raw).strip())
    flush()
    while lines and not lines[-1]:
        lines.pop()
    return lines


def encode_book(pages: list[str], answer: int | None = None) -> bytes:
    if not 1 <= len(pages) <= 127:
        raise ValueError("book requires 1-127 pages")
    if answer is not None and not 0 <= answer < len(pages):
        raise ValueError("answer page outside book")
    offset = 9 + 2 * len(pages)
    offsets = bytearray()
    bodies = bytearray()
    for page in pages:
        lines = page.splitlines()
        if len(lines) > 24 or any(len(line) > 40 for line in lines) or len(lines) == 24 and len(lines[-1]) == 40:
            raise ValueError("card page exceeds reader display budget")
        if any(c != "\n" and not 0x20 <= ord(c) <= 0x5F for c in page):
            raise ValueError("card page outside uppercase display alphabet")
        data = page_bytes(page) + b"\0"
        offsets.extend(offset.to_bytes(2, "little"))
        bodies.extend(data)
        offset += len(data)
    result = MAGIC + len(pages).to_bytes(2, "little") + (0xFFFF if answer is None else answer).to_bytes(2, "little") + offsets + bodies
    if len(result) > 0x7000:
        raise ValueError(f"book exceeds $1000-$7FFF RAM buffer: {len(result)}")
    return result


def page_bytes(page: str) -> bytes:
    """Avoid a second newline after column 40's automatic display wrap."""
    lines = page.rstrip("\n").split("\n")
    return b"".join(line.encode("ascii") + (b"\r" if i < len(lines) - 1 and len(line) < 40 else b"")
                    for i, line in enumerate(lines))


def decode_book(data: bytes) -> tuple[list[str], int | None]:
    if data[:5] != MAGIC or len(data) < 11 or len(data) > 0x7000:
        raise ValueError("invalid card-book signature or size")
    count = int.from_bytes(data[5:7], "little")
    answer = int.from_bytes(data[7:9], "little")
    if not 1 <= count <= 127 or answer != 0xFFFF and answer >= count or 9 + 2 * count >= len(data):
        raise ValueError("invalid card-book header")
    pages = []
    expected = 9 + count * 2
    for i in range(count):
        offset = int.from_bytes(data[9 + 2 * i:11 + 2 * i], "little")
        if offset != expected:
            raise ValueError("noncontiguous page offsets")
        end = data.find(b"\0", offset)
        if end == -1:
            raise ValueError("unterminated page")
        lines = []
        line = ""
        for char in data[offset:end].decode("ascii"):
            if char == "\r":
                lines.append(line)
                line = ""
            else:
                line += char
                if len(line) == 40:
                    lines.append(line)
                    line = ""
        if line or not lines:
            lines.append(line)
        page = "\n".join(lines)
        pages.append(page)
        expected = end + 1
    if expected != len(data) or encode_book(pages, None if answer == 0xFFFF else answer) != data:
        raise ValueError("invalid page contents or trailing data")
    return pages, None if answer == 0xFFFF else answer


def paginate(identifier: str, title: str, parts: list[tuple[str, str]]) -> tuple[list[str], int | None]:
    pages = []
    answer = None
    for section, text in parts:
        body = reading_lines(text, preserve_layout=section.startswith("WORKSHEET "))
        if section == "ANSWERS":
            answer = len(pages)
        for start in range(0, max(1, len(body)), 18):
            header = ascii_reading(f"{identifier} {title}")[:38]
            pages.append("\n".join([header, ascii_reading(section)[:38], "", *body[start:start + 18],
                                    "N NEXT P BACK A ANSWER M BOOK Q EXIT"]))
    # Replace the section line with its page number; retain section context.
    result = []
    for i, page in enumerate(pages, 1):
        rows = page.splitlines()
        rows[1] = f"{i:03}/{len(pages):03} {rows[1]}"[:38]
        result.append("\n".join(rows))
    encode_book(result, answer)
    return result, answer


def compile_books() -> tuple[dict[str, bytes], dict[str, list[str]], dict]:
    catalog = json.loads((BOOK / "catalog.json").read_text())
    lessons = [r for r in catalog if r.get("lesson")]
    if len(lessons) != 42:
        raise ValueError("expected all 42 original lesson packets")
    order = ["READFIRST", *[r["id"] for r in lessons], "MODELS", "FEATURES", "CPULABS", "NATIVE", "BASICGUIDE", "CARDGUIDE", "BOARDATLAS"]
    introduction = (
        "APPLE-1 FIELD LIBRARY\n\n"
        "This is a paged reading edition. Predict, try on paper or host, then use A for answers.\n\n"
        "N next page. P previous. M choose book by two-digit number. Q returns to Monitor.\n\n"
        "The Pi runs NEURAL1 and local models. The 6502 reads lessons and executes small programs. "
        "No language model runs on the 6502.\n\n"
        "This edition is UPPERCASE. Case-sensitive host commands and exact output belong in the host source. "
        "All 42 packet READMEs, activities, text assets and answer keys are included. "
        "Figures and full source citations remain in the host book.\n\n"
        "Book 49 BOARDATLAS includes all 39 SP01 plates. Its vertical borders use !, a display-safe glyph. "
        "Use the same N/P/M/Q keys; plates use the full display without a footer.\n\n"
        "Use BASICLABS for saved Integer BASIC programs. See the host card guide for the load sequence. "
        "Starting this reader replaces BASIC program RAM; save your work first.\n\n"
        "This card image is host rehearsed. Installed firmware, screen characters, keys and timing still "
        "need acceptance on the finished hardware. Maintenance flashers in UTILITIES are preserved legacy "
        "files, not lesson launchers.\n\n"
        "Do not format or overwrite the preserved original. Build a new host image.\n\nBOOK INDEX\n"
    )
    introduction += "\n".join(f"{i:02} {name}" for i, name in enumerate(order))
    payloads = {}
    display = {}
    metadata = []
    source_paths = {BOOK / "catalog.json", ROOT / "software/card-reader/reader.asm", Path(__file__)}

    def add(name: str, title: str, parts: list[tuple[str, str]]) -> None:
        pages, answer = paginate(name, title, parts)
        payload = encode_book(pages, answer)
        payloads[name] = payload
        display[name] = pages
        metadata.append({"number": order.index(name), "name": name, "pages": len(pages), "answer_page": answer,
                         "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest(), "file_type": "06", "aux": "1000"})

    add("READFIRST", "START HERE", [("READ FIRST", introduction)])
    for r in lessons:
        packet = ROOT / r["lesson"]
        parts = []
        for filename, label in [("README.md", "LEARN"), ("ACTIVITY.md", "TRY"), ("ANSWERS.md", "ANSWERS")]:
            path = packet / filename
            text = path.read_text()
            text = text.split("\n## Worked companion")[0]
            parts.append((label, text))
            source_paths.add(path)
            if filename == "ACTIVITY.md":
                for asset in sorted((packet / "assets").glob("*.txt")):
                    source_paths.add(asset)
                    parts.append(("WORKSHEET " + asset.name, asset.read_text()))
        for filename in ("SOURCE-NOTES.md", "STATUS.md"):
            source_paths.add(packet / filename)
        parts.append(("SOURCES", f"Host packet: {r['lesson']}\nRead SOURCE-NOTES and STATUS for citations and open questions. "
                      "This uppercase reading copy is not an electrical procedure. Host code and source files preserve exact spelling and case."))
        add(r["id"], r["title"], parts)
    for name, prefix in [("MODELS", "L"), ("FEATURES", "F"), ("CPULABS", "T"), ("NATIVE", "N"), ("BASICGUIDE", "U"), ("CARDGUIDE", "K")]:
        parts = []
        for r in catalog:
            if not r["id"].startswith(prefix):
                continue
            parts.append((r["id"] + " " + r["title"], f"EVIDENCE MODE: {r['mode']}\n\n{r['explanation']}\n\n"
                          f"TRY: {r['challenge']}\n\nCHECK: {r['answer']}\n\nHOST LAB ID: {r['id']}"))
        add(name, name, parts)
    atlas_root = ROOT / "docs/field-library/SP01-two-boards-one-computer/card"
    atlas_sources = sorted(atlas_root.rglob("*.txt"))
    index = "SP01 PLATE INDEX\n\n" + "\n".join(p.relative_to(atlas_root).as_posix() for p in atlas_sources)
    atlas, _ = paginate("BOARDATLAS", "SP01 PLATES", [("PLATE INDEX", index)])
    for path in atlas_sources:
        source_paths.add(path)
        # Keep the diagram coordinates and width intact. `|` is outside the
        # original 64-glyph alphabet; ! provides a visible vertical border.
        atlas.append(ascii_reading(path.read_text().replace("|", "!")).rstrip("\n"))
    atlas_data = encode_book(atlas)
    payloads["BOARDATLAS"] = atlas_data
    display["BOARDATLAS"] = atlas
    metadata.append({"number": order.index("BOARDATLAS"), "name": "BOARDATLAS", "pages": len(atlas), "answer_page": None,
                     "bytes": len(atlas_data), "sha256": hashlib.sha256(atlas_data).hexdigest(), "file_type": "06", "aux": "1000"})
    assembled = LessonAssembler().assemble((ROOT / "software/card-reader/reader.asm").read_text(), origin=0x0800)
    if assembled.diagnostics or len(assembled.payload) > 0x400:
        raise ValueError(f"reader assembly does not fit: {assembled.diagnostics}")
    reader = bytearray(assembled.payload.ljust(0x400, b"\0"))
    for name in order:
        reader.extend((bytes([len(name)]) + name.encode("ascii")).ljust(16, b"\0"))
    payloads["READER"] = bytes(reader)
    inputs = {p.resolve().relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(source_paths)}
    manifest = {"schema_version": 1, "edition": "pre-hardware", "display": "40x24; SPACE-$5F plus CR; prose <=39x23; atlas <=40x24; no last-cell scroll",
                "format": "A1BK v1; BIN $06; reader $0800; books $1000-$7FFF", "hardware_accepted": False,
                "books": metadata, "source_sha256": inputs, "reader_sha256": hashlib.sha256(reader).hexdigest()}
    return payloads, display, manifest


def export(destination: Path) -> dict:
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("choose a new host directory")
    payloads, display, manifest = compile_books()
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "payloads").mkdir()
    for name, data in payloads.items():
        (destination / "payloads" / name).write_bytes(data)
    for name, pages in display.items():
        folder = destination / "pages" / name
        folder.mkdir(parents=True)
        for i, page in enumerate(pages, 1):
            (folder / f"{i:03}.txt").write_text(page + "\n", encoding="ascii")
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manifest = export(args.out)
    print(f"Compiled {len(manifest['books'])} books, {sum(b['pages'] for b in manifest['books'])} pages; RAM reader included; no device opened.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
