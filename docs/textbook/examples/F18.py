from neural1.interface import Mode, Portal

portal = Portal()
for key in ("1", "0", "2", "0", "3", "?"):
    print(key, "->", portal.select(key))
assert portal.mode == Mode.ABOUT
