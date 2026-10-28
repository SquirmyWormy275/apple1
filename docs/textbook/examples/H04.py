actions = {
    "convert hex on paper": "off-device",
    "run virtual program": "host-only",
    "open Replica serial port": "separate blocked hardware procedure",
    "flash EEPROM": "outside this lab",
}
for action, category in actions.items():
    print(action + " -> " + category)
assert actions["open Replica serial port"] != "host-only"
