from tools.textbook_support import cpu

w, r, a = cpu("LDX #$03\nAGAIN: DEX\nBNE AGAIN\nSTX $0400\nJMP $FF1F", trace=True)
print("Symbols:", a.symbols)
assert r.final_x == 0 and a.symbols["AGAIN"] == 0x302
