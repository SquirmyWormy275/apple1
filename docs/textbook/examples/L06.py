import json

from tools.textbook_support import ROOT

r = json.loads((ROOT / "docs/neural1/operations/evidence/pi-closeout-2026-09-10/post-boot-run.json").read_text())
print("Recorded campaign elapsed seconds:", round(r["elapsed_seconds"], 3))
print("Accepted commands:", r["family_result"]["accepted_transactions"])
print("New inference or benchmark: False")
assert r["elapsed_seconds"] > 0
