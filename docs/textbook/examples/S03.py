for number in (0, 15, 16, 42, 65, 128, 255):
    print(f"{number:3d} = ${number:02X} = {number:08b}")
assert int("2A", 16) == 42
