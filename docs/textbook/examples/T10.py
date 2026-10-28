from tools.textbook_support import cpu

for index, expected_stores in [(0x0F, 16), (0xFF, 1)]:
    source = f"LDY #${index:02X}\nLDA #$AA\nFILL: STA $0400,Y\nDEY\nBPL FILL\nJMP $FF1F"
    w, r, a = cpu(source, inspect=(0x400, 0x40F, 0x410, 0x4FF))
    stores = [row for row in r.trace if row.opcode == 0x99]
    print("Initial Y:", f"{index:02X}", "stores:", len(stores), "final Y:", f"{r.final_y:02X}")
    assert len(a.payload) == 13 and len(stores) == expected_stores
    if index == 0x0F:
        assert w.host_read(0x400, 17) == b"\xAA" * 16 + b"\x00"
    else:
        assert w.host_read(0x4FF) == b"\xAA" and w.host_read(0x400) == b"\x00"
print("A zero-length interpretation encoded as LDY #$FF does one store, not zero or 256.")
