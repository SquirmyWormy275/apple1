from tools.textbook_support import cpu

for left, right, carry, expected, flags in [
    (0xFF, 1, "CLC", 0, (1, 1, 0, 0)),
    (0x7F, 1, "CLC", 0x80, (0, 0, 1, 1)),
    (0x80, 0x80, "CLC", 0, (1, 1, 0, 1)),
    (0x41, 1, "SEC", 0x43, (0, 0, 0, 0)),
]:
    print(f"Binary {left:02X} + {right:02X}, {carry}")
    _, r, _ = cpu(f"CLD\n{carry}\nLDA #${left:02X}\nADC #${right:02X}\nJMP $FF1F", inspect=())
    actual = tuple(int(bool(r.final_p & mask)) for mask in (1, 2, 128, 64))
    print("C Z N V:", *actual)
    assert r.final_a == expected and actual == flags
