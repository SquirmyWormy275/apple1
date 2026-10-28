from tools.textbook_support import emit

record = {
    "action": "run a virtual example",
    "observation": "0300: 2A",
    "interpretation": "the modeled program stored 42",
    "limit": "not a physical board measurement",
}
emit(record)
assert "observation" in record and "limit" in record
