from tools.textbook_support import cpu

w, _, _ = cpu("""
LDA #$FF
STA $20
LDA #$04
STA $21
LDA #$5A
STA $0500
LDY #$01
LDA ($20),Y
STA $0400
LDX #$02
LDA #$00
STA $22
LDA #$05
STA $23
LDA ($20,X)
STA $0401
JMP $FF1F
""", inspect=(0x400, 0x401, 0x500))
assert w.host_read(0x400, 2) == b"ZZ"
print("($20),Y: dereference $20/$21 to $04FF, then add Y=1 -> $0500.")
print("($20,X): add X=2 to zero-page operand, dereference $22/$23 -> $0500.")
print("These are CPU teaching accesses, not extra permissions for experiment agents.")
