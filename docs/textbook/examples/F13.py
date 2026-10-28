from neural1.field_library import FieldLibraryAssistant, LessonCorpus
from neural1.models import FakeProvider
from tools.textbook_support import ROOT

corpus = LessonCorpus(ROOT / "docs/field-library")
text, paths = corpus.context("M03")
print("Lesson folders:", len(corpus.lessons()))
print("SOURCE documents:", len(paths), "nonempty:", bool(text))
assistant = FieldLibraryAssistant(corpus, FakeProvider(default="DETERMINISTIC EXPLANATION FROM RECORDED RESULT."))
for op in ("ASK", "HINT", "EXPLAIN", "CHECK"):
    result = assistant.answer(op, "M03", "What is the recorded screen output?")
    print(op, "prompt bytes:", result.prompt_bytes, "sources:", len(result.source_paths))
result = assistant.assemble_explain("A01", "LDA #$41\nJSR $FFEF\nJMP $FF1F")
print("TRACE has deterministic evidence:", result.deterministic_evidence is not None)
assert len(corpus.lessons()) == 42 and result.deterministic_evidence is not None
