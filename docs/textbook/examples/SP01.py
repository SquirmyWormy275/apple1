for original, replica in [
    ("DRAM banks", "62256 SRAM"),
    ("discrete terminal logic", "Propeller-centered I/O"),
    ("6820 PIA", "6821 PIA"),
    ("Monitor PROM pair", "modern ROM storage"),
]:
    print(original + " -> " + replica)
print("Shared conceptual contract: keyboard, display, memory, CPU.")
print("Live signal paths verified by this exercise: False")
