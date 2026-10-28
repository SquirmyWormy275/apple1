"""Run, capture and verify the off-device textbook's authored worked examples."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import re
import runpy
import subprocess
import sys
import textwrap
from pathlib import Path

from tools.textbook_support import ROOT

BOOK = ROOT / "docs/textbook"


def catalog() -> list[dict]:
    return json.loads((BOOK / "catalog.json").read_text())


def run(identifier: str) -> str:
    if sys.flags.optimize:
        raise ValueError("Run without -O: worked-example assertions must execute.")
    records = {record["id"]: record for record in catalog()}
    if identifier not in records or not re.fullmatch(r"[A-Z]{1,2}[0-9]{2}", identifier):
        raise ValueError("Unknown lab ID. Use python -m tools.textbook list.")
    record = records[identifier]
    stream = io.StringIO()
    with contextlib.redirect_stdout(stream):
        print(f"{identifier} / {record['title']}")
        print(f"MODE: {record['mode']} | HOST ONLY | NO MODEL INFERENCE")
        print()
        runpy.run_path(str(BOOK / "examples" / f"{identifier}.py"), run_name="__textbook_lab__")
        print("\nCHECKS PASSED | No physical serial connection was requested.")
    return stream.getvalue()


def render_capture(text: str, destination: Path) -> None:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as error:
        raise ValueError("Images require: python -m pip install -e '.[textbook]'") from error
    # Prefer fixed-width text for register columns; keep a portable fallback.
    font = None
    small = None
    for name in ("/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf", "DejaVuSansMono.ttf", "C:/Windows/Fonts/consola.ttf"):
        try:
            font = ImageFont.truetype(name, 22)
            small = ImageFont.truetype(name, 16)
            break
        except OSError:
            continue
    if font is None or small is None:
        font = ImageFont.load_default(size=22)
        small = ImageFont.load_default(size=16)
    lines = []
    for line in text.splitlines():
        lines.extend(textwrap.wrap(line, width=94, break_long_words=False, break_on_hyphens=False, replace_whitespace=False) or [""])
    image = Image.new("RGB", (1320, 110 + len(lines) * 31), "#0c1319")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1319, 4), fill="#62d5c3")
    draw.text((36, 22), "RECORDED STDOUT / TEXTBOOK WORKED EXAMPLE", font=small, fill="#79cddd")
    for index, line in enumerate(lines):
        # Render control characters visibly; input and source strings may contain CR.
        visible = "".join(c if ord(c) >= 32 else f"\\x{ord(c):02x}" for c in line)
        draw.text((36, 60 + index * 31), visible, font=font, fill="#cce7d1")
    draw.text(
        (36, image.height - 29),
        "Actual host output rendered for reading; not a deployed Pi-console screenshot.",
        font=small,
        fill="#95aaa9",
    )
    image.save(destination)


def capture(destination: Path, *, images: bool) -> None:
    destination = destination.resolve()
    if destination.exists():
        raise ValueError("Use a new output directory; retained captures are never overwritten.")
    if images:
        import importlib.util

        if importlib.util.find_spec("PIL") is None:
            raise ValueError("Images require: python -m pip install -e '.[textbook]'")
    destination.mkdir(parents=True)
    manifest = {"schema_version": 1, "target": "OFF_DEVICE", "model_inference": False, "records": [], "source_sha256": {}}
    sources = [
        BOOK / "catalog.json",
        *sorted((BOOK / "examples").glob("*.py")),
        ROOT / "tools/textbook.py",
        ROOT / "tools/textbook_support.py",
        *sorted((ROOT / "neural1").glob("*.py")),
        *sorted((ROOT / "tools").glob("*.py")),
        *[p for p in sorted((ROOT / "firmware/vendor/110REV03").rglob("*")) if p.is_file()],
        *sorted((ROOT / "software/ram-only").glob("*.hex")),
        *sorted((ROOT / "data/neural1/history").glob("*.json")),
        *sorted((ROOT / "art/provenance").glob("*.json")),
        ROOT / "cf-card/manifests/current.json",
        *sorted((ROOT / "docs/neural1/operations/evidence/pi-closeout-2026-09-10").glob("*.json")),
        *[p for p in sorted((ROOT / "docs/field-library").rglob("*.md")) if p.name != "WORKED.md"],
    ]
    for path in sources:
        manifest["source_sha256"][path.relative_to(ROOT).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    for record in catalog():
        identifier = record["id"]
        environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run(  # noqa: S603 - reviewed module and catalog identifiers
            [sys.executable, "-m", "tools.textbook", "run", identifier], cwd=ROOT, env=environment, capture_output=True, timeout=30
        )
        if result.returncode:
            raise ValueError(f"{identifier} failed; capture not complete: {result.stderr.decode(errors='replace')}")
        (destination / f"{identifier}.txt").write_bytes(result.stdout)
        entry = {"id": identifier, "mode": record["mode"], "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(), "exit_code": 0}
        if images:
            picture = destination / f"{identifier}.png"
            render_capture(result.stdout.decode(), picture)
            entry["image_sha256"] = hashlib.sha256(picture.read_bytes()).hexdigest()
        manifest["records"].append(entry)
        print(f"{identifier}: captured")
    (destination / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def verify(destination: Path, *, rerun: bool) -> None:
    manifest = json.loads((destination / "manifest.json").read_text())
    expected = {record["id"] for record in catalog()}
    actual = [entry["id"] for entry in manifest["records"]]
    if set(actual) != expected or len(actual) != len(expected):
        raise ValueError("Capture inventory does not match every catalog entry exactly once.")
    for relative, digest in manifest["source_sha256"].items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Capture source changed: {relative}")
    for entry in manifest["records"]:
        identifier = entry["id"]
        raw = (destination / f"{identifier}.txt").read_bytes()
        if hashlib.sha256(raw).hexdigest() != entry["stdout_sha256"]:
            raise ValueError(f"Changed transcript: {identifier}")
        if (
            "image_sha256" in entry
            and hashlib.sha256((destination / f"{identifier}.png").read_bytes()).hexdigest() != entry["image_sha256"]
        ):
            raise ValueError(f"Changed image: {identifier}")
        if rerun and run(identifier).encode() != raw:
            raise ValueError(f"Rerun differs: {identifier}")
    print(f"Verified {len(actual)} examples, source identities and capture hashes" + ("; all reruns match." if rerun else "."))


def build_pages() -> None:
    records = catalog()
    for index, record in enumerate(records):
        identifier = record["id"]
        transcript = (BOOK / "captures" / f"{identifier}.txt").read_text()
        example = (BOOK / "examples" / f"{identifier}.py").read_text()
        lesson = record["lesson"]
        destination = ROOT / lesson / "WORKED.md" if lesson else BOOK / "features" / f"{identifier}.md"
        destination.parent.mkdir(parents=True, exist_ok=True)
        prefix = "../../textbook/" if lesson else "../"
        original = (
            "[Lesson](README.md) · [Activity](ACTIVITY.md) · [Answers](ANSWERS.md) · [Source notes](SOURCE-NOTES.md)\n\n" if lesson else ""
        )
        previous = records[index - 1] if index else None
        following = records[index + 1] if index + 1 < len(records) else None

        def link(item, parent=destination.parent):
            target = ROOT / item["lesson"] / "WORKED.md" if item["lesson"] else BOOK / "features" / f"{item['id']}.md"
            relative = os.path.relpath(target, parent)
            return f"[{item['id']}: {item['title']}]({relative})"

        nav = " · ".join(([f"Previous: {link(previous)}"] if previous else []) + ([f"Next: {link(following)}"] if following else []))
        text = f"""# {identifier} worked lab: {record["title"]}

{original}**Goal:** {record["concept"]}.

**Mode:** `{record["mode"]}`. This companion runs on the host; it does not
change the original packet's paper activity or authorize physical Replica work.

## Understand the example

{record["explanation"]}

## Predict before running

Read the source below. Write down the expected printed values and the condition
that would make its checks fail. For a CPU trace, distinguish state before an
instruction from state after it. For a conceptual exercise, explain the rule
behind each classification rather than memorizing the printed label.

## Run it

From the checkout root with your environment active:

```bash
python -m tools.textbook run {identifier}
```

The runner executes this [complete source]({prefix}examples/{identifier}.py):

```python
{example.rstrip()}
```

## Recorded result

This output was actually executed and checked. The image is a readable render
of that stdout, not a screenshot of the deployed Pi console. A teaching fixture
or a host analogue is not independent historical or physical evidence.

```text
{transcript.rstrip()}
```

![{identifier} recorded worked-example output]({prefix}captures/{identifier}.png)

[Raw output]({prefix}captures/{identifier}.txt) · [Capture manifest]({prefix}captures/manifest.json)

## Change one thing

{record["challenge"]}

<details>
<summary>Compare your reasoning with the worked answer</summary>

{record["answer"]}

</details>

## Check your understanding

Explain the result without reading the code aloud. Name one condition that the
example did not test. Keep your prediction, changed input, actual output, and
interpretation together in your lab notebook. Use the linked textbook chapter
and the original source records for the broader context and evidence limits.

[Textbook home]({prefix}README.md) · {nav}
"""
        destination.write_text(text)
    print(f"Built {len(records)} worked guides from the catalog, examples and captured outputs.")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    one = commands.add_parser("run")
    one.add_argument("id")
    collect = commands.add_parser("capture")
    collect.add_argument("--out", type=Path, required=True)
    collect.add_argument("--images", action="store_true")
    check = commands.add_parser("verify")
    check.add_argument("directory", type=Path)
    check.add_argument("--rerun", action="store_true")
    commands.add_parser("build-pages")
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for record in catalog():
                print(f"{record['id']:4} {record['mode']:22} {record['title']}")
        elif args.command == "run":
            print(run(args.id), end="")
        elif args.command == "capture":
            capture(args.out, images=args.images)
        elif args.command == "verify":
            verify(args.directory, rerun=args.rerun)
        else:
            build_pages()
    except (OSError, ValueError, AssertionError, subprocess.TimeoutExpired) as error:
        print(f"Textbook lab stopped: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
