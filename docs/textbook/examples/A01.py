from neural1.assembler import LessonAssembler

for source in ("LDA #$41", "LDA $0400", "STA $0400", "STA #$41"):
    r = LessonAssembler().assemble(source, origin=0x300)
    print(source, "->", "REJECTED" if r.diagnostics else r.payload.hex(" ").upper())
assert LessonAssembler().assemble("STA #$41").diagnostics
