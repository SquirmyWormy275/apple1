from neural1.world import VirtualApple1World

world = VirtualApple1World()
context = ["remember the answer is 42"]
world.host_write(0x400, b"\x2a")
context.clear()
print("Conversation messages:", len(context))
print("Persistent byte:", world.host_read(0x400)[0])
assert not context and world.host_read(0x400)[0] == 42
