from tools.textbook_support import echo

r = echo("HI\r")
assert r.screen_text == r.buffer_text == "HI\r"
assert r.instructions == 30 and r.returned_to_monitor
