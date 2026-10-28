import json

from tools.textbook_support import ROOT

p = ROOT / "docs/neural1/operations/evidence/pi-closeout-2026-09-10/post-boot-run.json"
r = json.loads(p.read_text())
print("Evidence class:", r["classification"])
print("Run:", r["campaign_id"])
print("Accepted commands:", r["family_result"]["accepted_transactions"])
print("Independent output:", repr(r["family_result"]["independent_execution"]["screen_text"]))
assert r["family_result"]["accepted_transactions"] == 8
assert r["family_result"]["independent_execution"]["screen_text"] == "A"
