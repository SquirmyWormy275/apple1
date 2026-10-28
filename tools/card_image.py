"""Build and rehearse a NEW host CF image; never open a physical device.

The identified CFFA1 ROM performs the filesystem writes against modeled ATA.
The baseline remains read-only. The resulting image is a hardware candidate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from neural1.assembler import LessonAssembler
from tools.apple1_basic import ROM as BASIC_ROM
from tools.apple1_basic import resume_session, run_session
from tools.card_book import ROOT, compile_books, decode_book, encode_book, page_bytes
from tools.cffa1_model import Cffa1Machine, blank_virtual_card
from tools.prodos import ProdosImage


def screen_text(output: bytes) -> str:
    """40x24 scrolling character model, no cursor control or timing simulation."""
    rows = [""] * 24
    row, column = 0, 0
    for byte in output:
        char = byte & 0x7F
        if char == 13:
            row += 1
            column = 0
        elif 0x20 <= char <= 0x5F:
            rows[row] = rows[row].ljust(column)[:column] + chr(char)
            column += 1
            if column == 40:
                row += 1
                column = 0
        else:
            continue
        if row == 24:
            rows.pop(0)
            rows.append("")
            row = 23
    return "\n".join(rows).strip("\n")


def reader_step(machine: Cffa1Machine, keys: bytes = b"", *, start: bool = False) -> str:
    source = (ROOT / "software/card-reader/reader.asm").read_text()
    assembled = LessonAssembler().assemble(source, origin=0x800)
    if assembled.diagnostics:
        raise ValueError(assembled.diagnostics)
    if start:
        payloads, _, _ = compile_books()
        machine.memory[0x800:0x800 + len(payloads["READER"])] = payloads["READER"]
        machine.cpu.pc = 0x800
    machine.memory.output.clear()
    machine.memory.incoming.extend(keys)
    for _ in range(2_000_000):
        if machine.cpu.pc == 0xFF1F:
            return "MONITOR EXIT $FF1F"
        if machine.cpu.pc == assembled.symbols["KEY"] and not machine.memory.incoming:
            return screen_text(bytes(machine.memory.output))
        machine.cpu.step()
    raise RuntimeError(f"RAM reader instruction limit at {machine.cpu.pc:04X}")


def rehearse_reader() -> dict[str, str]:
    """Small deterministic fixture exercising the actual RAM reader and CFFA API."""
    machine = blank_virtual_card()
    machine.api(0x2C, name="EDUCATION")
    machine.prefix("EDUCATION")
    machine.write_file("READFIRST", encode_book(["FIRST PAGE", "SECOND PAGE", "ANSWER PAGE"], 2))
    machine.write_file("S01", encode_book(["LESSON S01", "LESSON ANSWER"], 1))
    observed = {}
    for action, keys, start, expected in [
        ("first", b"", True, "FIRST PAGE"), ("next", b"N", False, "SECOND PAGE"),
        ("previous", b"P", False, "FIRST PAGE"), ("answer", b"A", False, "ANSWER PAGE"),
        ("select", b"M01", False, "LESSON S01"), ("lesson-answer", b"A", False, "LESSON ANSWER"),
        ("exit", b"Q", False, "MONITOR EXIT $FF1F"),
    ]:
        observed[action] = reader_step(machine, keys, start=start)
        if expected not in observed[action]:
            raise AssertionError((action, observed[action]))
    machine.prefix("")
    observed["wrong-prefix"] = reader_step(machine, start=True)
    if "CFFA ERROR" not in observed["wrong-prefix"]:
        raise AssertionError("missing-prefix error was not visible")
    return observed


def regular_image(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("input must be a regular host image file, not a symlink or block device")
    if path.stat().st_size > 256 * 1024 * 1024:
        raise ValueError("image exceeds the host inspector's 256 MiB bound")
    return path.read_bytes()


def build(baseline_path: Path, destination: Path) -> dict:
    if destination.exists() or destination.is_symlink():
        raise FileExistsError("choose a new host build directory")
    registry = json.loads((ROOT / "cf-card/manifests/current.json").read_text())
    expected = registry["baseline"]
    baseline = regular_image(baseline_path)
    if len(baseline) != expected["size_bytes"] or hashlib.sha256(baseline).hexdigest() != expected["sha256"]:
        raise ValueError("baseline identity mismatch; hydrate the preserved LFS image")
    original = ProdosImage(baseline)
    payloads, display, edition = compile_books()
    machine = Cffa1Machine(baseline)
    machine.api(0x2C, name="EDUCATION")
    machine.prefix("EDUCATION")
    for name, data in payloads.items():
        machine.write_file(name, data, aux=0x800 if name == "READER" else 0x1000)
        if machine.read_file(name) != data:
            raise ValueError(f"CFFA readback differs: {name}")
    machine.prefix("")
    machine.api(0x2C, name="BASICLABS")
    machine.prefix("BASICLABS")
    basics = []
    for source in sorted((ROOT / "software/basic").glob("*.bas")):
        machine.save_basic(source.stem, source.read_text())
        encoded = machine.read_file(source.stem)
        if not encoded.startswith(b"A1\0"):
            raise ValueError("CFFA did not produce its versioned BASIC header")
        machine.memory[0x4A:0x100] = [0] * 182
        machine.memory[0x800:0x1000] = [0] * 2048
        machine.memory[0xE000:0xF000] = BASIC_ROM.read_bytes()
        machine.api(0x26, name=source.stem)
        session = source.with_suffix(".session").read_text().splitlines()
        tail = session[len(source.read_text().splitlines()):]
        result = resume_session(machine.memory, tail)
        reference = run_session(session)
        if result.stop != "waiting-for-input" or result.transcript.split(">RUN\n", 1)[1] != reference.transcript.split(">RUN\n", 1)[1]:
            raise ValueError(f"restored BASIC program differs: {source.stem}")
        basics.append({"name": source.stem, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                       "session_sha256": hashlib.sha256(source.with_suffix(".session").read_bytes()).hexdigest(),
                       "ba1_sha256": hashlib.sha256(encoded).hexdigest(),
                       "restored_output_sha256": hashlib.sha256(result.transcript.encode()).hexdigest(),
                       "restored_run": "matches cold source run"})
    machine.prefix("EDUCATION")
    reader_screens = {}
    all_screens = {}
    writes_before_reader = machine.memory.writes
    for i, record in enumerate(edition["books"]):
        name = record["name"]
        text = reader_step(machine, b"" if i == 0 else f"M{i:02}".encode(), start=i == 0)
        expected_screen = screen_text(b"\r" * 24 + page_bytes(display[name][0]))
        # The selection prompt precedes the clearing scroll; the final screen must match.
        if text != expected_screen:
            raise ValueError(f"reader screen mismatch: {name}")
        reader_screens[name] = text
        all_screens[name] = [text]
        for page in display[name][1:]:
            actual = reader_step(machine, b"N")
            expected_screen = screen_text(b"\r" * 24 + page_bytes(page))
            if actual != expected_screen:
                raise ValueError(f"reader page mismatch: {name}/{len(all_screens[name]) + 1}")
            all_screens[name].append(actual)
        answer = record["answer_page"]
        if answer is not None:
            actual = reader_step(machine, b"A")
            expected_screen = screen_text(b"\r" * 24 + page_bytes(display[name][answer]))
            if actual != expected_screen:
                raise ValueError(f"reader answer mismatch: {name}")
    if reader_step(machine, b"Q") != "MONITOR EXIT $FF1F":
        raise ValueError("reader did not return to the Monitor")
    if machine.memory.writes != writes_before_reader:
        raise ValueError("the RAM reader wrote to the virtual card")
    candidate = machine.memory.materialize()
    inspected = ProdosImage(candidate)
    for path, item in original.entries.items():
        if inspected.entries.get(path) != item:
            raise ValueError(f"legacy entry changed: {path}")
        if item.storage != 13 and inspected.read(path) != original.read(path):
            raise ValueError(f"legacy contents changed: {path}")
    for number, owner in original.owners.items():
        if owner not in ("/", "bitmap") and inspected.block(number) != original.block(number):
            raise ValueError(f"preserved allocated block changed: {number}")
    if candidate[original.total * 512:] != baseline[original.total * 512:]:
        raise ValueError("data beyond the first volume changed")
    for name, data in payloads.items():
        if inspected.read("/EDUCATION/" + name) != data:
            raise ValueError(f"independent readback differs: {name}")
        if name != "READER":
            decode_book(data)
    receipt = {
        "schema_version": 1, "baseline_sha256": expected["sha256"], "image_sha256": hashlib.sha256(candidate).hexdigest(),
        "image_bytes": len(candidate), "volume_blocks": original.total, "books": len(display),
        "display_pages": sum(len(p) for p in display.values()), "original_entries_preserved": len(original.entries),
        "original_allocated_blocks_preserved_except_root_and_bitmap": True, "tail_after_first_volume_unchanged": True,
        "ata_model_reads": machine.memory.reads, "ata_model_writes": machine.memory.writes,
        "changed_blocks": len(machine.memory.changed), "basics": basics, "inventory": inspected.inventory(),
        "reader_validation": "every page of all 50 books, answer jumps and Monitor exit checked by actual RAM reader + CFFA ROM",
        "reader_card_writes": 0,
        "runtime_source_sha256": {
            path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
            for path in ["tools/card_image.py", "tools/cffa1_model.py", "tools/prodos.py", "tools/apple1_basic.py",
                         "software/card-reader/reader.asm", "preservation/software/apple1-reference/provenance.json"]
        },
        "physical_devices_opened": 0, "hardware_accepted": False, "edition": edition,
    }
    all_screen_text = json.dumps(all_screens, indent=2) + "\n"
    receipt["reader_screens_sha256"] = hashlib.sha256(all_screen_text.encode()).hexdigest()
    destination.mkdir(parents=True, exist_ok=False)
    (destination / "education-candidate.img").write_bytes(candidate)
    (destination / "build.json").write_text(json.dumps(receipt, indent=2) + "\n")
    (destination / "reader-screens.json").write_text(json.dumps(reader_screens, indent=2) + "\n")
    (destination / "all-reader-screens.json").write_text(all_screen_text)
    return receipt


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    stage = sub.add_parser("build", help="build a new image from the verified preserved baseline")
    stage.add_argument("--baseline", type=Path, required=True)
    stage.add_argument("--out", type=Path, required=True)
    inspect = sub.add_parser("inspect", help="read a regular host image and validate its ProDOS allocation")
    inspect.add_argument("image", type=Path)
    sub.add_parser("rehearse", help="exercise the actual RAM pager and CFFA API on a virtual-only fixture")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "build":
        receipt = build(args.baseline, args.out)
        print(f"Built {receipt['books']} books, {receipt['display_pages']} pages, {len(receipt['basics'])} BA1 programs; hardware acceptance pending.")
        print("Image SHA-256:", receipt["image_sha256"])
    elif args.command == "inspect":
        print(json.dumps(ProdosImage(regular_image(args.image)).inventory(), indent=2))
    else:
        print(json.dumps(rehearse_reader(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
