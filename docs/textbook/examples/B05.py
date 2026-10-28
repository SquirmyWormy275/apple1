from hashlib import sha256

from tools.textbook_support import ROOT

p = ROOT / "software/ram-only/line-input-0300.hex"
original = p.read_bytes()
copy = bytes(original)
print("Artifact:", p.name)
print("Byte-identical copy:", sha256(original).digest() == sha256(copy).digest())
print("Physical card write: not performed")
assert original == copy
