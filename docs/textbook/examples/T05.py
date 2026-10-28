from tools.textbook_support import cpu

for left, right, incoming, expected, no_borrow in [(5, 3, "SEC", 2, True), (3, 5, "SEC", 254, False), (5, 3, "CLC", 1, True)]:
    print(f"Binary {left} - {right}, {incoming}")
    _, r, _ = cpu(f"CLD\n{incoming}\nLDA #${left:02X}\nSBC #${right:02X}\nJMP $FF1F", inspect=())
    print("Carry means no unsigned borrow:", bool(r.final_p & 1))
    assert r.final_a == expected and bool(r.final_p & 1) == no_borrow
_, r, _ = cpu("LDA #$80\nCMP #$01\nJMP $FF1F", inspect=())
assert r.final_a == 0x80 and r.final_p & 1 and not r.final_p & 128
print("CMP $80 against $01: unsigned 128 >= 1. Signed -128 < 1 needs signed reasoning.")
