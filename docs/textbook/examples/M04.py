from tools.textbook_support import cpu

w, r, a = cpu("LDA #$2B\nSTA $0400\nJMP $FF1F")
expected, actual = 42, w.host_read(0x400)[0]
print(f"Expected={expected}; actual={actual}; mismatch={expected != actual}")
assert actual == 43 and actual != expected
