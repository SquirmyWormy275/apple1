cards = [
    ("program bytes", "one encoded routine", "not a live-board result"),
    ("virtual transcript", "modeled execution", "not an electrical test"),
    ("manual", "documented design", "not proof of installed firmware"),
]
for artifact, supports, limit in cards:
    print(f"{artifact}: shows {supports}; limit: {limit}")
assert all(limit for artifact, supports, limit in cards)
