from neural1.assembler import LessonAssembler

r = LessonAssembler().assemble("LDA #$2A\nSTA $0400\nJMP $FF1F", origin=0x300)
assert not r.diagnostics
for i, byte in enumerate(r.payload):
    print(f"{r.origin + i:04X}: {byte:02X}")
assert r.payload[3:5] == bytes.fromhex("00 04")
