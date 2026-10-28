for row in range(1, 7):
    text = "*" * row
    print(text)
    assert len(text) == row
