from tools.textbook_support import echo

for text in ("\r", "HI\r"):
    print("Input:", repr(text))
    r = echo(text)
    assert r.buffer_text == r.screen_text == text and r.returned_to_monitor
