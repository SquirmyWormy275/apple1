from tools.textbook_support import cpu

w, r, _ = cpu("""
CLD
CLC
LDA #$FF
ADC #$01
STA $0400
LDA #$00
ADC #$00
STA $0401
JMP $FF1F
""", inspect=(0x400, 0x401), trace=True)
value = int.from_bytes(w.host_read(0x400, 2), "little")
print("Little-endian 16-bit result:", value, f"(${value:04X})")
assert value == 256
print("STA and LDA between the additions preserve carry; CLC there would lose the ninth bit.")
