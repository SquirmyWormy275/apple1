import hashlib
import json

from neural1.field_library import FieldLibraryAssistant, LessonCorpus
from neural1.models import RecordingProvider
from neural1.world import VirtualApple1World
from tools.textbook_support import ROOT

directory = ROOT / "docs/textbook/native/evidence/pi-console"
manifest = json.loads((directory / "manifest.json").read_text())
for name, expected in manifest["files_sha256"].items():
    assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected
print("Actual installed Pi revision:", manifest["installed_revision"])
print("This lab reads retained console output; no fresh inference is requested.")
for name in ("ask", "hint", "explain", "check", "trace"):
    record = json.loads((directory / f"{name}.json").read_text())
    assert record["exit_code"] == 0 and record["serial_opened"] is False
    result = json.loads(record["stdout"])
    print(name.upper(), "| grounded flag:", result["grounded"])
    print(result["text"].split("\n\nSOURCES:")[0])
trace = json.loads(json.loads((directory / "trace.json").read_text())["stdout"])["deterministic_evidence"]
world = VirtualApple1World()
world.host_write(trace["origin"], bytes.fromhex(trace["bytes"]))
rerun = world.execute(trace["origin"], max_instructions=20)
assert rerun.stop_reason == trace["stop_reason"] == "MONITOR_WARM_ENTRY"
assert rerun.instructions == trace["instructions"] == 3
assert world.host_read(0x400) == b"\x2A"
print("Fresh host re-evaluation of recorded bytes: $0400=2A; 3 instructions; Monitor return.")
print("Review finding: ASK falsely abstained despite available facts; grounded=True is not a fact-check.")
current = ROOT / "docs/textbook/native/evidence/pi-tutor-current"
retained = json.loads((current / "result.json").read_text())
for name, expected in json.loads((current / "manifest.json").read_text())["files_sha256"].items():
    assert hashlib.sha256((current / name).read_bytes()).hexdigest() == expected
replay = RecordingProvider.load_replay(current / "provider.jsonl")
answer = FieldLibraryAssistant(LessonCorpus(ROOT / "docs/field-library"), replay).answer("ASK", "M01", retained["question"], seed=7)
assert answer.text == retained["answer"]["text"] and answer.grounded
print("Staged revised source on real Pi; exact retained-response replay:")
print(answer.text)
print("The pinned installed application was not replaced.")
