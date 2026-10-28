from neural1.world import VirtualApple1World, WozMonSession

w = VirtualApple1World()
m = WozMonSession(w)
for command in ("0300: A9 2A 8D 00 04 4C 1F FF", "0300.0307", "0300R", "0400"):
    print(command, "->", m.transact(command))
assert w.host_read(0x400)[0] == 42
