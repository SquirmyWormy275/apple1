"""Keep the human lesson index synchronized with the runtime's actual catalog."""

import re
from pathlib import Path

from neural1.field_library import LessonCorpus

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "docs" / "field-library"


def test_library_index_lists_every_existing_lesson() -> None:
    text = (LIBRARY / "README.md").read_text(encoding="utf-8")
    indexed = re.findall(r"^\| \[[A-Z]{1,2}[0-9]{2}\]\(([^/]+)/README\.md\)", text, re.MULTILINE)
    actual = set(LessonCorpus(LIBRARY).lessons())
    assert set(indexed) == actual
    assert len(indexed) == len(actual), "lesson index contains duplicate entries"


def test_library_index_count_matches_the_actual_catalog() -> None:
    text = (LIBRARY / "README.md").read_text(encoding="utf-8")
    count = re.search(r"\b([0-9]+) lesson packets\b", text)
    assert count is not None, "state the packet count as a number in the introduction"
    assert int(count[1]) == len(LessonCorpus(LIBRARY).lessons())
