"""User-facing behavior using synthetic applications; no physical transport."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from neural1 import application, cli
from neural1.application import Application, ApplicationConfig
from neural1.console_ui import parse_command, render_result
from neural1.core import Neural1Error


@pytest.mark.parametrize('line', [
    'START --help', 'START extra', '1 extra', 'MODELS extra', 'STATUS extra',
    'RUNS extra', 'LESSONS extra', 'MODEL', 'STOP', 'RESUME', 'SHOW', 'EXPORT',
    'OPEN', 'META typo', 'META CLAIM', 'META QUEUE extra',
    'SELFHOST INGEST', 'SELFHOST LIST extra', 'SOURCE S01 typo',
    'ASK S01', 'ASK S01 ""', 'TRACE S01', 'QUIT extra', 'HELP START extra',
])
def test_invalid_commands_do_not_touch_storage_or_execute(line):
    app = Application.__new__(Application)
    app.config = Mock()
    app.start = Mock()
    app.cancel = Mock()
    with pytest.raises(Neural1Error, match='Usage:'):
        app.command(line)
    app.config.storage_check.assert_not_called()
    app.start.assert_not_called()
    app.cancel.assert_not_called()


def test_help_and_typo_recovery_work_without_storage():
    app = Application.__new__(Application)
    app.config = Mock()
    assert 'Takes no arguments' in app.command('HELP START')
    assert 'HELP command' in app.command('?')
    with pytest.raises(Neural1Error, match='Did you mean START'):
        app.command('STATR')
    with pytest.raises(Neural1Error, match='quotation mark'):
        app.command('ASK S01 "unfinished')
    with pytest.raises(Neural1Error, match='trailing backslash'):
        app.command('ASK S01 unfinished' + '\\')
    app.config.storage_check.assert_not_called()


def test_source_accepts_short_and_legacy_form_without_model(tmp_path, monkeypatch):
    from neural1.field_library import LessonCorpus

    app = Application.__new__(Application)
    app.config = Mock(checkout=tmp_path)
    context = Mock(return_value=('Lesson text', ('source.md',)))
    monkeypatch.setattr(LessonCorpus, 'context', context)
    model = Mock(side_effect=AssertionError('SOURCE must not call a model'))
    monkeypatch.setattr(application, 'check_model', model)
    assert app.command('SOURCE S01') == app.command('SOURCE S01 sources')
    assert app.command('SOURCE S01')['text'] == 'Lesson text'
    model.assert_not_called()


def test_readable_output_preserves_ids_paths_and_negative_results():
    identifier = 'N1-P-' + 'A' * 64
    path = '/a/very/long/path/' + 'b' * 64
    result = render_result({'campaign_id': identifier, 'path': path, 'passed': False, 'records': [], 'text': 'line one\nline two'}, width=40)
    assert identifier in result and path in result
    assert 'Passed: No' in result
    assert 'Records:\n  (none)' in result
    assert 'line one\nline two' in result
    assert '"campaign_id"' not in result


def test_readable_recorded_output_does_not_send_terminal_controls():
    result = render_result({'text': '\x1b[2JHI\r\x9b31m', 'price': None})
    assert '\x1b' not in result and '\r' not in result and '\x9b' not in result
    assert r'\x1b[2JHI\r\x9b31m' in result
    assert 'Price: null' in result


@pytest.mark.parametrize('options', [[], ['--retro'], ['--json']])
def test_interactive_output_and_quit_validation(tmp_path, monkeypatch, capsys, options):
    config_path = tmp_path / 'config.json'
    config_path.write_text('{}')
    config = Mock()
    monkeypatch.setattr(ApplicationConfig, 'load', Mock(return_value=config))
    app = Application.__new__(Application)
    app.config = config
    app.family = '4k-mind'
    app.model_id = 'fixture'
    app.preference_warning = None
    app.start = Mock(return_value='N1-P-' + 'A' * 64)
    monkeypatch.setattr(application, 'Application', Mock(return_value=app))
    inputs = iter(['HELP START', 'START extra', 'START', 'QUIT extra', 'QUIT'])
    monkeypatch.setattr('builtins.input', lambda prompt: next(inputs))
    assert application.main(['--config', str(config_path), *options]) == 0
    output = capsys.readouterr().out
    app.start.assert_called_once_with()
    assert 'Usage: START' in output and 'Usage: QUIT' in output
    assert 'N1-P-' + 'A' * 64 in output
    assert 'active runs continue' in output
    assert ('"started":' in output) == ('--json' in options)


def test_one_shot_console_keeps_json(tmp_path, monkeypatch, capsys):
    config_path = tmp_path / 'config.json'
    config_path.write_text('{}')
    monkeypatch.setattr(ApplicationConfig, 'load', Mock(return_value=Mock()))
    app = Mock(preference_warning=None)
    app.command.return_value = {'passed': False, 'id': 'N1-P-example'}
    monkeypatch.setattr(application, 'Application', Mock(return_value=app))
    assert application.main(['--config', str(config_path), '--command', 'STATUS']) == 0
    assert json.loads(capsys.readouterr().out) == app.command.return_value
    app.command.return_value = None
    assert application.main(['--config', str(config_path), '--command', '']) == 0
    assert json.loads(capsys.readouterr().out) is None


def test_missing_deployment_has_actionable_message_and_creates_nothing(tmp_path, capsys):
    config = tmp_path / 'missing.json'
    assert application.main(['--config', str(config)]) == 2
    error = capsys.readouterr().err
    assert 'python -m neural1.demos' in error
    assert '--config PATH' in error and str(config) in error
    assert 'Traceback' not in error
    assert list(tmp_path.iterdir()) == []


@pytest.mark.parametrize('contents', ['[]', '{}', '{"ssd": 42}'])
def test_malformed_config_has_friendly_error(tmp_path, capsys, contents):
    config = tmp_path / 'config.json'
    config.write_text(contents)
    assert application.main(['--config', str(config)]) == 2
    assert 'config requires' in capsys.readouterr().err


@pytest.mark.parametrize('contents', [None, '{bad json'])
def test_developer_cli_reports_input_errors(tmp_path, capsys, contents):
    spec = tmp_path / 'campaign.json'
    if contents is not None:
        spec.write_text(contents)
    assert cli.main(['validate-campaign', str(spec), 'unused-registry.json']) == 2
    captured = capsys.readouterr()
    assert captured.out == ''
    assert 'Traceback' not in captured.err
    assert ('File or directory not found' if contents is None else 'Invalid JSON at line') in captured.err


@pytest.mark.parametrize('arguments', [
    ['--debug', 'validate-campaign'], ['validate-campaign', '--debug'],
])
def test_developer_cli_debug_preserves_exception(tmp_path, arguments):
    with pytest.raises(FileNotFoundError):
        cli.main([*arguments, str(tmp_path / 'missing.json'), 'unused-registry.json'])


def test_console_debug_dispatch_and_exit_aliases(monkeypatch):
    main = Mock(return_value=0)
    monkeypatch.setattr(application, 'main', main)
    assert cli.main(['--debug', 'console', '--retro']) == 0
    main.assert_called_once_with(['--retro', '--debug'])
    assert parse_command('exit') == ['QUIT']
    assert parse_command('0') == ['QUIT']


def test_developer_cli_success_keeps_json(tmp_path, capsys):
    checkout = Path(__file__).resolve().parents[1]
    assert cli.main(['validate-campaign', str(checkout / 'configs/neural1/pilot-001/campaign.json'), str(checkout / 'configs/neural1/pilot-001/model-registry.template.json')]) == 0
    assert json.loads(capsys.readouterr().out)['valid'] is True
