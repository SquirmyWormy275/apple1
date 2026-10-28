segments = [
    ("introduce the replica", 30),
    ("show virtual bytes storing 42", 60),
    ("explain the memory read", 60),
    ("ask what changes for 43", 30),
]
for topic, seconds in segments:
    print(f"{seconds:3d}s: {topic}")
assert sum(seconds for topic, seconds in segments) == 180
print("Fallback: printed transcript and memory card.")
