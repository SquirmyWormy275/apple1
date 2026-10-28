from pathlib import Path
from tempfile import TemporaryDirectory

from neural1.core import Neural1Error
from neural1.models import FakeProvider, RecordingProvider

with TemporaryDirectory() as d:
    provider = RecordingProvider(FakeProvider(default="0300: 2A"), Path(d) / "record.jsonl")
    actual = provider.generate("INSPECT", agent_id="A", seed=7)
    replay = RecordingProvider.load_replay(Path(d) / "record.jsonl")
    assert replay.generate("INSPECT", agent_id="A", seed=7) == actual
    print("Exact replay:", actual.text)
    try:
        replay.generate("OTHER PROMPT", agent_id="A", seed=7)
        raise AssertionError("missing replay must fail")
    except Neural1Error:
        print("Changed prompt: refused")
