from tools.textbook_support import cpu

w, r, a = cpu("""
LDA #$41
JSR SUB
STA $0400
JMP $FF1F
SUB: PHA
LDA #$5A
STA $0401
PLA
RTS
""", inspect=(0x400, 0x401))
print("Before PC   SP   instruction byte")
for row in r.trace:
    print(f"       {row.pc:04X} {row.sp:02X}   {row.opcode:02X}")
print("Final SP:", f"{r.final_sp:02X}")
assert w.host_read(0x400, 2) == b"AZ" and r.final_a == 0x41
assert r.final_sp == r.trace[0].sp == 0xFF
assert [row.sp for row in r.trace if row.pc == a.symbols["SUB"]] == [0xFD]
print("JSR pushes two bytes; PHA pushes one; PLA and RTS balance them.")
