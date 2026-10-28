from neural1.application import preset
from neural1.console_ui import render_result

for family in ("4k-mind", "1976-multiverse", "selfhost1", "256-byte-universe", "ram-republic"):
    spec = preset(family, "fixture", seed=7)
    print(family, "generations=", spec.generations, "tokens=", spec.max_tokens)
text = render_result({"campaign_id": "N1-P-" + "A" * 64, "passed": False}, width=40)
print(text)
assert "N1-P-" + "A" * 64 in text and "Passed: No" in text
