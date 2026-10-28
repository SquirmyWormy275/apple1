from tools.textbook_support import cpu

for count in (6, 5):
    print("Comparison count:", count)
    w, r, a = cpu(f"LDY #$00\nLDA #$41\nLOOP: STA $0400,Y\nINY\nCPY #${count:02X}\nBNE LOOP\nJMP $FF1F", inspect=(0x404, 0x405))
    assert w.host_read(0x405)[0] == (0x41 if count == 6 else 0)
    assert r.stop_reason == "MONITOR_WARM_ENTRY"
