"""The console advertises only lessons the actual corpus can resolve."""
from pathlib import Path
from types import SimpleNamespace

from neural1.application import Application
from neural1.field_library import LessonCorpus


ROOT = Path(__file__).resolve().parents[1]


def test_special_lesson_resolves_by_short_and_full_identifiers():
    corpus = LessonCorpus(ROOT / 'docs/field-library')
    short = corpus.context('SP01')
    full = corpus.context('SP01-two-boards-one-computer')
    assert short == full
    assert short[0] and any(path.endswith('/SP01-two-boards-one-computer/README.md') for path in short[1])


def test_console_list_contains_only_resolvable_lessons():
    app = Application.__new__(Application)
    app.config = SimpleNamespace(checkout=ROOT, storage_check=lambda: None)
    names = app.command('LESSONS')
    corpus = LessonCorpus(ROOT / 'docs/field-library')
    assert 'SP01-two-boards-one-computer' in names
    assert not {'program-annotations', 'teacher-materials', 'visitor-mode'} & set(names)
    for name in names:
        text, paths = corpus.context(name)
        assert text and paths
    for name in ('program-annotations', 'teacher-materials', 'visitor-mode'):
        assert (corpus.root / name / 'README.md').is_file()  # Existing ancillary content is preserved.
