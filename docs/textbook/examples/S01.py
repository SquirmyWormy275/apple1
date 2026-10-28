objects = {"6502 circuit board": "hardware", "Monitor listing": "software", "Replica 1 Plus": "modern replica"}
for name, kind in objects.items():
    print(f"{name}: {kind}")
assert objects["Monitor listing"] == "software"
