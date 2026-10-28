from tools.textbook_support import cpu

print("Host analogue of PRINT 6*7:", 6 * 7)
w, r, a = cpu("LDA #$2A\nSTA $0400\nJMP $FF1F")
assert w.host_read(0x400)[0] == 6 * 7
print("No BASIC interpreter was executed.")
