from tools.textbook_support import cpu

for branch, expected in [("BNE", 0), ("BPL", 255)]:
    print("Branch:", branch)
    w, r, a = cpu(f"LDX #$05\nLOOP: DEX\n{branch} LOOP\nSTX $0400\nJMP $FF1F")
    assert r.final_x == expected
