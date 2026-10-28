"""Reproduce the structural part of the 42-packet host reading review.

These checks locate evidence and answer coverage. They do not certify historical
truth, rights clearance or a learner's understanding. Editorial findings and
the local-scan comparison ledger are retained beside the generated record.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ("README.md", "ACTIVITY.md", "ANSWERS.md", "SOURCE-NOTES.md", "STATUS.md")
SPECIAL_ANSWERS = {
    "S03": {"D": "The activity itself supplies the landmark table; check recall both ways."},
    "C03": {"G": "Optional coin drill: compare the chosen byte with its place-value sum."},
    "A06": {letter: "Worked design card and numbered acceptance criteria cover this part." for letter in "ABCDEF"},
    "X03": {"A": "Worked three-minute script includes the fallback; remaining sections give criteria."},
}


def review_packets() -> dict:
    pool_path = ROOT / "docs/field-library/SOURCES.md"
    pool = pool_path.read_text()
    known = set(re.findall(r"^\| ([A-Z][A-Z0-9-]+) \|", pool, re.MULTILINE))
    records = []
    catalog = json.loads((ROOT / "docs/textbook/catalog.json").read_text())
    for lesson in (r for r in catalog if r.get("lesson")):
        identifier = lesson["id"]
        folder = ROOT / lesson["lesson"]
        text = {name: (folder / name).read_text() for name in FIELDS}
        readme = text["README.md"]
        match = re.search(r"## Activity\n(.*?)(?=\n## )", readme, re.DOTALL)
        if match is None or not re.search(r"^\d+\.", match[1], re.MULTILINE):
            match = re.search(r"## First result\n(.*?)(?=\n## )", readme, re.DOTALL)
        actions = len(re.findall(r"^\d+\.", match[1], re.MULTILINE)) if match else 0
        if not 1 <= actions <= 3:
            raise ValueError(f"{identifier}: first-result action count {actions}")
        keys = set(re.findall(r"\b[HMPRAWB]-[A-Z][A-Z0-9-]+\b", text["SOURCE-NOTES.md"]))
        if keys - known:
            raise ValueError(f"{identifier}: unknown source keys {keys - known}")
        parts = set(re.findall(r"^## Part ([A-Z])", text["ACTIVITY.md"], re.MULTILINE))
        answered = set(re.findall(r"Part ([A-Z])", text["ANSWERS.md"]))
        exceptions = SPECIAL_ANSWERS.get(identifier, {})
        if parts - answered - exceptions.keys():
            raise ValueError(f"{identifier}: activity parts without answer/criteria mapping")
        for section in ("You will learn", "First result", "What you need", "Sources and boundaries"):
            if "## " + section not in readme:
                raise ValueError(f"{identifier}: missing {section}")
        paths = [folder / name for name in FIELDS]
        paths.extend(p for p in sorted((folder / "assets").rglob("*")) if p.is_file())
        if identifier == "SP01":
            paths.extend(sorted((folder / "card").rglob("*.txt")))
        records.append({
            "id": identifier, "disposition": "host-reading-candidate; physical acceptance pending",
            "first_result_actions": actions, "activity_parts": sorted(parts), "answer_parts": sorted(answered),
            "answer_mapping_notes": exceptions, "shared_source_keys": sorted(keys),
            "evidence_lab": identifier, "card_book": identifier, "mode": "OFF-DEVICE",
            "source_qualification": "citations resolve; local-scan ledger and editorial findings are separate; no authentication/rights clearance",
            "input_sha256": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
        })
    if len(records) != 42:
        raise ValueError("review must include exactly all 42 original packets")
    return {"schema_version": 1, "scope": "structural review plus separately recorded targeted editorial/source-location checks",
            "source_pool_sha256": hashlib.sha256(pool_path.read_bytes()).hexdigest(), "records": records,
            "does_not_establish": ["every historical claim independently corroborated", "rights clearance", "physical acceptance", "learner comprehension"]}
