raw = bytes(byte | 0x80 for byte in b"HI\r")
print("Harness keyboard bytes:", raw.hex(" ").upper())
decoded = bytes(byte & 0x7F for byte in raw)
print("Decoded:", repr(decoded.decode("ascii")))
assert raw == bytes.fromhex("C8 C9 8D") and decoded == b"HI\r"
