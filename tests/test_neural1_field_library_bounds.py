"""Deterministic retrieval and prompt bounds; synthetic provider only."""
from neural1.field_library import PROMPT_BYTES, UNSUPPORTED, FieldLibraryAssistant, LessonCorpus
from neural1.models import GenerationResult


class Capture:
    def __init__(self):
        self.prompts = []

    def generate(self, prompt, **kwargs):
        self.prompts.append(prompt)
        return GenerationResult('BOUNDED SYNTHETIC EXPLANATION')


def corpus(tmp_path):
    lesson = tmp_path / 'M01-fixture'
    lesson.mkdir()
    (lesson / 'README.md').write_text('Irrelevant filler.\n\n' * 300 + 'Deposit changes memory bytes. REPO\n\nExamine displays memory bytes without changing them.')
    (lesson / 'ANSWERS.md').write_text('ANSWER-ONLY: Examine does not change memory bytes. REPO')
    return LessonCorpus(tmp_path)


def test_relevant_verbatim_excerpt_and_total_prompt_bound(tmp_path):
    source = corpus(tmp_path)
    provider = Capture()
    answer = FieldLibraryAssistant(source, provider).answer('ASK', 'M01', 'Does deposit change memory bytes?')
    assert 'Deposit changes memory bytes. REPO' in provider.prompts[0]
    assert 'Irrelevant filler' not in provider.prompts[0]
    assert 'ANSWER-ONLY' not in provider.prompts[0]
    assert answer.source_paths and answer.source_keys == ('REPO',)
    assert len(provider.prompts[0].encode()) <= PROMPT_BYTES
    full, _ = source.context('M01')
    assert 'Irrelevant filler' in full  # SOURCE full-corpus access is unchanged.


def test_check_includes_relevant_actual_answers(tmp_path):
    provider = Capture()
    answer = FieldLibraryAssistant(corpus(tmp_path), provider).answer('CHECK', 'M01', 'Does examine change memory bytes?')
    assert 'ANSWER-ONLY' in provider.prompts[0]
    assert any(path.endswith('ANSWERS.md') for path in answer.source_paths)


def test_oversized_multibyte_question_refuses_without_provider(tmp_path):
    provider = Capture()
    result = FieldLibraryAssistant(corpus(tmp_path), provider).answer('ASK', 'M01', 'é' * 257)
    assert not provider.prompts and result.text == UNSUPPORTED and not result.grounded
    assert '512-byte' in result.support_note


def test_unmatched_support_refuses_without_provider(tmp_path):
    provider = Capture()
    result = FieldLibraryAssistant(corpus(tmp_path), provider).answer('ASK', 'M01', 'Quantum entanglement?')
    assert not provider.prompts and result.text == UNSUPPORTED


def test_large_trace_is_explicitly_omitted_but_full_evidence_retained(tmp_path):
    provider = Capture()
    evidence = {'screen_text': 'A', 'stop_reason': 'MONITOR_WARM_ENTRY', 'instructions': 500, 'trace': [{'instruction': 'NOP'}] * 500}
    result = FieldLibraryAssistant(corpus(tmp_path), provider)._answer('TRACE', 'M01', 'Explain memory bytes.', seed=0, agent_id='SYNTHETIC', evidence=evidence)
    assert result.deterministic_evidence == evidence
    assert '"screen_text":"A"' in provider.prompts[0]
    assert '"omitted_from_model_prompt":true' in provider.prompts[0]
    assert 'NOP' not in provider.prompts[0]
    assert len(provider.prompts[0].encode()) <= PROMPT_BYTES


def test_oversized_authoritative_evidence_is_not_silently_truncated(tmp_path):
    provider = Capture()
    evidence = {'screen_text': 'A' * 4000}
    result = FieldLibraryAssistant(corpus(tmp_path), provider)._answer('TRACE', 'M01', 'Explain memory bytes.', seed=0, agent_id='SYNTHETIC', evidence=evidence)
    assert result.text == UNSUPPORTED and not provider.prompts
    assert result.deterministic_evidence == evidence and not result.grounded
