import json
from hashlib import sha256

from tools.textbook_support import ROOT

p = ROOT / "software/ram-only/line-input-0300.hex"
manifest = json.loads((ROOT / "cf-card/manifests/current.json").read_text())
print("Source SHA-256:", sha256(p.read_bytes()).hexdigest())
print("Card manifest is a JSON object:", isinstance(manifest, dict))
print("Device opened / card written: False / False")
assert isinstance(manifest, dict)
