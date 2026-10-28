from tools.textbook_support import cpu

w, _, _ = cpu("""
LDA #$C1
AND #$7F
STA $0400
ORA #$80
STA $0401
EOR #$FF
STA $0402
LDA #$81
ASL A
STA $0403
ROL A
STA $0404
JMP $FF1F
""", inspect=tuple(range(0x400, 0x405)))
assert w.host_read(0x400, 5) == bytes.fromhex("41 C1 3E 02 05")
print("ASL $81 gives $02 with carry 1; ROL $02 rotates that carry into bit 0, giving $05.")
