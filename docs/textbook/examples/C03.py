value = 0x41
encoded = value | 0x80
print(f"ASCII: {value:08b}; high bit set: {encoded:08b}")
print(f"Mask $7F: ${encoded & 0x7F:02X}")
assert encoded == 0xC1 and (encoded & 0x7F) == value
