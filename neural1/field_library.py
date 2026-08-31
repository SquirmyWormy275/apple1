"""Source-grounded Field Library assistance; curriculum and execution remain authoritative."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from tools.apple1_emulator import Apple1RamHarness, EmulatorResult

from .models import ModelProvider


OPERATIONS = {"ASK", "HINT", "EXPLAIN", "SIMPLER", "DEEPER", "SOURCE", "CHECK", "TRACE", "COMPARE", "CHALLENGE"}
UNSUPPORTED = "NOT ESTABLISHED BY THE AVAILABLE LIBRARY SOURCES."


@dataclass(frozen=True)
class GroundedAnswer:
    operation: str
    text: str
    source_paths: tuple[str, ...]
    deterministic_evidence: dict[str, object] | None = None


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
            return GroundedAnswer(operation, UNSUPPORTED, paths)
        prompt = f"OPERATION: {operation}\nSOURCES:\n{context}\nQUESTION:\n{question}\nUse only SOURCES. If unsupported, answer exactly: {UNSUPPORTED}"
        result = self.model.generate(prompt, agent_id="FIELD-LIBRARY", seed=seed)
        return GroundedAnswer(operation, result.text.strip() or UNSUPPORTED, paths)

    def explain_program(self, lesson_id: str, program: str | Path, keyboard_input: str, *, seed: int = 0) -> GroundedAnswer:
        result: EmulatorResult = Apple1RamHarness.from_program_file(program).run_keyboard_line(keyboard_input)
        context, paths = self.corpus.context(lesson_id)
        evidence = {"screen_text": result.screen_text, "buffer_text": result.buffer_text, "returned_to_monitor": result.returned_to_monitor, "instructions": result.instructions}
        prompt = f"Explain this deterministic emulator result using only the lesson sources.\nSOURCES:\n{context}\nRESULT:\n{evidence}"
        response = self.model.generate(prompt, agent_id="FIELD-LIBRARY-CODE", seed=seed)
        return GroundedAnswer("TRACE", response.text.strip() or UNSUPPORTED, paths, evidence)
