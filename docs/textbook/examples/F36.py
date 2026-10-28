from tools.textbook_support import ROOT
from tools.virtual_bridge import StaticModelClient, VirtualApple1Bridge

bridge = VirtualApple1Bridge(StaticModelClient("THIS IS A FIXED RESPONSE."))
r = bridge.run(ROOT / "software/ram-only/line-input-0300.hex", "HI\r")
print("Keyboard echo:", repr(r.keyboard_echo))
print("Formatted response:", r.response_lines)
print("Serial opened:", r.serial_opened)
assert r.keyboard_echo == "HI\r" and not r.serial_opened
