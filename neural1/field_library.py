"""Source-grounded Field Library assistance; curriculum and execution remain authoritative."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from tools.apple1_emulator import Apple1RamHarness, EmulatorResult

from .assembler import LessonAssembler, trace_records
from .models import ModelProvider

OPERATIONS = {"ASK", "HINT", "EXPLAIN", "SIMPLER", "DEEPER", "SOURCE", "CHECK", "TRACE", "COMPARE", "CHALLENGE"}
UNSUPPORTED = "NOT ESTABLISHED BY THE AVAILABLE LIBRARY SOURCES."


@dataclass(frozen=True)
class GroundedAnswer:
    operation: str
    text: str
    source_paths: tuple[str, ...]
    deterministic_evidence: dict[str, object] | None = None
    source_keys: tuple[str, ...] = ()
    grounded: bool = True


class LessonCorpus:
    def __init__(self, root: str | Path = "docs/field-library") -> None:
        self.root = Path(root)

    def context(self, lesson_id: str, *, include_answers: bool = False) -> tuple[str, tuple[str, ...]]:
        matches = sorted(self.root.glob(f"{lesson_id}-*"))
        if len(matches) != 1:
            raise ValueError("lesson ID does not resolve uniquely")
        names = ["README.md", "SOURCE-NOTES.md", "STATUS.md", "ACTIVITY.md"]
        if include_answers:
            names.append("ANSWERS.md")
        paths = tuple(str(matches[0] / name) for name in names if (matches[0] / name).exists())
        return "\n\n".join(Path(path).read_text(encoding="utf-8") for path in paths), paths

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

    def answer(self, operation: str, lesson_id: str, question: str, *, seed: int = 0) -> GroundedAnswer:
        operation = operation.upper()
        if operation not in OPERATIONS:
            raise ValueError("unsupported Field Library operation")
        context, paths = self.corpus.context(lesson_id, include_answers=operation == "CHECK")
        if not question.strip() or not context.strip():
            return GroundedAnswer(operation, UNSUPPORTED, paths, source_keys=(), grounded=False)
        prompt = f"OPERATION: {operation}\nSOURCES:\n{context}\nQUESTION:\n{question}\nUse only SOURCES. If unsupported, answer exactly: {UNSUPPORTED}"
        result = self.model.generate(prompt, agent_id="FIELD-LIBRARY", seed=seed)
        answer = result.text.strip() or UNSUPPORTED
        keys = self.corpus.source_keys(context)
        if answer != UNSUPPORTED and keys:
            answer += "\n\nSOURCES: " + ", ".join(keys)
        return GroundedAnswer(operation, answer, paths, source_keys=keys, grounded=answer != UNSUPPORTED)

    def explain_program(self, lesson_id: str, program: str | Path, keyboard_input: str, *, seed: int = 0) -> GroundedAnswer:
        result: EmulatorResult = Apple1RamHarness.from_program_file(program).run_keyboard_line(keyboard_input)
        context, paths = self.corpus.context(lesson_id)
        evidence = {"screen_text": result.screen_text, "buffer_text": result.buffer_text, "returned_to_monitor": result.returned_to_monitor, "instructions": result.instructions}
        prompt = f"Explain this deterministic emulator result using only the lesson sources.\nSOURCES:\n{context}\nRESULT:\n{evidence}"
        response = self.model.generate(prompt, agent_id="FIELD-LIBRARY-CODE", seed=seed)
        keys = self.corpus.source_keys(context)
        text = response.text.strip() or UNSUPPORTED
        if text != UNSUPPORTED and keys:
            text += "\n\nSOURCES: " + ", ".join(keys)
        return GroundedAnswer("TRACE", text, paths, evidence, keys, text != UNSUPPORTED)

    def assemble_explain(self, lesson_id: str, source: str, *, origin: int = 0x0200, seed: int = 0) -> GroundedAnswer:
        assembled, execution = LessonAssembler().assemble_and_run(source, origin=origin)
        context, paths = self.corpus.context(lesson_id)
        evidence: dict[str, object] = {"origin": origin, "bytes": assembled.payload.hex(" ").upper(), "symbols": assembled.symbols, "diagnostics": [diagnostic.__dict__ for diagnostic in assembled.diagnostics]}
        if execution is not None:
            evidence.update({"stop_reason": execution.stop_reason, "screen_text": execution.screen_text, "instructions": execution.instructions, "trace": trace_records(execution)})
        prompt = f"Explain only this deterministic assembler/emulator evidence using the lesson sources.\nSOURCES:\n{context}\nEVIDENCE:\n{evidence}"
        response = self.model.generate(prompt, agent_id="FIELD-LIBRARY-ASSEMBLER", seed=seed)
        keys = self.corpus.source_keys(context)
        text = response.text.strip() or UNSUPPORTED
        if text != UNSUPPORTED and keys:
            text += "\n\nSOURCES: " + ", ".join(keys)
        return GroundedAnswer("TRACE", text, paths, evidence, keys, text != UNSUPPORTED)
