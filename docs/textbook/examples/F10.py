from neural1.family_runner import evaluate_family
from neural1.world import VirtualApple1World, WozMonSession

world = VirtualApple1World()
records = []
image = bytes.fromhex("A9 41 20 EF FF 4C 1F FF") + bytes(248)
for generation in range(2):
    for agent in range(1):
        commands = [f"{0x200 + i:04X}: " + image[i : i + 16].hex(" ").upper() for i in range(0, len(image), 16)] + ["0200R"]
        records.append(
            {
                "generation": generation,
                "agent_id": str(agent),
                "response": "\n".join(commands),
                "outputs": [WozMonSession(world).transact(c) for c in commands],
            }
        )
world.generation = 2
before = world.snapshot()
result = evaluate_family("256-byte-universe", world, records)
print("Family:", result["family"])
print("Candidate bytes:", len(image))
print("Passed authored fixture:", result["passed"])
print("Independent output:", repr(result["independent_execution"]["screen_text"]))
print("Evaluation preserved world:", world.snapshot() == before)
assert result["passed"] and result["independent_execution"]["screen_text"] == "A"
assert world.snapshot() == before
