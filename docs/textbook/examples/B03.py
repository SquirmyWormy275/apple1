items = [3, 1, 2]
total = 0
for index, item in enumerate(items):
    total += item
    print(f"index={index}; item={item}; total={total}")
assert total == 6
print("Stop: no items remain.")
