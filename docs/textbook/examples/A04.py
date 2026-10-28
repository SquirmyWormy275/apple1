from tools.textbook_support import cpu

for key, expected in [(0x59, 1), (0x4E, 0)]:
    print("Input:", chr(key))
    w, r, a = cpu(f"LDA #${key:02X}\nCMP #$59\nBEQ YES\nLDA #$00\nJMP SAVE\nYES: LDA #$01\nSAVE: STA $0400\nJMP $FF1F")
    assert w.host_read(0x400)[0] == expected
