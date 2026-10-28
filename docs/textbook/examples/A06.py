from tools.textbook_support import cpu

w, r, a = cpu("LDY #$00\nLDA #$41\nFILL: STA $0400,Y\nINY\nCPY #$05\nBNE FILL\nJMP $FF1F", inspect=(0x400, 0x404, 0x405))
print("Buffer:", repr(w.host_read(0x400, 6)))
assert w.host_read(0x400, 6) == b"AAAAA\x00"
