from neural1.assembler import LessonAssembler
from tools.textbook_support import cpu

_, r, a = cpu("LDX #$03\nLOOP: DEX\nBNE LOOP\nJMP $FF1F", inspect=(), trace=True)
assert a.payload[3:5] == bytes.fromhex("D0 FD")
print("Branch at $0303; next PC $0305; $0302 - $0305 = -3 -> $FD.")
assert r.final_x == 0
bad = LessonAssembler().assemble("BNE $0400", origin=0x300)
assert bad.diagnostics
print("Branch from $0300 to $0400 rejected: target is beyond +127 from $0302.")
forward = LessonAssembler().assemble("LDA DATA\nJMP $FF1F\nDATA: .BYTE $41", origin=0x300)
assert forward.symbols["DATA"] == 0x306 and forward.payload[:3] == bytes.fromhex("AD 06 03")
print("Forward DATA label is $0306; LDA absolute must occupy three bytes.")
