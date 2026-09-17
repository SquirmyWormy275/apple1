"""Bounded transcript pages preserve all actual chronological records."""
import json
from types import SimpleNamespace

import pytest

from neural1.application import Application
from neural1.core import Neural1Error


@pytest.fixture
def transcript_app(tmp_path):
    root = tmp_path / 'campaigns/N1-P-PAGINATION'
    path = root / 'cells/CELL/transcript.jsonl'
    path.parent.mkdir(parents=True)
    records = [{'generation': generation, 'agent_id': 'A', 'response': f'turn {generation}'} for generation in range(18)]
    path.write_text(''.join(json.dumps(row) + '\n' for row in records))
    app = Application.__new__(Application)
    app.config = SimpleNamespace(storage_check=lambda: None, output=tmp_path)
    return app, path, records


def test_explicit_pages_cover_all_eighteen_records_and_default_stays_latest_twelve(transcript_app):
    app, path, records = transcript_app
    original = path.read_bytes()
    first = app.command('TRANSCRIPT N1-P-PAGINATION 0')
    second = app.command('TRANSCRIPT N1-P-PAGINATION 1')
    key = 'cells/CELL/transcript.jsonl'
    assert first['page'] == 0 and second['page'] == 1
    assert first['page_size'] == second['page_size'] == 12
    assert first['total_records'] == second['total_records'] == {key: 18}
    assert first['transcripts'][key] == records[:12]
    assert second['transcripts'][key] == records[12:]
    assert first['transcripts'][key] + second['transcripts'][key] == records
    assert app.command('TRANSCRIPT N1-P-PAGINATION') == {key: records[-12:]}
    assert path.read_bytes() == original


@pytest.mark.parametrize('page', ['-1', 'invalid', '1.5', '2'])
def test_bad_or_unavailable_page_has_clear_error(transcript_app, page):
    app, _, _ = transcript_app
    with pytest.raises(Neural1Error, match='nonnegative integer|out of range'):
        app.command('TRANSCRIPT N1-P-PAGINATION ' + page)
