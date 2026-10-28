from neural1.history import research_status
from tools.textbook_support import ROOT, emit

status = research_status(ROOT / "data/neural1/history/1976-research-index.json")
emit(status)
assert isinstance(status, dict)
