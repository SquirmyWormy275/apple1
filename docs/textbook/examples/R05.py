rhythm = 0b10100100
for slot in range(8):
    event = bool(rhythm & (1 << (7 - slot)))
    print(f"slot {slot}: " + ("CLAP" if event else "rest"))
assert rhythm.bit_count() == 3
print("Sound hardware: not used")
