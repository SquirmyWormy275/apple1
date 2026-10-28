import json

from neural1.interface import PORTAL_FRAME
from neural1.visualization import validate_frame
from tools.textbook_support import ROOT

errors = validate_frame(PORTAL_FRAME)
print("Portal frame errors:", errors)
r = json.loads((ROOT / "art/provenance/portal-original.json").read_text())
print("Original portal asset:", r["asset_id"])
print("License status:", r["license_status"])
assert not errors and r["origin"] == "original"
