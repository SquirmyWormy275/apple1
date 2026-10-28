from neural1.world import VirtualApple1World, WozMonSession

w = VirtualApple1World()
m = WozMonSession(w)
for command in ("0300: 41 42 43", "0300.0302"):
    print(command, "->", m.transact(command))
assert w.host_read(0x300, 3) == b"ABC"
print("CPU address space:", 2**16, "bytes; lab RAM:", w.ram_budget, "bytes")
