from hashlib import sha256

original = b"RECORDED EXAMPLE\n"
changed = b"RECORDED EXAMPLE!\n"
print("Original:", sha256(original).hexdigest())
print("Changed: ", sha256(changed).hexdigest())
assert sha256(original).digest() != sha256(changed).digest()
