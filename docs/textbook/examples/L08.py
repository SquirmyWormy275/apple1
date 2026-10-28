from neural1.family_runner import evaluate_family
from neural1.world import VirtualApple1World, WozMonSession

for label, image, expected in [("positive", bytes.fromhex("A9 41 20 EF FF 4C 1F FF") + bytes(248), True), ("negative", bytes(256), False)]:
    w = VirtualApple1World()
    commands = [f"{0x200 + i:04X}: " + image[i : i + 16].hex(" ").upper() for i in range(0, 256, 16)] + ["0200R"]
    records = [
        {
            "agent_id": "fixture",
            "generation": 0,
            "response": "\n".join(commands),
            "outputs": [WozMonSession(w).transact(c) for c in commands],
        }
    ]
    r = evaluate_family("256-byte-universe", w, records)
    print(label, "passed:", r["passed"])
    assert r["passed"] is expected
