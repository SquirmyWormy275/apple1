import json

from tools.textbook_native import evaluate, verify
from tools.textbook_support import ROOT

for name in ("generate", "chat", "pi-phi4"):
    directory = ROOT / "docs/textbook/native/evidence" / name
    receipt = verify(directory)
    print("RETAINED REAL INFERENCE; this lab re-evaluates records without contacting a model.")
    print("Record:", name, "runtime:", receipt["runtime"]["version"], "model:", receipt["model"]["name"])
    print("Target:", receipt["target"])
    control = json.loads((directory / "health-control.json").read_text())
    print("Recorded arithmetic control:", repr(control["generation"]["text"]), "passed:", control["passed"])
    for label in receipt["trials"]:
        trial = json.loads((directory / f"{label}.json").read_text())
        result = trial["evaluation"]
        print(label, "task passed:", result["passed"], "accepted commands:", len(result["commands"]))
        print("Finish reason:", trial["generation"]["provider_metadata"]["done_reason"])
        assert result["passed"] is False
positive = "0300: A0 00 A9 2A 99 00 04 C8 C0 05 D0 F8 4C 1F FF\n0300R"
assert evaluate(positive)["passed"]
assert not evaluate(positive.replace("C0 05", "C0 06"))["passed"]
print("Authored positive passes; authored six-byte boundary violation fails the same task.")
print("Passing this lab verifies the recorded negative finding, not model success.")
