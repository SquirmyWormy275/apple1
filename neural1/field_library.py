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
        terms = set(re.findall(r'[A-Z0-9$-]{3,}', query.upper())) - ignored
        candidates = []
        for path in paths:
            for index, paragraph in enumerate(re.split(r'\n\s*\n', Path(path).read_text(encoding='utf-8'))):
                paragraph = paragraph.strip()
                if not paragraph:
                    continue
                score = sum(min(paragraph.upper().count(term), 3) for term in terms)
                if score:
                    candidates.append((score, path, index, paragraph))
        candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
        if include_answers:
            # Reserve the best matching actual answer paragraph before general sources.
            answer = next((item for item in candidates if Path(item[1]).name == 'ANSWERS.md'), None)
            if answer:
                candidates.remove(answer)
                candidates.insert(0, answer)
        selected: list[str] = []
        selected_paths: list[str] = []
        for _, path, _, paragraph in candidates:
            block = f'[{Path(path).name}]\n{paragraph}'
            proposed = '\n\n'.join([*selected, block])
            if len(proposed.encode('utf-8')) > budget:
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
        prefix = f'OPERATION: {operation}\nQUESTION:\n{question}{evidence_text}\nSOURCES (selected verbatim paragraphs, not the whole lesson):\n'
        suffix = f'\nUse only these SOURCES and supplied deterministic evidence. Never infer omitted trace details. If unsupported, answer exactly: {UNSUPPORTED}'
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
        return GroundedAnswer(operation, text, paths, evidence, keys, text != UNSUPPORTED, prompt_bytes=len(prompt.encode('utf-8')))

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
