from tools.firmware_static_audit import audit_vendor_source
from tools.textbook_support import ROOT

r = audit_vendor_source(ROOT / "firmware/vendor/110REV03")
print("Candidate only:", r["candidate_only"])
print("Candidate keyboard-bus writers:", sorted(r["keyboard_bus_writers"]))
print("Candidate serial strobe milliseconds:", r["serial_strobe_ms"])
assert r["candidate_only"] and r["keyboard_bus_writers"] == {"ps2", "serial"}
print("Firmware loaded / EEPROM written: False / False")
