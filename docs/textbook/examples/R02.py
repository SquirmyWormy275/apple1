positions = [0, 1, 2, 1, 0]
for frame, position in enumerate(positions):
    print(f"frame {frame}: |" + (" " * position + "*").ljust(8) + "|")
assert positions[0] == positions[-1]
