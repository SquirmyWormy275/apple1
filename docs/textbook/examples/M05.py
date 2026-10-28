from tools.textbook_support import cpu

w, r, a = cpu("LDA #$41\nJSR $FFEF\nJMP $FF1F", inspect=())
assert r.screen_text == "A" and r.stop_reason == "MONITOR_WARM_ENTRY"
print("JSR ECHO returned; JMP selected the warm-entry exit.")
