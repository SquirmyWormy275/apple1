from tools.textbook_support import cpu

w, r, a = cpu("LDA #$2A\nSTA $0400\nJMP $FF1F", trace=True)
assert w.host_read(0x400) == b"\x2a"
assert r.stop_reason == "MONITOR_WARM_ENTRY"
