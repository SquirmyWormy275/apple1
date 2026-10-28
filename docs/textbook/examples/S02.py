from tools.textbook_support import echo

r = echo("A\r")
assert r.screen_text == r.buffer_text == "A\r"
assert r.returned_to_monitor
