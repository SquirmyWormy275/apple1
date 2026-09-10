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


def test_actual_m01_monitor_aliases_select_teaching_not_unrelated_citation_table():
    source = LessonCorpus()
    for question, expected in [('What does a Woz Monitor deposit command do?', '*Change.*'), ('How can I inspect a memory byte?', '*Inspect.*'), ('Explain examining and depositing memory.', '*Change.*')]:
        context, paths = source.excerpts('M01', question, budget=2200)
        assert expected in context
        if 'examining' in question:
            assert '*Inspect.*' in context
        assert '| The Altair used lights and switches |' not in context
        assert 'R-MON-SYNTAX' in context or 'R-MON-8' in context
        assert not any(path.endswith('ANSWERS.md') for path in paths)
        assert len(context.encode()) <= 2200


def test_operation_guidance_and_explicit_length_truncation(tmp_path):
    class Limited(Capture):
        def generate(self, prompt, **kwargs):
            self.prompts.append(prompt)
            return GenerationResult('The exact unfinished response', provider_metadata={'done_reason': 'length'})
    provider = Limited()
    result = FieldLibraryAssistant(corpus(tmp_path), provider).answer('HINT', 'M01', 'How can I examine memory bytes?')
    assert 'one small helpful hint' in provider.prompts[0]
    assert provider.prompts[0].endswith('Respond in 1–3 short sentences.')
    assert provider.prompts[0].index(UNSUPPORTED) < provider.prompts[0].index('SOURCES (selected')
    assert result.text.startswith('The exact unfinished response')
    assert result.output_truncated and 'incomplete' in result.support_note
    assert result.prompt_bytes <= PROMPT_BYTES
