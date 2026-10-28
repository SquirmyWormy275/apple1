from tools.textbook_support import cpu

source = """
LDA #$41
STA $0420
LDA #$20
STA $0400
LDA $0420
STA $0401
STA $20
LDA #$00
LDA $20
STA $0402
JMP $FF1F
"""
w, r, _ = cpu(source, inspect=(0x400, 0x401, 0x402), trace=True)
assert w.host_read(0x400, 3) == bytes.fromhex("20 41 41")
print("Immediate $20 is a value; absolute $0420 and zero-page $20 are addresses.")
