"""Build display-native educational books; never opens a physical device.

Output filenames use CiderPress NAPS suffixes to retain ProDOS type/load address.
Original UTF-8 source, images and executable host code are kept in SOURCE.ZIP.
The display edition is uppercase ASCII and is for reading, not copying code.
"""
from __future__ import annotations

import argparse
import functools
import hashlib
import json
import re
import shutil
import struct
import subprocess
import textwrap
import unicodedata
import zipfile
from pathlib import Path

from py65.assembler import Assembler
from py65.devices.mpu6502 import MPU

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 0x1000
LIMIT = 0x8000
GROUPS = dict(S="START", C="COMPUTER", M="MONITOR", A="ASSEMBLY", B="BASIC",
              R="CREATIVE", H="HISTORY", X="PROJECTS", SP="HARDWARE")
PARTS = {"README.md": "READ", "ACTIVITY.md": "TRY", "ANSWERS.md": "KEY",
         "WORKED.md": "WORKED", "SOURCE-NOTES.md": "SOURCES", "STATUS.md": "STATUS"}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@functools.lru_cache(maxsize=1)
def assemble_reader() -> bytes:
    """Two-pass assembly; forward references always use absolute/relative mode."""
    lines = [line.split(";")[0].strip() for line in (ROOT / "cf-card/reader.s").read_text().splitlines()]
    labels: dict[str, int] = {}
    result = bytearray()
    for pass_number in range(2):
        result = bytearray()
        for line in lines:
            if not line:
                continue
            pc = ORIGIN + len(result)
            if line.endswith(":"):
                labels[line[:-1]] = pc
                continue
            if "FIRST_" in line:
                first = labels.get("END", ORIGIN)
                line = line.replace("FIRST_LO", f"${first & 255:02X}").replace("FIRST_HI", f"${first >> 8:02X}")
            op, *operand = line.split(maxsplit=1)
            if operand and re.fullmatch(r"[A-Z]+", operand[0]):
                # A local branch placeholder must be in range even on pass one.
                target = labels.get(operand[0], pc if op.startswith("B") else ORIGIN)
                line = f"{op} ${target:04X}"
            result.extend(Assembler(MPU()).assemble(line, pc=pc))
        if pass_number == 0:
            labels["END"] = ORIGIN + len(result)
    return bytes(result)


def ascii_text(text: str) -> str:
    replacements = {"→": "->", "←": "<-", "↔": "<->", "×": "X", "÷": "/",
                    "≤": "<=", "≥": ">=", "≠": "!=", "–": "-", "—": "--",
                    "’": "'", "‘": "'", "“": '"', "”": '"', "…": "...", "•": "*",
                    "✓": "PASS", "✅": "PASS", "⚠": "NOTE", "│": "|", "─": "-"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Keep image/link captions; exact URLs and case-sensitive code are in ZIP.
    text = re.sub(r"!?\[([^\]]*)\]\([^\n)]*\)", r"\1", text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c if c in "\n\t" or 32 <= ord(c) <= 126 else "" if unicodedata.combining(c) else "?" for c in text)
    return text.upper().expandtabs(4)


def pages_for(text: str, title: str) -> list[list[str]]:
    lines: list[str] = []
    for line in ascii_text(text).splitlines():
        # Preserve indentation and all characters when splitting wide code/tables.
        lines.extend(textwrap.wrap(line, width=40, replace_whitespace=False,
                                   drop_whitespace=False, break_on_hyphens=False) or [""])
    chunks = [lines[i:i + 20] for i in range(0, len(lines), 20)] or [[]]
    return [[ascii_text(title)[:40], f"PAGE {i + 1}/{len(chunks)} | DISPLAY EDITION", *chunk,
             *([""] * (20 - len(chunk))), "", "SPACE NEXT / B BACK / Q MONITOR"]
            for i, chunk in enumerate(chunks)]


def encode_screen(lines: list[str]) -> bytes:
    if len(lines) > 24 or any(len(line) > 40 for line in lines):
        raise ValueError("screen exceeds 40x24")
    lines = lines + [""] * (24 - len(lines))
    if len(lines[-1]) == 40:
        raise ValueError("last screen line would auto-scroll; reserve last column")
    out = bytearray(b"\r")  # Align to column zero after a Monitor/CFFA prompt.
    for i, line in enumerate(lines):
        data = line.encode("ascii")
        if any(c < 32 or c > 126 for c in data) or line != line.upper():
            raise ValueError("screen must be uppercase printable ASCII")
        out.extend(data)
        # Apple-1 hardware wraps at column 40; CR here would create a blank row.
        if i < 23 and len(line) < 40:
            out.extend(b"\r")
    return bytes(out) + b"\0"


def compile_book(pages: list[list[str]]) -> bytes:
    if not pages:
        raise ValueError("empty book")
    code = assemble_reader()
    encoded = [encode_screen(page) for page in pages]
    addresses: list[int] = []
    cursor = ORIGIN + len(code)
    for page in encoded:
        addresses.append(cursor)
        cursor += 4 + len(page)
    if cursor + 1 > LIMIT:
        raise ValueError("book exceeds Replica 32K RAM")
    result = bytearray(code)
    for i, page in enumerate(encoded):
        previous = addresses[max(i - 1, 0)]
        following = addresses[i + 1] if i + 1 < len(addresses) else 0
        result.extend(struct.pack("<HH", previous, following))
        result.extend(page)
    # Keep the final ProDOS block allocated even if a page's NUL starts it.
    # Some host writers otherwise represent that all-zero tail as a sparse hole.
    result.append(0xEA)
    return bytes(result)


class Builder:
    def __init__(self, output: Path):
        if output.exists():
            raise ValueError("choose a new output directory; builds are retained")
        self.output = output
        self.payload = output / "payload"
        self.payload.mkdir(parents=True)
        self.records: list[dict] = []
        self.inputs: dict[str, str] = {}

    def read(self, path: Path) -> str:
        data = path.read_bytes()
        self.inputs[str(path.relative_to(ROOT))] = digest(data)
        return data.decode("utf-8")

    def add(self, name: str, data: bytes, filetype: int, aux: int, **metadata) -> None:
        if any(not re.fullmatch(r"[A-Z][A-Z0-9.]{0,14}", part) for part in name.split("/")):
            raise ValueError(f"invalid ProDOS pathname: {name}")
        if name.count("/") > 1 or any(r["path"] == name for r in self.records):
            raise ValueError(f"nested or duplicate pathname: {name}")
        target = self.payload / f"{name}#{filetype:02x}{aux:04x}"
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(data)
        self.records.append(dict(path=name, file_type=filetype, aux_type=aux, bytes=len(data),
                                 sha256=digest(data), **metadata))

    def book(self, name: str, pages: list[list[str]], sources: list[str]) -> None:
        # Partition very large books without truncating or dropping pages.
        chunks: list[list[list[str]]] = []
        chunk: list[list[str]] = []
        used = len(assemble_reader())
        for page in pages:
            size = 4 + len(encode_screen(page))
            if used + size + 1 > LIMIT - ORIGIN:
                chunks.append(chunk)
                chunk, used = [], len(assemble_reader())
            chunk.append(page)
            used += size
        chunks.append(chunk)
        for i, part in enumerate(chunks):
            suffix = f".V{i+1}" if len(chunks) > 1 else ""
            self.add(name + suffix, compile_book(part), 6, ORIGIN, pages=len(part), sources=sources,
                     kind="6502-display-reader")
            screen = self.output / "screens" / (name + suffix + ".json")
            screen.parent.mkdir(parents=True, exist_ok=True)
            screen.write_text(json.dumps(part, indent=2) + "\n")

    def document(self, name: str, path: Path) -> None:
        relative = str(path.relative_to(ROOT))
        self.book(name, pages_for(self.read(path), name), [relative])


def build(output: Path) -> dict:
    b = Builder(output)
    field = ROOT / "docs/field-library"
    lessons = sorted(p for p in field.iterdir() if (p / "STATUS.md").is_file())
    if len(lessons) != 42:
        raise ValueError(f"expected 42 packets, found {len(lessons)}; review curriculum coverage")
    for lesson in lessons:
        identifier = lesson.name.split("-")[0]
        prefix = re.sub(r"\d", "", identifier)
        folder = GROUPS[prefix]
        for filename, label in PARTS.items():
            path = lesson / filename
            if not path.is_file():
                raise ValueError(f"missing required packet component: {path}")
            b.document(f"{folder}/{identifier}.{label}", path)
        assets = sorted(p for p in (lesson / "assets").rglob("*") if p.suffix in {".txt", ".md", ".hex", ".s", ".asm"})
        if assets:
            text = "\n\n".join(f"{p.name}\n{b.read(p)}" for p in assets)
            b.book(f"{folder}/{identifier}.ASSETS", pages_for(text, identifier + " ASSETS"),
                   [str(p.relative_to(ROOT)) for p in assets])

    atlas_root = field / "SP01-two-boards-one-computer/card"
    atlas = [atlas_root / f"{i:02}-{name}.txt" for i, name in enumerate(("title", "route", "big-picture"))]
    atlas += [p for section in ("original", "replica", "compare", "activity", "evidence", "sources")
              for p in sorted((atlas_root / section).glob("*.txt"))]
    atlas += [atlas_root / "99-index.txt"]
    if set(atlas) != set(atlas_root.rglob("*.txt")):
        raise ValueError("atlas reading order does not cover every source screen")
    # Preserve every source atlas screen without rewrapping its diagrams.
    atlas_pages = []
    for path in atlas:
        lines = b.read(path).splitlines()
        encode_screen(lines)
        atlas_pages.append(lines)
    if len(atlas_pages) != 39:
        raise ValueError("expected all 39 approved atlas screens")
    b.book("HARDWARE/ATLAS", pages_for("39 original atlas screens follow.\nSPACE next, B back, Q Monitor.\nThe source screen content is unchanged.", "SP01 ATLAS") + atlas_pages,
           [str(p.relative_to(ROOT)) for p in atlas])

    # Companion resources retain simple, stable, collision-free card names.
    companions = sorted([p for name in ("teacher-materials", "visitor-mode", "program-annotations")
                         for p in (field / name).glob("*.md")])
    for i, path in enumerate(companions, 1):
        b.document(f"TEACHERS/DOC{i:02}", path)
    for i, name in enumerate(("README.md", "SOURCES.md", "GLOSSARY.md", "EMULATOR-RUNS.md"), 1):
        b.document(f"REFERENCE/REF{i:02}", field / name)
    for i, name in enumerate(("apple1-learning-library-curriculum.md", "apple1-software-library.md", "emulator-demo-guide.md"), 5):
        b.document(f"REFERENCE/REF{i:02}", ROOT / "docs" / name)

    book = ROOT / "docs/textbook"
    for i, path in enumerate(sorted((book / "chapters").glob("*.md"))):
        b.document(f"TEXTBOOK/CH{i:02}", path)
    for i, name in enumerate(("README.md", "course-guide.md", "review.md", "coverage.md")):
        b.document(f"TEXTBOOK/GUIDE{i}", book / name)
    for i, path in enumerate(sorted((book / "reference").glob("*.md"))):
        b.document(f"TEXTBOOK/DESK{i}", path)
    for path in sorted((book / "features").glob("*.md")):
        b.document(f"FEATURES/{path.stem}", path)
    for path in sorted((book / "captures").glob("*.txt")):
        b.document(f"RUNS/{path.stem}", path)
    b.document("TEXTBOOK/NATIVE", book / "native/README.md")
    for i, path in enumerate(sorted((ROOT / "art").rglob("*.txt")), 1):
        b.document(f"ART/ART{i:02}", path)

    for path in sorted((ROOT / "software/ram-only").glob("*.hex")):
        data = bytes.fromhex(b.read(path))
        name = "LINE.INPUT" if path.stem == "line-input-0300" else "LINE.ECHO"
        b.add(f"RAMDEMOS/{name}", data, 6, 0x0300, kind="original-ram-only-candidate",
              sources=[str(path.relative_to(ROOT))])
    b.document("RAMDEMOS/READ.FIRST", ROOT / "software/ram-only/README.md")

    # Deterministic ZIP: exact original bytes, paths, images and host sources.
    archive_paths = []
    for folder in ("docs", "software/ram-only", "art", "tools", "tests", "neural1", "schemas", "configs", "data", "cf-card", "firmware"):
        archive_paths.extend(p for p in (ROOT / folder).rglob("*")
                             if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
                             and not p.is_relative_to(ROOT / "cf-card/releases"))
    archive_paths += [ROOT / "pyproject.toml", ROOT / "requirements-dev.txt", ROOT / "README.md"]
    archive_paths += [ROOT / "preservation/cf-card/2026-08-28/MANIFEST.md"]
    archive_paths += [ROOT / "docs" / name for name in ("apple1-learning-library-curriculum.md", "apple1-software-library.md", "emulator-demo-guide.md")]
    archive = output / "SOURCE.ZIP"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in sorted(set(archive_paths)):
            relative = str(path.relative_to(ROOT))
            data = path.read_bytes()
            self_info = zipfile.ZipInfo(relative, (2026, 10, 27, 0, 0, 0))
            self_info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(self_info, data)
            b.inputs[relative] = digest(data)
    b.add("HOSTSRC/SOURCE.ZIP", archive.read_bytes(), 0, 0, kind="host-source-archive")

    for folder in sorted({r["path"].split("/")[0] for r in b.records}):
        entries = [r for r in b.records if r["path"].startswith(folder + "/")]
        lines = [folder, "", "FILES ARE LOADED ONE AT A TIME.", "READERS LOAD AND RUN AT $1000.",
                 "SPACE NEXT / B BACK / Q MONITOR.", "", "CONTENTS:"]
        for record in entries:
            lines += [record["path"].split("/")[1], *("  " + p for p in record.get("sources", []))]
        b.book(folder + "/INDEX", pages_for("\n".join(lines), folder + " INDEX"), [])

    guide = """APPLE-1 FIELD LIBRARY
COMPLETE DISPLAY EDITION / 2026-10-27

READ THIS FIRST
In CFFA1: P selects a folder.
L loads a named binary at $1000.
Accept its $1000 address with ENTER.
Then Q leaves the CFFA1 menu.
At Monitor, type 1000R to read.
Choose START then S01.READ to begin.
Each folder has an INDEX reader.
Q in a reader returns to Monitor.
9000R returns to the CFFA1 menu.
Space moves ahead; B goes back.
On the final page, next exits.

LESSON FILE SUFFIXES
READ = lesson, TRY = activity
KEY = answers, WORKED = worked example
SOURCES = citations, STATUS = limits
ASSETS = worksheets and code to READ

FOLDERS
START, COMPUTER, MONITOR, ASSEMBLY
BASIC, CREATIVE, HISTORY, PROJECTS
HARDWARE: SP01 and 39-screen ATLAS
TEACHERS: teacher and visitor material
TEXTBOOK: 13 chapters and guides
FEATURES: all extended feature labs
RUNS: all 100 captured host examples
REFERENCE: sources and glossary
ART: text art and portal
RAMDEMOS: two original RAM candidates
HOSTSRC: exact-source ZIP for a PC

WHAT IS RUNNABLE HERE?
Only the reader program displays text.
Python, NEURAL1 and local models run
on a modern host, not the 6502.
Code in these screens is READ ONLY.
Its original case, complete links,
source, PNGs and tools are in the ZIP.
Some source review items remain open;
their status files are included.
Installation does not close them.

ATLAS: B/SPACE/Q still work even on
screens without navigation footers.
FILES ENDING .V1/.V2 CONTINUE IN THE
NEXT VOLUME; NO PAGES WERE DROPPED.

ORIGINAL CARD MATERIAL
UTILITIES and GAMES are preserved.
No firmware updater was executed.
No hardware operation was performed.
New readers are RAM-only programs.
They write no files or EEPROM.
Emulator checks do not establish
operation on your physical board.
"""
    b.book("START.HERE", pages_for(guide, "START HERE"), [])
    git = shutil.which("git")
    if git is None:
        raise ValueError("Git is required to record the source revision")
    revision = subprocess.check_output([git, "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()  # noqa: S603 -- fixed read-only Git arguments
    manifest = dict(schema_version=1, source_revision=revision,
                    lesson_packets=len(lessons), atlas_pages=len(atlas), reader_origin=ORIGIN,
                    source_hashes=b.inputs, files=b.records)
    data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    b.add("HOSTSRC/BUILD.JSON", data, 0, 0, kind="build-manifest")
    (output / "build.json").write_bytes(data)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = build(args.output.resolve())
    print(json.dumps({"lessons": manifest["lesson_packets"], "files": len(manifest["files"]),
                      "pages": sum(r.get("pages", 0) for r in manifest["files"]), "output": str(args.output)}))


if __name__ == "__main__":
    main()
