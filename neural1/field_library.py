"""Source-grounded Field Library assistance; curriculum and execution remain authoritative."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

from tools.apple1_emulator import Apple1RamHarness, EmulatorResult

from .assembler import LessonAssembler, trace_records
from .models import ModelProvider

OPERATIONS = {"ASK", "HINT", "EXPLAIN", "SIMPLER", "DEEPER", "SOURCE", "CHECK", "TRACE", "COMPARE", "CHALLENGE"}
PROMPT_BYTES = 3000
QUESTION_BYTES = 512

UNSUPPORTED = "NOT ESTABLISHED BY THE AVAILABLE LIBRARY SOURCES."


@dataclass(frozen=True)
class GroundedAnswer:
    operation: str
    text: str
    source_paths: tuple[str, ...]
    deterministic_evidence: dict[str, object] | None = None
    source_keys: tuple[str, ...] = ()
    grounded: bool = True
    support_note: str | None = None
    prompt_bytes: int = 0
    output_truncated: bool = False


class LessonCorpus:
    def __init__(self, root: str | Path = "docs/field-library") -> None:
        self.root = Path(root)

    def context(self, lesson_id: str, *, include_answers: bool = False) -> tuple[str, tuple[str, ...]]:
        if not re.fullmatch(r"[A-Za-z][0-9]{2}(?:-[a-z0-9-]+)?", lesson_id):
            raise ValueError("invalid lesson ID")
        exact = self.root / lesson_id
        matches = [exact] if exact.is_dir() else sorted(self.root.glob(f"{lesson_id}-*"))
        if len(matches) != 1:
            raise ValueError("lesson ID does not resolve uniquely")
        names = ["README.md", "SOURCE-NOTES.md", "STATUS.md", "ACTIVITY.md"]
        if include_answers:
            names.append("ANSWERS.md")
        paths = tuple(str(matches[0] / name) for name in names if (matches[0] / name).exists())
        return "\n\n".join(Path(path).read_text(encoding="utf-8") for path in paths), paths

    def excerpts(self, lesson_id: str, query: str, *, budget: int, include_answers: bool = False) -> tuple[str, tuple[str, ...]]:
        """Select verbatim paragraphs deterministically; never supply answer keys outside CHECK."""
        _, paths = self.context(lesson_id, include_answers=include_answers)
        ignored = {'THE', 'AND', 'FOR', 'WITH', 'DOES', 'WHAT', 'HOW', 'CAN', 'THIS', 'THAT', 'ONLY', 'EXPLAIN', 'FROM', 'ARE'}
        aliases = {word: 'CHANGE' for word in ('DEPOSIT', 'DEPOSITS', 'DEPOSITING', 'STORE', 'STORES', 'STORING', 'WRITE', 'WRITES', 'WRITING', 'CHANGE', 'CHANGES', 'CHANGING')}
        aliases.update({word: 'INSPECT' for word in ('INSPECT', 'INSPECTS', 'INSPECTING', 'EXAMINE', 'EXAMINES', 'EXAMINING', 'READ', 'READS', 'READING', 'SHOW', 'SHOWS', 'SHOWING')})

        def terms(text: str) -> set[str]:
            result = set()
            for word in re.findall(r'[A-Z0-9$-]{3,}', text.upper()):
                if word in ignored:
                    continue
                if word in aliases:
                    result.add(aliases[word])
                elif len(word) > 4 and word.endswith('S'):
                    result.add(word[:-1])
                else:
                    result.add(word)
            return result

        query_terms = terms(query)
        if query_terms & {'CHANGE', 'INSPECT'}:
            query_terms -= {'MONITOR', 'WOZ', 'COMMAND'}
        candidates = []
        for path in paths:
            filename = Path(path).name
            paragraphs = re.split(r'\n\s*\n', Path(path).read_text(encoding='utf-8'))
            # Citation tables contribute relevant original rows, never whole unrelated tables.
            blocks = [line for paragraph in paragraphs for line in (paragraph.splitlines() if paragraph.lstrip().startswith('|') else [paragraph])]
            for index, paragraph in enumerate(blocks):
                paragraph = paragraph.strip()
                if not paragraph or paragraph.startswith('#') or paragraph.count('?') > 1:
                    continue
                overlap = terms(paragraph) & query_terms
                score = len(overlap) + 4 * len(overlap & {'CHANGE', 'INSPECT'})
                if not score:
                    continue
                priority = 0 if filename == 'README.md' else 1 if filename == 'SOURCE-NOTES.md' else 2 if filename == 'STATUS.md' else 3
                if include_answers and filename == 'ANSWERS.md':
                    priority = -1
                candidates.append((priority, -score, path, index, paragraph))
        candidates.sort()
        selected: list[str] = []
        selected_paths: list[str] = []
        citation_candidates = [item for item in candidates if Path(item[2]).name == 'SOURCE-NOTES.md']
        citation_budget = min(450, budget // 4) if citation_candidates else 0
        primary_budget = budget - citation_budget
        # Reserve a small citation allowance rather than letting metadata displace teaching.
        ordered = [item for item in candidates if item not in citation_candidates] + citation_candidates
        for _, _, path, _, paragraph in ordered:
            block = f'[{Path(path).name}]\n{paragraph}'
            proposed = '\n\n'.join([*selected, block])
            limit = budget if Path(path).name == 'SOURCE-NOTES.md' else primary_budget
            if len(proposed.encode('utf-8')) > limit:
                continue
            selected.append(block)
            if path not in selected_paths:
                selected_paths.append(path)
        return '\n\n'.join(selected), tuple(selected_paths)

    def search(self, query: str, *, limit: int = 5) -> tuple[str, ...]:
        terms = {term for term in re.findall(r"[A-Z0-9$-]+", query.upper()) if len(term) > 2}
        scored = []
        for path in sorted(self.root.rglob("*.md")):
            if path.name == "ANSWERS.md":
                continue
            text = path.read_text(encoding="utf-8", errors="replace").upper()
            score = sum(text.count(term) for term in terms)
            if score:
                scored.append((-score, str(path)))
        return tuple(path for _, path in sorted(scored)[:limit])

    @staticmethod
    def source_keys(text: str) -> tuple[str, ...]:
        keys = set(re.findall(r"\b(?:[A-Z]-[A-Z0-9-]+|OWAD|BRIEL|REPO|RUN|WOZ-FWD)\b", text))
        return tuple(sorted(keys))


class FieldLibraryAssistant:
    def __init__(self, corpus: LessonCorpus, model: ModelProvider) -> None:
        self.corpus = corpus
        self.model = model

    def _answer(self, operation: str, lesson_id: str, question: str, *, seed: int, agent_id: str, evidence: dict[str, object] | None = None) -> GroundedAnswer:
        if not question.strip() or len(question.encode('utf-8')) > QUESTION_BYTES:
            return GroundedAnswer(operation, UNSUPPORTED, (), evidence, grounded=False, support_note='Question is empty or exceeds the bounded 512-byte question limit.')
        supplied_evidence = dict(evidence) if evidence is not None else None
        if supplied_evidence is not None and 'trace' in supplied_evidence:
            trace = supplied_evidence.pop('trace')
            encoded = json.dumps(trace, sort_keys=True).encode('utf-8')
            supplied_evidence['trace_detail'] = {'omitted_from_model_prompt': True, 'sha256': hashlib.sha256(encoded).hexdigest(), 'full_trace_retained_in_deterministic_evidence': True}
        evidence_text = '' if supplied_evidence is None else '\nDETERMINISTIC EVIDENCE (authoritative):\n' + json.dumps(supplied_evidence, ensure_ascii=False, separators=(',', ':'))
        actions = {'ASK': 'Answer the question directly.', 'HINT': 'Give one small helpful hint without a full solution.', 'EXPLAIN': 'Briefly explain the requested concept.', 'CHECK': 'Evaluate the statement against the supplied facts and answer evidence.', 'TRACE': 'Explain the supplied deterministic execution evidence.'}
        action = actions.get(operation, 'Help with the requested lesson operation.')
        policy = f'Use only the supplied source facts and deterministic evidence. Never infer omitted trace details. Answer when the facts are present; only when the needed facts are absent, respond exactly: {UNSUPPORTED}'
        prefix = f'POLICY: {policy}{evidence_text}\nSOURCES (selected verbatim paragraphs, not the whole lesson):\n'
        suffix = f'\nOPERATION: {operation}. {action}\nQUESTION: {question}\nRespond in 1–3 short sentences.'
        available = PROMPT_BYTES - len((prefix + suffix).encode('utf-8'))
        if available < 400:
            return GroundedAnswer(operation, UNSUPPORTED, (), evidence, grounded=False, support_note='Exact deterministic evidence exceeds the bounded prompt budget; evidence retained without model interpretation.')
        context, paths = self.corpus.excerpts(lesson_id, question, budget=min(2200, available), include_answers=operation == 'CHECK')
        if not context:
            return GroundedAnswer(operation, UNSUPPORTED, paths, evidence, grounded=False, support_note='No relevant complete source paragraph fits the bounded prompt.')
        prompt = prefix + context + suffix
        assert len(prompt.encode('utf-8')) <= PROMPT_BYTES
        response = self.model.generate(prompt, agent_id=agent_id, seed=seed)
        text = response.text.strip() or UNSUPPORTED
        keys = self.corpus.source_keys(context)
        if text != UNSUPPORTED and keys:
            text += '\n\nSOURCES: ' + ', '.join(keys)
        truncated = (response.provider_metadata or {}).get('done_reason') == 'length'
        note = 'Model output reached its length limit; the returned text is incomplete.' if truncated else None
        return GroundedAnswer(operation, text, paths, evidence, keys, text != UNSUPPORTED, support_note=note, prompt_bytes=len(prompt.encode('utf-8')), output_truncated=truncated)

    def answer(self, operation: str, lesson_id: str, question: str, *, seed: int = 0) -> GroundedAnswer:
        operation = operation.upper()
        if operation not in OPERATIONS:
            raise ValueError('unsupported Field Library operation')
        return self._answer(operation, lesson_id, question, seed=seed, agent_id='FIELD-LIBRARY')

    def explain_program(self, lesson_id: str, program: str | Path, keyboard_input: str, *, seed: int = 0) -> GroundedAnswer:
        result: EmulatorResult = Apple1RamHarness.from_program_file(program).run_keyboard_line(keyboard_input)
        evidence = {"screen_text": result.screen_text, "buffer_text": result.buffer_text, "returned_to_monitor": result.returned_to_monitor, "instructions": result.instructions}
        return self._answer('TRACE', lesson_id, 'Explain the deterministic program output, memory buffer and return to Monitor.', seed=seed, agent_id='FIELD-LIBRARY-CODE', evidence=evidence)

    def assemble_explain(self, lesson_id: str, source: str, *, origin: int = 0x0200, seed: int = 0) -> GroundedAnswer:
        assembled, execution = LessonAssembler().assemble_and_run(source, origin=origin)
        evidence: dict[str, object] = {"origin": origin, "bytes": assembled.payload.hex(" ").upper(), "symbols": assembled.symbols, "diagnostics": [diagnostic.__dict__ for diagnostic in assembled.diagnostics]}
        if execution is not None:
            evidence.update({"stop_reason": execution.stop_reason, "screen_text": execution.screen_text, "instructions": execution.instructions, "trace": trace_records(execution)})
        return self._answer('TRACE', lesson_id, 'Explain the deterministic assembly bytes, screen output, instructions and return to Monitor.', seed=seed, agent_id='FIELD-LIBRARY-ASSEMBLER', evidence=evidence)
