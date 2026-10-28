from tools.textbook_support import cpu

source = """
LDA #$A5
STA $03FF
STA $0405
LDY #$00
COPY: LDA DATA,Y
STA $0400,Y
INY
CPY #$05
BNE COPY
JMP $FF1F
DATA: .BYTE $48,$45,$4C,$4C,$4F
"""
w, r, a = cpu(source, inspect=(0x3FF, 0x400, 0x404, 0x405))
print("Data label:", f"{a.symbols['DATA']:04X}")
print("Copied:", repr(w.host_read(0x400, 5)))
assert w.host_read(0x3FF, 7) == b"\xA5HELLO\xA5"
assert r.final_y == 5 and r.stop_reason == "MONITOR_WARM_ENTRY"
