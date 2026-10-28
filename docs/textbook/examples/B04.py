items = [5, 3, 1, 4, 2]
passes = 0
while True:
    swaps = 0
    for i in range(len(items) - 1):
        if items[i] > items[i + 1]:
            items[i], items[i + 1] = items[i + 1], items[i]
            swaps += 1
    passes += 1
    print(f"pass={passes}; list={items}; swaps={swaps}")
    if swaps == 0:
        break
assert items == [1, 2, 3, 4, 5]
