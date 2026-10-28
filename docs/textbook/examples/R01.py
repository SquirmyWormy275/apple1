lines = ["+" + "-" * 38 + "+", "|" + "APPLE-1 / HELLO".center(38) + "|", "+" + "-" * 38 + "+"]
for line in lines:
    print(line)
    assert len(line) == 40 and all(32 <= ord(c) <= 126 for c in line)
