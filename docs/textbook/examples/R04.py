rooms = {"HALL": {"EAST": "LAB"}, "LAB": {"WEST": "HALL"}}
state = "HALL"
for action in ("EAST", "NORTH", "WEST"):
    previous = state
    state = rooms[state].get(action, state)
    print(f"{previous} + {action} -> {state}")
assert state == "HALL"
