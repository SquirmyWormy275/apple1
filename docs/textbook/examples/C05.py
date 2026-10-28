from tools.textbook_support import cpu

for flag, expected in [("CLC", 0x42), ("SEC", 0x43)]:
    print("Carry setup:", flag)
    w, r, a = cpu(f"CLD\n{flag}\nLDA #$41\nADC #$01\nSTA $0400\nJMP $FF1F")
    assert w.host_read(0x400)[0] == expected
