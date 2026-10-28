from tools.textbook_support import cpu

w, r, a = cpu("LDA #$5A\nSTA $0402\nLDX $0402\nJMP $FF1F", inspect=(0x402,))
assert r.final_x == 0x5A and w.host_read(0x402) == b"Z"
