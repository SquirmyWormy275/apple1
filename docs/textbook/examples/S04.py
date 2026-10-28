rows = [
    ("emulator returned to Monitor", "recorded virtual observation"),
    ("board will do the same", "untested physical claim"),
    ("manual describes a register", "documented design"),
]
for statement, kind in rows:
    print(statement + " -> " + kind)
assert rows[0][1] != rows[1][1]
