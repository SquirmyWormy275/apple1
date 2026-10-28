from tools.apple1_emulator import load_hex_program
from tools.textbook_support import ROOT

payload = load_hex_program(ROOT / "software/ram-only/line-input-0300.hex")
for offset in range(0, len(payload), 8):
    print(f"{0x300 + offset:04X}:", payload[offset : offset + 8].hex(" ").upper())
assert len(payload) == 26 and payload[-3:] == bytes.fromhex("4C 1F FF")
print("Last instruction: JMP $FF1F")

high_bits = sum(byte >= 0x80 for byte in payload)
print("Bytes with bit 7 set:", high_bits)
assert high_bits == 15
