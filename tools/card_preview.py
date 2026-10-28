"""Render retained RAM-reader observations as a labeled gallery and offline viewer."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path


def render(build_dir: Path, output: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont

    if output.exists() or output.is_symlink():
        raise FileExistsError("choose a new preview directory")
    screens = json.loads((build_dir / "all-reader-screens.json").read_text())
    receipt = json.loads((build_dir / "build.json").read_text())
    if hashlib.sha256((build_dir / "all-reader-screens.json").read_bytes()).hexdigest() != receipt["reader_screens_sha256"]:
        raise ValueError("retained screen hashes differ from build receipt")
    if set(screens) != {r["name"] for r in receipt["edition"]["books"]}:
        raise ValueError("capture inventory differs from the built edition")
    output.mkdir(parents=True, exist_ok=False)
    font, small = None, None
    for name in ("/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf", "DejaVuSansMono.ttf", "C:/Windows/Fonts/consola.ttf"):
        try:
            font = ImageFont.truetype(name, 20)
            small = ImageFont.truetype(name, 13)
            break
        except OSError:
            continue
    if font is None or small is None:
        font, small = ImageFont.load_default(size=20), ImageFont.load_default(size=13)

    def picture(name: str, number: int):
        image = Image.new("RGB", (880, 740), "#0b1418")
        draw = ImageDraw.Draw(image)
        draw.text((30, 20), f"APPLE-1 CARD READER / {name} / {number + 1:03}", font=font, fill="#ffffff")
        draw.rounded_rectangle((24, 62, 856, 668), radius=12, fill="#050b08", outline="#52745b")
        for row, line in enumerate(screens[name][number].splitlines()):
            for column, char in enumerate(line):
                draw.text((50 + column * 18, 75 + row * 24), char, font=font, fill="#cbf3ae")
        draw.text((30, 690), "Actual RAM reader + CFFA1 ROM; modeled display. No physical capture.", font=small, fill="#a3b5b9")
        return image

    for name in screens:
        picture(name, 0).save(output / f"{name}.png")
    atlas_map = next(i for i, text in enumerate(screens["BOARDATLAS"]) if "ORIGINAL APPLE-1 / ATLAS MAP" in text)
    picture("BOARDATLAS", atlas_map).save(output / "BOARDATLAS-map.png")
    frames = [picture(name, page) for name, page in [
        ("READFIRST", 0), ("READFIRST", 1), ("C01", 0),
        ("C01", next(b["answer_page"] for b in receipt["edition"]["books"] if b["name"] == "C01")),
        ("BASICGUIDE", 0), ("MODELS", 0), ("BOARDATLAS", atlas_map),
    ]]
    frames[0].save(output / "reader-tour.gif", save_all=True, append_images=frames[1:], duration=2200, loop=0)
    # The embedded data are exact observed screens; the browser only selects
    # among them. It does not pretend to be another emulator or a live board.
    data = json.dumps(screens).replace("<", "\\u003c")
    books = json.dumps(receipt["edition"]["books"]).replace("<", "\\u003c")
    options = "".join(f'<option value="{html.escape(r["name"])}">{r["number"]:02} {html.escape(r["name"])}</option>'
                      for r in receipt["edition"]["books"])
    document = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Apple-1 card reading edition</title><style>
body{margin:0;background:#0b1418;color:#e4efed;font:18px system-ui;max-width:900px;padding:24px;margin:auto}
a{color:#a8dfb4}select,button{font:inherit;padding:10px;border:1px solid #729b82;background:#13251e;color:white;border-radius:6px;margin:3px}
pre{background:#050b08;color:#cbf3ae;border:1px solid #52745b;border-radius:12px;padding:24px;min-height:29em;overflow:auto;font:clamp(11px,2.1vw,20px)/1.2 monospace;white-space:pre}
p{line-height:1.5}button:focus-visible,select:focus-visible{outline:3px solid #fbdd7e}
</style><h1>Apple-1 card reading edition</h1><p>Browse actual output retained from the RAM reader and CFFA1 firmware running on a modeled NMOS 6502. This offline viewer selects recorded pages; it is not a physical capture or a live emulator.</p>
<label for="book">Book</label><select id="book">__A1_OPTIONS__</select><p><button id="previous">P · Previous</button><button id="next">N · Next</button><button id="answer">A · Answers</button> <span id="count" aria-live="polite"></span></p>
<pre id="screen" aria-label="Recorded 40 by 24 display" tabindex="0"></pre><p>All original lesson readings, activities, text worksheets and answers are included. The uppercase copy gives host lab routes for local models and software features. Source code and exact case-sensitive commands remain in the repository.</p>
<script>const screens=__A1_SCREENS__,books=__A1_BOOKS__;let page=0;const book=document.getElementById('book'),screen=document.getElementById('screen');
function show(){const rows=screens[book.value];page=Math.max(0,Math.min(page,rows.length-1));screen.textContent=rows[page];document.getElementById('count').textContent=(page+1)+' / '+rows.length;document.getElementById('previous').disabled=page===0;document.getElementById('next').disabled=page===rows.length-1;document.getElementById('answer').disabled=books.find(b=>b.name===book.value).answer_page===null;}
book.onchange=()=>{page=0;show()};document.getElementById('previous').onclick=()=>{page--;show()};document.getElementById('next').onclick=()=>{page++;show()};document.getElementById('answer').onclick=()=>{const b=books.find(b=>b.name===book.value);if(b.answer_page!==null)page=b.answer_page;show()};
document.addEventListener('keydown',e=>{if(e.target===book)return;const id={n:'next',p:'previous',a:'answer'}[e.key.toLowerCase()];if(id){e.preventDefault();document.getElementById(id).click()}});show();</script></html>"""
    document = document.replace("__A1_OPTIONS__", options).replace("__A1_SCREENS__", data).replace("__A1_BOOKS__", books)
    (output / "index.html").write_text(document)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    render(args.build, args.out)
    print("Rendered actual reader observations; offline preview at", args.out / "index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
